"""
Redix Healthcare Data Conversion REST API
Clean, simple wrapper around redix executable (Windows/Linux)
With improved filename conventions for better user experience
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks, Depends, Query, Path # Added Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, FileResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
import subprocess
import os
import uuid
import glob
from datetime import datetime, timezone, date # timezone imported here
import logging
import platform
import configparser
import shutil # For file operations like deleting directories
import asyncio
import functools # For asyncio.to_thread
import aiosqlite # For async SQLite access
import json
from prometheus_fastapi_instrumentator import Instrumentator

# Configuration management
STAGING_CONFIG_PROFILES: Dict[str, Dict[str, str]] = {}
DEFAULT_STAGING_PROFILE_NAME: Optional[str] = None
StagingProfileEnum = Enum('StagingProfileEnum', {'_default': 'default'}) # Placeholder until config loaded

# Batch Job Status Enum
class BatchJobStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    COMPLETED_WITH_ERRORS = "COMPLETED_WITH_ERRORS"
    FAILED = "FAILED"

class LogLevelEnum(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"

class FileTypeEnum(str, Enum):
    input = "input"
    output = "output"
    error = "error"
    ack = "ack"
    ta1 = "ta1"
    staging = "staging"
    shared = "shared"
    archive = "archive"

# --- Batch Job Status Tracking (Persistent with SQLite) ---
# BASE_WORK_DIR is not yet defined globally when DB_PATH is initialized here.
# It's safer to define DB_PATH after BASE_WORK_DIR is guaranteed to be set.
# For now, let's keep the initialization in init_db and ensure BASE_WORK_DIR is ready before init_db is called.
DB_PATH = None 
db_connection: Optional[aiosqlite.Connection] = None  # Persistent connection

async def get_db_connection() -> aiosqlite.Connection:
    """Get the persistent DB connection."""
    if db_connection is None:
        raise RuntimeError("Database connection not initialized")
    return db_connection

async def init_db():
    """Initialize the database schema."""
    global db_connection, DB_PATH
    # Ensure DB_PATH is set before attempting to connect
    if DB_PATH is None:
        # This fallback mirrors the main script's logic if BASE_WORK_DIR is available
        if 'BASE_WORK_DIR' in globals() and BASE_WORK_DIR is not None:
             DB_PATH = os.environ.get('REDIX_DB_PATH', os.path.join(BASE_WORK_DIR, 'batch_jobs.db'))
        else: # Fallback if BASE_WORK_DIR isn't globally available at this early stage
             DB_PATH = os.environ.get('REDIX_DB_PATH', 'batch_jobs.db') # Connect in current working directory
        logger.info(f"Database path set to: {DB_PATH}")

    db_connection = await aiosqlite.connect(DB_PATH)
    await db_connection.execute('''CREATE TABLE IF NOT EXISTS batch_jobs
                                   (job_id TEXT PRIMARY KEY, 
                                    status TEXT, 
                                    profile TEXT,
                                    input_folder TEXT,
                                    output_folder TEXT,
                                    start_time TEXT, 
                                    end_time TEXT, 
                                    total_files_found INTEGER, 
                                    files_processed INTEGER, 
                                    successful_files INTEGER, 
                                    failed_files INTEGER, 
                                    error TEXT)''')
    await db_connection.execute('''CREATE TABLE IF NOT EXISTS batch_logs
                                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    job_id TEXT, 
                                    timestamp TEXT, 
                                    level TEXT, 
                                    message TEXT)''')
    await db_connection.execute('''CREATE TABLE IF NOT EXISTS batch_file_details
                                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    job_id TEXT,
                                    filename TEXT,
                                    status TEXT,
                                    success INTEGER,
                                    summary TEXT,
                                    warnings TEXT,
                                    output_url TEXT,
                                    error_url TEXT,
                                    ack_url TEXT,
                                    ta1_url TEXT,
                                    archive_path TEXT)''')
    await db_connection.commit()

async def create_batch_job(job_id: str, profile: str, input_folder: str, output_folder: str, initial_status: BatchJobStatusEnum = BatchJobStatusEnum.PENDING):
    """Create a new batch job entry in the database."""
    start_time = datetime.now(timezone.utc).isoformat()
    db = await get_db_connection()
    await db.execute('''INSERT INTO batch_jobs 
                                 (job_id, status, profile, input_folder, output_folder, start_time, total_files_found, files_processed, successful_files, failed_files) 
                                 VALUES (?, ?, ?, ?, ?, ?, 0, 0, 0, 0)''', 
                             (job_id, initial_status.value, profile, input_folder, output_folder, start_time))
    await db.commit()

async def update_batch_job(job_id: str, updates: Dict[str, Any]):
    """Update batch job fields atomically."""
    set_clauses = []
    values = []
    for key, value in updates.items():
        set_clauses.append(f"{key} = ?")
        if key in ['start_time', 'end_time']:
            value = value.astimezone(timezone.utc).isoformat() if value else None
        elif key == 'status' and isinstance(value, BatchJobStatusEnum):
            value = value.value
        values.append(value)
    if not set_clauses:
        return
    query = f"UPDATE batch_jobs SET {', '.join(set_clauses)} WHERE job_id = ?"
    values.append(job_id)
    db = await get_db_connection()
    await db.execute(query, tuple(values))
    await db.commit()

async def get_batch_job(job_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a batch job by ID, including file details."""
    db = await get_db_connection()
    db.row_factory = aiosqlite.Row
    cursor = await db.execute('SELECT * FROM batch_jobs WHERE job_id = ?', (job_id,))
    row = await cursor.fetchone()
    if row:
        job_data = dict(row)
        # Convert stored ISO strings back to datetime objects, assuming UTC
        job_data['start_time'] = datetime.fromisoformat(job_data['start_time']).replace(tzinfo=timezone.utc)
        job_data['end_time'] = datetime.fromisoformat(job_data['end_time']).replace(tzinfo=timezone.utc) if job_data['end_time'] else None
        # Fetch file details from separate table
        cursor = await db.execute('SELECT * FROM batch_file_details WHERE job_id = ?', (job_id,))
        details_rows = await cursor.fetchall()
        details = []
        for d_row in details_rows:
            detail = dict(d_row)
            detail['success'] = bool(detail['success'])
            detail['warnings'] = json.loads(detail['warnings']) if detail['warnings'] else []
            details.append(detail)
        job_data['details'] = details
        return job_data
    return None

async def list_batch_jobs(status: Optional[str] = None, profile: Optional[str] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
    """List batch jobs with optional filters."""
    db = await get_db_connection()
    db.row_factory = aiosqlite.Row
    query = 'SELECT job_id, status, profile, input_folder, output_folder, start_time, end_time, total_files_found, files_processed, successful_files, failed_files, error FROM batch_jobs'
    params = []
    where_clauses = []
    if status:
        where_clauses.append('status = ?')
        params.append(status)
    if profile:
        where_clauses.append('profile = ?')
        params.append(profile)
    if start_date:
        where_clauses.append('start_time >= ?')
        params.append(start_date.isoformat()) # Use isoformat directly if timezone-aware, or naive if stored as naive
    if end_date:
        where_clauses.append('end_time <= ?')
        params.append(end_date.isoformat()) # Use isoformat directly if timezone-aware, or naive if stored as naive
    if where_clauses:
        query += ' WHERE ' + ' AND '.join(where_clauses)
    query += ' ORDER BY start_time DESC LIMIT ? OFFSET ?'
    params.extend([limit, offset])
    cursor = await db.execute(query, tuple(params))
    rows = await cursor.fetchall()
    jobs = []
    for row in rows:
        job = dict(row)
        # Convert stored ISO strings back to datetime objects, assuming UTC
        job['start_time'] = datetime.fromisoformat(job['start_time']).replace(tzinfo=timezone.utc)
        job['end_time'] = datetime.fromisoformat(job['end_time']).replace(tzinfo=timezone.utc) if job['end_time'] else None
        jobs.append(job)
    return jobs

async def get_batch_summary(start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, profile: Optional[str] = None) -> Dict[str, Any]:
    """Get aggregate summary of batch jobs."""
    db = await get_db_connection()
    query = '''SELECT COUNT(*), SUM(successful_files), SUM(failed_files), AVG(files_processed) 
               FROM batch_jobs WHERE status IN (?, ?)''' # Updated for enum values
    params = [BatchJobStatusEnum.COMPLETED.value, BatchJobStatusEnum.COMPLETED_WITH_ERRORS.value]
    where_clauses = []
    if profile:
        where_clauses.append('profile = ?')
        params.append(profile)
    if start_date:
        where_clauses.append('start_time >= ?')
        params.append(start_date.isoformat()) # Use isoformat directly if timezone-aware
    if end_date:
        where_clauses.append('end_time <= ?')
        params.append(end_date.isoformat()) # Use isoformat directly if timezone-aware
    if where_clauses:
        query += ' AND ' + ' AND '.join(where_clauses)
    cursor = await db.execute(query, tuple(params))
    row = await cursor.fetchone()
    return {
        'total_jobs': row[0],
        'total_successful_files': row[1] or 0,
        'total_failed_files': row[2] or 0,
        'average_files_processed': row[3] or 0.0
    }

async def add_batch_log(job_id: str, level: str, message: str):
    """Add a log entry for a batch job."""
    db = await get_db_connection()
    timestamp = datetime.now(timezone.utc).isoformat()
    await db.execute('INSERT INTO batch_logs (job_id, timestamp, level, message) VALUES (?, ?, ?, ?)', 
                     (job_id, timestamp, level, message))
    await db.commit()

async def get_batch_logs(job_id: str, limit: int = 50, offset: int = 0, log_level: Optional[str] = None) -> List[Dict[str, str]]:
    """Retrieve paginated logs for a batch job with optional level filter."""
    db = await get_db_connection()
    query = 'SELECT timestamp, level, message FROM batch_logs WHERE job_id = ?'
    params = [job_id]
    if log_level:
        query += ' AND level = ?'
        params.append(log_level)
    query += ' ORDER BY id DESC LIMIT ? OFFSET ?'
    params.extend([limit, offset])
    cursor = await db.execute(query, tuple(params))
    rows = await cursor.fetchall()
    return [{'timestamp': row[0], 'level': row[1], 'message': row[2]} for row in rows]

async def add_batch_file_detail(job_id: str, file_detail: Dict[str, Any]):
    """Add file detail for a batch job."""
    db = await get_db_connection()
    await db.execute('''INSERT INTO batch_file_details 
                                 (job_id, filename, status, success, summary, warnings, output_url, error_url, ack_url, ta1_url, archive_path) 
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (job_id, file_detail['filename'], file_detail['status'], int(file_detail.get('success', False)),
                              file_detail.get('summary'), json.dumps(file_detail.get('warnings', [])),
                              file_detail.get('output_url'), file_detail.get('error_url'), file_detail.get('ack_url'),
                              file_detail.get('ta1_url'), file_detail.get('archive_path')))
    await db.commit()

async def get_batch_file_details(job_id: str, filename: str) -> Optional[Dict[str, Any]]:
    """Retrieve details for a specific file in a batch job."""
    db = await get_db_connection()
    db.row_factory = aiosqlite.Row
    cursor = await db.execute('SELECT * FROM batch_file_details WHERE job_id = ? AND filename = ?', (job_id, filename))
    row = await cursor.fetchone()
    if row:
        detail = dict(row)
        detail['success'] = bool(detail['success'])
        detail['warnings'] = json.loads(detail['warnings']) if detail['warnings'] else []
        return detail
    return None

# Initialize a placeholder logger BEFORE loading config to prevent NameError
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    """Load configuration from redix_cloud.conf file"""
    config = configparser.ConfigParser()

    # Look for config file in current directory first, then in common locations
    config_locations = [
        'redix_cloud.conf',
        './redix_cloud.conf',
        '/etc/redix/redix_cloud.conf',
        os.path.expanduser('~/redix_cloud.conf')
    ]

    config_file_found = None
    for location in config_locations:
        if os.path.exists(location):
            config_file_found = location
            break

    if not config_file_found:
        # Use print here as logger might not be fully configured yet for early exit
        print(f"FATAL: Configuration file 'redix_cloud.conf' not found. Checked locations: {config_locations}")
        raise Exception(f"Configuration file 'redix_cloud.conf' not found. Checked locations: {config_locations}")

    try:
        config.read(config_file_found)
        print(f"Loaded configuration from: {config_file_found}") # Using print as it's very early in startup
        
        # --- IMPORTANT: BASE_WORK_DIR now loaded from environment or config ---
        global BASE_WORK_DIR
        # Prioritize environment variable, then config file, then hardcoded fallback
        BASE_WORK_DIR = os.environ.get('REDIX_BASE_WORK_DIR') # Check for specific env var
        if BASE_WORK_DIR:
            logger.info(f"BASE_WORK_DIR loaded from environment variable REDIX_BASE_WORK_DIR: {BASE_WORK_DIR}")
        else:
            BASE_WORK_DIR = config.get('paths', 'base_work_dir', fallback='/opt/redix-api/data')
            logger.info(f"BASE_WORK_DIR loaded from redix_cloud.conf: {BASE_WORK_DIR}")

        # Load staging profiles
        global STAGING_CONFIG_PROFILES, DEFAULT_STAGING_PROFILE_NAME, StagingProfileEnum
        STAGING_CONFIG_PROFILES = {}
        
        if 'staging_profiles' in config:
            DEFAULT_STAGING_PROFILE_NAME = config.get('staging_profiles', 'default_staging_profile', fallback=None)

            profile_names_for_enum = {}
            for section_name in config.sections():
                if section_name.startswith('staging_profiles.'):
                    profile_name = section_name.split('staging_profiles.', 1)[1]
                    STAGING_CONFIG_PROFILES[profile_name] = dict(config.items(section_name))
                    profile_names_for_enum[profile_name] = profile_name 
            
            if profile_names_for_enum:
                # Dynamically create the Enum class with loaded profile names
                StagingProfileEnum = Enum('StagingProfileEnum', profile_names_for_enum)
            else:
                # Fallback Enum if no profiles are defined
                StagingProfileEnum = Enum('StagingProfileEnum', {'_no_profiles_found': 'no_profiles_available'})
       
         # <<< INSERT HERE >>>
        ProfileEnum = Enum(
            'ProfileEnum', 
            {p: p for p in STAGING_CONFIG_PROFILES.keys()} if STAGING_CONFIG_PROFILES else {'dummy': 'dummy'}
        )



        if not STAGING_CONFIG_PROFILES and DEFAULT_STAGING_PROFILE_NAME:
            logger.warning(f"Default staging profile '{DEFAULT_STAGING_PROFILE_NAME}' is defined but no profiles found in [staging_profiles.<profile_name>] sections.")

        return config
    except Exception as e:
        logger.error(f"Error reading configuration file {config_file_found}: {str(e)}") # Using logger after init
        raise Exception(f"Error reading configuration file {config_file_found}: {str(e)}")

# Load configuration - This block now correctly handles potential exceptions and calls logger.
try:
    config = load_config()
except Exception as e:
    # Use print for final fatal message if logger itself failed, or if this is the very last resort exit.
    # The logger should now be active, so a logger.critical is more appropriate.
    logger.critical(f"FATAL: {str(e)}")
    logger.critical("Please create redix_cloud.conf file with proper configuration.")
    exit(1)

# Re-configure logging based on config values loaded by load_config()
log_level = config.get('logging', 'log_level', fallback='INFO').upper()
log_file = config.get('logging', 'log_file', fallback='').strip()

logging_config = {
    'level': getattr(logging, log_level),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

if log_file:
    logging_config['filename'] = log_file
    # If a log file is specified, clear previous handlers and add file handler
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(**logging_config)
    logger = logging.getLogger(__name__) # Re-get logger to ensure it uses new config

# Extract configuration values
# REDIX_LIBS_PATH still from config
REDIX_LIBS_PATH = config.get('paths', 'redix_libs_path')
SERVER_HOST = config.get('server', 'host', fallback='0.0.0.0')
SERVER_PORT = config.getint('server', 'port', fallback=8000)
API_TITLE = config.get('server', 'title', fallback='Redix Solutions: Healthcare EDI & Data Transformation')
API_DESCRIPTION = config.get('server', 'description', fallback='Convert healthcare data between different formats.')
API_VERSION = config.get('server', 'version', fallback='2.0.0')
SUBPROCESS_TIMEOUT = config.getint('processing', 'subprocess_timeout', fallback=30)
CORS_ORIGINS = [origin.strip() for origin in config.get('security', 'cors_origins', fallback='*').split(',')]
CORS_ALLOW_CREDENTIALS = config.getboolean('security', 'cors_allow_credentials', fallback=True)
ENABLE_SWAGGER = config.getboolean('features', 'enable_swagger_ui', fallback=True)
DOCS_URL = config.get('features', 'docs_url', fallback='/docs') if ENABLE_SWAGGER else None
CLEANUP_TEMP_FILES = config.getboolean('features', 'cleanup_temp_files', fallback=True)
ALLOW_RULE_FILE_UPLOAD = config.getboolean('features', 'allow_rule_file_upload', fallback=True)

# Set up directory paths from config - these now depend on BASE_WORK_DIR being resolved first
if BASE_WORK_DIR is None: # Should not happen if load_config works, but defensive check
    logger.critical("FATAL: BASE_WORK_DIR not resolved during configuration loading.")
    exit(1)

INPUT_DIR = os.path.join(BASE_WORK_DIR, config.get('directories', 'input_dir', fallback='input'))
OUTPUT_DIR = os.path.join(BASE_WORK_DIR, config.get('directories', 'output_dir', fallback='output'))
ERROR_DIR = os.path.join(BASE_WORK_DIR, config.get('directories', 'error_dir', fallback='error'))
ACK_DIR = os.path.join(BASE_WORK_DIR, config.get('directories', 'ack_dir', fallback='ack'))
RULES_DIR = os.path.join(BASE_WORK_DIR, config.get('directories', 'rules_dir', fallback='rules'))
STAGING_DIR = os.path.join(BASE_WORK_DIR, config.get('directories', 'staging_dir', fallback='staging'))
ARCHIVE_DIR = os.path.join(BASE_WORK_DIR, config.get('directories', 'archive_dir', fallback='archive'))
# NEW: Dedicated directory for batch processing input files
BATCH_INPUT_DIR = os.path.join(BASE_WORK_DIR, config.get('directories', 'batch_input_dir', fallback='batch_input'))
# SHARED_DIR can be outside BASE_WORK_DIR, so it's directly from config.
SHARED_DIR = config.get('directories', 'shared_dir', fallback='/opt/redix-api/data/shared')

# Enums for all dropdown fields (used for documentation/validation in forms, not directly for config parsing)
class ConversionFlagEnum(str, Enum):
    e = "e - UN/EDIFACT/RMap"
    x = "x - X12"
    f = "f - fixed-length flat file"
    c = "c - XML"
    t = "t - CSV delimited variable-length flat file"
    n = "n - NCPDP"
    h = "h - HL7"

class WarningLevelEnum(int, Enum):
    stop_on_first_error = 0
    continue_with_warnings = 1
    ignore_all_errors = 2

class SegmentTerminatorEnum(str, Enum):
    new_line = "new line"
    exclamation = "!"
    quote = '"'
    dollar = "$"
    percent = "%"

class ElementSeparatorEnum(str, Enum):
    asterisk = "*"
    comma = ","
    dollar = "$"
    percent = "%"

class CompositeSeparatorEnum(str, Enum):
    colon = ":"
    asterisk = "*"
    semicolon = ";"
    dollar = "$"
    percent = "%"

class ReleaseCharacterEnum(str, Enum):
    question = "?"
    pipe = "|"
    exclamation = "!"

# Create directories if they don't exist
def ensure_directories():
    """Ensures all necessary directories for the API exist."""
    # Ensure BASE_WORK_DIR exists first, before joining subdirectories
    os.makedirs(BASE_WORK_DIR, exist_ok=True)
    logger.info(f"Ensured base directory exists: {BASE_WORK_DIR}")

    for directory in [INPUT_DIR, OUTPUT_DIR, ERROR_DIR, ACK_DIR, RULES_DIR, STAGING_DIR, ARCHIVE_DIR, BATCH_INPUT_DIR]:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")
    # Shared directory might be an existing mount point, so don't create by default, just check
    if not os.path.exists(SHARED_DIR):
        logger.warning(f"Shared directory does not exist: {SHARED_DIR}. Please ensure it's properly configured and mounted if intended for use.")

# Initialize directories on startup
ensure_directories()

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url=DOCS_URL
)

# Instrument for Prometheus metrics
Instrumentator().instrument(app).expose(app)

# CORS middleware configuration from config file
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key Authentication
API_KEY = os.environ.get("REDIX_API_KEY", "secret")  # Set via env var in production
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key_header

# Global variable to store the path to the Redix executable
redix_exe_path: Optional[str] = None

def load_redix_engine():
    """
    Attempts to locate redix executable (redix64.exe on Windows, redix64 on Linux).
    Sets redix_exe_path global variable.
    """
    global redix_exe_path

    if not REDIX_LIBS_PATH:
        logger.error("REDIX_LIBS_PATH not configured. Please set redix_libs_path in redix_cloud.conf.")
        redix_exe_path = None
        return

    if not os.path.exists(REDIX_LIBS_PATH):
        logger.error(f"REDIX_LIBS_PATH does not exist: {REDIX_LIBS_PATH}")
        redix_exe_path = None
        return

    libs_dir = os.path.abspath(REDIX_LIBS_PATH)

    # Determine executable name based on platform
    if platform.system() == "Windows":
        exe_name = "redix64.exe"
    else:  # Linux/Unix
        exe_name = "redix64"

    exe_path = os.path.join(libs_dir, exe_name)

    if os.path.exists(exe_path):
        # On Linux, check if executable has execute permissions
        if platform.system() != "Windows":
            if not os.access(exe_path, os.X_OK):
                logger.error(f"Found {exe_name} at {exe_path} but it's not executable. Run: chmod +x {exe_path}")
                redix_exe_path = None
                return

        logger.info(f"Found {exe_name} at: {exe_path}. Redix engine ready.")
        redix_exe_path = exe_path
    else:
        logger.error(f"{exe_name} not found in {libs_dir}. Redix engine not available.")
        redix_exe_path = None

# Load the Redix engine on startup
load_redix_engine()

def generate_filename_base(input_source: str, conversion_flag_char: str, user_prefix: Optional[str] = None) -> str:
    """
    Generate a descriptive filename base that users can easily identify.

    Args:
        input_source: Original input filename (e.g., "mydata.txt") or a descriptive string ("data_input")
        conversion_flag_char: The single character conversion flag (e.g., 'e', 'x')
        user_prefix: Optional user-defined prefix for the files

    Returns:
        Base filename without extension, e.g., "claims_data_x_20250708_143022_a7b3"
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    short_id = str(uuid.uuid4())[:4]  # Shorter ID for readability

    # 1. Determine the base name from the input_source
    if input_source and input_source != 'data_input':
        base_name_raw = os.path.splitext(os.path.basename(input_source))[0]
        # Sanitize: keep only alphanumeric, hyphens, underscores. Limit length.
        clean_base_name = ''.join(c for c in base_name_raw if c.isalnum() or c in '-_')[:30]
    else:
        clean_base_name = "data_input" # Default if no meaningful input_source filename

    # 2. Prepend user_prefix if provided and clean
    final_base_name = clean_base_name
    if user_prefix:
        user_prefix_clean = ''.join(c for c in user_prefix if c.isalnum() or c in '-_')[:10]
        if user_prefix_clean:
            # If the clean_base_name was just "data_input" or empty, the prefix takes precedence.
            # Otherwise, prepend the prefix.
            if clean_base_name == "data_input" or not clean_base_name.strip():
                final_base_name = user_prefix_clean
            else:
                final_base_name = f"{user_prefix_clean}_{clean_base_name}"
    
    # 3. Final fallback to "conversion" if everything else results in an empty or whitespace string
    if not final_base_name.strip():
        final_base_name = "conversion"

    # 4. Construct the full filename base using the *correct* single character conversion flag
    return f"{final_base_name}_{conversion_flag_char}_{timestamp}_{short_id}"


async def get_error_message(error_code: int) -> str:
    """
    Calls errcode executable to get the proper error message for a given error code.
    Uses asyncio.to_thread for blocking subprocess.run call.
    """
    try:
        if platform.system() == "Windows":
            errcode_exe_name = "errcode64.exe"
        else:
            errcode_exe_name = "errcode64"

        errcode_exe = os.path.join(REDIX_LIBS_PATH, errcode_exe_name)

        if not os.path.exists(errcode_exe):
            return f"Error code {error_code} ({errcode_exe_name} not available)"

        if platform.system() != "Windows":
            if not os.access(errcode_exe, os.X_OK):
                return f"Error code {error_code} ({errcode_exe_name} not executable)"

        cmd = [errcode_exe, str(error_code)]

        # Use asyncio.to_thread to run the blocking subprocess.run in a separate thread
        result = await asyncio.to_thread(
            subprocess.run,
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=REDIX_LIBS_PATH,
            check=False # Do not raise CalledProcessError
        )
        
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()

        return f"Error code {error_code} (could not get description)"

    except subprocess.TimeoutExpired:
        return f"Error code {error_code} (errcode timed out)"
    except Exception as e:
        logger.error(f"Error calling errcode executable: {e}")
        return f"Error code {error_code} (error getting description)"

async def call_redix_exe(input_file: str, ifd_path: str, ofd_path: str, ack_file: str, err_file: str, # ack_file is no longer optional
                   output_file: str, conversion_flag: str, user_data: Optional[str], warning_level: int,
                   ta1_file: Optional[str] = None, # TA1FileName (-t) (optional)
                   segment_terminator: str = "new line", element_separator: str = "*", composite_separator: str = ":", release_character: str = "?", # Required params
                   out_ifd: Optional[str] = None, # OutIFD (-x) (optional)
                   out_ofd: Optional[str] = None, # OutOFD (-y) (optional)
                   out_output_file: Optional[str] = None, # OutOutputFileName (-g) (optional)
                   out_conversion_flag: Optional[str] = None # OutConversionFlag (-h) (optional)
                   ) -> int:
    """
    Executes redix executable with the given parameters.
    """

    if not REDIX_LIBS_PATH:
        raise Exception("REDIX_LIBS_PATH not configured.")

    if redix_exe_path is None:
        raise Exception("Redix executable is not loaded.")

    # Convert special values for segment terminator
    if segment_terminator == "new line" or segment_terminator == "0":
        segment_terminator_arg = "0"
    else:
        segment_terminator_arg = segment_terminator

    # Construct the complete command based on image provided parameters
    cmd = [
        redix_exe_path,
        f"-i={input_file}",
        f"-o={output_file}",
        f"-a={ack_file}", # Parameter -a is for AcknowledgementFileName, always passed now
        f"-e={err_file}",
        f"-f={ifd_path}",
        f"-d={ofd_path}",
        f"-c={conversion_flag}",
        f"-s={segment_terminator_arg}",
        f"-l={element_separator}",
        f"-m={composite_separator}",
        f"-r={release_character}",
    ]

    # Add optional parameters based on image provided
    # Note: WarningLevel is often defined by the API consumer (e.g., in ConversionRequest),
    # so we pass it here explicitly. The image lists it as optional, but in our API flow,
    # it's usually always provided with a default.
    cmd.append(f"-w={warning_level}") # Passing warning_level, as it's always available from request

    if ta1_file: # -t: TA1FileName (optional)
        cmd.append(f"-t={ta1_file}")
    if user_data: # -u: Userdata (optional)
        cmd.append(f"-u={user_data}")
    if out_ifd: # -x: OutIFD (optional)
        cmd.append(f"-x={out_ifd}")
    if out_ofd: # -y: OutOFD (optional)
        cmd.append(f"-y={out_ofd}")
    if out_output_file: # -g: OutOutputFileName (optional)
        cmd.append(f"-g={out_output_file}")
    if out_conversion_flag: # -h: OutConversionFlag (optional)
        cmd.append(f"-h={out_conversion_flag}")
    
    # Always append -k=1 for Use999
    cmd.append(f"-k=1") 
    logger.info(f"Appended -k=1 to Redix command line.")


    exe_name = "redix64.exe" if platform.system() == "Windows" else "redix64"

    logger.info(f"Executing {exe_name} with command: {cmd}")

    try:
        # Subprocess inherits environment variables from the parent process by default.
        # Ensure REDIX_BASE_WORK_DIR is set in the parent process (before FastAPI starts).
        result = await asyncio.to_thread(
            subprocess.run,
            cmd,
            capture_output=True,
            text=True,
            timeout=SUBPROCESS_TIMEOUT,
            cwd=REDIX_LIBS_PATH,
            shell=False,
            check=False # Do not raise CalledProcessError
        )
        
        logger.info(f"{exe_name} completed. Return code: {result.returncode}")
        logger.info(f"STDOUT: {result.stdout.strip()}")
        logger.info(f"STDERR: {result.stderr.strip()}")

        # Read error file
        error_details = ""
        if os.path.exists(err_file):
            try:
                with open(err_file, 'r', encoding='utf-8', errors='ignore') as f:
                    error_details = f.read().strip()
            except Exception as e:
                logger.warning(f"Could not read error file {err_file}: {e}")
                pass

        # Parse return code from STDOUT
        parsed_code = None
        stdout_stripped = result.stdout.strip()
        if stdout_stripped and (stdout_stripped.startswith('-') and stdout_stripped[1:].isdigit() or stdout_stripped.isdigit()):
            try:
                parsed_code = int(stdout_stripped)
            except ValueError:
                pass

        final_code = 0
        is_critical = False

        if parsed_code is not None and parsed_code != 0:
            final_code = parsed_code
            # Treat -901 as a warning, not critical
            if final_code == -901:
                logger.info(f"Treating code {final_code} as warning (always non-critical)")
                # Do not raise an exception, just return the code
                return final_code
            elif warning_level in [1, 2] and (error_details.startswith("Warning:") or "warn" in stdout_stripped.lower()):
                logger.info(f"Treating code {final_code} as warning based on warning_level and output")
                # Do not raise an exception, just return the code
                return final_code
            else:
                is_critical = True
        elif result.stderr.strip():
            is_critical = True
            final_code = -1 # Indicate a stderr error
        elif error_details and not error_details.startswith("Warning:"):
            is_critical = True
            final_code = -2 # Indicate an error file error
        elif result.returncode != 0:
            is_critical = True
            final_code = result.returncode

        if is_critical:
            error_msg = await get_error_message(final_code)
            full_error_message = f"{exe_name} failed (Code: {final_code}): {error_msg}. "
            if result.stderr.strip():
                full_error_message += f"STDERR: {result.stderr.strip()} "
            if error_details:
                full_error_message += f"Error File: {error_details}"
            raise Exception(full_error_message)

        return final_code

    except subprocess.TimeoutExpired as e:
        raise Exception(f"{exe_name} timed out after {e.timeout} seconds")
    except Exception as e:
        # Re-raise the exception if it's already an HTTPException or a custom error
        if isinstance(e, HTTPException):
            raise
        raise Exception(f"Failed to execute {exe_name}: {str(e)}")

# Pydantic Models
class ConversionRequest(BaseModel):
    # This field is used internally by convert_core to receive the path to the actual input file.
    # It will be populated by file-upload (after saving), server-file, or staging-file endpoints.
    input_file: Optional[str] = Field(None, description="Path to Input File on the server (internal use, do not populate directly via API for most endpoints).")
    input_data: Optional[str] = Field(None, description="Input Data as a string. Do not use with input_file.")
    conversion_flag: str = Field(..., description="Conversion Flag (e=UN/EDIFACT/RMap, x=X12, f=fixed-length, c=XML, t=CSV, n=NCPDP, h=HL7)")
    ifd_file: str = Field(..., description="IFD Filename (e.g., 'myrule.ifd' from RULES_DIR or full path if uploaded temp file)")
    ofd_file: str = Field(..., description="OFD Filename (e.g., 'myrule.ofd' from RULES_DIR or full path if uploaded temp file)")
    warning_level: int = Field(1, description="Warning Level (0=Stop on first error, 1=Continue with warnings, 2=Ignore all errors)")
    user_data: Optional[str] = Field("", description="User Data (optional)")
    segment_terminator: str = Field("new line", description="Segment Terminator")
    element_separator: str = Field("*", description="Element Separator")
    composite_separator: str = Field(":", description="Composite Separator")
    release_character: str = Field("?", description="Release Character")
    # New optional output/conversion flags based on the image
    ta1_file: Optional[str] = Field(None, description="TA1 File Name (optional)")
    out_ifd: Optional[str] = Field(None, description="Output IFD File (optional)")
    out_ofd: Optional[str] = Field(None, description="Output OFD File (optional)")
    out_output_file: Optional[str] = Field(None, description="Output Output File Name (optional)")
    out_conversion_flag: Optional[str] = Field(None, description="Output Conversion Flag (optional)")


class ConversionResponse(BaseModel):
    success: bool
    conversion_id: str
    filename_base: str
    input_file_name: Optional[str] = None # New field
    input_file_path: Optional[str] = None
    input_file_view_url: Optional[str] = None # New field
    output_file_path: Optional[str] = None
    output_file_view_url: Optional[str] = None
    error_file_path: Optional[str] = None
    error_file_view_url: Optional[str] = None
    ack_file_path: Optional[str] = None
    ack_file_view_url: Optional[str] = None
    ta1_file_path: Optional[str] = None
    ta1_file_view_url: Optional[str] = None
    archived_file_path: Optional[str] = None  # New field for archive functionality
    archived_file_view_url: Optional[str] = None  # New field for archive functionality
    conversion_result_summary: str
    warnings: List[str] = []
    processing_time_ms: int

class BatchStatusResponse(BaseModel):
    job_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_files_found: Optional[int] = 0
    files_processed: Optional[int] = 0
    successful_files: Optional[int] = 0
    failed_files: Optional[int] = 0
    summary: Optional[str] = None
    details: List[Dict[str, Any]] = [] # For individual file results
    error: Optional[str] = None

class BatchJobSummary(BaseModel):
    job_id: str
    status: str
    profile: str
    input_folder: str
    output_folder: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_files_found: int
    files_processed: int
    successful_files: int
    failed_files: int
    error: Optional[str] = None

class BatchSummaryResponse(BaseModel):
    total_jobs: int
    total_successful_files: int
    total_failed_files: int
    average_files_processed: float

class BatchFileDetail(BaseModel):
    filename: str
    status: str
    success: bool
    summary: str
    warnings: List[str]
    output_url: Optional[str]
    error_url: Optional[str]
    ack_url: Optional[str]
    ta1_url: Optional[str]
    archive_path: Optional[str]


# Mapping for conversion flags (for health check and form options)
CONVERSION_FLAGS = {
    "e": "e - UN/EDIFACT/RMap",
    "x": "x - X12",
    "f": "f - fixed-length flat file",
    "c": "c - XML",
    "t": "t - CSV delimited variable-length flat file",
    "n": "n - NCPDP",
    "h": "h - HL7"
}

# Helper function for safe path resolution and listing
def safe_list_directory(base_dir: str, sub_path: str = "", include_dirs: bool = False) -> List[dict]:
    """
    Safely lists files and (optionally) directories within a specified base directory,
    preventing directory traversal.
    """
    target_dir = os.path.join(base_dir, sub_path)
    # Normalize path to prevent directory traversal
    abs_target_dir = os.path.abspath(target_dir)

    # Ensure the resolved path is within the base directory
    if not abs_target_dir.startswith(os.path.abspath(base_dir)):
        logger.warning(f"Attempted directory traversal: {target_dir} outside {base_dir}")
        return []

    if not os.path.exists(abs_target_dir) or not os.path.isdir(abs_target_dir):
        return []

    files_info = []
    try:
        with os.scandir(abs_target_dir) as entries:
            for entry in sorted(entries, key=lambda e: e.name.lower()):
                file_info = {
                    "name": entry.name,
                    "path": os.path.relpath(entry.path, base_dir),
                    "is_dir": entry.is_dir(),
                    "size": entry.stat().st_size if not entry.is_dir() else None,
                    "last_modified": datetime.fromtimestamp(entry.stat().st_mtime).isoformat()
                }
                if entry.is_file() or (entry.is_dir() and include_dirs):
                    files_info.append(file_info)
    except Exception as e:
        logger.error(f"Error listing directory {abs_target_dir}: {e}")
    return files_info

def safe_file_path(base_dir: str, relative_path: str, allow_dirs: bool = False) -> Optional[str]:
    """
    Constructs a full file path and validates that it's within the base_dir.
    Returns the absolute path if valid, None otherwise.
    """
    if not relative_path: # Prevent empty path leading to base_dir itself
        return None
    full_path = os.path.join(base_dir, relative_path)
    abs_path = os.path.abspath(full_path)
    # Ensure the path starts with the absolute base directory path and is not just the base directory itself
    # Adding os.path.sep handles cases like /path/to/base_dir vs /path/to/base_directory_malicious
    if not abs_path.startswith(os.path.abspath(base_dir) + os.path.sep) and abs_path != os.path.abspath(base_dir):
        logger.warning(f"Attempted access outside base directory: {relative_path} from {base_dir}")
        return None
    
    if not allow_dirs and os.path.isdir(abs_path):
        return None # If we don't allow directories, and it's a directory, return None
    
    return abs_path

# --- Background Task for Batch Processing ---
async def _process_batch_folder_in_background(job_id: str,
                                              input_folder_full_path: str,
                                              config_profile_data: Dict[str, str],
                                              output_base_dir: str,
                                              batch_user_data: Optional[str]): # Renamed to batch_user_data
    
    await update_batch_job(job_id, {"status": BatchJobStatusEnum.PROCESSING})
    await add_batch_log(job_id, "INFO", f"Batch processing started for folder: {input_folder_full_path}")
    
    processed_count = 0
    success_count = 0
    failed_count = 0
    
    file_results = []

    # Extract common parameters from config profile data
    try:
        conversion_flag_char = config_profile_data['conversion_flag'].strip()[0]
        ifd_file_name = config_profile_data['ifd_file'].strip()
        ofd_file_name = config_profile_data['ofd_file'].strip()
        warning_level = int(config_profile_data.get('warning_level', str(WarningLevelEnum.continue_with_warnings.value)))
        segment_terminator = config_profile_data.get('segment_terminator', SegmentTerminatorEnum.new_line.value)
        element_separator = config_profile_data.get('element_separator', ElementSeparatorEnum.asterisk.value)
        composite_separator = config_profile_data.get('composite_separator', CompositeSeparatorEnum.colon.value)
        release_character = config_profile_data.get('release_character', ReleaseCharacterEnum.question.value)
        profile_user_data = config_profile_data.get('user_data', '') # User data from profile
    except KeyError as e:
        error_msg = f"Batch processing failed: Missing mandatory parameter in profile. {e}"
        logger.error(error_msg)
        await add_batch_log(job_id, "ERROR", error_msg)
        await update_batch_job(job_id, {"status": BatchJobStatusEnum.FAILED, "error": error_msg, "end_time": datetime.now(timezone.utc)})
        return
    except ValueError as e:
        error_msg = f"Batch processing failed: Invalid parameter in profile. {e}"
        logger.error(error_msg)
        await add_batch_log(job_id, "ERROR", error_msg)
        await update_batch_job(job_id, {"status": BatchJobStatusEnum.FAILED, "error": error_msg, "end_time": datetime.now(timezone.utc)})
        return

    # List files in the batch input folder
    try:
        files_in_folder = [f for f in os.listdir(input_folder_full_path) if os.path.isfile(os.path.join(input_folder_full_path, f))]
        total_files = len(files_in_folder)
        await update_batch_job(job_id, {"total_files_found": total_files})
        logger.info(f"Batch Job {job_id}: Found {total_files} files in {input_folder_full_path}")
        await add_batch_log(job_id, "INFO", f"Found {total_files} files in {input_folder_full_path}")
    except Exception as e:
        error_msg = f"Batch processing failed: Could not list files in input folder {input_folder_full_path}: {e}"
        logger.error(error_msg)
        await add_batch_log(job_id, "ERROR", error_msg)
        await update_batch_job(job_id, {"status": BatchJobStatusEnum.FAILED, "error": error_msg, "end_time": datetime.now(timezone.utc)})
        return

    for filename in files_in_folder:
        file_path_in_batch_input = os.path.join(input_folder_full_path, filename)
        processed_count += 1
        current_file_status = {"filename": filename, "status": "PENDING"}

        try:
            # Determine the final user_data for this specific file
            # If batch_user_data is provided and not empty, it overrides the profile's user_data.
            final_file_user_data = batch_user_data.strip() if batch_user_data is not None and batch_user_data.strip() != '' else profile_user_data
            
            # Generate new unique filename base for this file's output
            # Use original filename for base to avoid issues with generate_filename_base
            # The generate_filename_base takes input_source (filename of the file),
            # conversion_flag_char, and an optional user_prefix.
            file_specific_filename_base = generate_filename_base(filename, conversion_flag_char, final_file_user_data) # Use final_file_user_data as prefix
            
            # Construct paths for this specific conversion output/error/ack/ta1 files
            file_specific_output_file = os.path.join(output_base_dir, f"{file_specific_filename_base}_output.txt")
            file_specific_ack_file = os.path.join(ACK_DIR, f"{file_specific_filename_base}.ack")
            file_specific_err_file = os.path.join(ERROR_DIR, f"{file_specific_filename_base}.err")
            file_specific_ta1_file = os.path.join(output_base_dir, f"{file_specific_filename_base}.ta1") # TA1 in same output folder

            # Construct the internal ConversionRequest object for this file
            request_for_core = ConversionRequest(
                input_file=file_path_in_batch_input, # Path to the current file in the batch folder
                conversion_flag=conversion_flag_char,
                ifd_file=ifd_file_name,
                ofd_file=ofd_file_name,
                warning_level=warning_level,
                user_data=final_file_user_data, # Pass the resolved user data
                segment_terminator=segment_terminator,
                element_separator=element_separator,
                composite_separator=composite_separator,
                release_character=release_character,
                ta1_file=file_specific_ta1_file # Pass generated TA1 path
            )

            # Call the core conversion logic
            conversion_result = await convert_core(request_for_core, file_specific_filename_base)
            
            # Update current file status
            current_file_status["success"] = conversion_result.success
            current_file_status["summary"] = conversion_result.conversion_result_summary
            current_file_status["warnings"] = conversion_result.warnings
            current_file_status["output_url"] = conversion_result.output_file_view_url
            current_file_status["error_url"] = conversion_result.error_file_view_url
            current_file_status["ack_url"] = conversion_result.ack_file_view_url
            current_file_status["ta1_url"] = conversion_result.ta1_file_view_url
            
            # Decide on file movement based on Redix return code from summary
            redix_return_code = 0
            if conversion_result.conversion_result_summary:
                try:
                    redix_return_code = int(conversion_result.conversion_result_summary.split(' ')[0])
                except (ValueError, IndexError):
                    logger.warning(f"Batch Job {job_id}: Could not parse return code from summary: {conversion_result.conversion_result_summary}. Defaulting to 0 for file {filename}.")
                    await add_batch_log(job_id, "WARNING", f"Could not parse return code for {filename}. Defaulting to 0.")
                    redix_return_code = 0 # Default to success if parsing fails

            if redix_return_code == 0 or redix_return_code == -901: # Success or acceptable warning
                success_count += 1
                current_file_status["status"] = "COMPLETED"
                # Move input file to archive
                archive_file_path = os.path.join(ARCHIVE_DIR, os.path.basename(file_path_in_batch_input)) # Keep original filename in archive
                shutil.move(file_path_in_batch_input, archive_file_path)
                current_file_status["archive_path"] = archive_file_path
                logger.info(f"Batch Job {job_id}: Successfully processed and moved '{filename}' to archive.")
                await add_batch_log(job_id, "INFO", f"Successfully processed and moved '{filename}' to archive.")
            else: # Failure
                failed_count += 1
                current_file_status["status"] = "FAILED"
                logger.warning(f"Batch Job {job_id}: Conversion failed for '{filename}' with code {redix_return_code}. File remains in batch input directory for review.")
                await add_batch_log(job_id, "WARNING", f"Conversion failed for '{filename}' with code {redix_return_code}.")

        except HTTPException as http_exc:
            failed_count += 1
            current_file_status["status"] = "FAILED_API_ERROR"
            current_file_status["error"] = str(http_exc.detail)
            logger.error(f"Batch Job {job_id}: API error for '{filename}': {http_exc.detail}")
            await add_batch_log(job_id, "ERROR", f"API error for '{filename}': {http_exc.detail}")
            # File remains in batch input directory

        except Exception as e:
            failed_count += 1
            current_file_status["status"] = "FAILED_EXCEPTION"
            current_file_status["error"] = str(e)
            logger.error(f"Batch Job {job_id}: Unexpected error processing '{filename}': {e}")
            await add_batch_log(job_id, "ERROR", f"Unexpected error processing '{filename}': {e}")
            # File remains in batch input directory
        
        await add_batch_file_detail(job_id, current_file_status)
        
        # Update overall job status
        await update_batch_job(job_id, {
            "files_processed": processed_count,
            "successful_files": success_count,
            "failed_files": failed_count
        })

    # Final update after all files are processed
    final_status = BatchJobStatusEnum.COMPLETED if failed_count == 0 else BatchJobStatusEnum.COMPLETED_WITH_ERRORS
    await update_batch_job(job_id, {"status": final_status, "end_time": datetime.now(timezone.utc)})
    logger.info(f"Batch Job {job_id}: Completed processing. Successful: {success_count}, Failed: {failed_count}")
    await add_batch_log(job_id, "INFO", f"Completed processing. Successful: {success_count}, Failed: {failed_count}")


# --- API Endpoints ---

@app.get("/")
async def health_check():
    """Basic health check for the API."""
    return {
        "status": "healthy",
        "version": API_VERSION,
        "conversion_flags": list(CONVERSION_FLAGS.keys()),
        "redix_engine_status": "loaded" if redix_exe_path else "not loaded",
        "platform": platform.system()
    }

@app.get("/api/v1/form-options")
async def get_form_options():
    """Get dynamic options for the conversion form."""
    ifd_files = []
    ofd_files = []

    if os.path.exists(RULES_DIR):
        try:
            files = os.listdir(RULES_DIR)
            ifd_files = sorted([f for f in files if f.lower().endswith('.ifd')])
            ofd_files = sorted([f.name for f in os.scandir(RULES_DIR) if f.is_file() and f.name.lower().endswith('.ofd')]) # More robust listing for OFD
        except Exception as e:
            logger.error(f"Error listing rules directory: {e}")

    return {
        "conversion_flags": [
            {"value": "e", "label": "e - UN/EDIFACT/RMap"},
            {"value": "x", "label": "x - X12"},
            {"value": "f", "label": "f - fixed-length flat file"},
            {"value": "c", "label": "c - XML"},
            {"value": "t", "label": "t - CSV delimited variable-length flat file"},
            {"value": "n", "label": "n - NCPDP"},
            {"value": "h", "label": "h - HL7"}
        ],
        "ifd_files": [{"value": f, "label": f} for f in ifd_files],
        "ofd_files": [{"value": f, "label": f} for f in ofd_files],
        "warning_levels": [
            {"value": 0, "label": "0 - Stop on first error"},
            {"value": 1, "label": "1 - Continue with warnings"},
            {"value": 2, "label": "2 - Ignore all errors"}
        ],
        "allow_rule_file_upload": ALLOW_RULE_FILE_UPLOAD,
        "staging_profiles": list(STAGING_CONFIG_PROFILES.keys()) # NEW: Expose available staging profiles
    }

@app.get("/api/v1/files")
async def list_user_files(limit: int = 50):
    """List recent conversion files with descriptive names."""
    try:
        files = []

        # Scan output directory for recent files
        output_pattern = os.path.join(OUTPUT_DIR, "*_output.txt")
        # Get all output files, then sort by modification time, and slice
        all_output_files = glob.glob(output_pattern)
        # Filter out directories if any match the pattern accidentally
        output_files_and_times = [(f, os.path.getmtime(f)) for f in all_output_files if os.path.isfile(f)]
        output_files_and_times.sort(key=lambda x: x[1], reverse=True)
        recent_output_files = [f for f, _ in output_files_and_times[:limit]]


        for file_path in recent_output_files:
            file_name = os.path.basename(file_path)
            # Remove '_output.txt' to get the base name
            base_name = file_name.rsplit('_output.txt', 1)[0] if file_name.endswith('_output.txt') else file_name

            # Check for related files
            input_file = os.path.join(INPUT_DIR, f"{base_name}_input.txt")
            ack_file = os.path.join(ACK_DIR, f"{base_name}.ack")
            err_file = os.path.join(ERROR_DIR, f"{base_name}.err")
            ta1_file = os.path.join(OUTPUT_DIR, f"{base_name}.ta1") # TA1 often in output dir

            file_info = {
                "base_name": base_name,
                "created": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                "input_url": f"/api/v1/view-file/input/{os.path.basename(input_file)}" if os.path.exists(input_file) else None,
                "output_url": f"/api/v1/view-file/output/{file_name}",
                "ack_url": f"/api/v1/view-file/ack/{os.path.basename(ack_file)}" if os.path.exists(ack_file) else None,
                "error_url": f"/api/v1/view-file/error/{os.path.basename(err_file)}" if os.path.exists(err_file) else None,
                "ta1_url": f"/api/v1/view-file/ta1/{os.path.basename(ta1_file)}" if os.path.exists(ta1_file) else None
            }
            files.append(file_info)

        return {"files": files}
    except Exception as e:
        logger.error(f"Failed to list files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")


@app.get("/api/v1/server-files")
async def list_server_files(path: str = "", include_dirs: bool = False):
    """
    Lists files and directories within the configured SHARED_DIR.
    Use `path` query parameter to navigate subdirectories.
    """
    try:
        files_and_dirs = safe_list_directory(SHARED_DIR, path, include_dirs)
        return {"current_path": path, "files": files_and_dirs}
    except Exception as e:
        logger.error(f"Error listing server files in path '{path}': {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list server files: {str(e)}")

@app.get("/api/v1/staging-files")
async def list_staging_files():
    """Lists files currently in the staging directory."""
    try:
        files_info = safe_list_directory(STAGING_DIR)
        return {"files": files_info}
    except Exception as e:
        logger.error(f"Error listing staging files: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list staging files: {str(e)}")

@app.get("/api/v1/staging-profiles")
async def list_staging_profiles():
    """Lists available staging configuration profiles defined in redix_cloud.conf."""
    return {
        "default_profile": DEFAULT_STAGING_PROFILE_NAME,
        "available_profiles": list(STAGING_CONFIG_PROFILES.keys())
    }

@app.post("/api/v1/staging/upload")
async def upload_to_staging(file: UploadFile = File(..., description="File to upload to staging area")):
    """Uploads a file to the staging directory."""
    staging_file_path = os.path.join(STAGING_DIR, file.filename)

    # Prevent overwriting existing files or ensure unique names
    if os.path.exists(staging_file_path):
        name, ext = os.path.splitext(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        staging_file_path = os.path.join(STAGING_DIR, f"{name}_{timestamp}{ext}")
        logger.warning(f"File {file.filename} already exists in staging. Saving as {os.path.basename(staging_file_path)}")

    try:
        await file.seek(0)
        content = await file.read()
        with open(staging_file_path, 'wb') as f:
            f.write(content)
        logger.info(f"Uploaded {file.filename} to staging as {os.path.basename(staging_file_path)}")
        return {"message": f"File '{os.path.basename(staging_file_path)}' uploaded to staging successfully", "filename": os.path.basename(staging_file_path)}
    except Exception as e:
        logger.error(f"Failed to upload file to staging: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload file to staging: {str(e)}")

@app.delete("/api/v1/staging/{filename}")
async def delete_from_staging(filename: str):
    """Deletes a file from the staging directory."""
    file_path = safe_file_path(STAGING_DIR, filename)

    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found in staging area.")
    if os.path.isdir(file_path):
        raise HTTPException(status_code=400, detail=f"Cannot delete directory '{filename}'.")

    try:
        os.remove(file_path)
        logger.info(f"Deleted file from staging: {filename}")
        return {"message": f"File '{filename}' deleted successfully."}
    except Exception as e:
        logger.error(f"Failed to delete file '{filename}' from staging: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")


@app.post("/api/v1/convert/file-upload")
async def convert_file_upload(
    Input_File: UploadFile = File(..., description="Input File to upload *"),
    IFD_File: UploadFile = File(..., description="IFD Rule File to upload *"),
    OFD_File: UploadFile = File(..., description="OFD Rule File to upload *"),
    Conversion_Flag: ConversionFlagEnum = Form(ConversionFlagEnum.e, description="Conversion Flag * (e=UN/EDIFACT/RMap, x=X12, f=fixed-length, c=XML, t=CSV, n=NCPDP, h=HL7)"),
    WarningLevel: WarningLevelEnum = Form(WarningLevelEnum.continue_with_warnings, description="Warning Level * (0=Stop on first error, 1=Continue with warnings, 2=Ignore all errors)"),
    User_Data: str = Form("", description="User Data (optional)"),
    Segment_Terminator: SegmentTerminatorEnum = Form(SegmentTerminatorEnum.new_line, description="Segment Terminator *"),
    Element_Separator: ElementSeparatorEnum = Form(ElementSeparatorEnum.asterisk, description="Element Separator *"),
    Composite_Separator: CompositeSeparatorEnum = Form(CompositeSeparatorEnum.colon, description="Composite Separator *"),
    Release_Character: ReleaseCharacterEnum = Form(ReleaseCharacterEnum.question, description="Release Character *")
):
    """
    Option 1: Browser Upload - Upload files directly from your browser.
    Input, IFD, and OFD files are all uploaded via this endpoint.
    """
    conversion_id_short = str(uuid.uuid4())[:8]

    if not ALLOW_RULE_FILE_UPLOAD:
         raise HTTPException(status_code=403, detail="Uploading IFD/OFD rule files is disabled by server configuration.")

    # Get the single character for the conversion flag from the enum value
    # e.g., Conversion_Flag.value is "e - UN/EDIFACT/RMap", so [0] gives 'e'
    conversion_flag_char = Conversion_Flag.value[0]
    # Don't use User_Data as prefix in generate_filename_base for direct upload, to avoid filename issues
    filename_base = generate_filename_base(Input_File.filename, conversion_flag_char, None)

    input_file_save_path = os.path.join(INPUT_DIR, f"{filename_base}_input.txt")
    temp_ifd_path = os.path.join(RULES_DIR, f"upload_ifd_{conversion_id_short}_{IFD_File.filename}")
    temp_ofd_path = os.path.join(RULES_DIR, f"upload_ofd_{conversion_id_short}_{OFD_File.filename}")

    # List of files to clean up at the end (only temporary rule files created from uploads)
    files_to_cleanup = [temp_ifd_path, temp_ofd_path]

    try:
        await Input_File.seek(0)
        content = await Input_File.read()
        with open(input_file_save_path, 'wb') as f:
            f.write(content)
        logger.info(f"Saved uploaded input file: {input_file_save_path}")

        await IFD_File.seek(0)
        with open(temp_ifd_path, 'wb') as f:
            f.write(await IFD_File.read())
        logger.info(f"Saved uploaded IFD rule file: {temp_ifd_path}")

        await OFD_File.seek(0)
        with open(temp_ofd_path, 'wb') as f:
            f.write(await OFD_File.read())
        logger.info(f"Saved uploaded OFD rule file: {temp_ofd_path}")

        request = ConversionRequest(
            input_file=input_file_save_path,
            conversion_flag=conversion_flag_char,
            ifd_file=temp_ifd_path,
            ofd_file=temp_ofd_path,
            warning_level=WarningLevel.value,
            user_data=User_Data,
            segment_terminator=Segment_Terminator.value,
            element_separator=Element_Separator.value,
            composite_separator=Composite_Separator.value,
            release_character=Release_Character.value
        )

        result = await convert_core(request, filename_base)
        result.input_file_path = input_file_save_path
        result.input_file_view_url = f"/api/v1/view-file/input/{os.path.basename(input_file_save_path)}"
        result.input_file_name = os.path.basename(Input_File.filename)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File upload conversion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File upload conversion failed: {str(e)}")
    finally:
        if CLEANUP_TEMP_FILES:
            for f_path in files_to_cleanup:
                if os.path.exists(f_path):
                    try:
                        os.remove(f_path)
                        logger.info(f"Cleaned up temporary rule file: {f_path}")
                    except Exception as e:
                        logger.warning(f"Failed to cleanup {f_path}: {e}")


@app.post("/api/v1/convert/staging-file")
async def convert_staging_file(
    Staged_Filename: str = Form(..., description="Filename of the input file previously uploaded to the staging area. Please refer to /api/v1/staging-files for available filenames. *"),
    Config_Profile: Optional[StagingProfileEnum] = Form(None, description=f"Name of the predefined staging configuration profile from redix_cloud.conf. Defaults to '{DEFAULT_STAGING_PROFILE_NAME}' if not provided. *"),
    User_Data: Optional[str] = Form(None, description="Optional user data specific to this conversion. If left blank, profile setting is used.")
):
    """
    Option 3: Staged File Processing - Convert a file previously uploaded to the staging area,
    using a predefined configuration profile from `redix_cloud.conf`.
    """
    staged_file_src_path = safe_file_path(STAGING_DIR, Staged_Filename)

    if not staged_file_src_path or not os.path.exists(staged_file_src_path) or os.path.isdir(staged_file_src_path):
        raise HTTPException(status_code=400, detail=f"Staged file '{Staged_Filename}' not found or is a directory.")

    profile_name_to_use = Config_Profile.value if Config_Profile else DEFAULT_STAGING_PROFILE_NAME
    
    if not profile_name_to_use:
        raise HTTPException(status_code=400, detail="No staging config profile specified in request and no default profile configured in redix_cloud.conf.")

    config_profile_data = STAGING_CONFIG_PROFILES.get(profile_name_to_use)

    if not config_profile_data:
        raise HTTPException(status_code=400, detail=f"Staging config profile '{profile_name_to_use}' not found in redix_cloud.conf. Available profiles: {', '.join(STAGING_CONFIG_PROFILES.keys()) if STAGING_CONFIG_PROFILES else 'None'}.")

    try:
        conversion_flag_char = config_profile_data['conversion_flag'].strip()[0]
        ifd_file = config_profile_data['ifd_file'].strip()
        ofd_file = config_profile_data['ofd_file'].strip()
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Staging profile '{profile_name_to_use}' is missing a mandatory parameter: {e}. Check redix_cloud.conf.")
    
    warning_level_val = config_profile_data.get('warning_level', str(WarningLevelEnum.continue_with_warnings.value))
    try:
        warning_level = int(warning_level_val)
    except ValueError:
        raise HTTPException(status_code=500, detail=f"Invalid 'warning_level' in profile '{profile_name_to_use}'. Must be an integer.")

    segment_terminator = config_profile_data.get('segment_terminator', SegmentTerminatorEnum.new_line.value)
    element_separator = config_profile_data.get('element_separator', ElementSeparatorEnum.asterisk.value)
    composite_separator = config_profile_data.get('composite_separator', CompositeSeparatorEnum.colon.value)
    release_character = config_profile_data.get('release_character', ReleaseCharacterEnum.question.value)
    
    profile_user_data = config_profile_data.get('user_data', '')
    if User_Data is not None and User_Data.strip() != '':
        final_user_data = User_Data.strip()
    else:
        final_user_data = profile_user_data

    filename_base = generate_filename_base(Staged_Filename, conversion_flag_char, None)
    input_file_dest_path = os.path.join(INPUT_DIR, f"{filename_base}_input.txt")

    try:
        shutil.move(staged_file_src_path, input_file_dest_path)
        logger.info(f"Moved staged file from {staged_file_src_path} to {input_file_dest_path} for processing.")

        core_request = ConversionRequest(
            input_file=input_file_dest_path,
            conversion_flag=conversion_flag_char,
            ifd_file=ifd_file,
            ofd_file=ofd_file,
            warning_level=warning_level,
            user_data=final_user_data,
            segment_terminator=segment_terminator,
            element_separator=element_separator,
            composite_separator=composite_separator,
            release_character=release_character
        )

        result = await convert_core(core_request, filename_base)
        
        return_code = 0
        if result.conversion_result_summary:
            try:
                return_code = int(result.conversion_result_summary.split(' ')[0])
            except (ValueError, IndexError):
                logger.warning(f"Could not parse return code from summary: {result.conversion_result_summary}. Defaulting to 0.")
                return_code = 0

        if return_code == 0 or return_code == -901:
            archive_file_path = os.path.join(ARCHIVE_DIR, f"{filename_base}_input.txt")
            try:
                shutil.move(input_file_dest_path, archive_file_path)
                logger.info(f"Successfully moved processed file to archive: {archive_file_path}")
                result.archived_file_path = archive_file_path
                result.archived_file_view_url = f"/api/v1/view-file/archive/{os.path.basename(archive_file_path)}"
            except Exception as archive_error:
                logger.error(f"Failed to move file to archive: {archive_error}")
        else:
            logger.info(f"Input file {input_file_dest_path} remains in INPUT_DIR due to conversion return code {return_code}.")
        
        result.input_file_path = input_file_dest_path
        result.input_file_view_url = f"/api/v1/view-file/input/{os.path.basename(input_file_dest_path)}"
        result.input_file_name = Staged_Filename
        return result

    except HTTPException as http_exc:
        if os.path.exists(input_file_dest_path):
            try:
                shutil.move(input_file_dest_path, staged_file_src_path)
                logger.warning(f"Moved file back to staging due to HTTP exception: {os.path.basename(input_file_dest_path)}")
            except Exception as rollback_e:
                logger.error(f"Failed to move file back to staging after HTTP exception: {rollback_e}")
        raise http_exc
        
    except Exception as e:
        logger.error(f"Staged file conversion failed: {str(e)}")
        if os.path.exists(input_file_dest_path):
            try:
                shutil.move(input_file_dest_path, staged_file_src_path)
                logger.warning(f"Moved file back to staging due to exception: {os.path.basename(input_file_dest_path)}")
            except Exception as rollback_e:
                logger.error(f"Failed to move file back to staging after exception: {rollback_e}")
        raise HTTPException(status_code=500, detail=f"Staged file conversion failed: {str(e)}")


async def convert_core(request: ConversionRequest, filename_base: str) -> ConversionResponse:
    """Core conversion function, refactored to be called by various input methods."""
    start_time = datetime.now()
    conversion_id = str(uuid.uuid4())

    if redix_exe_path is None:
        raise HTTPException(status_code=500, detail="Redix executable not available")

    def resolve_rule_file(file_name: str) -> Optional[str]:
        if os.path.isabs(file_name) and os.path.exists(file_name):
            return file_name
        rules_path = safe_file_path(RULES_DIR, file_name)
        if rules_path and os.path.exists(rules_path):
            return rules_path
        return None

    ifd_path = resolve_rule_file(request.ifd_file)
    ofd_path = resolve_rule_file(request.ofd_file)

    if not ifd_path:
        raise HTTPException(status_code=400, detail=f"IFD file not found or accessible: {request.ifd_file}")
    if not ofd_path:
        raise HTTPException(status_code=400, detail=f"OFD file not found or accessible: {request.ofd_file}")

    input_file_path = None
    temp_input_created = False

    if request.input_data:
        input_file_path = os.path.join(INPUT_DIR, f"{filename_base}_input.txt")
        try:
            with open(input_file_path, 'w', encoding='utf-8') as f:
                f.write(request.input_data)
            temp_input_created = True
            logger.info(f"Created temporary input file from data string: {input_file_path}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to prepare input data: {str(e)}")
    elif request.input_file:
        input_file_path = request.input_file
        if not os.path.exists(input_file_path):
            raise HTTPException(status_code=400, detail=f"Input file not found at provided path: {input_file_path}")
    else:
        raise HTTPException(status_code=400, detail="No input data or input file specified for conversion.")


    output_file = os.path.join(OUTPUT_DIR, f"{filename_base.replace('0_', '')}_output.txt")
    ack_file = os.path.join(ACK_DIR, f"{filename_base.replace('0_', '')}.ack")
    
    err_file = os.path.join(ERROR_DIR, f"{filename_base.replace('0_', '')}.err")
    generated_ta1_path = os.path.join(OUTPUT_DIR, f"{filename_base.replace('0_', '')}.ta1")
    ta1_file_for_redix = request.ta1_file if request.ta1_file else generated_ta1_path


    try:
        return_code = await call_redix_exe(
            input_file_path, ifd_path, ofd_path, ack_file, err_file,
            output_file, request.conversion_flag, request.user_data,
            request.warning_level, 
            ta1_file_for_redix,
            request.segment_terminator,
            request.element_separator, request.composite_separator,
            request.release_character,
            request.out_ifd, request.out_ofd, request.out_output_file, request.out_conversion_flag
        )

        success = True 
        summary = ""
        warnings = []

        if return_code == 0:
            summary = "0 (success)"
        elif return_code == -901:
            summary = f"{return_code} (warnings - acceptable)"
            warnings = [await get_error_message(return_code)]
        elif request.warning_level in [1, 2]:
            summary = f"{return_code} (warnings)"
            warnings = [await get_error_message(return_code)]
        else:
            success = False
            summary = f"{return_code} (failure)"
            warnings = [await get_error_message(return_code)]

        output_path = output_file if os.path.exists(output_file) else None
        error_path = err_file if os.path.exists(err_file) else None
        ack_path = ack_file if os.path.exists(ack_file) else None
        
        ta1_path_for_response = None
        if request.ta1_file and os.path.exists(request.ta1_file):
             ta1_path_for_response = request.ta1_file
        elif os.path.exists(generated_ta1_path):
            ta1_path_for_response = generated_ta1_path
        
        archived_file_path = None
        archived_file_view_url = None

        output_url = f"/api/v1/view-file/output/{os.path.basename(output_file)}" if output_path else None
        error_url = f"/api/v1/view-file/error/{os.path.basename(err_file)}" if error_path else None
        ack_url = f"/api/v1/view-file/ack/{os.path.basename(ack_file)}" if ack_path else None
        ta1_url = f"/api/v1/view-file/ta1/{os.path.basename(ta1_path_for_response)}" if ta1_path_for_response else None


        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)

        return ConversionResponse(
            success=success,
            conversion_id=conversion_id,
            filename_base=filename_base,
            input_file_path=input_file_path,
            input_file_view_url=f"/api/v1/view-file/input/{os.path.basename(input_file_path)}" if input_file_path else None,
            output_file_path=output_path,
            output_file_view_url=output_url,
            error_file_path=error_path,
            error_file_view_url=error_url,
            ack_file_path=ack_path,
            ack_file_view_url=ack_url,
            ta1_file_path=ta1_path_for_response,
            ta1_file_view_url=ta1_url,
            archived_file_path=archived_file_path,
            archived_file_view_url=archived_file_view_url,
            conversion_result_summary=summary,
            warnings=warnings,
            processing_time_ms=processing_time
        )

    except Exception as e:
        logger.error(f"Core conversion failed for filename_base {filename_base}: {str(e)}")
        if isinstance(e, HTTPException):
            raise
        error_details = ""
        if os.path.exists(err_file):
            try:
                with open(err_file, 'r', encoding='utf-8', errors='ignore') as f:
                    error_details = f.read().strip()
                if error_details:
                    e_detail = f"{str(e)}. Error file content: {error_details}"
                    raise HTTPException(status_code=500, detail=f"Conversion failed: {e_detail}")
            except Exception:
                pass
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    finally:
        if CLEANUP_TEMP_FILES and temp_input_created:
            should_clean_temp_input = False
            if 'result' in locals() and result.success:
                should_clean_temp_input = True

            if should_clean_temp_input:
                if input_file_path and os.path.exists(input_file_path):
                    try:
                        os.remove(input_file_path)
                        logger.info(f"Cleaned up temporary string input file (success): {input_file_path}")
                    except Exception as e:
                        logger.warning(f"Cleanup failed for {input_file_path}: {e}")
            else:
                if input_file_path and os.path.exists(input_file_path):
                    logger.info(f"Preserving temporary string input file {input_file_path} due to non-success conversion or external error.")


# --- Batch Processing Models and Endpoints ---
@app.post("/api/v1/batch-convert/folder", summary="Batch Convert Files in a Folder",
          description="Initiates asynchronous conversion for all files in a specified server subfolder using a predefined profile.")
async def batch_convert_folder(
    background_tasks: BackgroundTasks,
    Input_Subfolder: str = Form(..., description=f"Name of the subfolder within {os.path.basename(BATCH_INPUT_DIR)} containing files to process. *"),
    Config_Profile: StagingProfileEnum = Form(..., description="Name of the predefined conversion profile to apply to all files in this batch. *"),
    Output_Subfolder: Optional[str] = Form(None, description=f"Optional subfolder within {os.path.basename(OUTPUT_DIR)} to place converted files. Defaults to batch_job_id if not provided."),
    User_Data: Optional[str] = Form(None, description="Optional user data to apply to all files in this batch. If left blank, profile setting is used."),
    api_key: str = Depends(get_api_key)
):
    job_id = str(uuid.uuid4())
    input_folder_full_path = safe_file_path(BATCH_INPUT_DIR, Input_Subfolder, allow_dirs=True)

    if not input_folder_full_path or not os.path.exists(input_folder_full_path) or not os.path.isdir(input_folder_full_path):
        raise HTTPException(status_code=400, detail=f"Input subfolder '{Input_Subfolder}' not found or is not a directory in {os.path.basename(BATCH_INPUT_DIR)}.")
    
    config_profile_data = STAGING_CONFIG_PROFILES.get(Config_Profile.value)
    if not config_profile_data:
        raise HTTPException(status_code=400, detail=f"Config profile '{Config_Profile.value}' not found. Available: {', '.join(STAGING_CONFIG_PROFILES.keys())}. Check redix_cloud.conf.")

    output_subfolder_name = Output_Subfolder if Output_Subfolder else job_id
    batch_output_full_path = os.path.join(OUTPUT_DIR, output_subfolder_name)
    os.makedirs(batch_output_full_path, exist_ok=True)

    await create_batch_job(job_id, Config_Profile.value, input_folder_full_path, batch_output_full_path)
    logger.info(f"Batch conversion job {job_id} initiated for folder: {input_folder_full_path} using profile: {Config_Profile.value}")

    background_tasks.add_task(
        _process_batch_folder_in_background,
        job_id,
        input_folder_full_path,
        config_profile_data,
        batch_output_full_path,
        User_Data
    )

    return {"job_id": job_id, "status": "Batch processing initiated. Use /api/v1/batch-status/{job_id} to check progress."}

@app.get("/api/v1/batch-status/{Job_Id}", response_model=BatchStatusResponse, summary="Get Batch Job Status",
          description="Retrieves the current status and results of a specific batch conversion job.")
async def get_batch_status(
    Job_Id: str = Path(..., alias="Job_Id"),
    api_key: str = Depends(get_api_key)
):
    status = await get_batch_job(Job_Id)
    if not status:
        raise HTTPException(status_code=404, detail=f"Batch job '{Job_Id}' not found.")
    return status

@app.get("/api/v1/batch-jobs", response_model=List[BatchJobSummary])
async def list_batch_jobs_api(
    Status: Optional[BatchJobStatusEnum] = Query(None, alias="Status", description="Filter by job status (e.g., PENDING, COMPLETED)."),
    Config_Profile: Optional[StagingProfileEnum] = Query(None, alias="Config_Profile", description="Filter by configuration profile used."),
    Start_Date: Optional[date] = Query(None, alias="Start_Date", description="Filter by start date (YYYY-MM-DD)"),
    End_Date: Optional[date] = Query(None, alias="End_Date", description="Filter by end date (YYYY-MM-DD)"),
    Limit: int = Query(10, ge=1, le=100, alias="Limit", description="Maximum number of jobs to return."),
    Offset: int = Query(0, ge=0, alias="Offset", description="Number of jobs to skip."),
    api_key: str = Depends(get_api_key)
):
    start_dt = datetime.combine(Start_Date, datetime.min.time(), tzinfo=timezone.utc) if Start_Date else None
    end_dt = datetime.combine(End_Date, datetime.min.time(), tzinfo=timezone.utc) if End_Date else None
    jobs = await list_batch_jobs(Status, Config_Profile.value if Config_Profile else None, start_dt, end_dt, Limit, Offset)
    return jobs

@app.get("/api/v1/batch-jobs/summary", response_model=BatchSummaryResponse)
async def get_batch_jobs_summary(
    Start_Date: Optional[date] = Query(None, alias="Start_Date", description="Start date for summary (YYYY-MM-DD)"),
    End_Date: Optional[date] = Query(None, alias="End_Date", description="End date for summary (YYYY-MM-DD)"),
    Config_Profile: Optional[StagingProfileEnum] = Query(None, alias="Config_Profile", description="Filter by configuration profile used."),
    api_key: str = Depends(get_api_key)
):
    start_dt = datetime.combine(Start_Date, datetime.min.time(), tzinfo=timezone.utc) if Start_Date else None
    end_dt = datetime.combine(End_Date, datetime.min.time(), tzinfo=timezone.utc) if End_Date else None
    summary = await get_batch_summary(start_dt, end_dt, Config_Profile.value if Config_Profile else None)
    return summary

@app.get("/api/v1/batch-jobs/{Job_Id}/logs")
async def get_batch_job_logs(
    Job_Id: str = Path(..., alias="Job_Id"),
    Limit: int = Query(50, alias="Limit"),
    Offset: int = Query(0, alias="Offset"),
    Log_Level: Optional[LogLevelEnum] = Query(None, alias="Log_Level", description="Log Level"),
    api_key: str = Depends(get_api_key)
):
    logs = await get_batch_logs(Job_Id, Limit, Offset, Log_Level.value if Log_Level else None)
    if not logs and not await get_batch_job(Job_Id):
        raise HTTPException(status_code=404, detail=f"Batch job '{Job_Id}' not found.")
    return logs

@app.get("/api/v1/batch-jobs/{Job_Id}/files/{Filename}/details", response_model=BatchFileDetail)
async def get_batch_file_detail(
    Job_Id: str = Path(..., alias="Job_Id"),
    Filename: str = Path(..., alias="Filename"),
    api_key: str = Depends(get_api_key)
):
    detail = await get_batch_file_details(Job_Id, Filename)
    if not detail:
        raise HTTPException(status_code=404, detail=f"File '{Filename}' not found in batch job '{Job_Id}'.")
    return detail

@app.get("/api/v1/download-file/{File_Type}/{Filename}")
async def download_generated_file(
    File_Type: FileTypeEnum = Path(..., alias="File_Type", description="Type of file to download"),
    Filename: str = Path(..., alias="Filename", description="Name of the file"),
    api_key: str = Depends(get_api_key)
):
    base_dir_map = {
        "input": INPUT_DIR,
        "output": OUTPUT_DIR,
        "error": ERROR_DIR,
        "ack": ACK_DIR,
        "ta1": OUTPUT_DIR,
        "staging": STAGING_DIR,
        "shared": SHARED_DIR,
        "archive": ARCHIVE_DIR
    }
    file_type = File_Type.value
    if file_type not in base_dir_map:
        raise HTTPException(status_code=400, detail="Invalid file type. Supported: input, output, error, ack, ta1, staging, shared, archive.")

    base_dir = base_dir_map[file_type]
    file_path = safe_file_path(base_dir, Filename)

    if not file_path or not os.path.exists(file_path) or os.path.isdir(file_path):
        raise HTTPException(status_code=404, detail="File not found or access denied.")

    try:
        return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type="application/octet-stream")
    except Exception as e:
        logger.error(f"Failed to download file {file_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")


@app.get("/api/v1/view-file/{File_Type}/{Filename}")
async def view_generated_file(
    File_Type: FileTypeEnum = Path(..., alias="File_Type", description="Type of file to view"),
    Filename: str = Path(..., alias="Filename", description="Name of the file"),
    api_key: str = Depends(get_api_key)
):
    base_dir_map = {
        "input": INPUT_DIR,
        "output": OUTPUT_DIR,
        "error": ERROR_DIR,
        "ack": ACK_DIR,
        "ta1": OUTPUT_DIR,
        "staging": STAGING_DIR,
        "shared": SHARED_DIR,
        "archive": ARCHIVE_DIR
    }
    file_type = File_Type.value
    if file_type not in base_dir_map:
        raise HTTPException(status_code=400, detail="Invalid file type. Supported: input, output, error, ack, ta1, staging, shared, archive.")

    base_dir = base_dir_map[file_type]
    file_path = safe_file_path(base_dir, Filename)

    if not file_path or not os.path.exists(file_path) or os.path.isdir(file_path):
        raise HTTPException(status_code=404, detail="File not found or access denied.")

    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        return PlainTextResponse(content)
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")



@app.get("/engine/info")
async def get_engine_info():
    """Get information about the Redix engine installation."""
    return {
        "redix_executable_path": redix_exe_path,
        "redix_libs_path": REDIX_LIBS_PATH,
        "engine_status": "loaded" if redix_exe_path else "not loaded",
        "platform": platform.system(),
        "base_work_dir": BASE_WORK_DIR,
        "db_path": DB_PATH,
        "directories": {
            "input": INPUT_DIR,
            "output": OUTPUT_DIR,
            "error": ERROR_DIR,
            "ack": ACK_DIR,
            "rules": RULES_DIR,
            "staging": STAGING_DIR,
            "shared": SHARED_DIR,
            "archive": ARCHIVE_DIR,
            "batch_input": BATCH_INPUT_DIR
        }
    }


# Startup event to initialize DB async
@app.on_event("startup")
async def startup_event():
    await init_db()

# Shutdown event to close DB connection
@app.on_event("shutdown")
async def shutdown_event():
    global db_connection
    if db_connection:
        await db_connection.close()

# This block ensures the FastAPI application runs when the script is executed directly.
if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Redix Healthcare Data Conversion API...")
    logger.info(f"Configuration loaded successfully")
    logger.info(f"Platform: {platform.system()}")
    logger.info(f"Base work directory: {BASE_WORK_DIR}")
    logger.info(f"Database path: {DB_PATH}")
    logger.info(f"Redix executable: {redix_exe_path}")
    logger.info(f"Allow Rule File Upload: {ALLOW_RULE_FILE_UPLOAD}")
    if DEFAULT_STAGING_PROFILE_NAME:
        logger.info(f"Default Staging Profile: '{DEFAULT_STAGING_PROFILE_NAME}'")
    if STAGING_CONFIG_PROFILES:
        logger.info(f"Loaded Staging Profiles: {', '.join(STAGING_CONFIG_PROFILES.keys())}")
    else:
        logger.info("No Staging Profiles loaded from redix_cloud.conf.")
    logger.info(f"Batch Input Directory: {BATCH_INPUT_DIR}")

    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
# MediLink_Gmail.py
import sys, os, subprocess, time, webbrowser, requests, json, ssl, signal, re
from collections import deque
from datetime import datetime

# Set up Python path to find MediCafe when running directly
def setup_python_path():
    """Set up Python path to find MediCafe package"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(current_dir)
    
    # Add workspace root to Python path if not already present
    if workspace_root not in sys.path:
        sys.path.insert(0, workspace_root)
    
    return workspace_root

# Set up paths before importing MediCafe
WORKSPACE_ROOT = setup_python_path()

from MediCafe.core_utils import get_shared_config_loader, extract_medilink_config, check_internet_connection

# New helpers
from MediLink.gmail_oauth_utils import (
    get_authorization_url as oauth_get_authorization_url,
    exchange_code_for_token as oauth_exchange_code_for_token,
    refresh_access_token as oauth_refresh_access_token,
    is_valid_authorization_code as oauth_is_valid_authorization_code,
)
from MediLink.gmail_http_utils import (
    generate_self_signed_cert as http_generate_self_signed_cert,
    wrap_socket_for_server as http_wrap_socket_for_server,
    inspect_token as http_inspect_token,
    get_certificate_fingerprint as http_get_certificate_fingerprint,
    SSLRequestHandler,
)
try:
    from MediLink import certificate_authority
    CERTIFICATE_AUTHORITY_AVAILABLE = True
except ImportError:
    certificate_authority = None
    CERTIFICATE_AUTHORITY_AVAILABLE = False
try:
    from MediLink.firefox_cert_utils import diagnose_firefox_certificate_exceptions
    FIREFOX_CERT_DIAG_AVAILABLE = True
except ImportError:
    FIREFOX_CERT_DIAG_AVAILABLE = False
    def diagnose_firefox_certificate_exceptions(*args, **kwargs):
        return {'error': 'Firefox certificate diagnostics not available'}
from MediLink.gmail_html_utils import (
    build_cert_info_html as html_build_cert_info_html,
    build_root_status_html as html_build_root_status_html,
    build_diagnostics_html as html_build_diagnostics_html,
    build_troubleshoot_html as html_build_troubleshoot_html,
    build_simple_error_html as html_build_simple_error_html,
    build_fallback_status_html as html_build_fallback_status_html,
    build_fallback_cert_html as html_build_fallback_cert_html,
)

# Import connection diagnostics module
try:
    from MediLink.connection_diagnostics import (
        run_diagnostics as _run_diagnostics_base,
        get_firefox_xp_compatibility_notes,
        BROWSER_DIAGNOSTIC_HINTS,
        run_all_selftests as _run_all_selftests,
        detect_available_tls_versions,
        is_windows_xp as detect_is_windows_xp,
    )
    DIAGNOSTICS_AVAILABLE = True
except ImportError as diag_import_err:
    DIAGNOSTICS_AVAILABLE = False
    _run_diagnostics_base = None
    _run_all_selftests = None
    def get_firefox_xp_compatibility_notes():
        return {'notes': []}
    BROWSER_DIAGNOSTIC_HINTS = {}
    def detect_available_tls_versions():
        # Fallback: detect TLS versions without diagnostics module
        import ssl as _ssl
        _tls = []
        for _name, _attr in [('TLSv1', 'PROTOCOL_TLSv1'), ('TLSv1.1', 'PROTOCOL_TLSv1_1'), 
                             ('TLSv1.2', 'PROTOCOL_TLSv1_2'), ('TLSv1.3', 'PROTOCOL_TLSv1_3')]:
            if hasattr(_ssl, _attr):
                _tls.append(_name)
        return _tls
    def detect_is_windows_xp(os_name=None, os_version=None):
        # Fallback: detect XP without diagnostics module
        import platform as _platform
        _os = os_name if os_name is not None else _platform.system()
        _ver = os_version if os_version is not None else _platform.release()
        return _os == 'Windows' and _ver.startswith('5.')
from MediCafe.gmail_token_service import (
    get_gmail_access_token as shared_get_gmail_access_token,
    resolve_credentials_path as shared_resolve_credentials_path,
    resolve_token_path as shared_resolve_token_path,
    clear_gmail_token_cache as shared_clear_token_cache,
    save_gmail_token as shared_save_gmail_token,
)

# Get shared config loader
MediLink_ConfigLoader = get_shared_config_loader()
if MediLink_ConfigLoader:
    load_configuration = MediLink_ConfigLoader.load_configuration
    log = MediLink_ConfigLoader.log
else:
    # Fallback functions if config loader is not available
    def load_configuration():
        return {}, {}
    def log(message, level="INFO"):
        print("[{}] {}".format(level, message))

try:
    from MediCafe.error_reporter import (
        capture_unhandled_traceback as _capture_unhandled_traceback,
        submit_support_bundle_email as _submit_support_bundle_email,
    )
    sys.excepthook = _capture_unhandled_traceback  # Ensure unhandled exceptions hit MediCafe reporter
    log("MediCafe error reporter registered for Gmail flow exceptions.", level="DEBUG")
except Exception as error_reporter_exc:
    _submit_support_bundle_email = None
    # Keep server running even if error reporter is unavailable
    try:
        log("Unable to register MediCafe error reporter: {}".format(error_reporter_exc), level="DEBUG")
    except Exception:
        pass
from http.server import HTTPServer
from threading import Thread, Event
import platform
import ctypes

# Default configuration values
DEFAULT_SERVER_PORT = 8000
DEFAULT_CERT_DAYS = 365
LOSS_ALERT_SECONDS = 20  # TODO: allow configuration via MediLink_Config in a future update.
CONNECTION_WATCHDOG_INTERVAL = 5

def resolve_openssl_cnf(base_dir):
    """Find openssl.cnf file, searching local dir then fallback path. Returns best-effort path."""
    # Try relative path first
    openssl_cnf = 'openssl.cnf'
    if os.path.exists(openssl_cnf):
        log("Found openssl.cnf at: {}".format(os.path.abspath(openssl_cnf)), level="DEBUG")
        return openssl_cnf

    # Try base directory
    medilink_openssl = os.path.join(base_dir, 'openssl.cnf')
    if os.path.exists(medilink_openssl):
        log("Found openssl.cnf at: {}".format(medilink_openssl), level="DEBUG")
        return medilink_openssl

    # Try fallback path (one directory up)
    parent_dir = os.path.dirname(base_dir)
    alternative_path = os.path.join(parent_dir, 'MediBot', 'openssl.cnf')
    if os.path.exists(alternative_path):
        log("Found openssl.cnf at: {}".format(alternative_path), level="DEBUG")
        return alternative_path

    # Return relative path as fallback (may not exist)
    log("Could not find openssl.cnf - using fallback path", level="DEBUG")
    return openssl_cnf


# Lazy resolution cache for openssl.cnf - only resolved when actually needed
_openssl_cnf_cache = None

def get_openssl_cnf():
    """Lazy resolution of openssl.cnf - only resolved when actually needed (e.g., HTTPS server startup).
    
    This avoids running the resolution when scripts only import add_downloaded_email
    from this module, which was causing duplicate openssl.cnf checks in logs.
    """
    global _openssl_cnf_cache
    if _openssl_cnf_cache is None:
        medilink_dir = os.path.dirname(os.path.abspath(__file__))
        _openssl_cnf_cache = resolve_openssl_cnf(medilink_dir)
    return _openssl_cnf_cache


config, _ = load_configuration()
medi = extract_medilink_config(config)


def _cert_provider_defaults():
    return {
        'mode': 'self_signed',
        'profile': 'default',
        'root_subject': 'CN=MediLink Managed Root CA',
        'server_subject': 'CN=127.0.0.1',
        'san': ['127.0.0.1', 'localhost'],
        'root_valid_days': 3650,
        'server_valid_days': DEFAULT_CERT_DAYS
    }


def _str_or_default(value, default):
    if isinstance(value, str):
        text = value.strip()
        return text or default
    return default if value in (None, '') else value


def _int_default(value, default):
    try:
        return int(value)
    except Exception:
        return default


def refresh_certificate_provider_settings(source_config=None):
    global CERT_PROVIDER_SETTINGS, CERT_MODE, MANAGED_CA_PROFILE_NAME
    global MANAGED_CA_ROOT_SUBJECT, MANAGED_CA_SERVER_SUBJECT
    global MANAGED_CA_SAN_LIST, MANAGED_CA_ROOT_VALID_DAYS, MANAGED_CA_SERVER_VALID_DAYS
    cfg = source_config or config
    provider_settings = None
    if MediLink_ConfigLoader and hasattr(MediLink_ConfigLoader, 'get_certificate_provider_config'):
        try:
            provider_settings = MediLink_ConfigLoader.get_certificate_provider_config(cfg)
        except Exception:
            provider_settings = None
    if not provider_settings:
        provider_settings = _cert_provider_defaults()
    CERT_PROVIDER_SETTINGS = provider_settings
    CERT_MODE = _str_or_default(provider_settings.get('mode'), 'self_signed')
    MANAGED_CA_PROFILE_NAME = _str_or_default(provider_settings.get('profile'), 'default')
    MANAGED_CA_ROOT_SUBJECT = _str_or_default(provider_settings.get('root_subject'), '/CN=MediLink Managed Root CA')
    MANAGED_CA_SERVER_SUBJECT = _str_or_default(provider_settings.get('server_subject'), '/CN=127.0.0.1')
    if isinstance(provider_settings.get('san'), list):
        MANAGED_CA_SAN_LIST = [str(item) for item in provider_settings.get('san') if item]
        if not MANAGED_CA_SAN_LIST:
            MANAGED_CA_SAN_LIST = ['127.0.0.1', 'localhost']
    else:
        MANAGED_CA_SAN_LIST = ['127.0.0.1', 'localhost']
    MANAGED_CA_ROOT_VALID_DAYS = _int_default(provider_settings.get('root_valid_days'), 3650)
    MANAGED_CA_SERVER_VALID_DAYS = _int_default(provider_settings.get('server_valid_days'), DEFAULT_CERT_DAYS)
    global MANAGED_CA_ENABLED
    MANAGED_CA_ENABLED = bool(CERTIFICATE_AUTHORITY_AVAILABLE and CERT_MODE == 'managed_ca')


def rebuild_ca_profile():
    global CA_PROFILE, MANAGED_CA_ENABLED
    CA_PROFILE = None
    MANAGED_CA_ENABLED = bool(CERTIFICATE_AUTHORITY_AVAILABLE and CERT_MODE == 'managed_ca')
    if not (MANAGED_CA_ENABLED and certificate_authority):
        return
    try:
        ca_storage_root = certificate_authority.resolve_default_ca_dir(local_storage_path=local_storage_path)
        profile = certificate_authority.create_profile(
            profile_name=MANAGED_CA_PROFILE_NAME,
            storage_root=ca_storage_root,
            server_cert_path=ABS_CERT_FILE,
            server_key_path=ABS_KEY_FILE,
            openssl_config=get_openssl_cnf(),
            san_list=MANAGED_CA_SAN_LIST,
            root_subject=MANAGED_CA_ROOT_SUBJECT,
            server_subject=MANAGED_CA_SERVER_SUBJECT
        )
        profile['root_valid_days'] = MANAGED_CA_ROOT_VALID_DAYS
        profile['server_valid_days'] = MANAGED_CA_SERVER_VALID_DAYS
        CA_PROFILE = profile
    except Exception as profile_exc:
        MANAGED_CA_ENABLED = False
        CA_PROFILE = None
        try:
            log("Unable to initialize managed CA profile: {}".format(profile_exc), level="WARNING")
        except Exception:
            pass


refresh_certificate_provider_settings(config)
rebuild_ca_profile()


def _update_certificate_provider_mode(new_mode, extra_fields=None):
    if not MediLink_ConfigLoader or not hasattr(MediLink_ConfigLoader, 'update_certificate_provider_config'):
        return False, "Config mutation helper unavailable"
    payload = {'mode': new_mode}
    if isinstance(extra_fields, dict):
        payload.update(extra_fields)
    success, error = MediLink_ConfigLoader.update_certificate_provider_config(payload)
    if success:
        try:
            MediLink_ConfigLoader.clear_config_cache()
        except Exception:
            pass
        try:
            global config, medi
            config, _ = load_configuration()
            medi = extract_medilink_config(config)
            refresh_certificate_provider_settings(config)
            rebuild_ca_profile()
        except Exception:
            pass
    return success, error
TOKEN_PATH = shared_resolve_token_path(medi)
local_storage_path = medi.get('local_storage_path', '.')
downloaded_emails_file = os.path.join(local_storage_path, 'downloaded_emails.txt')

server_port = medi.get('gmail_server_port', DEFAULT_SERVER_PORT)
LOCAL_SERVER_BASE_URL = 'https://127.0.0.1:{}'.format(server_port)
cert_file = 'server.cert'
key_file = 'server.key'
# Note: openssl.cnf resolution is now lazy - see get_openssl_cnf() function

ABS_CERT_FILE = os.path.abspath(cert_file)
ABS_KEY_FILE = os.path.abspath(key_file)
CA_PROFILE = None
CA_STATUS_CACHE = {}
MANAGED_CA_ENABLED = False
CA_PROFILE = None


def is_managed_ca_active():
    return bool(MANAGED_CA_ENABLED and CA_PROFILE and certificate_authority)


def get_managed_ca_status(refresh=False):
    """Return cached CA status, refreshing via helper when necessary."""
    global CA_STATUS_CACHE
    if not is_managed_ca_active():
        return {}
    if refresh or not CA_STATUS_CACHE:
        try:
            CA_STATUS_CACHE = certificate_authority.describe_status(CA_PROFILE, log=log) or {}
        except Exception as status_err:
            try:
                log("Unable to describe managed CA status: {}".format(status_err), level="DEBUG")
            except Exception:
                pass
            CA_STATUS_CACHE = {}
    return CA_STATUS_CACHE


httpd = None  # Global variable for the HTTP server
shutdown_event = Event()  # Event to signal shutdown
server_crashed = False  # Flag to track if server thread crashed
LAST_SECURE_ACTIVITY_TS = time.time()
CERT_WARNING_EMITTED = False
SECURE_ACTIVITY_PATHS = {'/_diag', '/download', '/delete-files', '/_cert', '/status', '/ca/root.crt', '/ca/server-info.json', '/ca/enable'}

# Safe-to-close flag and lightweight server status tracking
SAFE_TO_CLOSE = False
SERVER_STATUS = {
    'phase': 'idle',  # idle|processing|downloading|cleanup_triggered|cleanup_confirmed|done|error
    'linksReceived': 0,
    'filesDownloaded': 0,
    'filesToDelete': 0,
    'filesDeleted': 0,
    'lastError': None,
}
RECENT_REQUESTS = deque(maxlen=25)
CONNECTION_LOSS_REPORTED = False
HAD_SECURE_ACTIVITY = False
WATCHDOG_THREAD = None

def set_safe_to_close(value):
    global SAFE_TO_CLOSE
    SAFE_TO_CLOSE = bool(value)

def set_phase(phase):
    try:
        SERVER_STATUS['phase'] = str(phase or '')
    except Exception:
        SERVER_STATUS['phase'] = 'error'

def set_counts(links_received=None, files_downloaded=None, files_to_delete=None, files_deleted=None):
    try:
        if links_received is not None:
            SERVER_STATUS['linksReceived'] = int(links_received)
        if files_downloaded is not None:
            SERVER_STATUS['filesDownloaded'] = int(files_downloaded)
        if files_to_delete is not None:
            SERVER_STATUS['filesToDelete'] = int(files_to_delete)
        if files_deleted is not None:
            SERVER_STATUS['filesDeleted'] = int(files_deleted)
    except Exception:
        pass

def set_error(msg):
    try:
        SERVER_STATUS['lastError'] = str(msg or '')
    except Exception:
        SERVER_STATUS['lastError'] = 'Unknown error'

def get_safe_status():
    try:
        elapsed = max(0, int(time.time() - LAST_SECURE_ACTIVITY_TS))
        return {
            'safeToClose': bool(SAFE_TO_CLOSE),
            'phase': SERVER_STATUS.get('phase', 'idle'),
            'counts': {
                'linksReceived': SERVER_STATUS.get('linksReceived', 0),
                'filesDownloaded': SERVER_STATUS.get('filesDownloaded', 0),
                'filesToDelete': SERVER_STATUS.get('filesToDelete', 0),
                'filesDeleted': SERVER_STATUS.get('filesDeleted', 0),
            },
            'lastError': SERVER_STATUS.get('lastError'),
            'connectivity': {
                'secondsSinceSecureActivity': elapsed,
                'certificateWarningActive': bool(CERT_WARNING_EMITTED)
            }
        }
    except Exception:
        return {'safeToClose': False, 'phase': 'error'}


def record_request_event(method, path, status, note=None, client=None):
    try:
        RECENT_REQUESTS.appendleft({
            'time': datetime.utcnow().isoformat() + 'Z',
            'method': method,
            'path': path,
            'status': status,
            'note': note,
            'client': client
        })
        if path in SECURE_ACTIVITY_PATHS:
            mark_secure_activity()
    except Exception:
        pass


def _get_client_ip(handler):
    try:
        return handler.client_address[0]
    except Exception:
        return None


def mark_secure_activity():
    global LAST_SECURE_ACTIVITY_TS, CERT_WARNING_EMITTED, HAD_SECURE_ACTIVITY
    LAST_SECURE_ACTIVITY_TS = time.time()
    CERT_WARNING_EMITTED = False
    HAD_SECURE_ACTIVITY = True


def maybe_warn_secure_idle():
    global CERT_WARNING_EMITTED
    elapsed = time.time() - LAST_SECURE_ACTIVITY_TS
    if elapsed > LOSS_ALERT_SECONDS:
        _maybe_report_connection_loss(elapsed)
    if elapsed > 120 and not CERT_WARNING_EMITTED:
        log("No secure local HTTPS activity detected for {:.0f} seconds. Browser may still need to trust https://127.0.0.1:8000.".format(elapsed), level="WARNING")
        CERT_WARNING_EMITTED = True
    return elapsed


def _maybe_report_connection_loss(elapsed):
    global CONNECTION_LOSS_REPORTED
    if CONNECTION_LOSS_REPORTED or not HAD_SECURE_ACTIVITY or SAFE_TO_CLOSE:
        return
    CONNECTION_LOSS_REPORTED = True
    log("No HTTPS activity for {:.0f} seconds. Triggering automated connection loss report.".format(elapsed), level="WARNING")
    if _submit_support_bundle_email is None:
        log("Support bundle reporter unavailable; unable to auto-send connection loss bundle.", level="WARNING")
        return
    try:
        sent = _submit_support_bundle_email(zip_path=None, include_traceback=False)
        if sent:
            log("Connection loss bundle submitted via MediCafe error reporter.", level="INFO")
        else:
            log("Connection loss bundle creation/send failed; bundle queued for later.", level="WARNING")
    except Exception as report_exc:
        log("Failed to submit connection loss bundle: {}".format(report_exc), level="WARNING")


def _connection_watchdog_loop():
    while not shutdown_event.is_set():
        try:
            maybe_warn_secure_idle()
        except Exception as watchdog_err:
            try:
                log("Connection watchdog loop error: {}".format(watchdog_err), level="DEBUG")
            except Exception:
                pass
        time.sleep(CONNECTION_WATCHDOG_INTERVAL)


def ensure_connection_watchdog_running():
    global WATCHDOG_THREAD
    if WATCHDOG_THREAD and WATCHDOG_THREAD.is_alive():
        return
    WATCHDOG_THREAD = Thread(target=_connection_watchdog_loop, name="connection-watchdog", daemon=True)
    WATCHDOG_THREAD.start()


def get_certificate_summary(cert_path):
    summary = {
        'present': False
    }
    try:
        if os.path.exists(cert_path):
            summary['present'] = True
            ssl_impl = getattr(ssl, '_ssl', None)
            can_decode = ssl_impl is not None and hasattr(ssl_impl, '_test_decode_cert')
            if can_decode:
                cert_dict = ssl._ssl._test_decode_cert(cert_path)
                not_before = cert_dict.get('notBefore')
                not_after = cert_dict.get('notAfter')
                summary.update({
                    'subject': cert_dict.get('subject'),
                    'issuer': cert_dict.get('issuer'),
                    'notBefore': not_before,
                    'notAfter': not_after,
                    'serialNumber': cert_dict.get('serialNumber')
                })
            else:
                summary['warning'] = 'Certificate decoding not supported on this Python build.'
    except Exception as cert_err:
        summary['error'] = str(cert_err)
    return summary


def build_diagnostics_payload():
    try:
        recent = list(RECENT_REQUESTS)
    except Exception:
        recent = []
    
    # Get SSL/TLS information (uses shared helper to avoid duplication)
    ssl_info = {
        'version': getattr(ssl, 'OPENSSL_VERSION', 'Unknown'),
        'versionInfo': getattr(ssl, 'OPENSSL_VERSION_INFO', None),
        'availableTlsVersions': detect_available_tls_versions(),
    }
    
    # Check if running on Windows XP (uses shared helper)
    xp_detected = detect_is_windows_xp(os_name, os_version)
    
    # Build payload
    payload = {
        'status': 'ok',
        'time': datetime.utcnow().isoformat() + 'Z',
        'serverPort': server_port,
        'safeStatus': get_safe_status(),
        'certificate': get_certificate_summary(cert_file),
        'certificateAuthority': {
            'mode': CERT_MODE,
            'managed': is_managed_ca_active(),
            'status': get_managed_ca_status()
        },
        'recentRequests': recent,
        'connectivity': {
            'secondsSinceSecureActivity': max(0, int(time.time() - LAST_SECURE_ACTIVITY_TS)),
            'certificateWarningActive': bool(CERT_WARNING_EMITTED)
        },
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Private-Network': 'true'
        },
        'platform': {
            'os': os_name,
            'version': os_version,
            'isWindowsXP': xp_detected,
            'pythonVersion': sys.version_info[:3],
        },
        'ssl': ssl_info,
        'diagnosticsAvailable': DIAGNOSTICS_AVAILABLE,
        'endpoints': {
            'diag_html': '/_diag?html=1',
            'diag_full': '/_diag?full=1',
            'cert': '/_cert',
            'troubleshoot': '/_troubleshoot',
            'selftest': '/_selftest',
            'selftest_html': '/_selftest?html=1',
            'health': '/_health',
            'status': '/status',
        }
    }
    
    if payload['certificateAuthority']['managed']:
        payload['managedCA'] = {
            'nextSteps': [
                'If Firefox still blocks requests, download /ca/root.crt, import under Authorities, and restart Firefox.',
                'After importing, restart the MediLink helper if prompted so a managed server certificate is issued.'
            ],
            'enableEndpoint': '/ca/enable',
            'statusEndpoint': '/ca/server-info.json'
        }
    else:
        payload['managedCA'] = {
            'offerEscalation': True,
            'enableEndpoint': '/ca/enable',
            'statusEndpoint': '/ca/server-info.json'
        }

    if xp_detected:
        payload['xpNotes'] = [
            'Running on Windows XP - some features may be limited.',
            'Firefox 52 ESR is the last version supporting Windows XP.',
            'TLS 1.2 support requires Firefox 24+ or IE 11.',
            'Certificate exceptions may need to be re-added after browser restart.',
        ]
    
    return payload


# Define the scopes for the Gmail API and other required APIs
SCOPES = ' '.join([
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/script.external_request",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/script.scriptapp",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/userinfo.email"
])

# Determine the operating system and version
os_name = platform.system()
os_version = platform.release()

# Set the credentials path based on the OS and version
CREDENTIALS_PATH = shared_resolve_credentials_path(medi, os_name=os_name, os_version=os_version)

# Resolve relative paths properly for both dev (repo_root) and prod (absolute) environments
# In dev, relative paths assume repo_root as working directory, but script may run from MediLink directory
if not os.path.isabs(CREDENTIALS_PATH):
    # If path doesn't exist at current location, try resolving relative to project root
    if not os.path.exists(CREDENTIALS_PATH):
        project_root_path = os.path.join(WORKSPACE_ROOT, CREDENTIALS_PATH)
        if os.path.exists(project_root_path):
            CREDENTIALS_PATH = os.path.normpath(project_root_path)
        else:
            # Fallback: try relative to current working directory (handles different working directories)
            cwd_path = os.path.join(os.getcwd(), CREDENTIALS_PATH)
            if os.path.exists(cwd_path):
                CREDENTIALS_PATH = os.path.normpath(cwd_path)

# Log the selected path for verification
log("Using CREDENTIALS_PATH: {}".format(CREDENTIALS_PATH), level="DEBUG")

REDIRECT_URI = 'https://127.0.0.1:{}'.format(server_port)


def run_connection_diagnostics(cert_file='server.cert', key_file='server.key', 
                               server_port=8000, auto_fix=False, openssl_cnf='openssl.cnf'):
    """
    Run connection diagnostics using existing module functions.
    Wrapper that passes existing functions to avoid duplication.
    """
    if not DIAGNOSTICS_AVAILABLE or _run_diagnostics_base is None:
        return {'summary': {'can_start_server': True}, 'environment': {}, 'issues': [], 'warnings': []}
    
    # Pass existing functions to the diagnostics module to avoid duplication
    # Use lazy resolution if default parameter value is used, otherwise use provided value
    resolved_openssl_cnf = get_openssl_cnf() if openssl_cnf == 'openssl.cnf' else openssl_cnf
    return _run_diagnostics_base(
        cert_file=cert_file,
        key_file=key_file,
        server_port=server_port,
        os_name=os_name,  # Use existing module-level variable
        os_version=os_version,  # Use existing module-level variable
        cert_summary_fn=get_certificate_summary,  # Use existing function
        auto_fix=auto_fix,
        generate_cert_fn=http_generate_self_signed_cert if (auto_fix and CERT_MODE != 'managed_ca') else None,
        openssl_cnf=resolved_openssl_cnf
    )


def get_authorization_url():
    return oauth_get_authorization_url(CREDENTIALS_PATH, REDIRECT_URI, SCOPES, log)

def exchange_code_for_token(auth_code, retries=3):
    return oauth_exchange_code_for_token(auth_code, CREDENTIALS_PATH, REDIRECT_URI, log, retries=retries)

def _mask_token_value(value):
    """Mask a token value for safe logging. Returns first 4 and last 4 chars, or '***' if too short."""
    try:
        s = str(value or '')
        if len(s) <= 8:
            return '***'
        return s[:4] + '...' + s[-4:]
    except Exception:
        return '***'


def _mask_sensitive_dict(data):
    """Create a copy of a dict with sensitive fields masked for logging."""
    if not isinstance(data, dict):
        return data
    try:
        masked = data.copy()
        # Mask token fields
        for key in ['access_token', 'refresh_token', 'id_token']:
            if key in masked and masked[key]:
                masked[key] = _mask_token_value(masked[key])
        # Mask Authorization header if present
        if 'Authorization' in masked:
            auth_val = str(masked['Authorization'])
            if 'Bearer ' in auth_val:
                # Extract token from "Bearer <token>"
                parts = auth_val.split('Bearer ', 1)
                if len(parts) > 1:
                    token = parts[1].strip()
                    masked['Authorization'] = 'Bearer ' + _mask_token_value(token)
        return masked
    except Exception:
        return data


def get_access_token():
    return shared_get_gmail_access_token(log=log, medi_config=medi, os_name=os_name, os_version=os_version)

def refresh_access_token(refresh_token):
    return oauth_refresh_access_token(refresh_token, CREDENTIALS_PATH, log)

def bring_window_to_foreground():
    """Brings the current window to the foreground on Windows."""
    try:
        if platform.system() == 'Windows':
            pid = os.getpid()
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            current_pid = ctypes.c_ulong()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(current_pid))
            if current_pid.value != pid:
                ctypes.windll.user32.SetForegroundWindow(hwnd)
                if ctypes.windll.user32.GetForegroundWindow() != hwnd:
                    ctypes.windll.user32.ShowWindow(hwnd, 9)
                    ctypes.windll.user32.SetForegroundWindow(hwnd)
    except Exception as e:
        log("Error bringing window to foreground: {}".format(e))

class RequestHandler(SSLRequestHandler):
    def _set_headers(self):
        from MediLink.gmail_http_utils import set_standard_headers
        set_standard_headers(self)

    def _build_troubleshoot_html(self):
        """Build comprehensive troubleshooting HTML page.
        
        Delegates to gmail_html_utils.build_troubleshoot_html for HTML generation.
        """
        # Run diagnostics to gather environment/issue info
        diag_report = None
        if DIAGNOSTICS_AVAILABLE:
            try:
                diag_report = run_connection_diagnostics(
                    cert_file=cert_file,
                    key_file=key_file,
                    server_port=server_port,
                    auto_fix=True,  # Enable auto-fix on troubleshoot page
                    openssl_cnf=get_openssl_cnf()
                )
                # If certificate was auto-fixed, log it
                if diag_report.get('fixes_successful'):
                    log("Auto-fixed certificate issues from troubleshoot page: {}".format(diag_report['fixes_successful']), level="INFO")
            except Exception as e:
                log("Error running diagnostics for troubleshoot page: {}".format(e), level="WARNING")
        
        # Get Firefox notes and browser hints
        firefox_notes = get_firefox_xp_compatibility_notes() if DIAGNOSTICS_AVAILABLE else {'notes': []}
        browser_hints = BROWSER_DIAGNOSTIC_HINTS if DIAGNOSTICS_AVAILABLE else {}
        
        # Get Firefox certificate diagnosis if available and certificate issues exist
        firefox_diagnosis = None
        if FIREFOX_CERT_DIAG_AVAILABLE and diag_report and diag_report.get('issues'):
            try:
                firefox_path = medi.get('firefox_path') or medi.get('browser_path')
                firefox_diagnosis = diagnose_firefox_certificate_exceptions(
                    cert_file=cert_file,
                    server_port=server_port,
                    firefox_path=firefox_path,
                    log=log
                )
            except Exception as fx_err:
                log("Firefox diagnosis unavailable for troubleshoot page: {}".format(fx_err), level="DEBUG")
        
        # Get certificate info for contextual guidance
        cert_info = None
        try:
            cert_info = get_certificate_summary(cert_file)
        except Exception:
            pass
        
        # Delegate HTML generation to utility module
        provider_payload = None
        try:
            provider_payload = {
                'mode': CERT_MODE,
                'status': get_managed_ca_status(),
                'san': MANAGED_CA_SAN_LIST,
                'root_subject': MANAGED_CA_ROOT_SUBJECT,
                'server_subject': MANAGED_CA_SERVER_SUBJECT
            }
        except Exception:
            provider_payload = None
        return html_build_troubleshoot_html(
            diag_report=diag_report,
            firefox_notes=firefox_notes,
            browser_hints=browser_hints,
            server_port=server_port,
            certificate_provider=provider_payload,
            firefox_diagnosis=firefox_diagnosis,
            cert_info=cert_info
        )

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_headers()
        self.end_headers()
        record_request_event('OPTIONS', self.path, 200, note='preflight', client=_get_client_ip(self))
        try:
            origin = self.headers.get('Origin')
        except Exception:
            origin = None
        try:
            print("[CORS] Preflight {0} from {1}".format(self.path, origin))
        except Exception:
            pass

    def do_POST(self):
        """Handle POST requests with comprehensive exception handling to prevent server crashes."""
        from MediLink.gmail_http_utils import (
            parse_content_length, read_post_data, parse_json_data,
            send_error_response, safe_write_response, log_request_error
        )
        try:
            if self.path == '/download':
                set_phase('processing')
                try:
                    content_length = parse_content_length(self.headers, log_fn=log)
                except (KeyError, ValueError) as e:
                    send_error_response(self, 400, "Missing or invalid Content-Length header", log_fn=log, error_details=str(e))
                    return
                post_data = read_post_data(self, content_length, log_fn=log)
                if post_data is None:
                    return  # Client disconnected
                try:
                    data = parse_json_data(post_data, log_fn=log)
                except (ValueError, UnicodeDecodeError) as e:
                    send_error_response(self, 400, "Invalid request format", log_fn=log, error_details=str(e))
                    return
                links = data.get('links', [])
                log("Received links: {}".format(links), level="DEBUG")
                try:
                    print("[Handshake] Received {0} link(s) from webapp".format(len(links)))
                except Exception:
                    pass
                try:
                    set_counts(links_received=len(links))
                except Exception:
                    pass
                file_ids = [link.get('fileId', None) for link in links if link.get('fileId')]
                log("File IDs received from client: {}".format(file_ids), level="DEBUG")
                set_phase('downloading')
                try:
                    download_docx_files(links)
                except Exception as e:
                    set_phase('error')
                    set_error(str(e))
                # Only delete files that actually downloaded successfully
                downloaded_names = load_downloaded_emails()
                successful_ids = []
                try:
                    name_to_id = { (link.get('filename') or ''): link.get('fileId') for link in links if link.get('fileId') }
                    for name in downloaded_names:
                        fid = name_to_id.get(name)
                        if fid:
                            successful_ids.append(fid)
                except Exception as e:
                    log("Error computing successful file IDs for cleanup: {}".format(e))
                    successful_ids = file_ids  # Fallback: attempt all provided IDs
                try:
                    set_counts(files_to_delete=len(successful_ids))
                except Exception:
                    pass
                # Trigger cleanup in Apps Script with auth
                try:
                    cleanup_ok = False
                    if successful_ids:
                        ok = send_delete_request_to_gas(successful_ids)
                        if ok:
                            set_phase('cleanup_confirmed')
                            try:
                                set_counts(files_deleted=len(successful_ids))
                            except Exception:
                                pass
                            cleanup_ok = True
                        else:
                            set_phase('cleanup_triggered')
                            set_error('Cleanup request not confirmed')
                    else:
                        log("No successful file IDs to delete after download.")
                        set_phase('done')
                        cleanup_ok = True  # nothing to delete -> safe
                except Exception as e:
                    log("Cleanup trigger failed: {}".format(e))
                    set_phase('error')
                    set_error(str(e))
                    cleanup_ok = False
                self.send_response(200)
                self._set_headers()
                self.end_headers()
                try:
                    set_safe_to_close(bool(cleanup_ok))
                except Exception:
                    pass
                response = json.dumps({"status": "success", "message": "All files downloaded", "fileIds": successful_ids, "safeToClose": bool(cleanup_ok)})
                safe_write_response(self, response)
                try:
                    print("[Handshake] Completed. Returning success for {0} fileId(s)".format(len(successful_ids)))
                except Exception:
                    pass
                shutdown_event.set()
                bring_window_to_foreground()
                record_request_event('POST', '/download', 200, note='download', client=_get_client_ip(self))
                return
            elif self.path == '/shutdown':
                log("Shutdown request received.")
                self.send_response(200)
                self._set_headers()
                self.end_headers()
                response = json.dumps({"status": "success", "message": "Server is shutting down."})
                safe_write_response(self, response)
                shutdown_event.set()
                record_request_event('POST', '/shutdown', 200, note='shutdown', client=_get_client_ip(self))
                return
            elif self.path == '/delete-files':
                try:
                    content_length = parse_content_length(self.headers, log_fn=log)
                except (KeyError, ValueError) as e:
                    send_error_response(self, 400, "Missing or invalid Content-Length header", log_fn=log, error_details=str(e))
                    return
                post_data = read_post_data(self, content_length, log_fn=log)
                if post_data is None:
                    return  # Client disconnected
                try:
                    data = parse_json_data(post_data, log_fn=log)
                except (ValueError, UnicodeDecodeError) as e:
                    send_error_response(self, 400, "Invalid request format", log_fn=log, error_details=str(e))
                    return
                file_ids = data.get('fileIds', [])
                log("File IDs to delete received from client: {}".format(file_ids))
                if not isinstance(file_ids, list):
                    send_error_response(self, 400, "Invalid fileIds parameter.", log_fn=log)
                    return
                self.send_response(200)
                self._set_headers()
                self.end_headers()
                response = json.dumps({"status": "success", "message": "Files deleted successfully."})
                safe_write_response(self, response)
                record_request_event('POST', '/delete-files', 200, note='cleanup', client=_get_client_ip(self))
                return
            elif self.path == '/ca/enable':
                try:
                    content_length = parse_content_length(self.headers, log_fn=log)
                except (KeyError, ValueError) as e:
                    send_error_response(self, 400, "Missing or invalid Content-Length header", log_fn=log, error_details=str(e))
                    return
                post_data = read_post_data(self, content_length, log_fn=log)
                if post_data is None:
                    return
                try:
                    data = parse_json_data(post_data, log_fn=log)
                except (ValueError, UnicodeDecodeError) as e:
                    send_error_response(self, 400, "Invalid request format", log_fn=log, error_details=str(e))
                    return
                desired_mode = _str_or_default(data.get('mode'), 'managed_ca').lower()
                if desired_mode not in ('managed_ca', 'self_signed'):
                    desired_mode = 'managed_ca'
                extra_fields = {}
                if desired_mode == 'managed_ca':
                    extra_fields = {
                        'profile': MANAGED_CA_PROFILE_NAME,
                        'root_subject': MANAGED_CA_ROOT_SUBJECT,
                        'server_subject': MANAGED_CA_SERVER_SUBJECT,
                        'san': MANAGED_CA_SAN_LIST,
                        'root_valid_days': MANAGED_CA_ROOT_VALID_DAYS,
                        'server_valid_days': MANAGED_CA_SERVER_VALID_DAYS
                    }
                success, error = _update_certificate_provider_mode(desired_mode, extra_fields)
                response = {
                    'success': bool(success),
                    'mode': CERT_MODE,
                    'managed': is_managed_ca_active()
                }
                if error:
                    response['error'] = error
                status_code = 200 if success else 500
                self.send_response(status_code)
                self._set_headers()
                self.end_headers()
                safe_write_response(self, json.dumps(response))
                record_request_event('POST', '/ca/enable', status_code, note='ca-enable', client=_get_client_ip(self))
                return
            else:
                self.send_response(404)
                self._set_headers()
                self.end_headers()
        except KeyError as e:
            send_error_response(self, 400, "Missing required header: {}".format(str(e)), log_fn=log, error_details=str(e))
        except (ValueError, TypeError) as e:
            # Note: json.JSONDecodeError doesn't exist in Python 3.4.4; json.loads raises ValueError
            send_error_response(self, 400, "Invalid request format: {}".format(str(e)), log_fn=log, error_details=str(e))
        except OSError as e:
            from MediLink.gmail_http_utils import _is_expected_disconnect
            if _is_expected_disconnect(e):
                log("Client disconnected during POST request handling: {}".format(e), level="DEBUG")
                self.close_connection = True
            else:
                log("Connection error in POST request: {} - This usually indicates a network error, client disconnect, or socket issue on Windows XP".format(e), level="ERROR")
                send_error_response(self, 500, "Connection error", log_fn=log, error_details=str(e))
        except Exception as e:
            log_request_error(e, self.path, "POST", log, headers=self.headers)
            send_error_response(self, 500, "Internal server error", log_fn=log, error_details=str(e))

    def do_GET(self):
        """Handle GET requests with comprehensive exception handling to prevent server crashes."""
        from MediLink.gmail_http_utils import (
            _is_expected_disconnect,
            send_error_response, log_request_error
        )
        try:
            log("Full request path: {}".format(self.path), level="DEBUG")
            if self.path == '/_health':
                try:
                    print("[Health] Probe OK")
                except Exception:
                    pass
                self.send_response(200)
                self._set_headers()
                self.end_headers()
                try:
                    self.wfile.write(json.dumps({"status": "ok"}).encode('ascii'))
                except Exception:
                    try:
                        self.wfile.write(b'{"status":"ok"}')
                    except OSError as e:
                        if _is_expected_disconnect(e):
                            self.close_connection = True
                        else:
                            raise
                record_request_event('GET', '/_health', 200, note='health-probe', client=_get_client_ip(self))
                return
            elif self.path.startswith('/_selftest'):
                # Run self-tests to verify server connectivity and SSL configuration
                # This endpoint helps diagnose Firefox/XP connectivity issues
                self.send_response(200)
                
                # Check if HTML format is requested
                want_html = 'html=1' in self.path or 'format=html' in self.path
                
                if DIAGNOSTICS_AVAILABLE and _run_all_selftests:
                    try:
                        # Run self-tests (skip network tests since we ARE the server)
                        selftest_results = _run_all_selftests(
                            port=server_port,
                            cert_file=cert_file,
                            include_network=False  # Can't test ourselves while handling request
                        )
                        # Add note about network tests
                        selftest_results['note'] = 'Network tests skipped (cannot self-test while handling request). Run from external script for full test.'
                    except Exception as st_err:
                        log("Error running self-tests: {}".format(st_err), level="ERROR")
                        selftest_results = {
                            'error': str(st_err),
                            'tests': {},
                            'summary': {'total': 0, 'passed': 0, 'failed': 0, 'all_passed': False}
                        }
                else:
                    selftest_results = {
                        'error': 'Diagnostics module not available',
                        'tests': {},
                        'summary': {'total': 0, 'passed': 0, 'failed': 0, 'all_passed': False}
                    }
                
                if want_html:
                    # Build simple HTML response
                    html_parts = ['<!DOCTYPE html><html><head><meta charset="utf-8"><title>MediLink Self-Test</title>',
                                  '<style>body{font-family:Arial,sans-serif;padding:20px;background:#f5f3e8;}',
                                  '.container{max-width:800px;margin:0 auto;background:white;padding:24px;border:1px solid #ccc;}',
                                  'h1{color:#3B2323;}.pass{color:#1f5132;}.fail{color:#dc2626;}',
                                  'pre{background:#f0f0f0;padding:12px;overflow:auto;}</style></head><body>',
                                  '<div class="container"><h1>MediLink Self-Test Results</h1>']
                    
                    summary = selftest_results.get('summary', {})
                    if summary.get('all_passed'):
                        html_parts.append('<p class="pass"><strong>All tests passed</strong></p>')
                    else:
                        html_parts.append('<p class="fail"><strong>{} of {} tests failed</strong></p>'.format(
                            summary.get('failed', 0), summary.get('total', 0)))
                    
                    if selftest_results.get('note'):
                        html_parts.append('<p><em>{}</em></p>'.format(selftest_results['note']))
                    
                    html_parts.append('<h2>Test Results</h2><pre>{}</pre>'.format(
                        json.dumps(selftest_results, indent=2, default=str)))
                    
                    html_parts.append('<p><a href="/_diag?html=1">Full Diagnostics</a> | ')
                    html_parts.append('<a href="/_troubleshoot">Troubleshooting Guide</a> | ')
                    html_parts.append('<a href="/">Server Status</a></p>')
                    html_parts.append('</div></body></html>')
                    
                    response_body = ''.join(html_parts)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                else:
                    response_body = json.dumps(selftest_results, indent=2, default=str)
                    self.send_header('Content-type', 'application/json')
                
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.send_header('Access-Control-Allow-Private-Network', 'true')
                self.end_headers()
                
                try:
                    self.wfile.write(response_body.encode('utf-8'))
                except Exception as write_err:
                    log("Failed to write selftest response: {}".format(write_err))
                
                record_request_event('GET', '/_selftest', 200, note='selftest', client=_get_client_ip(self))
                return
            elif self.path == '/status':
                maybe_warn_secure_idle()
                self.send_response(200)
                self._set_headers()
                self.end_headers()
                try:
                    payload = json.dumps(get_safe_status())
                except Exception:
                    payload = '{}'
                try:
                    self.wfile.write(payload.encode('ascii'))
                except Exception:
                    try:
                        self.wfile.write(payload.encode('utf-8'))
                    except Exception:
                        try:
                            self.wfile.write(payload.encode('utf-8', errors='ignore'))
                        except OSError as e:
                            if _is_expected_disconnect(e):
                                self.close_connection = True
                            else:
                                raise
                record_request_event('GET', '/status', 200, note='status', client=_get_client_ip(self))
                return
            elif self.path.startswith('/_diag'):
                # Check if HTML format is requested (browser access)
                want_html = 'html=1' in self.path or 'format=html' in self.path
                include_full = 'full=1' in self.path or 'refresh=1' in self.path
                
                # Build basic diagnostics payload
                diag_payload = build_diagnostics_payload()
                
                # Run comprehensive diagnostics if available and requested
                if DIAGNOSTICS_AVAILABLE and include_full:
                    try:
                        # Enable auto_fix for runtime diagnostics
                        # User will be notified if server restart is needed
                        full_diag = run_connection_diagnostics(
                            cert_file=cert_file,
                            key_file=key_file,
                            server_port=server_port,
                            auto_fix=True,  # Enable auto-fix during runtime
                            openssl_cnf=get_openssl_cnf()
                        )
                        diag_payload['fullDiagnostics'] = full_diag
                        
                        # If certificate was auto-fixed, add prominent notification
                        if full_diag.get('user_action_required') and full_diag['user_action_required'].get('requires_restart'):
                            diag_payload['certificateAutoFixed'] = True
                            diag_payload['restartRequired'] = True
                        
                        diag_payload['firefoxNotes'] = get_firefox_xp_compatibility_notes()
                        diag_payload['browserHints'] = BROWSER_DIAGNOSTIC_HINTS
                    except Exception as full_diag_err:
                        log("Error running full diagnostics: {}".format(full_diag_err), level="WARNING")
                        diag_payload['fullDiagnosticsError'] = str(full_diag_err)
                
                self.send_response(200)
                
                if want_html and DIAGNOSTICS_AVAILABLE:
                    # Return HTML diagnostics page
                    try:
                        if 'fullDiagnostics' not in diag_payload:
                            # Enable auto_fix for HTML diagnostics view
                            full_diag = run_connection_diagnostics(
                                cert_file=cert_file,
                                key_file=key_file,
                                server_port=server_port,
                                auto_fix=True,  # Enable auto-fix during runtime
                                openssl_cnf=get_openssl_cnf()
                            )
                            # Check if certificate was auto-fixed
                            if full_diag.get('user_action_required') and full_diag['user_action_required'].get('requires_restart'):
                                diag_payload['certificateAutoFixed'] = True
                                diag_payload['restartRequired'] = True
                        else:
                            full_diag = diag_payload['fullDiagnostics']
                        # Pass auto-fix flags to HTML builder
                        diag_html = html_build_diagnostics_html(full_diag, server_port, certificate_auto_fixed=diag_payload.get('certificateAutoFixed', False), restart_required=diag_payload.get('restartRequired', False))
                    except Exception as html_err:
                        log("Error building diagnostics HTML: {}".format(html_err), level="WARNING")
                        diag_html = "<html><body><h1>Diagnostics</h1><pre>{}</pre></body></html>".format(
                            json.dumps(diag_payload, indent=2)
                        )
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                    self.send_header('Access-Control-Allow-Private-Network', 'true')
                    self.end_headers()
                    try:
                        self.wfile.write(diag_html.encode('utf-8'))
                    except Exception as write_err:
                        log("Failed to write diagnostics HTML: {}".format(write_err))
                else:
                    # Return JSON diagnostics
                    self._set_headers()
                    self.end_headers()
                    try:
                        self.wfile.write(json.dumps(diag_payload).encode('utf-8'))
                    except Exception as write_err:
                        log("Failed to write diagnostics payload: {}".format(write_err))
                record_request_event('GET', '/_diag', 200, note='diagnostics', client=_get_client_ip(self))
                return
            elif self.path.startswith('/_troubleshoot'):
                # Comprehensive troubleshooting page
                try:
                    troubleshoot_html = self._build_troubleshoot_html()
                except Exception as ts_err:
                    log("Error building troubleshoot page: {}".format(ts_err), level="ERROR")
                    troubleshoot_html = html_build_simple_error_html("Troubleshooting Error", str(ts_err), server_port)
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.send_header('Access-Control-Allow-Private-Network', 'true')
                self.end_headers()
                try:
                    self.wfile.write(troubleshoot_html.encode('utf-8'))
                except Exception as write_err:
                    log("Failed to write troubleshoot page: {}".format(write_err))
                record_request_event('GET', '/_troubleshoot', 200, note='troubleshoot', client=_get_client_ip(self))
                return
            elif self.path == '/_cert_download' or self.path.startswith('/_cert_download'):
                # Serve certificate file for download (check before /_cert to avoid path matching conflict)
                try:
                    if os.path.exists(cert_file):
                        self.send_response(200)
                        self.send_header('Content-type', 'application/x-x509-ca-cert')
                        self.send_header('Content-Disposition', 'attachment; filename="medilink-local.crt"')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        with open(cert_file, 'rb') as f:
                            self.wfile.write(f.read())
                        record_request_event('GET', '/_cert_download', 200, note='cert-download', client=_get_client_ip(self))
                    else:
                        self.send_response(404)
                        self._set_headers()
                        self.end_headers()
                        self.wfile.write(b'Certificate file not found')
                        record_request_event('GET', '/_cert_download', 404, note='cert-not-found', client=_get_client_ip(self))
                except Exception as e:
                    log("Error serving certificate download: {}".format(e), level="ERROR")
                    self.send_response(500)
                    self._set_headers()
                    self.end_headers()
                    try:
                        self.wfile.write(b'Error serving certificate file')
                    except Exception:
                        pass
                return
            elif self.path == '/_cert_fingerprint':
                # Return certificate fingerprint as JSON (for diagnostics) - check before /_cert to avoid path matching conflict
                try:
                    fingerprint = http_get_certificate_fingerprint(cert_file, log=log)
                    cert_info = get_certificate_summary(cert_file)
                    response_data = {
                        'fingerprint': fingerprint,
                        'certificate': cert_info,
                        'download_url': '/_cert_download'
                    }
                    self.send_response(200)
                    self._set_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response_data).encode('utf-8'))
                    record_request_event('GET', '/_cert_fingerprint', 200, note='cert-fingerprint', client=_get_client_ip(self))
                except Exception as e:
                    log("Error serving certificate fingerprint: {}".format(e), level="ERROR")
                    self.send_response(500)
                    self._set_headers()
                    self.end_headers()
                    try:
                        self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                    except Exception:
                        pass
                return
            elif self.path == '/_cert_diagnose_firefox':
                # Diagnose Firefox certificate exceptions - check before /_cert to avoid path matching conflict
                try:
                    if not FIREFOX_CERT_DIAG_AVAILABLE:
                        response_data = {'error': 'Firefox certificate diagnostics not available'}
                    else:
                        # Try to get Firefox path from config
                        firefox_path = medi.get('firefox_path') or medi.get('browser_path')
                        diagnosis = diagnose_firefox_certificate_exceptions(
                            cert_file=cert_file,
                            server_port=server_port,
                            firefox_path=firefox_path,
                            log=log
                        )
                        response_data = diagnosis
                    
                    self.send_response(200)
                    self._set_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response_data).encode('utf-8'))
                    record_request_event('GET', '/_cert_diagnose_firefox', 200, note='cert-diagnose-firefox', client=_get_client_ip(self))
                except Exception as e:
                    log("Error serving Firefox certificate diagnosis: {}".format(e), level="ERROR")
                    self.send_response(500)
                    self._set_headers()
                    self.end_headers()
                    try:
                        self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                    except Exception:
                        pass
                return
            elif self.path == '/_cert' or self.path.startswith('/_cert'):
                try:
                    cert_info = get_certificate_summary(cert_file)
                    fingerprint = http_get_certificate_fingerprint(cert_file, log=log)
                    
                    # Detect browser from User-Agent header for tailored instructions
                    browser_info = None
                    try:
                        user_agent = self.headers.get('User-Agent', '')
                        if 'Firefox/52' in user_agent and 'Windows NT 5' in user_agent:
                            browser_info = {'name': 'Firefox', 'version': '52', 'isWindowsXP': True}
                        elif 'Firefox/' in user_agent:
                            # Try to extract Firefox version
                            match = re.search(r'Firefox/(\d+)', user_agent)
                            if match:
                                version = match.group(1)
                                is_xp = 'Windows NT 5' in user_agent
                                browser_info = {'name': 'Firefox', 'version': version, 'isWindowsXP': is_xp}
                    except Exception as ua_err:
                        log("Error detecting browser from User-Agent: {}".format(ua_err), level="DEBUG")
                    
                    cert_html = html_build_cert_info_html(cert_info, fingerprint=fingerprint, browser_info=browser_info, server_port=server_port)
                except Exception as cert_err:
                    log("Error generating certificate info page: {}".format(cert_err), level="ERROR")
                    # Provide a fallback HTML page on error
                    cert_html = html_build_fallback_cert_html(str(cert_err), server_port)
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.send_header('Access-Control-Allow-Private-Network', 'true')
                self.end_headers()
                try:
                    self.wfile.write(cert_html.encode('utf-8'))
                except Exception as write_err:
                    log("Failed to write cert info payload: {}".format(write_err))
                record_request_event('GET', '/_cert', 200, note='cert-info', client=_get_client_ip(self))
                return
            elif self.path.startswith('/ca/root.crt'):
                if not is_managed_ca_active():
                    self.send_response(404)
                    self._set_headers()
                    self.end_headers()
                    try:
                        self.wfile.write(json.dumps({'error': 'Managed CA mode disabled'}).encode('utf-8'))
                    except Exception:
                        pass
                    record_request_event('GET', '/ca/root.crt', 404, note='ca-root-missing', client=_get_client_ip(self))
                    return
                root_path = CA_PROFILE.get('root_cert_path')
                if not root_path or not os.path.exists(root_path):
                    try:
                        certificate_authority.ensure_root(CA_PROFILE, log=log, subprocess_module=subprocess)
                        root_path = CA_PROFILE.get('root_cert_path')
                    except Exception as root_err:
                        log("Unable to ensure managed CA root before download: {}".format(root_err), level="ERROR")
                if not root_path or not os.path.exists(root_path):
                    self.send_response(500)
                    self._set_headers()
                    self.end_headers()
                    try:
                        self.wfile.write(json.dumps({'error': 'Managed CA root not available'}).encode('utf-8'))
                    except Exception:
                        pass
                    record_request_event('GET', '/ca/root.crt', 500, note='ca-root-error', client=_get_client_ip(self))
                    return
                try:
                    with open(root_path, 'rb') as root_file:
                        root_bytes = root_file.read()
                except Exception as read_err:
                    log("Failed to read managed CA root for download: {}".format(read_err), level="ERROR")
                    self.send_response(500)
                    self._set_headers()
                    self.end_headers()
                    try:
                        self.wfile.write(json.dumps({'error': 'Unable to read managed root'}).encode('utf-8'))
                    except Exception:
                        pass
                    record_request_event('GET', '/ca/root.crt', 500, note='ca-root-read-failed', client=_get_client_ip(self))
                    return
                self.send_response(200)
                self.send_header('Content-type', 'application/x-x509-ca-cert')
                self.send_header('Content-Disposition', 'attachment; filename="medilink-managed-root.crt"')
                self.send_header('Cache-Control', 'no-store, max-age=0')
                self.send_header('Content-Length', str(len(root_bytes)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.send_header('Access-Control-Allow-Private-Network', 'true')
                self.end_headers()
                try:
                    self.wfile.write(root_bytes)
                except Exception as write_err:
                    log("Failed to stream managed CA root: {}".format(write_err), level="ERROR")
                record_request_event('GET', '/ca/root.crt', 200, note='ca-root-download', client=_get_client_ip(self))
                return
            elif self.path.startswith('/ca/server-info'):
                refresh = 'refresh=1' in self.path or 'full=1' in self.path
                status = get_managed_ca_status(refresh=refresh)
                payload = {
                    'mode': CERT_MODE,
                    'managed': is_managed_ca_active(),
                    'status': status,
                    'download': '/ca/root.crt'
                }
                response_code = 200 if payload['managed'] else 503
                self.send_response(response_code)
                self._set_headers()
                self.end_headers()
                try:
                    self.wfile.write(json.dumps(payload).encode('utf-8'))
                except Exception as info_err:
                    log("Failed to write CA status payload: {}".format(info_err), level="ERROR")
                record_request_event('GET', '/ca/server-info.json', response_code, note='ca-info', client=_get_client_ip(self))
                return
            if self.path.startswith("/?code="):
                try:
                    auth_code = self.path.split('=')[1].split('&')[0]
                except IndexError as e:
                    log("Invalid authorization code path format: {}".format(self.path), level="ERROR")
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    try:
                        self.wfile.write("Invalid authorization code format. Please try again.".encode())
                    except Exception:
                        pass
                    return
                try:
                    auth_code = requests.utils.unquote(auth_code)
                except Exception as e:
                    log("Error unquoting authorization code: {}".format(e), level="ERROR")
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    try:
                        self.wfile.write("Invalid authorization code format. Please try again.".encode())
                    except Exception:
                        pass
                    return
                log("Received authorization code: {}".format(_mask_token_value(auth_code)), level="DEBUG")
                if oauth_is_valid_authorization_code(auth_code, log):
                    try:
                        token_response = exchange_code_for_token(auth_code)
                        if 'access_token' not in token_response:
                            if token_response.get("status") == "error":
                                self.send_response(400)
                                self.send_header('Content-type', 'text/html')
                                self.end_headers()
                                self.wfile.write(token_response["message"].encode())
                                return
                            raise ValueError("Access token not found in response.")
                    except Exception as e:
                        log("Error during token exchange: {}".format(e))
                        self.send_response(500)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write("An error occurred during authentication. Please try again.".encode())
                    else:
                        log("Token response: {}".format(_mask_sensitive_dict(token_response)), level="DEBUG")
                    if 'access_token' in token_response:
                        if shared_save_gmail_token(token_response, log=log, medi_config=medi):
                            # Success - continue with response
                            self.send_response(200)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                            self.wfile.write("Authentication successful. You can close this window now.".encode())

                        # Only launch webapp if not in Gmail send-only mode
                        global httpd
                        if httpd is not None and not getattr(httpd, 'gmail_send_only_mode', False):
                            initiate_link_retrieval(config)
                        else:
                            # For Gmail send-only: just signal completion
                            log("Gmail send-only authentication complete. Server will shutdown after token poll.")
                            shutdown_event.set()
                    else:
                        log("Authentication failed with response: {}".format(_mask_sensitive_dict(token_response)))
                        if 'error' in token_response:
                            error_description = token_response.get('error_description', 'No description provided.')
                            log("Error details: {}".format(error_description))
                        if token_response.get('error') == 'invalid_grant':
                            log("Invalid grant error encountered. Authorization code: {}, Response: {}".format(_mask_token_value(auth_code), _mask_sensitive_dict(token_response)), level="DEBUG")
                            check_invalid_grant_causes(auth_code)
                            shared_clear_token_cache(log=log, medi_config=medi)
                            user_message = "Authentication failed: Invalid or expired authorization code. Please try again."
                        else:
                            user_message = "Authentication failed. Please check the logs for more details."
                        self.send_response(400)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(user_message.encode())
                        shutdown_event.set()
                else:
                    log("Invalid authorization code format: {}".format(_mask_token_value(auth_code)), level="DEBUG")
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    try:
                        self.wfile.write("Invalid authorization code format. Please try again.".encode())
                    except Exception:
                        pass
                    shutdown_event.set()
            elif self.path == '/downloaded-emails':
                self.send_response(200)
                self._set_headers()
                self.end_headers()
                downloaded_emails = load_downloaded_emails()
                response = json.dumps({"downloadedEmails": list(downloaded_emails)})
                try:
                    self.wfile.write(response.encode('utf-8'))
                except OSError as e:
                    if _is_expected_disconnect(e):
                        self.close_connection = True
                    else:
                        raise
            elif self.path == '/':
                # Serve friendly root status page
                # Detect Firefox from User-Agent
                user_agent = self.headers.get('User-Agent', '')
                is_firefox = 'Firefox/' in user_agent
                
                # Run Firefox certificate diagnostic if Firefox detected
                firefox_diagnosis = None
                if is_firefox and FIREFOX_CERT_DIAG_AVAILABLE:
                    try:
                        firefox_path = medi.get('firefox_path') or medi.get('browser_path')
                        firefox_diagnosis = diagnose_firefox_certificate_exceptions(
                            cert_file=cert_file,
                            server_port=server_port,
                            firefox_path=firefox_path,
                            log=log
                        )
                    except Exception as diag_err:
                        log("Error running Firefox diagnostic for root page: {}".format(diag_err), level="DEBUG")
                        # Continue without diagnosis - page will still render
                
                try:
                    safe_status = get_safe_status()
                    cert_info = get_certificate_summary(cert_file)
                    ca_payload = {
                        'mode': CERT_MODE,
                        'managed': is_managed_ca_active(),
                        'status': get_managed_ca_status()
                    }
                    root_html = html_build_root_status_html(
                        safe_status,
                        cert_info,
                        RECENT_REQUESTS,
                        server_port,
                        firefox_diagnosis=firefox_diagnosis,
                        ca_details=ca_payload
                    )
                except Exception as e:
                    log("Error building root status HTML: {}".format(e))
                    root_html = html_build_fallback_status_html(server_port)
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.send_header('Access-Control-Allow-Private-Network', 'true')
                self.end_headers()
                try:
                    self.wfile.write(root_html.encode('utf-8'))
                except OSError as e:
                    if _is_expected_disconnect(e):
                        self.close_connection = True
                    else:
                        raise
                record_request_event('GET', '/', 200, note='root-page', client=_get_client_ip(self))
                return
            else:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.send_header('Access-Control-Allow-Private-Network', 'true')
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                try:
                    self.wfile.write(b'HTTPS server is running.')
                except OSError as e:
                    if _is_expected_disconnect(e):
                        self.close_connection = True
                    else:
                        raise
        except IndexError as e:
            log("IndexError in do_GET for path {}: {}".format(self.path, e), level="ERROR")
            try:
                self.send_response(400)
                self._set_headers()
                self.end_headers()
                error_response = json.dumps({"status": "error", "message": "Invalid request path format"})
                self.wfile.write(error_response.encode('utf-8'))
            except Exception:
                pass
        except OSError as e:
            from MediLink.gmail_http_utils import _is_expected_disconnect
            if _is_expected_disconnect(e):
                log("Client disconnected during GET request: {}".format(e), level="DEBUG")
                self.close_connection = True
            else:
                log("Connection error in GET request: {} - This usually indicates a network error, client disconnect, or socket issue on Windows XP".format(e), level="ERROR")
                send_error_response(self, 500, "Connection error", log_fn=log, error_details=str(e))
        except Exception as e:
            log_request_error(e, self.path, "GET", log, headers=self.headers)
            send_error_response(self, 500, "Internal server error", log_fn=log, error_details=str(e))

def generate_self_signed_cert(cert_path, key_path):
    """
    Ensure local HTTPS materials exist.

    When managed CA mode is enabled, delegate to certificate_authority helpers.
    Otherwise, fall back to the legacy self-signed generator.
    """
    global CA_STATUS_CACHE
    if MANAGED_CA_ENABLED and CA_PROFILE and certificate_authority:
        try:
            status = certificate_authority.ensure_managed_certificate(
                CA_PROFILE,
                log=log,
                subprocess_module=subprocess
            )
            CA_STATUS_CACHE = status or {}
            return status
        except Exception as ca_err:
            log("Managed CA ensure failed: {}. Falling back to self-signed certificates.".format(ca_err), level="WARNING")
    cert_days = medi.get('gmail_cert_days', DEFAULT_CERT_DAYS)
    http_generate_self_signed_cert(get_openssl_cnf(), cert_path, key_path, log, subprocess, cert_days)
    CA_STATUS_CACHE = {}
    return None

def run_server():
    global httpd
    try:
        log("Attempting to start server on port " + str(server_port))
        if not os.path.exists(cert_file):
            log("Error: Certificate file not found: " + cert_file)
        if not os.path.exists(key_file):
            log("Error: Key file not found: " + key_file)
        httpd = HTTPServer(('0.0.0.0', server_port), RequestHandler)
        httpd.gmail_send_only_mode = False  # Default: allow full webapp flow
        httpd.timeout = 30  # Request timeout to prevent hanging on malformed or slow requests
        # Use XP-compatible SSL socket wrapping (supports TLS 1.0/1.1 for Firefox 52 ESR)
        httpd.socket = http_wrap_socket_for_server(httpd.socket, cert_file, key_file, log)
        log("Starting HTTPS server on port {}".format(server_port))
        try:
            print("[Server] HTTPS server ready at https://127.0.0.1:{0}".format(server_port))
        except Exception:
            pass
        httpd.serve_forever()
    except Exception as e:
        global server_crashed
        server_crashed = True  # Mark that server has crashed
        import traceback
        error_type = type(e).__name__
        error_msg = str(e)
        error_msg_full = "HTTPS server thread crashed: {}: {}".format(error_type, error_msg)
        log(error_msg_full, level="ERROR")
        
        # Collect comprehensive diagnostic information
        diagnostic_info = {
            'error_type': error_type,
            'error_message': error_msg,
            'server_port': server_port,
            'cert_file_exists': os.path.exists(cert_file),
            'key_file_exists': os.path.exists(key_file),
            'server_thread_alive': False,
        }
        
        # Capture traceback once for logging and file writing
        tb_str = None
        try:
            tb_str = traceback.format_exc()
            log("Server thread crash traceback: {}".format(tb_str), level="ERROR")
            diagnostic_info['traceback'] = tb_str
        except Exception:
            pass
        
        # Log server state at time of crash
        try:
            status = get_safe_status()
            log("Server status at crash time: {}".format(status), level="ERROR")
            diagnostic_info['server_status'] = status
        except Exception:
            pass
        
        # Write traceback to file so error_reporter can include it in bundle
        if tb_str:
            try:
                trace_path = os.path.join(local_storage_path, 'traceback.txt')
                with open(trace_path, 'w') as f:
                    f.write(tb_str)
                log("Traceback saved to {}".format(trace_path), level="INFO")
            except Exception as trace_err:
                log("Failed to save traceback to file: {}".format(trace_err), level="WARNING")
        else:
            log("No traceback available to save", level="WARNING")
        
        # Automatically submit error report - error_reporter handles collection and submission
        report_submitted = False
        if _submit_support_bundle_email is not None:
            try:
                log("Submitting error report for server crash...", level="INFO")
                # Write diagnostic info to a temporary file for inclusion in bundle
                try:
                    diagnostic_file = os.path.join(local_storage_path, 'server_crash_diagnostics.json')
                    import json as json_module
                    with open(diagnostic_file, 'w') as df:
                        json_module.dump(diagnostic_info, df, indent=2)
                    log("Server crash diagnostic information saved to: {}".format(diagnostic_file), level="INFO")
                except Exception as diag_file_err:
                    log("Failed to save diagnostic file: {}".format(diag_file_err), level="WARNING")
                # submit_support_bundle_email() automatically collects bundle if zip_path is None
                # and handles online/offline submission, bundle size limits, etc.
                success = _submit_support_bundle_email(zip_path=None, include_traceback=True)
                report_submitted = success
                if success:
                    log("Error report submitted successfully for server crash", level="INFO")
                else:
                    log("Error report submission failed or queued for later submission", level="WARNING")
            except Exception as report_exc:
                log("Error report submission failed for server crash: {}".format(report_exc), level="WARNING")
        else:
            log("Support bundle reporter unavailable; cannot auto-submit crash diagnostics.", level="WARNING")
        
        # Display concise console message to user AFTER submission attempt
        try:
            print("\n" + "=" * 60)
            print("SERVER ERROR - HTTPS Server Thread Crashed")
            print("=" * 60)
            print("Error Type: {}".format(error_type))
            print("Error Message: {}".format(error_msg))
            if report_submitted:
                print("\nError report has been automatically submitted.")
            else:
                print("\nError report is being collected and will be submitted when possible.")
            print("Returning to main menu...")
            print("=" * 60 + "\n")
        except Exception:
            pass
        stop_server()

def stop_server():
    global httpd
    if httpd:
        log("Stopping HTTPS server.")
        httpd.shutdown()
        httpd.server_close()
        log("HTTPS server stopped.")
    shutdown_event.set()
    bring_window_to_foreground()

def load_downloaded_emails():
    downloaded_emails = set()
    if os.path.exists(downloaded_emails_file):
        with open(downloaded_emails_file, 'r') as file:
            downloaded_emails = set(line.strip() for line in file)
    log("Loaded downloaded emails: {}".format(downloaded_emails), level="DEBUG")
    return downloaded_emails

def add_downloaded_email(filename, config=None, log_fn=None):
    """
    Add a filename to downloaded_emails.txt.
    
    Reuses existing config loading pattern and file update logic.
    Can be called from both MediLink_Gmail.py and external scripts.
    
    Args:
        filename: Filename to add (just the name, not full path)
        config: Optional config dict. If None, loads using existing pattern
        log_fn: Optional logging function (defaults to module log)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Use provided log function or fall back to module log
        _log = log_fn if log_fn is not None else log
        
        # Load config if not provided
        if config is None:
            try:
                config, _ = load_configuration()
            except Exception as e:
                _log("Failed to load configuration: {}".format(e), level="ERROR")
                return False
        
        # Extract MediLink config using existing pattern
        medi = extract_medilink_config(config)
        local_storage_path = medi.get('local_storage_path', '.')
        downloaded_emails_file_path = os.path.join(local_storage_path, 'downloaded_emails.txt')
        
        # Load existing entries to avoid duplicates (reusing load_downloaded_emails logic)
        downloaded_emails = set()
        if os.path.exists(downloaded_emails_file_path):
            try:
                with open(downloaded_emails_file_path, 'r') as file:
                    downloaded_emails = set(line.strip() for line in file if line.strip())
            except Exception as e:
                _log("Warning: Failed to read existing downloaded_emails.txt: {}".format(e), level="WARNING")
        
        # Check if already in list (case-insensitive check)
        filename_lower = filename.lower()
        if any(existing.lower() == filename_lower for existing in downloaded_emails):
            _log("Filename already in downloaded_emails.txt: {}".format(filename), level="DEBUG")
            return True  # Already exists, consider it successful
        
        # Add to set and append to file (reusing pattern from download_docx_files line 1787-1789)
        downloaded_emails.add(filename)
        try:
            with open(downloaded_emails_file_path, 'a') as file:
                file.write(filename + '\n')
            _log("Added filename to downloaded_emails.txt: {}".format(filename), level="DEBUG")
            return True
        except Exception as e:
            _log("Failed to write to downloaded_emails.txt: {}".format(e), level="ERROR")
            return False
            
    except Exception as e:
        _log = log_fn if log_fn is not None else log
        _log("Error in add_downloaded_email: {}".format(e), level="ERROR")
        return False

def download_docx_files(links):
    # Check internet connectivity before attempting downloads
    if not check_internet_connection():
        log("No internet connection available. Cannot download files without internet access.", level="WARNING")
        return
    
    downloaded_emails = load_downloaded_emails()
    downloads_count = 0
    for link in links:
        url = None  # Initialize to prevent NameError in exception handler
        try:
            url = link.get('url', '')
            filename = link.get('filename', '')
            log("Processing link: url='{}', filename='{}'".format(url, filename), level="DEBUG")
            lower_name = (filename or '').lower()
            looks_like_csv = any(lower_name.endswith(ext) for ext in ['.csv', '.tsv', '.txt', '.dat'])
            if looks_like_csv:
                log("[CSV Routing Preview] Detected CSV-like filename: {}. Would route to CSV processing directory.".format(filename))
            if filename in downloaded_emails:
                log("Skipping already downloaded email: {}".format(filename))
                continue
            log("Downloading .docx file from URL: {}".format(url), level="DEBUG")
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                file_path = os.path.join(local_storage_path, filename)
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                log("Downloaded .docx file: {}".format(filename))
                # Use extracted function to update downloaded_emails.txt (DRY)
                # Pass global config to use any runtime updates (see line 272)
                add_downloaded_email(filename, config=config)
                downloaded_emails.add(filename)
                downloads_count += 1
                try:
                    set_counts(files_downloaded=downloads_count)
                except Exception:
                    pass
            else:
                log("Failed to download .docx file from URL: {}. Status code: {}".format(url, response.status_code))
        except Exception as e:
            log("Error downloading .docx file from URL: {}. Error: {}".format(url, e))

def open_browser_with_executable(url, browser_path=None):
    try:
        if browser_path:
            log("Attempting to open URL with provided executable: {} {}".format(browser_path, url), level="DEBUG")
            process = subprocess.Popen([browser_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                log("Browser opened with provided executable path using subprocess.Popen.")
            else:
                log("Browser failed to open using subprocess.Popen. Return code: {}. Stderr: {}".format(process.returncode, stderr))
        else:
            log("No browser path provided. Attempting to open URL with default browser: {}".format(url), level="DEBUG")
            webbrowser.open(url)
            log("Default browser opened.", level="DEBUG")
    except Exception as e:
        log("Failed to open browser: {}".format(e))

def initiate_link_retrieval(config):
    log("Initiating two-tab launch: local status page first, then GAS webapp.")
    medi = extract_medilink_config(config)
    dep_id = (medi.get('webapp_deployment_id', '') or '').strip()
    if not dep_id:
        log("webapp_deployment_id is empty. Please set it in config before continuing.")
        shutdown_event.set()
        return

    # First tab: Open local status page to verify connectivity and trust
    local_status_url = LOCAL_SERVER_BASE_URL + '/'
    log("Opening local status page: {}".format(local_status_url))
    try:
        print("[Launch] Opening local server status page...")
        open_browser_with_executable(local_status_url)
        # Brief pause to let the first tab load and surface any certificate prompts
        time.sleep(1.5)
    except Exception as e:
        log("Warning: Failed to open local status page: {}".format(e))

    # Second tab: Open GAS webapp for the main workflow
    url_get = "https://script.google.com/macros/s/{}/exec?action=get_link".format(dep_id)
    try:
        log("Opening GAS web app: {}".format(url_get), level="DEBUG")
    except Exception:
        pass
    # Preflight probe to surface HTTP status/redirects before opening the browser
    try:
        probe_url = "https://script.google.com/macros/s/{}/exec".format(dep_id)
        try:
            resp = requests.get(probe_url, allow_redirects=False, timeout=8)
            loc = resp.headers.get('Location')
            log("Preflight probe: status={} location={}".format(resp.status_code, loc), level="DEBUG")
        except Exception as probe_err:
            log("Preflight probe failed: {}".format(probe_err))
    except Exception:
        pass
    try:
        print("[Launch] Opening MediLink web application...")
        open_browser_with_executable(url_get)
    except Exception as e:
        log("Warning: Failed to open GAS webapp: {}".format(e))
    log("Preparing POST call.", level="DEBUG")
    url = "https://script.google.com/macros/s/{}/exec".format(dep_id)
    downloaded_emails = list(load_downloaded_emails())
    payload = {"downloadedEmails": downloaded_emails}
    access_token = get_access_token()
    if not access_token:
        log("Access token not found. Please authenticate first.")
        shutdown_event.set()
        return
    token_info = http_inspect_token(access_token, log, delete_token_file_fn=delete_token_file, stop_server_fn=stop_server)
    if token_info is None:
        log("Access token is invalid. Please re-authenticate.")
        shutdown_event.set()
        return
    headers = {'Authorization': 'Bearer {}'.format(access_token), 'Content-Type': 'application/json'}
    log("Request headers: {}".format(_mask_sensitive_dict(headers)), level="DEBUG")
    log("Request payload: {}".format(payload), level="DEBUG")
    handle_post_response(url, payload, headers)

def handle_post_response(url, payload, headers):
    try:
        response = requests.post(url, json=payload, headers=headers)
        log("Response status code: {}".format(response.status_code), level="DEBUG")
        log("Response body: {}".format(response.text), level="DEBUG")
        if response.status_code == 200:
            response_data = response.json()
            log("Parsed response data: {}".format(response_data), level="DEBUG")
            if response_data.get("status") == "error":
                log("Error message from server: {}".format(response_data.get("message")))
                print("Error: {}".format(response_data.get("message")))
                shutdown_event.set()
            else:
                log("Link retrieval initiated successfully.")
        elif response.status_code == 401:
            # Automatic re-auth: clear token and prompt user to re-consent, keep server up
            log("Unauthorized (401). Clearing cached token and initiating re-authentication flow. Response body: {}".format(response.text))
            delete_token_file()
            auth_url = get_authorization_url()
            print("Your Google session needs to be refreshed to regain permissions. A browser window will open to re-authorize the app with the required scopes.")
            open_browser_with_executable(auth_url)
            # Wait for the OAuth redirect/flow to complete; the server remains running
            shutdown_event.wait()
        elif response.status_code == 403:
            # Treat 403 similarly; scopes may be missing/changed. Force a fresh consent.
            log("Forbidden (403). Clearing cached token and prompting for fresh consent. Response body: {}".format(response.text))
            delete_token_file()
            auth_url = get_authorization_url()
            print("Permissions appear insufficient (403). Opening browser to request the correct Google permissions.")
            open_browser_with_executable(auth_url)
            shutdown_event.wait()
        elif response.status_code == 404:
            log("Not Found. Verify the URL and ensure the Apps Script is deployed correctly. Response body: {}".format(response.text))
            shutdown_event.set()
        else:
            log("Failed to initiate link retrieval. Unexpected status code: {}. Response body: {}".format(response.status_code, response.text))
            shutdown_event.set()
    except requests.exceptions.RequestException as e:
        log("RequestException during link retrieval initiation: {}".format(e))
        shutdown_event.set()
    except Exception as e:
        log("Unexpected error during link retrieval initiation: {}".format(e))
        shutdown_event.set()

def send_delete_request_to_gas(file_ids):
    """Send a delete_files action to the Apps Script web app for the provided Drive file IDs.
    Relies on OAuth token previously obtained. Sends user notifications via GAS.
    """
    try:
        medi = extract_medilink_config(config)
        url = "https://script.google.com/macros/s/{}/exec".format(medi.get('webapp_deployment_id', ''))
        access_token = get_access_token()
        if not access_token:
            log("Access token not found. Skipping cleanup request to GAS.")
            return False
        headers = {'Authorization': 'Bearer {}'.format(access_token), 'Content-Type': 'application/json'}
        payload = {"action": "delete_files", "fileIds": list(file_ids)}
        log("Initiating cleanup request to GAS. Payload size: {} id(s)".format(len(file_ids)))
        resp = requests.post(url, json=payload, headers=headers)
        log("Cleanup response status: {}".format(resp.status_code))
        # Print a concise console message
        if resp.ok:
            try:
                body = resp.json()
                msg = body.get('message', 'Files deleted successfully') if isinstance(body, dict) else 'Files deleted successfully'
            except Exception:
                msg = 'Files deleted successfully'
            print("Cleanup complete: {} ({} file(s))".format(msg, len(file_ids)))
            return True
        else:
            print("Cleanup failed with status {}: {}".format(resp.status_code, resp.text))
            return False
    except Exception as e:
        log("Error sending delete request to GAS: {}".format(e))
        print("Cleanup request error: {}".format(e))
        return False

def inspect_token(access_token):
    return http_inspect_token(access_token, log, delete_token_file_fn=delete_token_file, stop_server_fn=stop_server)

def delete_token_file():
    try:
        if os.path.exists(TOKEN_PATH):
            shared_clear_token_cache(log=log, medi_config=medi)
            if os.path.exists(TOKEN_PATH):
                log("Failed to remove token cache at {}. Check file locks/permissions.".format(TOKEN_PATH), level="WARNING")
            else:
                log("Deleted token cache at {}".format(TOKEN_PATH))
        else:
            log("Token cache already cleared (no file at {}).".format(TOKEN_PATH), level="DEBUG")
    except Exception as e:
        log("Error deleting token cache at {}: {}".format(TOKEN_PATH, e), level="ERROR")

def signal_handler(sig, frame):
    log("Signal received: {}. Initiating shutdown.".format(sig))
    stop_server()
    sys.exit(0)

def auth_and_retrieval():
    access_token = get_access_token()
    if not access_token:
        log("Access token not found or expired. Please authenticate first.")
        auth_url = get_authorization_url()
        open_browser_with_executable(auth_url)
        shutdown_event.wait()
    else:
        log("Access token found. Proceeding.")
        initiate_link_retrieval(config)
        shutdown_event.wait()

def is_valid_authorization_code(auth_code):
    return oauth_is_valid_authorization_code(auth_code, log)

def clear_token_cache():
    shared_clear_token_cache(log=log, medi_config=medi)

def check_invalid_grant_causes(auth_code):
    log("FUTURE IMPLEMENTATION: Checking common causes for invalid_grant error with auth code: {}".format(_mask_token_value(auth_code)))


def ensure_authenticated_for_gmail_send(max_wait_seconds=120):
    """Ensure a valid Gmail access token is available for sending.

    - Reuses existing OAuth helpers in this module.
    - Starts the local HTTPS server if needed, opens the browser for consent,
      and polls for a token for up to max_wait_seconds.
    - Returns True if a usable access token is available after the flow; otherwise False.
    """
    try:
        token = get_access_token()
    except Exception:
        token = None
    if token:
        return True

    # Prepare server and certificates
    try:
        generate_self_signed_cert(cert_file, key_file)
    except Exception as e:
        log("Warning: could not ensure self-signed certs: {}".format(e))

    server_started_here = False
    global httpd
    try:
        if httpd is None:
            log("Starting local HTTPS server for OAuth redirect handling.")
            server_thread = Thread(target=run_server)
            server_thread.daemon = True
            server_thread.start()
            ensure_connection_watchdog_running()
            server_started_here = True
            time.sleep(0.5)  # Wait for server to initialize
            # Set flag to prevent webapp launch
            if httpd is not None:
                httpd.gmail_send_only_mode = True
    except Exception as e:
        log("Failed to start OAuth local server: {}".format(e))

    try:
        auth_url = get_authorization_url()
        print("Opening browser to authorize Gmail permission for sending...")
        open_browser_with_executable(auth_url)
    except Exception as e:
        log("Failed to open authorization URL: {}".format(e))

    # Poll for token availability within timeout
    start_ts = time.time()
    token = None
    while time.time() - start_ts < max_wait_seconds:
        try:
            token = get_access_token()
        except Exception:
            token = None
        if token:
            break
        time.sleep(3)

    if server_started_here:
        try:
            # Reset flag before shutdown
            if httpd is not None:
                httpd.gmail_send_only_mode = False
            stop_server()
        except Exception:
            pass

    if not token:
        print("Gmail authorization not completed within timeout. Please finish consent and retry.")

    return bool(token)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    try:
        # Run diagnostics with auto_fix enabled at startup
        if DIAGNOSTICS_AVAILABLE:
            try:
                diag_report = run_connection_diagnostics(
                    cert_file=cert_file,
                    key_file=key_file,
                    server_port=server_port,
                    auto_fix=True,  # Enable auto-fix at startup
                    openssl_cnf=get_openssl_cnf()
                )
                # Log if certificate was auto-fixed
                if diag_report.get('fixes_successful'):
                    log("Auto-fixed certificate issues: {}".format(diag_report['fixes_successful']), level="INFO")
            except Exception as diag_err:
                log("Error running startup diagnostics: {}".format(diag_err), level="WARNING")
                # Continue - certificate generation will still run below
        
        # Existing certificate generation (fallback if diagnostics not available)
        generate_self_signed_cert(cert_file, key_file)
        from threading import Thread
        log("Starting server thread.")
        server_thread = Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()
        ensure_connection_watchdog_running()
        auth_and_retrieval()
        log("Stopping HTTPS server.")
        stop_server()
        log("Waiting for server thread to finish.")
        server_thread.join(timeout=5)  # Wait up to 5 seconds for thread to finish
        
        # Check if server crashed - if so, exit with error code so batch file can return to menu
        # Note: Reading global variable doesn't require 'global' declaration
        if server_crashed:
            log("Server thread crashed. Exiting with error code to return to main menu.", level="ERROR")
            sys.exit(1)
    except KeyboardInterrupt:
        log("KeyboardInterrupt received, stopping server.")
        stop_server()
        sys.exit(0)
    except Exception as e:
        error_msg = "An error occurred: {}".format(e)
        log(error_msg, level="ERROR")
        # Also print to console so user sees the error immediately
        try:
            import traceback
            print("[ERROR] {}".format(error_msg))
            traceback.print_exc()
        except Exception:
            pass
        stop_server()
        sys.exit(1)
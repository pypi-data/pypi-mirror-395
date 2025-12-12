"""
Hardcoded mapping tables for module name to package name.

These mappings handle cases where the import name differs from the pip package name,
which cannot be determined automatically from metadata.
"""

# Classic mismatches: import name differs from pip package name
# Format: import_name -> [package_name, ...]  (list for multiple candidates)
CLASSIC_MISMATCHES: dict[str, list[str]] = {
    # Computer Vision
    "cv2": ["opencv-python", "opencv-contrib-python", "opencv-python-headless"],
    "cv": ["opencv-python"],

    # Image Processing
    "PIL": ["Pillow"],
    "skimage": ["scikit-image"],
    "imageio": ["imageio"],
    "wand": ["Wand"],

    # Machine Learning
    "sklearn": ["scikit-learn"],
    "xgboost": ["xgboost"],
    "lightgbm": ["lightgbm"],
    "catboost": ["catboost"],
    "numba": ["numba"],
    "cupy": ["cupy"],
    "jax": ["jax"],
    "flax": ["flax"],

    # Data Science
    "yaml": ["PyYAML"],
    "bs4": ["beautifulsoup4"],
    "lxml": ["lxml"],

    # NLP
    "spacy": ["spacy"],
    "nltk": ["nltk"],
    "gensim": ["gensim"],
    "jieba": ["jieba"],

    # Cryptography
    "Crypto": ["pycryptodome", "pycrypto"],
    "Cryptodome": ["pycryptodomex"],
    "nacl": ["pynacl"],
    "OpenSSL": ["pyOpenSSL"],

    # Date/Time
    "dateutil": ["python-dateutil"],
    "pytz": ["pytz"],
    "arrow": ["arrow"],
    "pendulum": ["pendulum"],
    "maya": ["maya"],
    "dateparser": ["dateparser"],

    # Scheduling
    "schedule": ["schedule"],
    "apscheduler": ["APScheduler"],
    "rq": ["rq"],

    # Environment & Configuration
    "dotenv": ["python-dotenv"],
    "decouple": ["python-decouple"],
    "toml": ["toml"],
    "configobj": ["configobj"],

    # Web & Networking
    "jwt": ["PyJWT"],
    "jose": ["python-jose"],
    "websocket": ["websocket-client"],
    "socketio": ["python-socketio"],
    "engineio": ["python-engineio"],
    "slugify": ["python-slugify"],
    "magic": ["python-magic"],
    "whois": ["python-whois"],
    "curl": ["pycurl"],
    "socks": ["PySocks"],
    "paramiko": ["paramiko"],
    "fabric": ["fabric"],

    # Database
    "MySQLdb": ["mysqlclient"],
    "mysql": ["mysql-connector-python"],
    "pymysql": ["PyMySQL"],
    "psycopg2": ["psycopg2-binary", "psycopg2"],
    "pymongo": ["pymongo"],
    "redis": ["redis"],
    "clickhouse_driver": ["clickhouse-driver"],
    "elasticsearch": ["elasticsearch"],
    "neo4j": ["neo4j"],
    "cassandra": ["cassandra-driver"],

    # Messaging
    "telegram": ["python-telegram-bot"],
    "discord": ["discord.py"],
    "slack_sdk": ["slack-sdk"],
    "slack": ["slackclient"],
    "tweepy": ["tweepy"],
    "pika": ["pika"],
    "kafka": ["kafka-python"],
    "nats": ["nats-py"],

    # GUI
    "wx": ["wxPython"],
    "gi": ["PyGObject"],
    "PyQt5": ["PyQt5"],
    "PyQt6": ["PyQt6"],
    "PySide2": ["PySide2"],
    "PySide6": ["PySide6"],
    "tkinter": [],  # Built-in, but sometimes needs tk package on system

    # Hardware & Serial
    "serial": ["pyserial"],
    "usb": ["pyusb"],
    "hid": ["hidapi"],
    "smbus": ["smbus2"],

    # Scientific
    "scipy": ["scipy"],
    "sympy": ["sympy"],

    # Audio & Video
    "pydub": ["pydub"],
    "soundfile": ["soundfile"],
    "librosa": ["librosa"],
    "moviepy": ["moviepy"],
    "ffmpeg": ["ffmpeg-python"],

    # Document Processing
    "docx": ["python-docx"],
    "pptx": ["python-pptx"],
    "openpyxl": ["openpyxl"],
    "xlrd": ["xlrd"],
    "xlwt": ["xlwt"],
    "PyPDF2": ["PyPDF2"],
    "pypdf": ["pypdf"],
    "fitz": ["PyMuPDF"],
    "reportlab": ["reportlab"],

    # Testing
    "mock": ["mock"],
    "faker": ["Faker"],
    "factory": ["factory-boy"],
    "hypothesis": ["hypothesis"],

    # CLI
    "click": ["click"],
    "typer": ["typer"],
    "rich": ["rich"],
    "tqdm": ["tqdm"],
    "colorama": ["colorama"],
    "termcolor": ["termcolor"],

    # Validation
    "pydantic": ["pydantic"],
    "marshmallow": ["marshmallow"],
    "cerberus": ["cerberus"],
    "voluptuous": ["voluptuous"],
    "jsonschema": ["jsonschema"],
    "validators": ["validators"],

    # Async
    "aiohttp": ["aiohttp"],
    "httpx": ["httpx"],
    "trio": ["trio"],
    "anyio": ["anyio"],
    "uvloop": ["uvloop"],

    # Configuration
    "hydra": ["hydra-core"],
    "omegaconf": ["omegaconf"],

    # Logging
    "loguru": ["loguru"],
    "structlog": ["structlog"],

    # File Monitoring
    "watchdog": ["watchdog"],
    "inotify": ["inotify"],

    # Shell & Process
    "sh": ["sh"],
    "plumbum": ["plumbum"],
    "pexpect": ["pexpect"],

    # Security & Credentials
    "keyring": ["keyring"],
    "keyrings": ["keyring"],

    # Cloud SDKs
    "oss2": ["oss2"],  # Aliyun OSS
    "qiniu": ["qiniu"],  # Qiniu Cloud

    # Web Scraping
    "scrapy": ["Scrapy"],
    "selenium": ["selenium"],
    "playwright": ["playwright"],
    "pyppeteer": ["pyppeteer"],

    # Other common mismatches
    "attr": ["attrs"],
    "attrs": ["attrs"],
    "charset_normalizer": ["charset-normalizer"],
    "idna": ["idna"],
    "certifi": ["certifi"],
    "urllib3": ["urllib3"],
    "pkg_resources": ["setuptools"],
    "setuptools": ["setuptools"],
    "distutils": ["setuptools"],
    "mpl_toolkits": ["matplotlib"],
    "google.protobuf": ["protobuf"],
    "grpc": ["grpcio"],
    "graphql": ["graphql-core"],
    "jinja2": ["Jinja2"],
    "Jinja2": ["Jinja2"],
    "markupsafe": ["MarkupSafe"],
    "MarkupSafe": ["MarkupSafe"],
    "werkzeug": ["Werkzeug"],
    "Werkzeug": ["Werkzeug"],
    "itsdangerous": ["itsdangerous"],
    "flask": ["Flask"],
    "Flask": ["Flask"],
    "django": ["Django"],
    "Django": ["Django"],
    "fastapi": ["fastapi"],
    "starlette": ["starlette"],
    "uvicorn": ["uvicorn"],
    "gunicorn": ["gunicorn"],
    "gevent": ["gevent"],
    "greenlet": ["greenlet"],
    "celery": ["celery"],
    "kombu": ["kombu"],
    "billiard": ["billiard"],
    "amqp": ["amqp"],
    "sentry_sdk": ["sentry-sdk"],
    "stripe": ["stripe"],
    "twilio": ["twilio"],

    # Utility
    "humanize": ["humanize"],
    "inflect": ["inflect"],
    "shortuuid": ["shortuuid"],
    "nanoid": ["nanoid"],
    "pathvalidate": ["pathvalidate"],
}


# .pth injected modules (like PyWin32)
# These modules appear in site-packages but not in top_level.txt
PTH_INJECTED_MODULES: dict[str, str] = {
    # PyWin32 modules
    "win32api": "pywin32",
    "win32gui": "pywin32",
    "win32con": "pywin32",
    "win32clipboard": "pywin32",
    "win32com": "pywin32",
    "win32crypt": "pywin32",
    "win32event": "pywin32",
    "win32evtlog": "pywin32",
    "win32file": "pywin32",
    "win32job": "pywin32",
    "win32lz": "pywin32",
    "win32net": "pywin32",
    "win32pdh": "pywin32",
    "win32pipe": "pywin32",
    "win32print": "pywin32",
    "win32process": "pywin32",
    "win32profile": "pywin32",
    "win32ras": "pywin32",
    "win32security": "pywin32",
    "win32service": "pywin32",
    "win32serviceutil": "pywin32",
    "win32timezone": "pywin32",
    "win32trace": "pywin32",
    "win32transaction": "pywin32",
    "win32ts": "pywin32",
    "win32wnet": "pywin32",
    "pythoncom": "pywin32",
    "pywintypes": "pywin32",
    "servicemanager": "pywin32",
    "mmapfile": "pywin32",
    "odbc": "pywin32",
    "dde": "pywin32",
    "timer": "pywin32",
    "win2kras": "pywin32",
    "winxpgui": "pywin32",

    # Other .pth injected modules
    # Note: google is NOT a .pth injected module - it's a namespace package
    # handled separately in namespace.py
}


# Binary vs source package preferences
# For packages that have both binary and source versions
BINARY_PREFERENCES: dict[str, dict] = {
    "psycopg2": {
        "source": "psycopg2",
        "binary": "psycopg2-binary",
        "recommended": "psycopg2-binary",
        "note": "Use psycopg2-binary for development, psycopg2 for production",
    },
    "lxml": {
        "source": "lxml",
        "binary": "lxml",  # Same package, wheels available
        "recommended": "lxml",
        "note": "Pre-built wheels available for most platforms",
    },
}


# Platform-specific package mappings
# import_name -> {platform: package_name}
PLATFORM_SPECIFIC: dict[str, dict[str, str]] = {
    "tensorflow": {
        "darwin_arm64": "tensorflow-macos",
        "darwin_x86_64": "tensorflow",
        "linux": "tensorflow",
        "win32": "tensorflow",
        "default": "tensorflow",
    },
    "torch": {
        "default": "torch",
        # Note: PyTorch has complex versioning with CUDA variants
        # Users may need torch+cu118, torch+cpu, etc.
    },
}


def get_hardcoded_mapping(module_name: str) -> list[str] | None:
    """
    Get package candidates from hardcoded mappings.

    Args:
        module_name: The import module name (top-level)

    Returns:
        List of package name candidates, or None if not found
    """
    # Check classic mismatches first
    if module_name in CLASSIC_MISMATCHES:
        candidates = CLASSIC_MISMATCHES[module_name]
        if candidates:
            return candidates

    # Check .pth injected modules
    if module_name in PTH_INJECTED_MODULES:
        return [PTH_INJECTED_MODULES[module_name]]

    return None


def get_all_hardcoded_modules() -> set[str]:
    """Get all module names that have hardcoded mappings."""
    modules = set(CLASSIC_MISMATCHES.keys())
    modules.update(PTH_INJECTED_MODULES.keys())
    return modules

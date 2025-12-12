"""
Namespace package mappings.

Handles packages like google.cloud.*, azure.*, zope.* where the top-level
module name is shared across many different packages.
"""

from typing import Any

# Namespace package mappings
# Structure: top_level -> {submodule -> package_name or nested dict}
NAMESPACE_PACKAGES: dict[str, dict[str, Any]] = {
    "google": {
        "cloud": {
            "storage": "google-cloud-storage",
            "bigquery": "google-cloud-bigquery",
            "pubsub": "google-cloud-pubsub",
            "pubsub_v1": "google-cloud-pubsub",
            "firestore": "google-cloud-firestore",
            "firestore_v1": "google-cloud-firestore",
            "spanner": "google-cloud-spanner",
            "bigtable": "google-cloud-bigtable",
            "datastore": "google-cloud-datastore",
            "logging": "google-cloud-logging",
            "monitoring": "google-cloud-monitoring",
            "vision": "google-cloud-vision",
            "speech": "google-cloud-speech",
            "texttospeech": "google-cloud-texttospeech",
            "translate": "google-cloud-translate",
            "language": "google-cloud-language",
            "videointelligence": "google-cloud-videointelligence",
            "aiplatform": "google-cloud-aiplatform",
            "functions": "google-cloud-functions",
            "run": "google-cloud-run",
            "compute": "google-cloud-compute",
            "container": "google-cloud-container",
            "kms": "google-cloud-kms",
            "secretmanager": "google-cloud-secret-manager",
            "tasks": "google-cloud-tasks",
            "scheduler": "google-cloud-scheduler",
            "redis": "google-cloud-redis",
            "memcache": "google-cloud-memcache",
            "sql": "google-cloud-sql-connector",
            "ndb": "google-cloud-ndb",
            "exceptions": "google-cloud-core",
            "operation": "google-cloud-core",
            "_helpers": "google-cloud-core",
        },
        "auth": "google-auth",
        "oauth2": "google-auth",
        "api_core": "google-api-core",
        "api": "google-api-python-client",
        "protobuf": "protobuf",
        "ads": {
            "googleads": "google-ads",
        },
        "analytics": {
            "data": "google-analytics-data",
            "admin": "google-analytics-admin",
        },
        "generativeai": "google-generativeai",
    },

    "azure": {
        "storage": {
            "blob": "azure-storage-blob",
            "queue": "azure-storage-queue",
            "file": "azure-storage-file-share",
            "fileshare": "azure-storage-file-share",
            "filedatalake": "azure-storage-file-datalake",
        },
        "identity": "azure-identity",
        "keyvault": {
            "secrets": "azure-keyvault-secrets",
            "keys": "azure-keyvault-keys",
            "certificates": "azure-keyvault-certificates",
        },
        "cosmos": "azure-cosmos",
        "cosmosdb": "azure-cosmos",
        "servicebus": "azure-servicebus",
        "eventhub": "azure-eventhub",
        "functions": "azure-functions",
        "mgmt": {
            "resource": "azure-mgmt-resource",
            "compute": "azure-mgmt-compute",
            "network": "azure-mgmt-network",
            "storage": "azure-mgmt-storage",
            "keyvault": "azure-mgmt-keyvault",
            "sql": "azure-mgmt-sql",
            "cosmosdb": "azure-mgmt-cosmosdb",
            "web": "azure-mgmt-web",
            "containerservice": "azure-mgmt-containerservice",
            "monitor": "azure-mgmt-monitor",
        },
        "ai": {
            "ml": "azure-ai-ml",
            "textanalytics": "azure-ai-textanalytics",
            "formrecognizer": "azure-ai-formrecognizer",
            "vision": "azure-ai-vision",
            "language": "azure-ai-language-questionanswering",
        },
        "core": "azure-core",
        "common": "azure-common",
    },

    "zope": {
        "interface": "zope.interface",
        "component": "zope.component",
        "event": "zope.event",
        "schema": "zope.schema",
        "configuration": "zope.configuration",
        "security": "zope.security",
        "proxy": "zope.proxy",
        "deprecation": "zope.deprecation",
        "hookable": "zope.hookable",
        "exceptions": "zope.exceptions",
    },

    "boto3": {
        # boto3 is a single package but has many submodules
        "_default": "boto3",
    },

    "botocore": {
        "_default": "botocore",
    },

    "aws_cdk": {
        "_default": "aws-cdk-lib",
        "core": "aws-cdk.core",
        "aws_s3": "aws-cdk.aws-s3",
        "aws_lambda": "aws-cdk.aws-lambda",
        "aws_dynamodb": "aws-cdk.aws-dynamodb",
        "aws_ec2": "aws-cdk.aws-ec2",
        "aws_ecs": "aws-cdk.aws-ecs",
        "aws_iam": "aws-cdk.aws-iam",
        "aws_sqs": "aws-cdk.aws-sqs",
        "aws_sns": "aws-cdk.aws-sns",
        "aws_apigateway": "aws-cdk.aws-apigateway",
    },

    "sqlalchemy": {
        "_default": "SQLAlchemy",
    },

    "openai": {
        "_default": "openai",
    },

    "anthropic": {
        "_default": "anthropic",
    },

    "langchain": {
        "_default": "langchain",
        "community": "langchain-community",
        "core": "langchain-core",
        "openai": "langchain-openai",
        "anthropic": "langchain-anthropic",
    },

    "transformers": {
        "_default": "transformers",
    },

    "huggingface_hub": {
        "_default": "huggingface-hub",
    },

    # Airflow ecosystem
    "airflow": {
        "_default": "apache-airflow",
        "providers": {
            "google": "apache-airflow-providers-google",
            "amazon": "apache-airflow-providers-amazon",
            "microsoft": {
                "azure": "apache-airflow-providers-microsoft-azure",
            },
            "postgres": "apache-airflow-providers-postgres",
            "mysql": "apache-airflow-providers-mysql",
            "http": "apache-airflow-providers-http",
            "ssh": "apache-airflow-providers-ssh",
            "slack": "apache-airflow-providers-slack",
        },
    },

    # Databricks
    "databricks": {
        "sdk": "databricks-sdk",
        "connect": "databricks-connect",
        "sql": "databricks-sql-connector",
    },

    # Snowflake
    "snowflake": {
        "connector": "snowflake-connector-python",
        "sqlalchemy": "snowflake-sqlalchemy",
        "snowpark": "snowflake-snowpark-python",
    },

    # TensorFlow ecosystem
    "tensorflow": {
        "_default": "tensorflow",
        "keras": "tensorflow",
        "data": "tensorflow",
        "lite": "tensorflow",
    },
    "tf_keras": {
        "_default": "tf-keras",
    },
    "keras": {
        "_default": "keras",
    },

    # PyTorch ecosystem
    "torch": {
        "_default": "torch",
    },
    "torchvision": {
        "_default": "torchvision",
    },
    "torchaudio": {
        "_default": "torchaudio",
    },

    # Flask extensions
    "flask_sqlalchemy": {"_default": "Flask-SQLAlchemy"},
    "flask_login": {"_default": "Flask-Login"},
    "flask_wtf": {"_default": "Flask-WTF"},
    "flask_cors": {"_default": "Flask-Cors"},
    "flask_restful": {"_default": "Flask-RESTful"},
    "flask_migrate": {"_default": "Flask-Migrate"},
    "flask_mail": {"_default": "Flask-Mail"},
    "flask_caching": {"_default": "Flask-Caching"},

    # Django extensions
    "rest_framework": {"_default": "djangorestframework"},
    "django_filters": {"_default": "django-filter"},
    "corsheaders": {"_default": "django-cors-headers"},
    "debug_toolbar": {"_default": "django-debug-toolbar"},
    "django_celery_beat": {"_default": "django-celery-beat"},
    "django_celery_results": {"_default": "django-celery-results"},

    # Other popular packages
    "alembic": {"_default": "alembic"},
    "celery": {"_default": "celery"},
    "stripe": {"_default": "stripe"},
    "twilio": {"_default": "twilio"},
    "sentry_sdk": {"_default": "sentry-sdk"},

    # Apache projects
    "apache_beam": {"_default": "apache-beam"},
    "pyspark": {"_default": "pyspark"},
}

# Known namespace package prefixes
# These are top-level modules that are definitely namespace packages
NAMESPACE_PREFIXES: set[str] = {
    "google",
    "azure",
    "zope",
    "aws_cdk",
    "boto3",
    "botocore",
    "airflow",
    "databricks",
    "snowflake",
    "tensorflow",
    "torch",
    "flask_sqlalchemy",
    "flask_login",
    "flask_wtf",
    "flask_cors",
    "rest_framework",
}


def _flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict[str, str]:
    """Flatten a nested dictionary into dot-separated keys."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(_flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def resolve_namespace_package(
    top_level: str,
    sub_modules: list[str],
) -> list[str]:
    """
    Resolve a namespace package import to its pip package name(s).

    Args:
        top_level: The top-level module name (e.g., "google")
        sub_modules: List of submodule names (e.g., ["cloud", "storage"])

    Returns:
        List of candidate package names, empty if not found
    """
    if top_level not in NAMESPACE_PACKAGES:
        return []

    mapping = NAMESPACE_PACKAGES[top_level]

    # Check for _default first (packages where top-level is enough)
    if "_default" in mapping and not sub_modules:
        return [mapping["_default"]]

    # Navigate through the submodule path
    current = mapping
    for sub in sub_modules:
        if isinstance(current, dict):
            if sub in current:
                current = current[sub]
            elif "_default" in current:
                # Submodule not found, but there's a default
                return [current["_default"]]
            else:
                # Can't resolve further
                break
        else:
            # Reached a string (package name)
            return [current] if isinstance(current, str) else []

    # Return the resolved value
    if isinstance(current, str):
        return [current]
    elif isinstance(current, dict):
        if "_default" in current:
            return [current["_default"]]
        # Return all possible packages at this level
        return list(set(
            v if isinstance(v, str) else v.get("_default", "")
            for v in current.values()
            if v and (isinstance(v, str) or isinstance(v, dict) and "_default" in v)
        ))

    return []


def is_namespace_package(module_name: str) -> bool:
    """Check if a module might be a namespace package."""
    top_level = module_name.split(".")[0]
    return top_level in NAMESPACE_PREFIXES or top_level in NAMESPACE_PACKAGES


def get_all_namespace_mappings() -> dict[str, str]:
    """Get all namespace mappings as a flat dictionary."""
    result = {}
    for top_level, mapping in NAMESPACE_PACKAGES.items():
        flat = _flatten_dict(mapping, top_level)
        for key, value in flat.items():
            if not key.endswith("._default") and value:
                result[key] = value
    return result

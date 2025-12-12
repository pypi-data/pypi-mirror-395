"""Tests for the mapping modules - v0.2.0 comprehensive tests."""

import pytest

from pyimport2pkg.mappings import (
    get_hardcoded_mapping,
    get_all_hardcoded_modules,
    resolve_namespace_package,
    is_namespace_package,
    CLASSIC_MISMATCHES,
    PTH_INJECTED_MODULES,
    NAMESPACE_PACKAGES,
)


class TestHardcodedMappingsClassicMismatches:
    """Test classic module-package mismatches."""

    def test_cv2_opencv_python(self):
        """Test cv2 -> opencv-python mapping."""
        result = get_hardcoded_mapping("cv2")
        assert result is not None
        assert "opencv-python" in result

    def test_cv2_multiple_candidates(self):
        """Test cv2 has multiple candidates."""
        result = get_hardcoded_mapping("cv2")
        assert len(result) >= 3
        assert "opencv-python" in result
        assert "opencv-contrib-python" in result
        assert "opencv-python-headless" in result

    def test_pil_pillow(self):
        """Test PIL -> Pillow mapping."""
        result = get_hardcoded_mapping("PIL")
        assert result is not None
        assert "Pillow" in result

    def test_sklearn_scikit_learn(self):
        """Test sklearn -> scikit-learn mapping."""
        result = get_hardcoded_mapping("sklearn")
        assert result is not None
        assert "scikit-learn" in result

    def test_yaml_pyyaml(self):
        """Test yaml -> PyYAML mapping."""
        result = get_hardcoded_mapping("yaml")
        assert result is not None
        assert "PyYAML" in result

    def test_bs4_beautifulsoup4(self):
        """Test bs4 -> beautifulsoup4 mapping."""
        result = get_hardcoded_mapping("bs4")
        assert result is not None
        assert "beautifulsoup4" in result

    def test_dateutil_python_dateutil(self):
        """Test dateutil -> python-dateutil mapping."""
        result = get_hardcoded_mapping("dateutil")
        assert result is not None
        assert "python-dateutil" in result

    def test_jwt_pyjwt(self):
        """Test jwt -> PyJWT mapping."""
        result = get_hardcoded_mapping("jwt")
        assert result is not None
        assert "PyJWT" in result

    def test_dotenv_python_dotenv(self):
        """Test dotenv -> python-dotenv mapping."""
        result = get_hardcoded_mapping("dotenv")
        assert result is not None
        assert "python-dotenv" in result

    def test_usb_pyusb(self):
        """Test usb -> pyusb mapping."""
        result = get_hardcoded_mapping("usb")
        assert result is not None
        assert "pyusb" in result


class TestHardcodedMappingsNLP:
    """Test NLP package mappings."""

    def test_spacy(self):
        """Test spacy mapping."""
        result = get_hardcoded_mapping("spacy")
        assert result is not None
        assert "spacy" in result

    def test_nltk(self):
        """Test nltk mapping."""
        result = get_hardcoded_mapping("nltk")
        assert result is not None
        assert "nltk" in result

    def test_gensim(self):
        """Test gensim mapping."""
        result = get_hardcoded_mapping("gensim")
        assert result is not None
        assert "gensim" in result

    def test_jieba(self):
        """Test jieba mapping."""
        result = get_hardcoded_mapping("jieba")
        assert result is not None
        assert "jieba" in result


class TestHardcodedMappingsScheduling:
    """Test scheduling package mappings."""

    def test_apscheduler(self):
        """Test apscheduler mapping."""
        result = get_hardcoded_mapping("apscheduler")
        assert result is not None
        assert "APScheduler" in result

    def test_celery(self):
        """Test celery mapping."""
        result = get_hardcoded_mapping("celery")
        assert result is not None
        assert "celery" in result

    def test_rq(self):
        """Test rq mapping."""
        result = get_hardcoded_mapping("rq")
        assert result is not None
        assert "rq" in result

    def test_schedule(self):
        """Test schedule mapping."""
        result = get_hardcoded_mapping("schedule")
        assert result is not None
        assert "schedule" in result


class TestHardcodedMappingsLogging:
    """Test logging package mappings added in v0.2.0."""

    def test_loguru(self):
        """Test loguru mapping."""
        result = get_hardcoded_mapping("loguru")
        assert result is not None
        assert "loguru" in result

    def test_structlog(self):
        """Test structlog mapping."""
        result = get_hardcoded_mapping("structlog")
        assert result is not None
        assert "structlog" in result


class TestHardcodedMappingsDatabase:
    """Test database package mappings."""

    def test_pymongo(self):
        """Test pymongo mapping."""
        result = get_hardcoded_mapping("pymongo")
        assert result is not None
        assert "pymongo" in result

    def test_elasticsearch(self):
        """Test elasticsearch mapping."""
        result = get_hardcoded_mapping("elasticsearch")
        assert result is not None
        assert "elasticsearch" in result

    def test_redis(self):
        """Test redis mapping."""
        result = get_hardcoded_mapping("redis")
        assert result is not None
        assert "redis" in result

    def test_psycopg2(self):
        """Test psycopg2 mapping."""
        result = get_hardcoded_mapping("psycopg2")
        assert result is not None
        assert "psycopg2-binary" in result or "psycopg2" in result

    def test_pymysql(self):
        """Test pymysql mapping."""
        result = get_hardcoded_mapping("pymysql")
        assert result is not None
        assert "PyMySQL" in result


class TestHardcodedMappingsScraping:
    """Test web scraping package mappings."""

    def test_scrapy(self):
        """Test scrapy mapping."""
        result = get_hardcoded_mapping("scrapy")
        assert result is not None
        assert "Scrapy" in result

    def test_lxml(self):
        """Test lxml mapping."""
        result = get_hardcoded_mapping("lxml")
        assert result is not None
        assert "lxml" in result

    def test_selenium(self):
        """Test selenium mapping."""
        result = get_hardcoded_mapping("selenium")
        assert result is not None
        assert "selenium" in result

    def test_playwright(self):
        """Test playwright mapping."""
        result = get_hardcoded_mapping("playwright")
        assert result is not None
        assert "playwright" in result


class TestHardcodedMappingsCloudSDK:
    """Test cloud-related SDK mappings."""

    def test_oss2(self):
        """Test oss2 (Aliyun OSS) mapping."""
        result = get_hardcoded_mapping("oss2")
        assert result is not None
        assert "oss2" in result

    def test_qiniu(self):
        """Test qiniu mapping."""
        result = get_hardcoded_mapping("qiniu")
        assert result is not None
        assert "qiniu" in result

    def test_grpc(self):
        """Test grpc -> grpcio mapping."""
        result = get_hardcoded_mapping("grpc")
        assert result is not None
        assert "grpcio" in result


class TestPTHInjectedModules:
    """Test PTH injected modules (PyWin32, etc.)."""

    def test_win32api(self):
        """Test win32api -> pywin32 mapping."""
        result = get_hardcoded_mapping("win32api")
        assert result is not None
        assert "pywin32" in result

    def test_win32gui(self):
        """Test win32gui -> pywin32 mapping."""
        result = get_hardcoded_mapping("win32gui")
        assert result is not None
        assert "pywin32" in result

    def test_win32con(self):
        """Test win32con -> pywin32 mapping."""
        result = get_hardcoded_mapping("win32con")
        assert result is not None
        assert "pywin32" in result

    def test_win32clipboard(self):
        """Test win32clipboard -> pywin32 mapping."""
        result = get_hardcoded_mapping("win32clipboard")
        assert result is not None
        assert "pywin32" in result

    def test_win32com(self):
        """Test win32com -> pywin32 mapping."""
        result = get_hardcoded_mapping("win32com")
        assert result is not None
        assert "pywin32" in result

    def test_pythoncom(self):
        """Test pythoncom -> pywin32 mapping."""
        result = get_hardcoded_mapping("pythoncom")
        assert result is not None
        assert "pywin32" in result

    def test_pywintypes(self):
        """Test pywintypes -> pywin32 mapping."""
        result = get_hardcoded_mapping("pywintypes")
        assert result is not None
        assert "pywin32" in result

    def test_pywin32_modules_all_present(self):
        """Test that all known PyWin32 modules are mapped."""
        pywin32_modules = [
            "win32api", "win32gui", "win32con", "win32clipboard",
            "win32event", "win32file", "win32pipe", "win32process",
            "win32security", "win32service", "win32com", "pythoncom",
            "pywintypes"
        ]
        for module in pywin32_modules:
            result = get_hardcoded_mapping(module)
            assert result is not None, f"{module} not found in hardcoded mappings"
            assert "pywin32" in result, f"{module} does not map to pywin32"


class TestHardcodedMappingsHelpers:
    """Test helper functions for hardcoded mappings."""

    def test_unknown_module_returns_none(self):
        """Test that unknown modules return None."""
        result = get_hardcoded_mapping("unknown_module_xyz_123")
        assert result is None

    def test_get_all_hardcoded_modules(self):
        """Test getting all hardcoded module names."""
        modules = get_all_hardcoded_modules()

        # Check that key modules are present
        assert "cv2" in modules
        assert "PIL" in modules
        assert "sklearn" in modules
        assert "yaml" in modules
        assert "win32api" in modules

        # Should have substantial number of modules
        assert len(modules) >= 50

    def test_hardcoded_mappings_structure(self):
        """Test that all hardcoded mappings have correct structure."""
        # Test CLASSIC_MISMATCHES
        for module_name, packages in CLASSIC_MISMATCHES.items():
            assert isinstance(module_name, str), f"{module_name} is not a string"
            assert isinstance(packages, list), f"{module_name} packages is not a list"
            # Note: some modules like tkinter may have empty list (built-in)
            for pkg in packages:
                assert isinstance(pkg, str), f"{module_name} has non-string package: {pkg}"

        # Test PTH_INJECTED_MODULES
        for module_name, package in PTH_INJECTED_MODULES.items():
            assert isinstance(module_name, str), f"{module_name} is not a string"
            assert isinstance(package, str), f"{module_name} package is not a string"


class TestNamespaceMappingsGoogle:
    """Test Google Cloud namespace packages."""

    def test_google_cloud_storage(self):
        """Test google.cloud.storage mapping."""
        result = resolve_namespace_package("google", ["cloud", "storage"])
        assert "google-cloud-storage" in result

    def test_google_cloud_bigquery(self):
        """Test google.cloud.bigquery mapping."""
        result = resolve_namespace_package("google", ["cloud", "bigquery"])
        assert "google-cloud-bigquery" in result

    def test_google_cloud_pubsub(self):
        """Test google.cloud.pubsub mapping."""
        result = resolve_namespace_package("google", ["cloud", "pubsub"])
        assert "google-cloud-pubsub" in result

    def test_google_auth(self):
        """Test google.auth mapping."""
        result = resolve_namespace_package("google", ["auth"])
        assert "google-auth" in result

    def test_google_api_core(self):
        """Test google.api_core mapping."""
        result = resolve_namespace_package("google", ["api_core"])
        assert "google-api-core" in result


class TestNamespaceMappingsAzure:
    """Test Azure namespace packages."""

    def test_azure_storage_blob(self):
        """Test azure.storage.blob mapping."""
        result = resolve_namespace_package("azure", ["storage", "blob"])
        assert "azure-storage-blob" in result

    def test_azure_identity(self):
        """Test azure.identity mapping."""
        result = resolve_namespace_package("azure", ["identity"])
        assert "azure-identity" in result

    def test_azure_core(self):
        """Test azure.core mapping."""
        result = resolve_namespace_package("azure", ["core"])
        assert "azure-core" in result


class TestNamespaceMappingsAirflow:
    """Test Airflow provider namespace packages added in v0.2.0."""

    def test_airflow_providers_amazon(self):
        """Test airflow.providers.amazon mapping."""
        result = resolve_namespace_package("airflow", ["providers", "amazon"])
        assert "apache-airflow-providers-amazon" in result

    def test_airflow_providers_google(self):
        """Test airflow.providers.google mapping."""
        result = resolve_namespace_package("airflow", ["providers", "google"])
        assert "apache-airflow-providers-google" in result

    def test_airflow_providers_postgres(self):
        """Test airflow.providers.postgres mapping."""
        result = resolve_namespace_package("airflow", ["providers", "postgres"])
        assert "apache-airflow-providers-postgres" in result


class TestNamespaceMappingsDatabricks:
    """Test Databricks namespace packages added in v0.2.0."""

    def test_databricks_sdk(self):
        """Test databricks.sdk mapping."""
        result = resolve_namespace_package("databricks", ["sdk"])
        assert "databricks-sdk" in result

    def test_databricks_connect(self):
        """Test databricks.connect mapping."""
        result = resolve_namespace_package("databricks", ["connect"])
        assert "databricks-connect" in result


class TestNamespaceMappingsSnowflake:
    """Test Snowflake namespace packages added in v0.2.0."""

    def test_snowflake_connector(self):
        """Test snowflake.connector mapping."""
        result = resolve_namespace_package("snowflake", ["connector"])
        assert "snowflake-connector-python" in result

    def test_snowflake_snowpark(self):
        """Test snowflake.snowpark mapping."""
        result = resolve_namespace_package("snowflake", ["snowpark"])
        assert "snowflake-snowpark-python" in result


class TestNamespaceMappingsFlaskExtensions:
    """Test Flask extension mappings.

    Note: Flask extensions use underscore module names but hyphen package names.
    These are not namespace packages but hardcoded mappings might be needed.
    """

    def test_flask_is_mapped(self):
        """Test flask itself is mapped."""
        result = get_hardcoded_mapping("flask")
        assert result is not None
        assert "Flask" in result

    def test_Flask_capitalized(self):
        """Test Flask (capitalized) is mapped."""
        result = get_hardcoded_mapping("Flask")
        assert result is not None
        assert "Flask" in result


class TestNamespaceMappingsZope:
    """Test Zope namespace packages."""

    def test_zope_interface(self):
        """Test zope.interface mapping."""
        result = resolve_namespace_package("zope", ["interface"])
        assert "zope.interface" in result

    def test_zope_component(self):
        """Test zope.component mapping."""
        result = resolve_namespace_package("zope", ["component"])
        assert "zope.component" in result


class TestNamespaceMappingsHelpers:
    """Test helper functions for namespace mappings."""

    def test_unknown_namespace_returns_empty(self):
        """Test that unknown namespace returns empty list."""
        result = resolve_namespace_package("unknown_namespace", ["submodule"])
        assert result == []

    def test_is_namespace_package_true(self):
        """Test is_namespace_package returns True for known namespaces."""
        assert is_namespace_package("google") is True
        assert is_namespace_package("google.cloud") is True
        assert is_namespace_package("azure") is True
        assert is_namespace_package("zope") is True
        assert is_namespace_package("airflow") is True
        assert is_namespace_package("databricks") is True
        assert is_namespace_package("snowflake") is True

    def test_is_namespace_package_false(self):
        """Test is_namespace_package returns False for non-namespaces."""
        assert is_namespace_package("numpy") is False
        assert is_namespace_package("pandas") is False
        assert is_namespace_package("requests") is False

    def test_namespace_packages_structure(self):
        """Test that all namespace packages have correct structure."""
        def check_namespace_dict(data: dict, prefix: str = "") -> None:
            """Recursively check namespace structure."""
            for sub_path, value in data.items():
                full_path = f"{prefix}.{sub_path}" if prefix else sub_path
                assert isinstance(sub_path, str), f"{full_path} key is not a string"
                # Value can be string (package name) or dict (nested namespace)
                if isinstance(value, dict):
                    check_namespace_dict(value, full_path)
                else:
                    assert isinstance(value, str), f"{full_path} value should be string or dict, got {type(value)}"

        for top_level, sub_mappings in NAMESPACE_PACKAGES.items():
            assert isinstance(top_level, str), f"{top_level} is not a string"
            assert isinstance(sub_mappings, dict), f"{top_level} sub_mappings is not a dict"
            check_namespace_dict(sub_mappings, top_level)


class TestMappingIntegration:
    """Integration tests for mappings."""

    def test_hardcoded_covers_common_packages(self):
        """Test that common problematic packages are covered."""
        common_modules = [
            "cv2", "PIL", "sklearn", "yaml", "bs4", "jwt", "dateutil",
            "dotenv", "usb", "serial", "wx"
        ]
        for module in common_modules:
            result = get_hardcoded_mapping(module)
            assert result is not None, f"{module} not found in hardcoded mappings"

    def test_namespace_covers_major_cloud_providers(self):
        """Test that major cloud provider namespaces are covered."""
        providers = ["google", "azure"]
        for provider in providers:
            assert is_namespace_package(provider), f"{provider} not recognized as namespace"

    def test_hardcoded_count(self):
        """Test that we have a substantial number of hardcoded mappings."""
        modules = get_all_hardcoded_modules()
        # After v0.2.0 additions, should have at least 80 modules
        assert len(modules) >= 80, f"Only {len(modules)} hardcoded modules, expected >= 80"

    def test_namespace_count(self):
        """Test that we have enough namespace packages."""
        # Count total namespace mappings
        total_mappings = sum(len(subs) for subs in NAMESPACE_PACKAGES.values())
        # After v0.2.0 additions, should have at least 60 mappings
        assert total_mappings >= 60, f"Only {total_mappings} namespace mappings, expected >= 60"


class TestMappingEdgeCases:
    """Test edge cases in mappings."""

    def test_case_sensitivity(self):
        """Test that module names are case-sensitive."""
        # PIL is the correct casing
        result = get_hardcoded_mapping("PIL")
        assert result is not None

        # pil might not be mapped (depending on implementation)
        result_lower = get_hardcoded_mapping("pil")
        # Either None or maps to same thing

    def test_submodule_handling(self):
        """Test that we properly handle submodule queries."""
        # Should handle google.cloud.storage as namespace
        result = resolve_namespace_package("google", ["cloud", "storage"])
        assert "google-cloud-storage" in result

    def test_empty_submodules(self):
        """Test handling empty submodules list."""
        result = resolve_namespace_package("google", [])
        # Should return something for base namespace or empty
        assert isinstance(result, list)

    def test_single_submodule(self):
        """Test single submodule resolution."""
        result = resolve_namespace_package("google", ["auth"])
        assert "google-auth" in result

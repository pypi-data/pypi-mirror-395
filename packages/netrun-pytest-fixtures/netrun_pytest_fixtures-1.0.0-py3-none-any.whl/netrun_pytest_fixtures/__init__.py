"""
Netrun Pytest Fixtures - Unified Test Fixtures Package
Netrun Systems - Service #70 Unified Test Fixtures

A comprehensive pytest fixtures package providing reusable testing utilities
for Netrun Systems services. Eliminates 71% fixture duplication across services.

Installation:
    pip install netrun-pytest-fixtures

Usage:
    Simply install the package - fixtures are automatically registered via pytest plugin.

    # In your test files
    def test_example(event_loop, mock_redis, rsa_key_pair):
        # Fixtures automatically available
        pass

Available Fixture Modules:
    - async_utils: Event loop fixtures (addresses 71% duplication)
    - auth: RSA keys, JWT claims, test users, permissions
    - database: SQLAlchemy async sessions, database testing
    - api_clients: httpx AsyncClient, FastAPI TestClient
    - redis: Mock Redis clients for caching tests
    - environment: Environment variable isolation
    - filesystem: Temporary files, directories, repo structures
    - logging: Logging reset and capture utilities

Version: 1.0.0
Author: Netrun Systems
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Netrun Systems"
__license__ = "MIT"

# Import all fixtures to make them available when package is loaded
# Pytest will auto-discover these when package is installed as plugin

from .async_utils import (
    event_loop,
    new_event_loop,
)

from .auth import (
    rsa_key_pair,
    temp_key_files,
    sample_jwt_claims,
    minimal_claims,
    expired_claims,
    test_user,
    admin_user,
    superadmin_user,
    test_tenant_id,
    mock_request,
    mock_request_with_jwt,
    mock_api_key_request,
    sample_role_hierarchy,
    sample_permission_map,
)

from .database import (
    test_database_url,
    async_engine,
    async_session_factory,
    async_db_session,
    init_test_database,
    mock_db_session,
    transaction_rollback_session,
)

from .api_clients import (
    base_url,
    async_client,
    test_client,
    mock_response,
    mock_async_client,
    auth_headers,
    api_key_headers,
    multipart_headers,
    mock_httpx_transport,
)

from .redis import (
    redis_url,
    mock_redis,
    mock_redis_client,
    mock_redis_pool,
    mock_redis_with_data,
    mock_redis_error,
    cleanup_redis_keys,
)

from .environment import (
    clean_env,
    sample_env_vars,
    mock_env_file,
    temp_env_file,
    reset_environment,
    isolated_env,
    mock_azure_env,
    production_like_env,
)

from .filesystem import (
    temp_directory,
    temp_file,
    temp_json_file,
    temp_yaml_file,
    temp_repo_structure,
    temp_config_file,
    temp_log_file,
    temp_csv_file,
    temp_binary_file,
)

from .logging import (
    reset_logging,
    sample_log_record,
    logger_with_handler,
    capture_logs,
    json_log_formatter,
    silence_loggers,
    log_level_setter,
    mock_log_handler,
    exception_log_record,
)

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__license__",

    # Async utilities
    "event_loop",
    "new_event_loop",

    # Authentication
    "rsa_key_pair",
    "temp_key_files",
    "sample_jwt_claims",
    "minimal_claims",
    "expired_claims",
    "test_user",
    "admin_user",
    "superadmin_user",
    "test_tenant_id",
    "mock_request",
    "mock_request_with_jwt",
    "mock_api_key_request",
    "sample_role_hierarchy",
    "sample_permission_map",

    # Database
    "test_database_url",
    "async_engine",
    "async_session_factory",
    "async_db_session",
    "init_test_database",
    "mock_db_session",
    "transaction_rollback_session",

    # API Clients
    "base_url",
    "async_client",
    "test_client",
    "mock_response",
    "mock_async_client",
    "auth_headers",
    "api_key_headers",
    "multipart_headers",
    "mock_httpx_transport",

    # Redis
    "redis_url",
    "mock_redis",
    "mock_redis_client",
    "mock_redis_pool",
    "mock_redis_with_data",
    "mock_redis_error",
    "cleanup_redis_keys",

    # Environment
    "clean_env",
    "sample_env_vars",
    "mock_env_file",
    "temp_env_file",
    "reset_environment",
    "isolated_env",
    "mock_azure_env",
    "production_like_env",

    # Filesystem
    "temp_directory",
    "temp_file",
    "temp_json_file",
    "temp_yaml_file",
    "temp_repo_structure",
    "temp_config_file",
    "temp_log_file",
    "temp_csv_file",
    "temp_binary_file",

    # Logging
    "reset_logging",
    "sample_log_record",
    "logger_with_handler",
    "capture_logs",
    "json_log_formatter",
    "silence_loggers",
    "log_level_setter",
    "mock_log_handler",
    "exception_log_record",
]


def pytest_configure(config):
    """
    Pytest hook to register markers and configuration.

    Called when pytest loads the plugin.
    """
    config.addinivalue_line(
        "markers",
        "asyncio: mark test as async (pytest-asyncio integration)"
    )
    config.addinivalue_line(
        "markers",
        "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers",
        "e2e: mark test as end-to-end test"
    )

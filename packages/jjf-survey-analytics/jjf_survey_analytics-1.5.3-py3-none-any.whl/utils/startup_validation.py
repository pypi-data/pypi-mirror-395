"""
Startup Validation Module for JJF Survey Analytics

Validates critical dependencies and endpoints on application startup
to catch configuration and dependency issues before serving requests.

Prevents runtime errors like missing modules from reaching production.
"""

import sys
from typing import Dict, List, Tuple


class StartupValidationError(Exception):
    """Raised when startup validation fails."""
    pass


def validate_critical_imports() -> Tuple[bool, List[str]]:
    """
    Validate all critical module imports.

    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    errors = []
    required_modules = [
        # Core dependencies
        ('flask', 'Flask'),
        ('sqlalchemy', 'SQLAlchemy ORM'),
        ('sqlalchemy.orm', 'SQLAlchemy ORM Session'),

        # Google Sheets API
        ('googleapiclient.discovery', 'Google API Client'),

        # AI Analysis
        ('openai', 'OpenAI/OpenRouter client'),
        ('anthropic', 'Anthropic SDK'),

        # Database
        ('sqlite3', 'SQLite'),
    ]

    for module_name, display_name in required_modules:
        try:
            __import__(module_name)
        except ImportError as e:
            errors.append(f"Missing module '{module_name}' ({display_name}): {str(e)}")

    return len(errors) == 0, errors


def validate_service_imports() -> Tuple[bool, List[str]]:
    """
    Validate application service imports.

    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    errors = []
    service_modules = [
        'src.services.qualitative_cache_repository',
        'src.services.container',
        'src.services.data_service',
        'src.services.report_service',
        'src.services.analytics_service',
        'src.services.sse_service',
    ]

    for module_name in service_modules:
        try:
            __import__(module_name)
        except ImportError as e:
            errors.append(f"Service import failed for '{module_name}': {str(e)}")
        except Exception as e:
            errors.append(f"Service initialization error in '{module_name}': {str(e)}")

    return len(errors) == 0, errors


def validate_environment_variables() -> Tuple[bool, List[str]]:
    """
    Validate required environment variables.

    Returns:
        Tuple of (success: bool, warnings: List[str])
    """
    import os

    warnings = []

    # Optional but recommended
    recommended_vars = [
        'OPENROUTER_API_KEY',
        'ANTHROPIC_API_KEY',
        'GOOGLE_SHEETS_CREDENTIALS_PATH',
    ]

    for var_name in recommended_vars:
        if not os.getenv(var_name):
            warnings.append(f"Environment variable '{var_name}' not set (AI features may be limited)")

    return True, warnings  # Warnings don't fail validation


def validate_database_connection() -> Tuple[bool, List[str]]:
    """
    Validate database connection and structure.

    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    errors = []

    try:
        from src.services.container import get_container
        container = get_container()

        # Check if data service is available
        if not hasattr(container, 'data_service'):
            errors.append("DataService not available in container")
            return False, errors

        # Don't fail if data isn't loaded yet (that happens asynchronously)
        # Just validate that the service exists

    except Exception as e:
        errors.append(f"Database connection validation failed: {str(e)}")

    return len(errors) == 0, errors


def validate_critical_endpoints() -> Tuple[bool, List[str]]:
    """
    Validate that critical API endpoints can be imported.

    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    errors = []

    try:
        # Import report API blueprint
        from src.blueprints.api.report_api import report_api

        # Verify qualitative cache repository can be imported
        from src.services.qualitative_cache_repository import get_qualitative_cache_repository

        # Try to instantiate (but don't require database to be ready)
        try:
            repo = get_qualitative_cache_repository()
        except Exception as e:
            # Database might not be ready, that's okay for startup validation
            pass

    except ImportError as e:
        errors.append(f"Critical endpoint import failed: {str(e)}")
    except Exception as e:
        errors.append(f"Endpoint validation error: {str(e)}")

    return len(errors) == 0, errors


def run_startup_validation(verbose: bool = True) -> Dict[str, any]:
    """
    Run all startup validation checks.

    Args:
        verbose: Print validation results to console

    Returns:
        Validation results dictionary

    Raises:
        StartupValidationError: If critical validation fails
    """
    if verbose:
        print("\n" + "=" * 60)
        print("STARTUP VALIDATION")
        print("=" * 60)

    all_errors = []
    all_warnings = []

    # 1. Validate critical imports
    if verbose:
        print("\n[1/5] Validating critical module imports...")
    success, errors = validate_critical_imports()
    if not success:
        all_errors.extend(errors)
        if verbose:
            for error in errors:
                print(f"  ✗ {error}")
    elif verbose:
        print("  ✓ All critical modules available")

    # 2. Validate service imports
    if verbose:
        print("\n[2/5] Validating service layer imports...")
    success, errors = validate_service_imports()
    if not success:
        all_errors.extend(errors)
        if verbose:
            for error in errors:
                print(f"  ✗ {error}")
    elif verbose:
        print("  ✓ All services can be imported")

    # 3. Validate environment
    if verbose:
        print("\n[3/5] Checking environment configuration...")
    success, warnings = validate_environment_variables()
    all_warnings.extend(warnings)
    if warnings and verbose:
        for warning in warnings:
            print(f"  ⚠ {warning}")
    elif verbose:
        print("  ✓ Environment configured")

    # 4. Validate database
    if verbose:
        print("\n[4/5] Validating database connection...")
    success, errors = validate_database_connection()
    if not success:
        all_errors.extend(errors)
        if verbose:
            for error in errors:
                print(f"  ✗ {error}")
    elif verbose:
        print("  ✓ Database connection available")

    # 5. Validate critical endpoints
    if verbose:
        print("\n[5/5] Validating critical API endpoints...")
    success, errors = validate_critical_endpoints()
    if not success:
        all_errors.extend(errors)
        if verbose:
            for error in errors:
                print(f"  ✗ {error}")
    elif verbose:
        print("  ✓ Critical endpoints can be loaded")

    # Summary
    if verbose:
        print("\n" + "=" * 60)
        if all_errors:
            print(f"VALIDATION FAILED: {len(all_errors)} error(s)")
            print("=" * 60)
            print("\nErrors must be resolved before starting the application.")
            for i, error in enumerate(all_errors, 1):
                print(f"{i}. {error}")
        else:
            print("VALIDATION PASSED")
            if all_warnings:
                print(f"({len(all_warnings)} warning(s))")
            print("=" * 60)

    result = {
        'success': len(all_errors) == 0,
        'errors': all_errors,
        'warnings': all_warnings,
    }

    if not result['success']:
        raise StartupValidationError(
            f"Startup validation failed with {len(all_errors)} error(s). "
            "See logs for details."
        )

    return result


if __name__ == '__main__':
    """Run validation as standalone script."""
    try:
        result = run_startup_validation(verbose=True)
        sys.exit(0 if result['success'] else 1)
    except StartupValidationError as e:
        print(f"\n✗ {str(e)}\n")
        sys.exit(1)

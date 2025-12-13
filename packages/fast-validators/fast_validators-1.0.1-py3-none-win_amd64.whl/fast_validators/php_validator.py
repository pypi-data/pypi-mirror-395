import os
from pathlib import Path
from .base_validator import Validator

try:
    from .validator_tree import validate_syntax, Language
    LIBRARY_MISSING_ERROR = ""
except (ImportError, OSError) as e:
    LIBRARY_MISSING_ERROR = (
        "The PHP validator component could not be loaded.\n"
        "Please ensure the library has been built by running.\n"
        f"Details: {e}"
    )


class Php_Validator(Validator):
    name: str = "php"

    def validate(self, source_code: str, file_path: str | Path) -> tuple[bool, str]:
        if LIBRARY_MISSING_ERROR:
            return False, LIBRARY_MISSING_ERROR

        path: str = os.fspath(file_path)
        try:
            return validate_syntax(source_code, Language.PHP, path)
        except Exception as e:
            return False, f"An unexpected error occurred while validating {path}: {str(e)}"

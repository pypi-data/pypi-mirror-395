from enum import IntEnum
from .base_validator import Validator


class Language(IntEnum):
    UNKNOWN = 0
    JSON    = 1
    YAML    = 2
    PYTHON  = 3
    PHP     = 4
    GO      = 5
    JS_TS   = 6
    TOML    = 7
    RUST    = 8
    LAST    = RUST


default_validator = Validator()
language_to_validator: list[Validator] = [default_validator] * (Language.LAST + 1)


def _initialize_validators():
    from .json_validator   import Json_Validator
    from .yaml_validator   import Yaml_Validator
    from .python_validator import Python_Validator
    from .php_validator    import Php_Validator
    from .go_validator     import Go_Validator
    from .js_ts_validator  import Js_Ts_Validator
    from .toml_validator   import Toml_Validator
    from .rust_validator   import Rust_Validator

    language_to_validator[Language.JSON  ] = Json_Validator()
    language_to_validator[Language.YAML  ] = Yaml_Validator()
    language_to_validator[Language.PYTHON] = Python_Validator()
    language_to_validator[Language.PHP   ] = Php_Validator()
    language_to_validator[Language.GO    ] = Go_Validator()
    language_to_validator[Language.JS_TS ] = Js_Ts_Validator()
    language_to_validator[Language.TOML  ] = Toml_Validator()
    language_to_validator[Language.RUST  ] = Rust_Validator()


_initialize_validators()


def get_validator_for_language(language: Language) -> Validator:
    return language_to_validator[language]


def validate_content_by_language(source_code: str, language: Language, file_path: str = "<code>") -> tuple[bool, str]:
    validator = get_validator_for_language(language)
    return validator.validate(source_code, file_path)

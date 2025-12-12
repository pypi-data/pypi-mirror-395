from __future__ import annotations

from typing import Any

from wexample_config.config_value.config_value import ConfigValue
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class FlutterConfigValue(ConfigValue):
    dart_format: bool | None = public_field(
        default=None,
        description="Format and fix Dart/Flutter code using dart format and dart fix",
    )
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )

    def to_option_raw_value(self) -> Any:
        from wexample_filestate_flutter.config_option.dart_format_config_option import (
            DartFormatConfigOption,
        )

        return {
            DartFormatConfigOption.get_name(): self.dart_format,
        }

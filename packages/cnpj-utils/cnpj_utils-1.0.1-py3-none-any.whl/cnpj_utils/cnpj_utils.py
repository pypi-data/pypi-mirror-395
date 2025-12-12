from collections.abc import Callable
from dataclasses import fields

from cnpj_fmt import CnpjFormatter, CnpjFormatterOptions
from cnpj_gen import CnpjGenerator, CnpjGeneratorOptions
from cnpj_val import CnpjValidator


class CnpjUtils:
    """Class to manipulate CNPJ strings."""

    __slots__ = ("formatter", "generator", "validator")

    def __init__(
        self,
        formatter: CnpjFormatterOptions | None = None,
        generator: CnpjGeneratorOptions | None = None,
    ):
        if formatter is None:
            formatter = CnpjFormatterOptions()
        if generator is None:
            generator = CnpjGeneratorOptions()

        formatter_kwargs = {
            field.name: getattr(formatter, field.name)
            for field in fields(CnpjFormatterOptions)
        }
        generator_kwargs = {
            field.name: getattr(generator, field.name)
            for field in fields(CnpjGeneratorOptions)
        }

        self.formatter = CnpjFormatter(**formatter_kwargs)
        self.generator = CnpjGenerator(**generator_kwargs)
        self.validator = CnpjValidator()

    def format(
        self,
        cnpj_string: str,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        slash_key: str | None = None,
        dash_key: str | None = None,
        escape: bool | None = None,
        on_fail: Callable | None = None,
    ) -> str:
        return self.formatter.format(
            cnpj_string,
            hidden,
            hidden_key,
            hidden_start,
            hidden_end,
            dot_key,
            slash_key,
            dash_key,
            escape,
            on_fail,
        )

    def generate(self, format: bool | None = None, prefix: str | None = None) -> str:
        return self.generator.generate(format, prefix)

    def is_valid(self, cnpj_string: str) -> bool:
        return self.validator.is_valid(cnpj_string)

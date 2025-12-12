from cnpj_fmt import (
    CnpjFormatter,
    CnpjFormatterError,
    CnpjFormatterHiddenRangeError,
    CnpjFormatterInvalidLengthError,
    CnpjFormatterOptions,
    cnpj_fmt,
)
from cnpj_gen import (
    CnpjGenerator,
    CnpjGeneratorError,
    CnpjGeneratorInvalidPrefixBranchIdError,
    CnpjGeneratorInvalidPrefixLengthError,
    CnpjGeneratorOptions,
    cnpj_gen,
)
from cnpj_val import CnpjValidator, cnpj_val

from .cnpj_utils import CnpjUtils

__all__ = [
    "CnpjFormatter",
    "CnpjFormatterError",
    "CnpjFormatterHiddenRangeError",
    "CnpjFormatterInvalidLengthError",
    "CnpjFormatterOptions",
    "CnpjGenerator",
    "CnpjGeneratorError",
    "CnpjGeneratorInvalidPrefixBranchIdError",
    "CnpjGeneratorInvalidPrefixLengthError",
    "CnpjGeneratorOptions",
    "CnpjUtils",
    "CnpjValidator",
    "cnpj_fmt",
    "cnpj_gen",
    "cnpj_utils",
    "cnpj_val",
]

__version__ = "1.0.1"

# Default instance of CnpjUtils
cnpj_utils = CnpjUtils()

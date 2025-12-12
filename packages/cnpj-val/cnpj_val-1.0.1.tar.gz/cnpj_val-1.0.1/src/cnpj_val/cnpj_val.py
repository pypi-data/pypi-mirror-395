from .cnpj_validator import CnpjValidator


def cnpj_val(cnpj_string: str) -> bool:
    """Validates a CNPJ string."""
    return CnpjValidator().is_valid(cnpj_string)

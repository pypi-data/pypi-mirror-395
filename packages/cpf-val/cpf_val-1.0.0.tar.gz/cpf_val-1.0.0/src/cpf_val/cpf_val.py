from .cpf_validator import CpfValidator


def cpf_val(cpf_string: str) -> bool:
    """Validates a CPF string."""
    return CpfValidator().is_valid(cpf_string)

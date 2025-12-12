from cpf_cd import CpfCheckDigits

CPF_LENGTH = 11


class CpfValidator:
    """Class to validate a CPF string."""

    def is_valid(self, cpf_string: str) -> bool:
        """Executes the CPF validation, returning a boolean value."""
        cpf_str_digits = "".join(filter(str.isdigit, cpf_string))

        if len(cpf_str_digits) != CPF_LENGTH:
            return False

        if len(set(cpf_str_digits)) == 1:
            return False

        cpf_num_digits = [int(digit) for digit in cpf_str_digits]
        cpf_first_check_digit = cpf_num_digits[-2]
        cpf_second_check_digit = cpf_num_digits[-1]
        cpf_check_digits = CpfCheckDigits(cpf_num_digits)

        return (
            cpf_first_check_digit == cpf_check_digits.first_digit
            and cpf_second_check_digit == cpf_check_digits.second_digit
        )

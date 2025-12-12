from qr_payment_cz.libs.exceptions import ParseException
from qr_payment_cz.libs.iban_calc import IBANCalculator


def test_iban_calc():
    iban_calculator = IBANCalculator("", "4444442", "0800")
    result = iban_calculator.calculate()
    assert result == "CZ88 0800 0000 0000 0444 4442"

    iban_calculator = IBANCalculator("670100", "2211136513", "6210")
    result = iban_calculator.calculate()
    assert result == "CZ78 6210 6701 0022 1113 6513"


def test_account_no_parse():
    result = IBANCalculator.parse_account_number("4444442/0800")
    assert result == ("000000", "0004444442", "0800")

    result = IBANCalculator.parse_account_number("670100-2211136513/6210")
    assert result == ("670100", "2211136513", "6210")


def test_account_no_validate():
    account_no = "4444442/0800"
    account_no_parsed = IBANCalculator.parse_account_number(account_no)
    result = IBANCalculator.validate_account_number(*account_no_parsed)
    assert result is True


def test_account_no_validate_err():
    account_no = "4444444/0800"
    account_no_parsed = IBANCalculator.parse_account_number(account_no)
    try:
        _ = IBANCalculator.validate_account_number(*account_no_parsed)
    except ParseException as _:
        assert True
        return
    assert False

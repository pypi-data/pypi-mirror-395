from qr_payment_cz.libs.exceptions import ParseException
from qr_payment_cz.libs.str_generator import StrGenerator


def test_generate_string_ok():
    generator = StrGenerator(
        "4444442/0800",
        ammount=999,
        message="Platba ČEZu",
        vs="1234567890",
        ks="0987654321",
    )
    result = generator.generate_string()
    assert result == "SPD*1.0*ACC:CZ8808000000000004444442*AM:999.00*CC:CZK*MSG:PLATBA CEZU*X-VS:1234567890*X_KS:0987654321"

    generator = StrGenerator(
        iban="CZ8808000000000004444442",
        ammount=999,
        message="Platba ČEZu",
        vs="1234567890",
        ks="0987654321",
    )
    result = generator.generate_string()
    assert result == "SPD*1.0*ACC:CZ8808000000000004444442*AM:999.00*CC:CZK*MSG:PLATBA CEZU*X-VS:1234567890*X_KS:0987654321"


def test_generate_string_err():
    try:
        _ = StrGenerator(
            "4444444/0800",
            ammount=999,
            message="Platba ČEZu",
            vs="1234567890",
            ks="0987654321",
        )
    except ParseException as _:
        assert True
        return
    assert False

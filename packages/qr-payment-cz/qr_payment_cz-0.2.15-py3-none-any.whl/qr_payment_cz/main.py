from qr_payment_cz.app import App
from qr_payment_cz.libs.exceptions import ParseException
from qr_payment_cz.libs.exceptions import PaymentException
from qr_payment_cz.libs.print import Print


def main():
    app = App()
    try:
        app.run()
    except (ParseException, PaymentException) as ex:
        Print.err(f"Exception occured while processing payment: {ex}")
        exit(1)


if __name__ == "__main__":
    main()

from argparse import ArgumentParser
from argparse import Namespace

import qrcode
from qrcode.image.pil import PilImage

from qr_payment_cz.libs.print import Print
from qr_payment_cz.libs.str_generator import StrGenerator


class App:
    def __init__(self):
        self.app_args: Namespace = self._parse_args()

    @classmethod
    def _parse_args(cls) -> Namespace:
        arg_parser = ArgumentParser()
        arg_parser.description = "QR payment generator for CZE based on https://qr-platba.cz/pro-vyvojare/specifikace-formatu/"
        arg_parser.add_argument(
            "-a",
            "--account",
            type=str,
            dest="account",
            required=False,
            help="Account number std bank account format",
        )
        arg_parser.add_argument(
            "-i",
            "--iban-account",
            type=str,
            dest="iban_acc",
            required=False,
            help="Account number in IBAN format",
        )
        arg_parser.add_argument(
            "-v",
            "--ammount-value",
            type=float,
            dest="ammount",
            required=True,
            help="Payment ammount",
        )
        arg_parser.add_argument(
            "-m",
            "--message",
            type=str,
            dest="message",
            required=False,
            help="Message text for payment",
        )
        arg_parser.add_argument(
            "-rn",
            "--receiver-name",
            type=str,
            dest="rn",
            required=False,
            help="Payment receiver name",
        )
        arg_parser.add_argument(
            "-vs",
            "--variable-symbol",
            type=int,
            dest="vs",
            required=False,
            help="Payment variable symbol",
        )
        arg_parser.add_argument(
            "-ss",
            "--specific-symbol",
            type=int,
            dest="ss",
            required=False,
            help="Payment specific symbol",
        )
        arg_parser.add_argument(
            "-ks",
            "--constant-symbol",
            type=int,
            dest="ks",
            required=False,
            help="Payment contant symbol",
        )
        arg_parser.add_argument(
            "-o",
            "--output-file",
            type=str,
            dest="output_file",
            required=False,
            help="Output PNG image file path",
        )
        arg_parser.add_argument(
            "-d",
            "--display-image",
            action="store_true",
            dest="display_image",
            help="Display generated QR code image",
        )
        arg_parser.add_argument(
            "-s",
            "--silent",
            action="store_true",
            dest="silent",
            help="Silent mode for info messages",
        )
        arg_parser.add_argument(
            "-fs",
            "--force-silent",
            action="store_true",
            dest="force_silent",
            help="Stronger silent mode for all messages",
        )

        args = arg_parser.parse_args()
        if not args.account and not args.iban_acc:
            arg_parser._print_message("Account number or IBAN is required\n")
            arg_parser.print_usage()
            exit(1)

        return args

    def run(self):
        if self.app_args.silent:
            Print.SILENT = True

        if self.app_args.force_silent:
            Print.STRONG_SILENT = True

        generator = StrGenerator(
            account=self.app_args.account,
            iban=self.app_args.iban_acc,
            ammount=self.app_args.ammount,
            message=self.app_args.message,
            rn=self.app_args.rn,
            vs=self.app_args.vs,
            ss=self.app_args.ss,
            ks=self.app_args.ks,
        )
        Print.msg("Preparing QR code ...")
        qr_code_str = generator.generate_string()
        Print.msg(f'QR code string: "{qr_code_str}"')

        if self.app_args.output_file:
            Print.msg(f"Generating QR code image '{self.app_args.output_file}'")
            img: PilImage = qrcode.make(qr_code_str)
            img.save(self.app_args.output_file)

        if self.app_args.display_image:
            Print.msg("Displaying QR code image")
            img: PilImage = qrcode.make(qr_code_str)
            img.show()

        Print.msg("DONE.")

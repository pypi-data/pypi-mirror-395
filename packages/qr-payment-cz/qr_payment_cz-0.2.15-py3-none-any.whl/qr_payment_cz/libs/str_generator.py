import re
import unicodedata
from dataclasses import dataclass

from qr_payment_cz.libs.exceptions import PaymentException
from qr_payment_cz.libs.iban_calc import IBANCalculator


@dataclass
class Payment:
    """
    # SPEC: https://qr-platba.cz/pro-vyvojare/specifikace-formatu/
    """

    ACC: str  # account number in IBAN format
    AM: float  # ammount of money payment
    MSG: str = None  # bank transaction message
    CC: str = "CZK"  # transaction currency
    RN: str = None  # name of transaction recceiver
    DT: str = None  # date of transaction to be done
    X_VS: int = None
    X_SS: int = None
    X_KS: int = None

    @property
    def acc(self):
        acc = self.ACC
        acc = acc.replace(" ", "")
        if acc[:2] != "CZ":
            raise PaymentException(f"Invalid IBAN format '{acc}'. CZ format expected.")
        if len(acc) != 24:
            raise PaymentException(f"Invalid IBAN format '{acc}' length must be 24 characters.")
        return f"*ACC:{acc}"

    @property
    def am(self):
        am = float(self.AM)
        return f"*AM:{am:.2f}"

    @property
    def cc(self):
        return f"*CC:{self.CC}"

    @property
    def rn(self):
        rn = self.RN[:35] if self.RN else ""
        rn_normalized = self._normalize_text(rn)
        return f"*RN:{rn_normalized}" if self.RN else ""

    @property
    def dt(self):
        dt = self.DT
        if self.DT and not re.match(r"^\d{8}$", dt):
            raise PaymentException("Invalid DT format. Use 'YYYYMMDD'")
        return f"*DT:{dt}" if self.DT else ""

    @property
    def msg(self):
        msg = self.MSG[:60] if self.MSG else ""
        msg_normalized = self._normalize_text(msg)

        return f"*MSG:{msg_normalized}" if self.MSG else ""

    @property
    def x_vs(self):
        vs = str(self.X_VS)[-10:]
        return f"*X-VS:{vs}" if self.X_VS else ""

    @property
    def x_ss(self):
        ss = str(self.X_SS)[-10:]
        return f"*X-SS:{ss}" if self.X_SS else ""

    @property
    def x_ks(self):
        ks = str(self.X_KS)[-10:]
        return f"*X_KS:{ks}" if self.X_KS else ""

    @classmethod
    def _normalize_text(cls, text: str) -> str:
        nfkd_form = unicodedata.normalize("NFKD", text)
        text_normalied = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        text_normalied = text_normalied.upper()
        text_normalied = text_normalied.encode("ISO-8859-1", "ignore").decode()
        text_normalied = text_normalied.replace("*", "_")
        return text_normalied


class StrGenerator:
    def __init__(
        self,
        account: str = None,
        iban: str = None,
        ammount: int = 0,
        message: str = None,
        rn: str = None,
        vs: int = None,
        ss: int = None,
        ks: int = None,
    ):
        if account:
            account_std = IBANCalculator.parse_account_number(account)
            IBANCalculator.validate_account_number(*account_std)
            iban = IBANCalculator(*account_std).calculate()

        self.payment = Payment(ACC=iban, AM=ammount, MSG=message)
        self.payment.RN = rn
        self.payment.X_VS = vs
        self.payment.X_SS = ss
        self.payment.X_KS = ks

    def generate_string(self) -> str:
        payment = self.payment
        result = f"SPD*1.0{payment.acc}{payment.am}{payment.cc}{payment.dt}{payment.msg}{payment.rn}{payment.x_vs}{payment.x_ks}{payment.x_ss}"
        return result

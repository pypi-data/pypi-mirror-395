import re

from refdatatypes.safedatatypes import safe_int

from qr_payment_cz.libs.exceptions import ParseException
from qr_payment_cz.libs.print import Print

BANK_IDS = {
    "0100": "Komerční banka, a.s. KOMB CZ",
    "0300": "Československá obchodní banka, a.s. CEKO CZ",
    "0600": "MONETA Money Bank, a.s. AGBA CZ",
    "0710": "Česká národní banka CNBA CZ",
    "0800": "Česká spořitelna, a.s. GIBA CZ",
    "2010": "Fio banka, a.s. FIOB CZ",
    "2020": "MUFG Bank (Europe) N.V. Prague Branch BOTK CZ",
    "2030": "Československé úvěrní družstvo",
    "2060": "Citfin, spořitelní družstvo CITF CZ",
    "2070": "TRINITY BANK a.s. MPUB CZ",
    "2100": "Hypoteční banka, a.s.",
    "2200": "Peněžní dům, spořitelní družstvo",
    "2220": "Artesa, spořitelní družstvo ARTT CZ",
    "2240": "Poštová banka, a.s., pobočka Česká republika POBN CZ",
    "2250": "Banka CREDITAS a.s. CTAS CZ",
    "2260": "NEY spořitelní družstvo",
    "2275": "Podnikatelská družstevní záložna",
    "2600": "Citibank Europe plc, organizační složka CITI CZ",
    "2700": "UniCredit Bank Czech Republic and Slovakia, a.s. BACX CZ",
    "3030": "Air Bank a.s. AIRA CZ",
    "3050": "BNP Paribas Personal Finance SA, odštěpný závod BPPF CZ",
    "3060": "PKO BP S.A., Czech Branch BPKO CZ",
    "3500": "ING Bank N.V. INGB CZ",
    "4000": "Expobank CZ a.s. EXPN CZ",
    "4300": "Českomoravská záruční a rozvojová banka, a.s. CMZR CZ",
    "5500": "Raiffeisenbank a.s. RZBC CZ",
    "5800": "J & T BANKA, a.s. JTBP CZ",
    "6000": "PPF banka a.s. PMBP CZ",
    "6100": "Equa bank a.s. EQBK CZ",
    "6200": "COMMERZBANK Aktiengesellschaft, pobočka Praha COBA CZ",
    "6210": "mBank S.A., organizační složka BREX CZ",
    "6300": "BNP Paribas S.A., pobočka Česká republika GEBA CZ",
    "6700": "Všeobecná úverová banka a.s., pobočka Praha SUBA CZ",
    "6800": "Sberbank CZ, a.s. VBOE CZ",
    "7910": "Deutsche Bank Aktiengesellschaft Filiale Prag, organizační složka DEUT CZ",
    "7940": "Waldviertler Sparkasse Bank AG SPWT CZ",
    "7950": "Raiffeisen stavební spořitelna a.s.",
    "7960": "Českomoravská stavební spořitelna, a.s.",
    "7970": "Wüstenrot - stavební spořitelna a.s.",
    "7980": "Wüstenrot hypoteční banka a.s.",
    "7990": "Modrá pyramida stavební spořitelna, a.s.",
    "8030": "Volksbank Raiffeisenbank Nordoberpfalz eG pobočka Cheb GENO CZ",
    "8040": "Oberbank AG pobočka Česká republika OBKL CZ",
    "8060": "Stavební spořitelna České spořitelny, a.s.",
    "8090": "Česká exportní banka, a.s. CZEE CZ",
    "8150": "HSBC France - pobočka Praha MIDL CZ",
    "8200": "PRIVAT BANK der Raiffeisenlandesbank Oberösterreich Aktiengesellschaft, pobočka Česká republika",
    "8215": "ALTERNATIVE PAYMENT SOLUTIONS, s.r.o.",
    "8220": "Payment Execution s.r.o. PAER CZ",
    "8225": "ORANGETRUST s.r.o. ORRR CZ",
    "8230": "EEPAYS s. r. o. EEPS CZ",
    "8240": "Družstevní záložna Kredit",
    "8250": "Bank of China (Hungary) Close Ltd. Prague branch, odštěpný závod BKCH CZ",
    "8255": "Bank of Communications Co., Ltd., Prague Branch odštěpný závod COMM CZ",
    "8260": "PAYMASTER a.s. PYYM CZ",
    "8265": "Industrial and Commercial Bank of China Limited Prague Branch, odštěpný závod ICBK CZ",
    "8270": "Fairplay Pay s.r.o. FAPO CZ",
    "8280": "B-Efekt a.s. BEFK CZ",
    "8290": "EUROPAY s.r.o. ERSO CZ",
    "8291": "Business Credit s.r.o.",
    "8292": "Money Change s.r.o.",
    "8293": "Mercurius partners s.r.o.",
    "8294": "GrisPayUnion s.r.o.",
    "8295": "NOVARED s.r.o. NVSR CZ",
    "8296": "PaySysEU s.r.o.",
    "8297": "EUPSProvider s.r.o.",
    "8298": "Andraste Capital s.r.o. ANCS CZ",
}


class IBANCalculator:
    def __init__(self, account_prefix: str, account_number: str, bank_id: str) -> None:
        self.account_prefix = f"{safe_int(account_prefix, 0):06d}"
        self.account_number = f"{safe_int(account_number, 0):010d}"
        self.bank_id = f"{safe_int(bank_id, 0):04d}"

    @classmethod
    def parse_account_number(cls, account_number: str) -> (str, str, str):
        r = re.compile(r"^(?P<account_prefix>\d{0,6}-)?(?P<account_no>\d{4,10})/(?P<bank_id>\d{4})$")
        match = r.match(account_number)
        if match:
            match_gr = match.groupdict()
            results = (
                safe_int((match_gr["account_prefix"] or "000000-")[:-1]),
                safe_int(match_gr["account_no"]),
                safe_int(match_gr["bank_id"]),
            )
            if (not results[0] and all(results[1:])) or all(results):
                return f"{results[0]:06d}", f"{results[1]:010d}", f"{results[2]:04d}"
        raise ParseException(f"Invalid account number '{account_number}'")

    @classmethod
    def validate_account_number(cls, account_prefix: str, account_number: str, bank_id: str) -> bool:
        if bank_id not in BANK_IDS:
            raise ParseException(f"Invalid bank ID '{bank_id}'")
        Print.msg(f"Bank {bank_id} => '{BANK_IDS[bank_id]}' detected.")

        account_no_2p = f"{account_prefix}{account_number}"
        if len(account_no_2p) != 16:
            raise ParseException(f"Invalid part of account number '{account_prefix}{account_number}' must be 16 characters long")

        # validate
        sum_weight = 0
        for item_index, item_value in enumerate(account_no_2p):
            item_value = int(item_value)
            item_pow = 15 - item_index
            item_weight = 2**item_pow % 11
            sum_weight += item_weight * item_value

        if sum_weight % 11 != 0:
            raise ParseException("Invalid account number '{account_number}'. Validation by MOD 11 failed.")

        return True

    def calculate(self) -> str:
        """ """
        bk = self.bank_id
        cu = self.account_prefix
        ac = self.account_number
        di = self._calc(f"{bk}{cu}{ac}123500")
        di = 98 - di
        if di < 10:
            di = f"0{di}"
        ib = f"CZ{di}{bk}{cu}{ac}"
        ib = f"{ib[0:4]} {ib[4:8]} {ib[8:12]} {ib[12:16]} {ib[16:20]} {ib[20:]}"
        return ib

    @classmethod
    def _calc(cls, buf: str) -> int:
        index = 0
        pz = -1
        while index <= len(buf):
            if pz < 0:
                dividend = buf[index : index + 9]
                index += 9
            elif 0 <= pz <= 9:
                dividend = str(pz) + buf[index : index + 8]
                index += 8
            else:
                dividend = str(pz) + buf[index : index + 7]
                index += 7
            pz = int(dividend) % 97
        return pz

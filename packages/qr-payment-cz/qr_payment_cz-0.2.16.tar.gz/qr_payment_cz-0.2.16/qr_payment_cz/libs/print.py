from al78tools.cli import cli_colors


class Print:
    SILENT = False
    STRONG_SILENT = False

    @classmethod
    def _print(cls, cli_message: str) -> None:
        print(cli_message)

    @classmethod
    def msg(cls, message: str) -> None:
        if cls.SILENT or cls.STRONG_SILENT:
            return
        cls._print(f"{cli_colors.CMD.bold}[info ]{cli_colors.CMD.reset} {message}")

    @classmethod
    def err(cls, message: str) -> None:
        if cls.STRONG_SILENT:
            return
        cls._print(f"{cli_colors.FG.red}[error]{cli_colors.CMD.reset} {message}")

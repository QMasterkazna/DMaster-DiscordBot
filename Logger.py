from datetime import datetime
import colorama

class Logger():
    def warn(self, text, section):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")

        print(f"{colorama.Fore.YELLOW}[{time}][{section} - WARN] {text}{colorama.Style.RESET_ALL}")

    def error(self, text, section):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")

        print(f"{colorama.Fore.RED}[{time}][{section} - ERROR] {text}{colorama.Style.RESET_ALL}")

    def log(self, text, section):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")

        print(f"{colorama.Fore.GREEN}[{time}][{section} - LOG] {text}{colorama.Style.RESET_ALL}")

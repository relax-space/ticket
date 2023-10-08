import wmi
from hashlib import md5
from datetime import date, timedelta
import os
import sys

try:
    from relax.util import str_to_int, fill_zero_2
except:
    pass


class SecretWin:
    def __init__(self):
        self.w = wmi.WMI()
        self.DAY = "WEBQMRBUFYYBFIXTDPUQWGPKAPQKNHGABDZBOWKGCEUIORLZNJZGLM"
        pass

    def _get_cpu(self) -> str:
        try:
            return self.w.Win32_processor()[0].ProcessorId.strip()
        except Exception as e:
            return str(e)

    def _get_disk(self) -> str:
        for disk in self.w.Win32_DiskDrive():
            return disk.SerialNumber

    def _get_code(self) -> str:
        code = f"relax{self._get_cpu()}{self._get_disk()}"
        return md5(code.encode()).hexdigest().upper()

    def _get_pwd(self, code, year: int, month: int, day: int) -> str:
        month_2 = fill_zero_2(month)
        day_2 = fill_zero_2(day)

        pwd = f"relax{code}{year}{month_2}{day_2}"
        pwd = md5(pwd.encode()).hexdigest().upper()

        day_str = self.DAY[day : day + 6]
        pwd = f"{year}{month_2}{day_str}{pwd[0:20]}"
        return pwd

    def _get_pwd_day(self, code, days: int) -> str:
        day_add = days
        current_date = date.today() + timedelta(days=day_add)
        return self._get_pwd(
            code, current_date.year, current_date.month, current_date.day
        )

    def _check_pwd(self, code, pwd):
        if code != self._get_code():
            return False, None
        if len(pwd) != 32:
            return False, None

        year = str_to_int(pwd[0:4])
        if year == 0:
            return False, None
        month = str_to_int(pwd[4:6])
        if month == 0:
            return False, None
        day_str = pwd[6:12]
        day = self.DAY.find(day_str)
        if day == -1:
            return False, None

        act_pwd = self._get_pwd(code, year, month, day)
        if act_pwd != pwd:
            return False, None

        act_date = date(year, month, day)
        now = date.today()
        if act_date < now:
            return False, None
        return True, act_date.strftime("%Y-%m-%d")


if __name__ == "__main__":
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, p)
    os.chdir(p)
    from relax.util import str_to_int, fill_zero_2

    sw = SecretWin()
    code = sw._get_code()
    # 202401EBQMRB03EFC9FAFA2C416C25DF
    pwd = sw._get_pwd_day(code, 90)

    result, expired = sw._check_pwd(code, pwd)

    print(code, pwd, result, expired)

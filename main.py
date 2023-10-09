from relax.util import get_companys, get_header, get_settings
from asyncio import get_event_loop
from os import path as os_path, chdir
from sys import path as sys_path
from relax.main_win import init


def main(headers, settings, companys):
    init(headers, settings, companys)
    pass


if __name__ == "__main__":
    p = os_path.dirname(os_path.abspath(__file__))
    sys_path.insert(0, p)
    chdir(p)
    headers = get_header()
    settings = get_settings()
    companys = get_companys()
    main(headers, settings, companys)
    pass

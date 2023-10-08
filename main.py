from relax.util import get_header, get_settings
import asyncio
import os
import sys
from relax.main_win import init


async def main(headers, settings):
    init(headers, settings)
    pass


if __name__ == "__main__":
    p = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, p)
    os.chdir(p)
    headers = get_header()
    settings = get_settings()
    asyncio.get_event_loop().run_until_complete(main(headers, settings))
    pass

from hashlib import md5
from datetime import date, datetime
from os import path

try:
    from relax.util import check_file_date
except:
    from util import check_file_date


def get_m():
    current = int(datetime.now().strftime("%d"))
    d1 = f"relax{current}"
    d2 = f"relax{current+100}"
    d3 = f"relax{current+200}"
    m1 = md5(d1.encode()).hexdigest().upper()
    m2 = md5(d2.encode()).hexdigest().upper()
    m3 = md5(d3.encode()).hexdigest().upper()
    return m1, m2, m3


def valid_count():
    if not path.exists("base_data/a"):
        return False
    with open("base_data/a", mode="r", encoding="utf8") as f:
        raw = f.read()
    m = get_m()
    m_last = m[-1]
    m = m[:-1]
    if m_last == raw:
        return False
    if not m.__contains__(raw):
        return False
    return True


def init_count():
    m1, m2, m3 = get_m()
    file_name = "base_data/a"
    with open(file_name, mode="r", encoding="utf8") as f:
        raw = f.read()
    new_value = ""
    if raw in (m1, m2, m3):
        return
    else:
        if not check_file_date(file_name):
            return
        new_value = m1
    with open(file_name, mode="w", encoding="utf8") as f:
        f.write(new_value)


def add_count():
    m1, m2, m3 = get_m()
    file_name = "base_data/a"
    with open(file_name, mode="r", encoding="utf8") as f:
        raw = f.read()
    new_value = ""
    if raw == m1:
        new_value = m2
    elif raw == m2:
        new_value = m3
    elif raw == m3:
        return
    else:
        if not check_file_date(file_name):
            return
        new_value = m1
    with open(file_name, mode="w", encoding="utf8") as f:
        f.write(new_value)

    pass


if __name__ == "__main__":
    print(get_m())
    pass

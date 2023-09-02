import os
import sys
import win32api
import win32con
import win32print
import time


def multi_print(dir):
    list = os.listdir(dir)
    for i in list:
        file_name = os.path.join(dir, i)
        # '/d:"%s"' % win32print.GetDefaultPrinter()
        win32api.ShellExecute(0, 'print', file_name, None, '.', 0)
        time.sleep(1)


def print_prod(dir):
    # 注：先手动设置 默认打印机的首选项
    # multi_print(os.path.join(dir, 'A4'))
    multi_print(os.path.join(dir, 'A5'))


def set_A5(handle):
    property = win32print.GetPrinter(handle, 2)
    pDevMode = property['pDevMode']
    pDevMode.PaperSize = win32con.DMPAPER_A5
    pDevMode.Orientation = win32con.DMORIENT_LANDSCAPE
    property['pDevMode'] = pDevMode
    win32print.SetPrinter(handle, 2, property, 0)
    time.sleep(5)


def set_A4(handle):
    property = win32print.GetPrinter(handle, 2)
    pDevMode = property['pDevMode']
    pDevMode.PaperSize = win32con.DMPAPER_A4
    pDevMode.Orientation = win32con.DMORIENT_PORTRAIT
    property['pDevMode'] = pDevMode
    win32print.SetPrinter(handle, 2, property, 0)
    # 等待本地电脑设置生效
    time.sleep(5)


def print_prod_2(dir):
    printer_name = win32print.GetDefaultPrinter()
    print_access = {'DesiredAccess': win32print.PRINTER_ALL_ACCESS}
    handle = win32print.OpenPrinter(printer_name, print_access)
    set_A5(handle)
    multi_print(os.path.join(dir, 'A5'))
    win32print.ClosePrinter(handle)

    time.sleep(60)

    handle = win32print.OpenPrinter(printer_name, print_access)
    set_A4(handle)
    multi_print(os.path.join(dir, 'A4'))
    win32print.ClosePrinter(handle)

    pass


if __name__ == '__main__':
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, p)
    os.chdir(p)
    from relax.util import get_settings

    settings = get_settings()

    print_folder = os.path.join(
        settings['folder_name'],
        settings['print_folder_name'],
    )
    if not os.path.isdir(print_folder):
        raise Exception('请先准备好打印内容')
    print_prod_2(print_folder)
    pass

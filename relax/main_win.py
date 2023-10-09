from asyncio import get_event_loop
from datetime import date
from os import path as os_path, chdir
from sys import path as sys_path
from tkinter import (
    END,
    BooleanVar,
    Button,
    Checkbutton,
    Entry,
    Frame,
    Label,
    StringVar,
    Tk,
    Menu,
    Toplevel,
    filedialog,
    messagebox,
    font,
    Radiobutton,
)
from tkcalendar import DateEntry
from datetime import date


try:
    from relax.util import (
        check_file_date,
        get_current_date,
        get_companys,
        get_cover_1,
        get_cover_1_bydate,
        get_cover_2,
        fill_zero_2,
        get_header,
        get_settings,
    )
    from relax.main_ import main_async
    from relax.count_ import valid_count, init_count
    from relax.secret_win import SecretWin
except:
    from util import (
        check_file_date,
        get_current_date,
        get_companys,
        get_cover_1,
        get_cover_1_bydate,
        get_cover_2,
        fill_zero_2,
        get_header,
        get_settings,
    )
    from main_ import main_async
    from count_ import valid_count, init_count
    from secret_win import SecretWin
finally:
    pass


def center_window(root: Tk, w, h):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = int((ws / 2) - (w / 2))
    y = int((hs / 2) - (h / 2))
    root.geometry(f"{w}x{h}+{x}+{y}")


def show_toplevel():
    def save_pwd():
        code = code_var.get()
        pwd = pwd_var.get()
        if (not pwd) or not pwd.strip():
            error_msg.set("激活码不能为空！")
            return
        is_enable, expired = _secret_obj._check_pwd(code, pwd)
        if not is_enable:
            error_msg.set("激活码无效或已过期！")
            return
        with open("base_data/pwd", mode="w", encoding="utf8") as f:
            f.write(pwd)
        _active_obj.update({"pwd": pwd, "is_enable": is_enable, "expired": expired})
        pass

    code_var = StringVar()
    pwd_var = StringVar()
    active_msg = StringVar()
    error_msg = StringVar()

    code_var.set(_active_obj.get("code"))
    pwd_var.set(_active_obj.get("pwd"))

    popup = Toplevel(root)
    popup.grab_set()
    popup.title("激活")
    popup.resizable(False, False)
    center_window(popup, 360, 160)

    lbl_0 = Label(popup, textvariable=active_msg)
    lbl_1 = Label(popup, text="机器码：")
    lbl_2 = Label(popup, text="激活码：")
    ety_code = Entry(popup, textvariable=code_var, width=40, state="readonly")
    ety_pwd = Entry(popup, textvariable=pwd_var, width=40)
    lbl_msg = Label(popup, textvariable=error_msg, fg="red")
    btn_confirm = Button(popup, text="激活", command=save_pwd)
    btn_cancel = Button(popup, text="取消", command=popup.destroy)

    lbl_0.grid(row=0, column=1, columnspan=2, sticky="W", pady=(10, 0))

    lbl_1.grid(row=1, column=0, sticky="E", padx=(10, 0), pady=(3, 0))
    ety_code.grid(row=1, column=1, columnspan=2, padx=(3, 10), pady=(10, 0))
    lbl_2.grid(row=2, column=0, sticky="E", padx=(10, 0), pady=(10, 0))
    ety_pwd.grid(row=2, column=1, columnspan=2, padx=(3, 10), pady=(3, 0))

    lbl_msg.grid(row=3, column=1, columnspan=2, sticky="W")

    btn_confirm.grid(row=4, column=1, ipadx=10, ipady=3, sticky="E", padx=(10, 40))
    btn_cancel.grid(row=4, column=2, ipadx=10, ipady=3, sticky="W")

    if _active_obj["is_enable"]:
        lbl_0.config(fg="green")
        active_msg.set(f"已激活，有效期至：{_active_obj['expired']}")
    else:
        lbl_0.config(fg="red")
        active_msg.set(f"未激活或者已过期")

    ety_pwd.focus_set()


def active():
    show_toplevel()
    pass


def load_view():
    pass


async def save_click():
    headers = get_header()
    headers.update({"Cookie": _cookie_var.get()})
    settings = get_settings()
    sdate = _date_var.get()
    current_company = {
        "company": {"name": _company_var.get(), "output_path": _output_var.get()},
        "stamp": {
            "path": _stamp_path_var.get(),
            "page_height": 750,
            "enable": _is_img_var.get(),
        },
    }

    is_download = _is_download_var.get()
    is_valid = valid_count()
    if is_download and (not is_valid):
        messagebox.showwarning("警告", "已达到最大下载次数，每日可下载2次。")
        return
    res = await main_async(headers, current_company, settings, sdate, is_download)
    if res:
        messagebox.showwarning("警告", res)
        return
    messagebox.showinfo("提示", "执行成功！")
    pass


def on_button_click():
    count = _count_event.get()
    if not count:
        return

    _count_event.set(False)
    # 创建一个事件循环并运行异步函数
    loop = get_event_loop()
    loop.run_until_complete(save_click())
    # loop.close()


def top_frame(headers, settings, companys):
    global _count_event
    _count_event = BooleanVar(value=True)
    global _company_var, _is_download_var, _date_var, _cookie_var, _cover_var_1, _cover_var_2, _output_var, _is_img_var, _stamp_path_var, _page_weight_var
    _company_var = StringVar()
    _is_download_var = BooleanVar()
    _date_var = StringVar()
    _cookie_var = StringVar()
    _cover_var_1 = StringVar()
    _cover_var_2 = StringVar()
    _output_var = StringVar()
    _is_img_var = BooleanVar()
    _stamp_path_var = StringVar()
    _page_weight_var = StringVar()

    fr1 = Frame(root)
    fr1.pack(fill="x")
    lbl_company = Label(fr1, text="请选择公司")

    def select():
        # 0 食安， 1：农惠民
        company_index = _company_var.get()
        company = companys[company_index]["company"]
        _cover_var_2.set(get_cover_2(company["name"]))
        _output_var.set(company["output_path"])
        stamp = companys[company_index]["stamp"]

        _is_img_var.set(stamp["enable"])
        _stamp_path_var.set(stamp["path"])
        pass

    rdo_1 = Radiobutton(
        fr1, text="食安", value="0", variable=_company_var, command=select
    )
    rdo_2 = Radiobutton(
        fr1, text="通用", value="1", variable=_company_var, command=select
    )

    chk_download = Checkbutton(fr1, text="是否下载", variable=_is_download_var)

    lbl_date = Label(fr1, text="下载日期：")
    ety_date = DateEntry(
        fr1,
        textvariable=_date_var,
        width=12,
        background="darkblue",
        foreground="white",
        borderwidth=2,
        date_pattern="y-mm-dd",
    )

    def on_date_select(e):
        sdate = _date_var.get()
        cover_1 = get_cover_1_bydate(sdate)
        _cover_var_1.set(cover_1)
        pass

    ety_date.bind("<<DateEntrySelected>>", on_date_select)
    lbl_cookie = Label(fr1, text="Cookie")
    ety_cookie = Entry(fr1, textvariable=_cookie_var, width=60)

    def clear():
        _cookie_var.set("")
        ety_cookie.delete(0, END)
        pass

    btn_cookie = Button(fr1, text="清空", command=clear)

    lbl_cover_1 = Label(fr1, text="封面标题1：")
    ety_cover_1 = Entry(fr1, textvariable=_cover_var_1, width=60)
    lbl_cover_2 = Label(fr1, text="封面标题2：")
    ety_cover_2 = Entry(fr1, textvariable=_cover_var_2, width=60)
    lbl_path = Label(fr1, text="输出路径：")
    ety_path = Entry(fr1, textvariable=_output_var, width=60)

    def output_click():
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        ety_path.delete(0, END)
        ety_path.insert(0, file_path)

    btn_path = Button(fr1, text="选择", command=output_click)

    chk_img = Checkbutton(fr1, text="是否盖章", variable=_is_img_var)
    lbl_stamp = Label(fr1, text="图章路径：")
    ety_stamp = Entry(fr1, textvariable=_stamp_path_var, width=60)

    def stamp_click():
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        ety_stamp.delete(0, END)
        ety_stamp.insert(0, file_path)

    btn_stamp = Button(fr1, text="选择", command=stamp_click)

    lbl_page_weight = Label(fr1, text="页面高度：")
    ety_page_weight = Entry(fr1, textvariable=_page_weight_var, width=60)

    btn_save = Button(
        fr1,
        text="生成",
        command=on_button_click,
        width=20,
    )

    row_index = 0
    lbl_company.grid(row=row_index, column=0, padx=(10, 0), pady=(10, 0), sticky="E")
    rdo_1.grid(row=row_index, column=1, padx=(0, 0), pady=(10, 0), sticky="W")
    rdo_2.grid(row=row_index, column=2, padx=(0, 0), pady=(10, 0), sticky="W")
    row_index += 1

    chk_download.grid(row=row_index, column=0, padx=(10, 0), pady=(4, 0), sticky="E")
    row_index += 1

    lbl_date.grid(row=row_index, column=0, padx=(10, 0), pady=(4, 0), sticky="E")
    ety_date.grid(
        row=row_index, column=1, columnspan=2, padx=(0, 0), pady=(4, 0), sticky="W"
    )
    row_index += 1
    lbl_cookie.grid(row=row_index, column=0, padx=(10, 0), pady=(4, 0), sticky="E")
    ety_cookie.grid(
        row=row_index, column=1, columnspan=2, padx=(0, 0), pady=(4, 0), sticky="W"
    )
    btn_cookie.grid(row=row_index, column=3, padx=(2, 0), pady=(3, 0))

    row_index += 1
    lbl_cover_1.grid(row=row_index, column=0, padx=(10, 0), pady=(4, 0), sticky="E")
    ety_cover_1.grid(
        row=row_index,
        column=1,
        columnspan=2,
        padx=(0, 0),
        pady=(4, 0),
        sticky="W",
    )
    row_index += 1
    lbl_cover_2.grid(row=row_index, column=0, padx=(10, 0), pady=(4, 0), sticky="E")
    ety_cover_2.grid(
        row=row_index, column=1, columnspan=2, padx=(0, 0), pady=(4, 0), sticky="W"
    )
    row_index += 1
    lbl_path.grid(row=row_index, column=0, padx=(10, 0), pady=(3, 0), sticky="E")
    ety_path.grid(
        row=row_index, column=1, columnspan=2, padx=(0, 0), pady=(3, 0), sticky="W"
    )
    btn_path.grid(row=row_index, column=3, padx=(2, 0), pady=(3, 0))

    row_index += 1
    chk_img.grid(row=row_index, column=0, padx=(10, 0), pady=(3, 0), sticky="E")

    row_index += 1
    lbl_stamp.grid(row=row_index, column=0, padx=(10, 0), pady=(3, 0), sticky="E")
    ety_stamp.grid(
        row=row_index, column=1, columnspan=2, padx=(0, 0), pady=(3, 0), sticky="W"
    )
    btn_stamp.grid(row=row_index, column=3, padx=(2, 0), pady=(3, 0))

    # row_index += 1
    # lbl_page_weight.grid(row=row_index, column=0, padx=(10, 0), pady=(4, 0), sticky="E")
    # ety_page_weight.grid(
    #     row=row_index, column=1, columnspan=2, padx=(0, 0), pady=(4, 0), sticky="W"
    # )

    row_index += 1
    btn_save.grid(
        row=row_index, column=1, ipadx=10, ipady=10, padx=10, pady=10, sticky="W"
    )

    # init value
    company_index = "0"
    current_company = companys[company_index]
    _company_var.set(company_index)

    _is_download_var.set(True)
    d1 = date.today()
    year = d1.year
    month = d1.month
    day = 3
    _date_var.set(f"{year}-{fill_zero_2(month)}-{fill_zero_2(day)}")
    _cookie_var.set("")

    _cover_var_1.set(get_cover_1(year, month))
    _cover_var_2.set(get_cover_2(current_company["company"]["name"]))
    _output_var.set(current_company["company"]["output_path"])
    _is_img_var.set(current_company["stamp"]["enable"])
    _stamp_path_var.set(current_company["stamp"]["path"])
    # _page_weight_var.set(current_company["stamp"]["page_height"])

    pass


def init_view(headers, settings, companys):
    global root
    root = Tk()
    center_window(root, 600, 400)
    root.title("对账单")

    if not _date_valid:
        lbl_msg = Label(
            root, text="产品不可用，请先将电脑时间设置正确！", fg="red", font=font.Font(size=20)
        )
        lbl_msg.pack(pady=20)
        root.mainloop()
        return

    menubar = Menu(root)
    activer = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="文件", menu=activer)
    activer.add_command(label="激活", command=active)
    root.config(menu=menubar)

    top_frame(headers, settings, companys)

    root.mainloop()


def init_active(code):
    file_name = "base_data/pwd"
    if not os_path.exists(file_name):
        return None, False, None

    with open(file_name, mode="r", encoding="utf8") as f:
        pwd = f.read()
    is_enable, expired = _secret_obj._check_pwd(code, pwd)
    return pwd, is_enable, expired


def init_key():
    global _secret_obj, _active_obj
    _active_obj = {
        "code": "",
        "pwd": "",
        "is_enable": False,
        "expired": "",
    }
    _secret_obj = SecretWin()
    code = _secret_obj._get_code()
    pwd, is_enable, expired = None, False, None
    if not _date_valid:
        return
    pwd, is_enable, expired = init_active(code)
    _active_obj.update(
        {"code": code, "pwd": pwd, "is_enable": is_enable, "expired": expired}
    )

    pass


def check_date():
    global _date_valid
    _date_valid = False
    network_d = get_current_date()
    local_d = date.today()
    if network_d != local_d:
        return False
    file_name = "base_data/pwd"
    if check_file_date(file_name) < 0:
        return False
    _date_valid = True
    return True


def init(headers, settings, companys):
    global _setting_data
    _setting_data = settings
    check_date()
    init_key()
    init_view(headers, settings, companys)
    init_count()
    pass


if __name__ == "__main__":
    p = os_path.dirname(os_path.dirname(os_path.abspath(__file__)))
    sys_path.insert(0, p)
    chdir(p)

    headers = get_header()
    settings = get_settings()
    companys = get_companys()
    init(headers, settings, companys)

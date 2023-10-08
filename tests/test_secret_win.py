from relax.secret_win import SecretWin


# py.test.exe -vs .\tests\test_secret_win.py::test_1
def test_1():
    sw = SecretWin()
    code = sw._get_code()
    # 202401EBQMRB03EFC9FAFA2C416C25DF
    print(sw._get_pwd_day(code, 90))
    assert sw._check_pwd(code, sw._get_pwd_day(code, -1))[0] == False, "error -1"
    assert sw._check_pwd(code, sw._get_pwd_day(code, 0))[0] == True, "error 0"
    assert sw._check_pwd(code, sw._get_pwd_day(code, 1))[0] == True, "error 0"

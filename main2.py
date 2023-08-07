import time
from selenium import webdriver

# browser exposes an executable file
# Through Selenium test we will invoke the executable file which will then #invoke actual browser

options = webdriver.IeOptions()
# options.attach_to_edge_chrome = True
# options.edge_executable_path = r"D:\file\browerdriver\IEDriverServer.exe"
driver = webdriver.Ie(options=options)

options = webdriver.IeOptions()
driver = webdriver.Ie(options=options)

# driver = webdriver.Ie(
#     options={"binary_location": r"D:\file\browerdriver\IEDriverServer.exe"}
# )
# to maximize the browser window1
driver.maximize_window()
# get method to launch the URL
driver.get(
    "https://loginaep.mall.icbc.com.cn/login/web/login?appId=hi&loginChannel=2&service=https%3A%2F%2Fsp.trade.icbc.com.cn%2Fj_spring_cas_security_check"
)
# to refresh the browser
driver.refresh()
# to close the browser
time.sleep(100)
driver.close()

import asyncio
import os

from pyppeteer import launch


async def login():
    host = 'https://baidu.com'
    chromium_drive = r"D:\file\browerdriver\IEDriverServer.exe"
    username = "15811016818"
    password = "xxm87375664"
    # 'headless': False：打开浏览器，True：隐藏浏览器
    browser = await launch(
        {
            'headless': False,
            'executablePath': chromium_drive,
            'args': ['--no-sandbox', '--disable-gpu'],
            'dumpio': True,
        }
    )
    context = await browser.createIncognitoBrowserContext()  # 开启无痕浏览器模式
    page = await context.newPage()

    await asyncio.gather(
        page.goto(f"{host}"),
        page.waitForNavigation(),
    )
    await page.click('#s-top-loginbtn')
    await page.waitFor(1000)

    await page.click('#TANGRAM__PSP_11__footerULoginBtn')
    await page.waitFor(1000)

    element = await page.J('#TANGRAM__PSP_11__userName')
    await element.click({'clickCount': 3})
    await page.type('#TANGRAM__PSP_11__userName', username)
    await page.waitFor(1000)

    element = await page.J('#TANGRAM__PSP_11__password')
    await element.click({'clickCount': 3})
    await page.type('#TANGRAM__PSP_11__password', password)
    await page.waitFor(1000)

    await page.click('#TANGRAM__PSP_11__submit')

    await page.waitFor(10000)


if __name__ == '__main__':
    task = asyncio.get_event_loop().run_until_complete(login())
    print(task)

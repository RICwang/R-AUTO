import os
import time
from DrissionPage import Chromium, ChromiumOptions

class AutoV2ex:
    def __init__(self, username=None, password=None, port=None, logger=None):
        self.res = False
        self.autoname = "v2ex"
        self.nickname = "[未登录]"
        self.logger = logger
        self.config = {"username": username, "password": password}
        self.rootpath = os.path.dirname(os.path.dirname(__file__))

        # 创建页面对象
        configFilepath = os.path.join(
            self.rootpath, 'volume', 'config', 'dp_configs.ini')
        co = ChromiumOptions(ini_path=configFilepath)
        co.set_local_port(port=port)
        co.set_user_data_path(os.path.join(
            self.rootpath, 'volume', 'user_data', self.autoname, username))
        co.mute(on_off=True)
        # 以该配置创建页面对象
        self.chromium = Chromium(addr_or_opts=co)

        self.logger.info('初始化成功')

    def __del__(self):
        self.chromium.quit(force=True)

    # 签到
    def signIn(self):
        self.logger.info(f'校验{self.autoname}签到状态...')
        signInPage = self.chromium.new_tab(url='https://www.v2ex.com/mission/daily')
        buttonEle = signInPage.ele('#Main').ele('tag:input@type=button')
        
        if buttonEle and '领取' in buttonEle.value:
            buttonEle.click()
            signInPage.wait(2)
            self.logger.info('签到成功')
        self.res = True

    # 登录
    def login(self):
        self.logger.info(f'校验{self.autoname}登录状态...')
        loginPage = self.chromium.new_tab(url='https://www.v2ex.com')
        # 等待页面加载
        loginPage.wait(2)
        topEles = loginPage.ele('tag:div@class=tools').eles('tag:a')

        # 已登录
        if topEles[-1].text == '登出':
            self.nickname = topEles[1].text
            self.logger.info(f'【{self.nickname}】已登录')
            self.chromium.close_tabs(loginPage)
            return

        # 未登录
        self.logger.info('未登录')
        self.logger.info('登录中...')
        topEles[-1].click(by_js=None)

        loginPage = self.chromium.latest_tab

        # 输入账号密码
        self.logger.info(
            f'账号：{self.config["username"]}，密码：{self.config["password"]}')
        
        loginFalseString = ''
        while True:
            # 等待页面加载
            loginPage.wait(1)
            if loginFalseString:
                self.logger.info(loginFalseString)
            # 输入账号密码
            inputEles = loginPage.eles('tag:input@class=sl')
            inputEles[0].input(vals=self.config['username'],
                               clear=True, by_js=True)
            inputEles[1].input(vals=self.config['password'],
                               clear=True, by_js=True)
            # 获取验证码
            vcEle = loginPage.ele('#captcha-image')
            tmpFolder = os.path.join(self.rootpath, 'static', 'tmp')
            vcFilepath = os.path.join(tmpFolder, time.strftime("%Y%m%d", time.localtime()))
            filename = f'vcLogin-{self.autoname}.png'
            vcAllFilepath = vcEle.save(path=vcFilepath, name=filename)
            vcStringPath = os.path.splitext(vcAllFilepath)[0]
            vcFilepathRelative = vcAllFilepath.replace(tmpFolder+"/", '')
            vc = ""
            while True:
                time.sleep(2)
                self.logger.info(f'请打开http://127.0.0.1:5000/update-vc/{vcFilepathRelative}，输入验证码...')
                if os.path.exists(vcStringPath):
                    with open(vcStringPath, 'r') as f:
                        vc = f.read()
                    if vc:
                        break

            # 输入验证码
            inputEles[2].input(vals=vc, clear=True, by_js=True)
            # 点击登录
            loginPage.ele('tag:input@class=super normal button').click()
            loginPage.wait(5)

            loginPage = self.chromium.latest_tab
            problemEle = loginPage.ele('tag:div@class=problem')
            # 登录成功
            if not problemEle:
                self.logger.info('登录成功')
                break
            # 登录失败
            loginFalseString = problemEle.text

        self.chromium.close_tabs(loginPage)
        return

    def main(self):
        self.logger.info('===============================================')
        # 登录
        self.login()
        self.logger.info('===============================================')

        # 签到
        self.signIn()
        self.logger.info('===============================================')
        

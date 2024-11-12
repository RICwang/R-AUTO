import os
from DrissionPage import Chromium, ChromiumOptions

class AutoMicrosoft:
    def __init__(self, username=None, password=None, port=None, logger=None):
        self.res = False
        self.autoname = "Microsoft"
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
        loginPage = self.chromium.new_tab(url='https://www.bing.com')
        loginPage.wait(5)
        loginPage.wait.ele_displayed('tag:span@class=points-container')
        loginPage.ele('tag:span@class=points-container').click()
        loginPage.wait(2)
        loginPage.wait.ele_displayed('tag:div@class=flyout_control_threeOffers')
        promoEles = loginPage.ele('tag:div@class=flyout_control_threeOffers').eles('tag:div@class=promo_cont')
        for promoEle in promoEles:
            aEle = promoEle.ele('tag:a')
            if not aEle:
                continue
            self.chromium.new_tab(url=aEle.attr('href'), background=True)

        loginPage.wait(2)
        
        self.res = True

    # 登录
    def login(self):
        self.logger.info(f'校验{self.autoname}登录状态...')
        loginPage = self.chromium.new_tab(url='https://www.bing.com')
        loginPage.wait.ele_displayed('tag:span@id=id_n')
        nicknameEle = loginPage.ele('tag:span@id=id_n')

        # 已登录
        if nicknameEle and nicknameEle.text != '':
            self.nickname = nicknameEle.text
            self.logger.info(f'【{self.nickname}】已登录')
            self.chromium.close_tabs(loginPage)
            return

        # 未登录
        self.logger.info('登录中...')
        loginPage.wait(2)
        loginPage.wait.ele_displayed('tag:span@id=id_s')
        loginPage.ele('tag:span@id=id_s').click(by_js=None)
        loginPage.wait(2)
        loginPage.ele('xpath://*[@id="b_idProviders"]/li[1]/a/span').click(by_js=None)
        # 等待页面加载
        loginPage.wait(2)
        self._login()

        self.chromium.close_tabs(loginPage)

    def _login(self):
        loginPage = self.chromium.latest_tab
        loginPage.ele('tag:input').focus().input(vals=self.config['username'], clear=True)
        loginPage.wait.ele_displayed('xpath://*[@id="idSIButton9"]')
        loginPage.ele('xpath://*[@id="idSIButton9"]').click()
        
        while True:
            loginPage.wait(2)
            loginPage = self.chromium.latest_tab
            while True:
                alertEle = loginPage.ele('xpath://*[@id="pollingDescription"]')
                if alertEle:
                    alertStr = alertEle.text
                    alertNum = loginPage.ele('xpath://*[@id="displaySign"]').text
                    self.logger.info(f'{alertStr}:{alertNum}')
                    loginPage.wait(5)
                else:
                    break
            # 确定登录        
            acceptEle = loginPage.ele('xpath://*[@id="acceptButton"]')
            if acceptEle:
                acceptEle.click(by_js=None)
                break
            # 超时重试
            errorEle = loginPage.ele('xpath://*[@id="errorDescription"]')
            if errorEle:
                loginPage.ele('xpath://*[@id="primaryButton"]').click(by_js=None)
                self.logger.info(errorEle.text)
                continue


    def main(self):
        self.logger.info('===============================================')
        # 登录
        self.login()
        self.logger.info('===============================================')

        # 签到
        self.signIn()
        self.logger.info('===============================================')
        

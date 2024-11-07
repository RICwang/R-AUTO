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
        loginPage.wait.ele_displayed('tag:span@class=points-container')
        loginPage.ele('tag:span@class=points-container').click()
        loginPage.wait.ele_displayed('tag:span@class=css-128')
        loginPage.ele('tag:span@class=css-128').click()
        signInPage = self.chromium.latest_tab
        signInPage.wait(1)
        if 'https://login.live.com/' in signInPage.url:
            self._login()
            
        # signInPage = self.chromium.new_tab(url='https://rewards.bing.com/')
        signInPage = self.chromium.latest_tab
        # signInPage.wait(20000)
        signInPage.wait.ele_displayed('tag:mee-card')
        cardEles = signInPage.ele('tag:mee-rewards-daily-set-section').eles('tag:mee-card')
        for cardEle in cardEles:
            # 判断是否有效的卡片
            disabledAttr = cardEle.attr('disabled')
            if disabledAttr:
                # 无效跳过
                continue
            checkedEle = cardEle.ele('tag:span@class=mee-icon mee-icon-SkypeCircleCheck')
            if checkedEle:
                continue
            cardEle.ele('tag:a@class=ds-card-sec ng-scope').click.for_new_tab()
        
        signInPage.wait(2)
        
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
        loginPage.wait.ele_displayed('tag:span@id=id_s')
        loginPage.ele('tag:span@id=id_s').click(by_js=None)
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
        

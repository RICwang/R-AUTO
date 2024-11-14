import os
from func.common import faker_str
from DrissionPage import Chromium, ChromiumOptions
from DrissionPage.common import Keys

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
        self.logger.info(f'正在完成{self.autoname}特定任务...')
        while True:
            signInPage = self.chromium.new_tab(url='https://www.bing.com')
            signInPage.wait.ele_displayed('#id_rh_w')
            signInPage.ele('#id_rh_w').click()
            signInPage.wait.ele_displayed('#rewid-f')
            rewidEle = signInPage.ele('#rewid-f')
            mainEles = rewidEle.ele('tag:div@class=flyout_control_threeOffers')
            if not mainEles:
                self.chromium.close_tabs(signInPage)
                break
            promoEles = mainEles.eles('tag:div@class=promo_cont')
            for promoEle in promoEles:
                finishEle = promoEle.ele('tag:div@class^fc_auto pc b_subtitle complete')
                if finishEle:
                    continue
                aEle = promoEle.ele('tag:a')
                aEle.click()
                signInPage.wait.ele_displayed('#id_rh_w')
                signInPage.ele('#id_rh_w').click()
                signInPage.wait(1)
                break
                
            self.chromium.close_tabs(signInPage)
            
        self.logger.info(f'正在完成{self.autoname}搜索任务...')
        while True:
            searchPage = self.chromium.new_tab(url='https://www.bing.com')
            searchPage.wait.ele_displayed('#id_rh_w')
            searchPage.ele('#id_rh_w').click()
            searchPage.wait(2)
            searchPage.wait.ele_displayed('tag:div@title^每天继续搜索并获得最多')
            maxCntEle = searchPage.ele('tag:div@title^每天继续搜索并获得最多')
            maxCnt = int(maxCntEle.attr('title').split(' ')[1])
            currentCntEle = maxCntEle.prev()
            currentCnt = int(currentCntEle.text.split(' ')[1])
            self.logger.info(f'【{currentCnt}/{maxCnt}】')
            if currentCnt >= maxCnt:
                break
            self.chromium.close_tabs(searchPage)

            searchPage = self.chromium.new_tab(url='https://www.bing.com')
            searchPage.ele('tag:input').focus().input(vals=faker_str(), clear=True)
            searchPage.wait(1)
            searchPage.ele('#search_icon').click()
            searchPage.wait.ele_displayed('#id_rh_w')
            searchPage.ele('#id_rh_w').click()
            searchPage.wait(1)
            self.chromium.close_tabs(searchPage)
        
        self.res = True

    # 登录
    def login(self):
        self.logger.info(f'校验{self.autoname}登录状态...')
        loginPage = self.chromium.new_tab(url='https://www.bing.com')
        loginPage.wait.ele_displayed('#id_n')
        nicknameEle = loginPage.ele('#id_n')

        # 已登录
        if nicknameEle and nicknameEle.text != '':
            self.nickname = nicknameEle.text
            self.logger.info(f'【{self.nickname}】已登录')
            self.chromium.close_tabs(loginPage)
            return

        # 未登录
        self.logger.info('登录中...')
        loginPage.wait.ele_displayed('#id_s')
        loginPage.ele('#id_s').click()
        loginPage.wait.ele_displayed('xpath://*[@id="b_idProviders"]/li[1]/a/span')
        loginPage.ele('xpath://*[@id="b_idProviders"]/li[1]/a/span').click()
        # 等待页面加载
        loginPage.wait(2)
        self._login()

        self.chromium.close_tabs(loginPage)

    def _login(self):
        loginPage = self.chromium.latest_tab
        loginPage.wait.ele_displayed('tag:input')
        loginPage.ele('tag:input').focus().input(vals=self.config['username'], clear=True)
        loginPage.wait.ele_displayed('#idSIButton9')
        loginPage.ele('#idSIButton9').click()
        
        while True:
            loginPage.wait(2)
            loginPage = self.chromium.latest_tab
            while True:
                alertEle = loginPage.ele('#pollingDescription')
                if alertEle:
                    alertStr = alertEle.text
                    alertNum = loginPage.ele('#displaySign').text
                    self.logger.info(f'{alertStr}:{alertNum}')
                    loginPage.wait(5)
                else:
                    break
            # 确定登录        
            acceptEle = loginPage.ele('#acceptButton')
            if acceptEle:
                acceptEle.click()
                loginPage.wait(5)
                break
            # 超时重试
            errorEle = loginPage.ele('#errorDescription')
            if errorEle:
                loginPage.ele('#primaryButton').click()
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
        

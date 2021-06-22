import base64
import json
import pickle
import time
from time import sleep
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

caps = DesiredCapabilities.CHROME          #设置可以查看performance日志
caps['loggingPrefs'] = {'performance': 'ALL'}
website = "http://www.magicargo.com/#/"


class magiCargoSpider(object):
    def __init__(self):           #初始化
        self.options = webdriver.ChromeOptions()
        # self.options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        self.options.add_experimental_option("debuggerAddress", "127.0.0.1:5003")      #调试方法启动浏览器
        self.driver = webdriver.Chrome(options=self.options)
        self.left=60

    def addCookie(self):
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))      #添加cookies

    def loadCookie(self):
        cookies = pickle.load(open("cookies.pkl", "rb"))         #载入cookies
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def stationToStation(self):
        button = self.driver.find_element_by_xpath('//*[@id="tab-second"]')
        button.click()

        button = self.driver.find_element_by_xpath('//*[@id="pane-second"]/form/div[1]/div[1]/div/div/div/div[1]/input')
        button.send_keys("济南(董家镇)")
        sleep(0.5)
        li = self.driver.find_element_by_xpath(
            '//*[@id="pane-second"]/form/div[1]/div[1]/div/div/div/div[2]/div[1]/div[1]/ul/li')
        li.click()

        button = self.driver.find_element_by_xpath('//*[@id="pane-second"]/form/div[1]/div[2]/div/div/div/div[1]/input')
        button.send_keys("183502")
        sleep(0.5)
        li = self.driver.find_element_by_xpath(
            '//*[@id="pane-second"]/form/div[1]/div[2]/div/div/div/div[2]/div[1]/div[1]/ul/li')
        li.click()

        button = self.driver.find_element_by_xpath('//*[@id="pane-second"]/form/div[2]/div[2]/div/div/button')
        button.click()
        sleep(4)

    def bookSpace(self):
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="app"]/div/div[1]/div/div[1]/main/div/div[2]/div/div[3]/div/div/div[1]/div[2]/div[6]/div[1]'))
            )
            button.click()
        except:
            self.driver.quit()

    def bookAndOrder(self):
        sleep(2)
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])          #调整到最新打开的窗口
        try:
            date = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[1]/div/div[2]/main/div/div/div[2]/div[2]/div[2]/form/div[7]/div/div/div[1]/span')
            date.click()
            cargo = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[1]/div/div[2]/main/div/div/div[2]/div[2]/div[2]/form/div[7]/div/div/div[2]/div[1]/div[1]/ul/li')
            sleep(0.5)
            cargo.click()

            amount = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="app"]/div/div[1]/div/div[2]/main/div/div/div[2]/div[2]/div[2]/form/div[8]/div/div/div/div/div/input'))
            )
            amount.clear()
            amount.send_keys("1")

            name = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[1]/div/div[2]/main/div/div/div[2]/div[2]/div[2]/form/div[10]/div/div/input')
            name.send_keys("货物")

            code = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[1]/div/div[2]/main/div/div/div[2]/div[2]/div[2]/form/div[11]/div/div/input')
            code.send_keys("123")

            confirm = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[1]/div/div[2]/main/div/div/div[2]/div[2]/div[2]/form/div[14]/div/div/div[1]/label/span/input')
            self.driver.execute_script("arguments[0].click();", confirm)

            button = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[1]/div/div[2]/main/div/div/div[2]/div[2]/div[2]/form/div[15]/div/button')
            sleep(1)
            # print(button.is_displayed())
            button.click()
        except:
            self.driver.quit()

    def getCaptcha(self):
        sleep(0.5)
        img1 = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/canvas[1]')
        img1.screenshot(r'./captcha.png')       #将验证码图片截图
        logs = self.driver.get_log("performance")       #得到chrome performance日志
        for log in logs:
            # print(log)
            if 'message' not in log:
                continue
            log_entry = json.loads(log['message'])
            # print(log_entry)
            try:
                if "data:" in log_entry['message']['params']['request']['url']:
                    # print(log_entry)
                    url = log_entry['message']['params']['request']['url']
                    # print(url)
                    url = url[22:]        ##得到背景图片base 64编码
                    # print(url)
                    with open('bg.png', 'wb') as f:
                        f.write(base64.b64decode(url))      ##保存背景图片
                    # break
            except Exception as e:
                pass

    def is_similar(self, image1, image2, x, y):
        '''判断两张图片 各个位置的像素是否相同
        #image1:带缺口的图片
        :param image2: 不带缺口的图片
        :param x: 位置x
        :param y: 位置y
        :return: (x,y)位置的像素是否相同
        '''
        # 获取两张图片指定位置的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        # 设置一个阈值 允许有误差
        threshold = 60
        # 彩色图 每个位置的像素点有三个通道
        if abs(pixel1[0] - pixel2[0]) < threshold \
                and abs(pixel1[1] - pixel2[1]) < threshold \
                and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_diff_location(self):  # 获取缺口图起点
        flag = Image.open('flag.png')
        bg = Image.open('bg.png')
        for x in range(self.left, flag.size[0]):  # 从左到右 x方向
            for y in range(flag.size[1]):  # 从上到下 y方向
                if not self.is_similar(flag, bg, x, y):
                    return x  # 找到缺口的左侧边界 在x方向上的位置

    def cutImage(self):
        img = Image.open("./captcha.png")
        # print(img.size)
        cropped = img.crop((0, 1, 310, 160))  # (left, upper, right, lower)
        cropped.save("./flag.png")

    def drag_and_drop(self, offset):
        knob = self.driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[2]/div")
        ActionChains(self.driver).drag_and_drop_by_offset(knob, offset, 0).perform()

    def main(self):
        start=time.time()
        self.stationToStation()
        self.bookSpace()
        self.bookAndOrder()
        self.getCaptcha()
        self.cutImage()
        # print(self.get_diff_location())
        self.drag_and_drop(self.get_diff_location())
        end=time.time()
        print("time speed:",end-start)


if __name__ == "__main__":
    spider = magiCargoSpider()
    spider.main()

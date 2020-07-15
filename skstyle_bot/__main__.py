from selenium import webdriver
from pathlib import Path
from time import sleep
import os

class Skstyle:
    def __init__(self,username,password):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)
        # self.driver.minimize_window()
        self.driver.get("https://skstyle.pl/admin/login.php")
        sleep(1)
        self.driver.find_element_by_xpath("//input[@name='email']").send_keys(username)
        sleep(1)
        self.driver.find_element_by_xpath("//input[@type='password']")\
            .send_keys(password)
        sleep(1)
        self.driver.find_element_by_xpath("//input[@value='Zaloguj']").click()
        sleep(1)
        self.driver.find_element_by_xpath("/html/body/header/nav/div/div[1]/ul/li[2]/a").click()

        """ comments are an attempt to implement mobile minimized window"""

        # try:
        #     self.driver.find_element_by_xpath("//*[@id='helpBanner']/div[2]/div/a").click()
        # except:
        #     pass
        # self.driver.find_element_by_xpath("///html/body/div[2]/div[1]/div[2]/div[2]/ul/li[1]/a[@href = 'https://skstyle.pl/admin/orders.php']").click()
        # sleep(1)
        # try:
        # except:
        #     self.driver.find_element_by_xpath("/html/body/header/nav/ul/li[2]/a").click()
            # sleep(1)
            # self.driver.find_element_by_xpath("/html/body/header/nav/div/div[1]/ul/li[2]/a").click()
            # sleep(1)
            # self.driver.find_element_by_xpath("/html/body/header/nav/div/div[1]/ul/li[2]/a/span[2]").click()
            # sleep(1)
            # self.driver.find_element_by_xpath("//a[@href='https://skstyle.pl/admin/orders.php']").click()
            # sleep(1)
        # finally:
        #     sleep(5)
        #     self.driver.close()
        

    def is_there_new_order(self):
        data_folder = Path('project/')
        file_to_open = data_folder / 'last_order.txt'
        if(file_to_open.is_file() and os.stat(file_to_open).st_size != 0):
            f = open(file_to_open, "r")
            last_printed_order = int(f.read())
            f.close()
            f = open(file_to_open, "w")
            latest_order = int(self.driver.find_element_by_xpath("/html/body/div[2]/form[2]/section[1]/div[2]/div[1]/div[2]").text)
            f.write(str(latest_order))
            #//div[@class='widthId']
            f.close()
            return last_printed_order,latest_order
        else:
            f = open(file_to_open, "w")
            latest_order = (self.driver.find_element_by_xpath("/html/body/div[2]/form[2]/section[1]/div[2]/div[1]/div[2]").text)
            f.write(latest_order)
            f.close()
            return None, latest_order

    def handle_orders(self,last_printed_order,latest_order):
        print(last_printed_order,latest_order)
        
if __name__ == "__main__":
    my_bot = Skstyle(input("Your login: "),input("Your password: "))
    last_printed_order,latest_order = my_bot.is_there_new_order()
    if(last_printed_order!=None):
        my_bot.handle_orders(last_printed_order,latest_order)

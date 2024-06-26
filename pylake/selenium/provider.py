import os

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pydata.logger.logger_mixing import LoggerMixing

class SeleniumProvider(LoggerMixing):

    def get_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--incognito")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        options.add_argument("--disable-extensions")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--incognito")
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--start-maximized")
        prefs = {'download.default_directory': "/tmp/"}
        options.add_experimental_option('prefs', prefs)
        try:
            USE_HEADLESS = os.getenv("USE_HEADLESS", 'False').lower() in ('true', '1', 't')
            if USE_HEADLESS == True:
                options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(5)
            return driver

        except Exception as e:
            self.logger.error(e)
            return None
        
    @staticmethod
    def get_by_id(driver, id, timeout):
        WebDriverWait(driver=driver, timeout=timeout).until(EC.presence_of_element_located((By.ID, id)))
        return driver.find_element(By.ID, id)

    @staticmethod
    def get_by_css(driver,css, timeout):
        WebDriverWait(driver=driver, timeout=timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        return driver.find_element(By.CSS_SELECTOR, css)
    
    @staticmethod
    def get_by_xpath(driver, x_path, timeout):
        WebDriverWait(driver=driver, timeout=timeout).until(EC.presence_of_element_located((By.XPATH, x_path)))
        return driver.find_element(By.CSS_SELECTOR, x_path)
    
    @staticmethod
    def write_from_xpath(driver, x_path, value, timeout):
        WebDriverWait(driver=driver, timeout=timeout).until(EC.presence_of_element_located((By.XPATH, x_path)))
        input_account = driver.find_element(By.XPATH, x_path)
        input_account.send_keys(value)

    def close_driver(self, driver):
        if driver != None:
            driver.close()
            driver = None


    
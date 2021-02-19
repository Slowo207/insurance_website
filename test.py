from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print('pass 1')

display = Display(visible=0, size=(800, 600))
display.start()

print('pass 2')

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')

print('pass 3')

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get('http://nytimes.com')
print(driver.title)

print('pass 4')

exit()

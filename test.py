from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(800, 600))
display.start()

print("test1)

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
      
print("test2")

driver = webdriver.Chrome(options=options)
driver.get('http://nytimes.com')
      
      print("test3")
      
print(driver.title)
print("test4")

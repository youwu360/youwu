from selenium import webdriver  
from pyvirtualdisplay import Display  
  
  
display = Display(visible=0, size=(800,600))  
display.start()  
driver = webdriver.PhantomJS()  
driver.get("http://www.baidu.com")  
print(driver.page_source)


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Ie()
browser.get('http://www.alltobid.com/guopai/index.html')

# my_input = raw_input("Enter Text To Search:")
# input_text = browser.find_element_by_name("wd")
# input_text.send_keys(my_input)

browser.switch_to_frame("content01")
search_button = browser.find_element_by_id("UserLogin1_btnLogin")
search_button.send_keys(Keys.RETURN)

# for handle in browser.window_handles:
browser.switch_to_window(browser.window_handles[0]) #switch to the opened window

text = browser.find_element_by_class_name("Messagefont1")
print text.text

input_uname = browser.find_element_by_name("UserName")
input_uname.send_keys("TestSamso")

input_pwd = browser.find_element_by_name("Password")
input_pwd.send_keys("TestPwd")

input_verify_code = browser.find_element_by_name("VerificationCode")
my_verify_code = raw_input("Enter Verification Code: ")
input_verify_code.send_keys(my_verify_code)

login_btn = browser.find_element_by_class_name("roundedRectangle2")
login_btn.click()

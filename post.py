from selenium import webdriver
import time
import pywinauto
from pywinauto.keyboard import send_keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import random
from selenium.webdriver.remote import switch_to
from selenium.webdriver.support.expected_conditions import frame_to_be_available_and_switch_to_it
from test.test_ssl import handle_error

picPath = 'D:\Desktop\cape-reinga.jpg'

d = webdriver.Chrome()

d.get('http://tangren.co.nz/')
print(d.title)

# Login
d.find_element_by_link_text('登陆').click()
time.sleep(3)
d.find_element_by_name('username').send_keys("tangren")
time.sleep(3)
d.find_element_by_name('password').send_keys('jian1980_')
time.sleep(3)
d.find_element_by_name('loginsubmit').click()
time.sleep(3)

# Post
d.find_element_by_link_text('吐槽大汇').click()
time.sleep(3)
element_to_hover_over = d.find_element_by_xpath('//*[@id="newspecial"]')
time.sleep(3)
hover = ActionChains(d).move_to_element(element_to_hover_over)
time.sleep(3)
hover.perform()
time.sleep(3)
d.find_element_by_link_text('发表帖子').click()
time.sleep(3)






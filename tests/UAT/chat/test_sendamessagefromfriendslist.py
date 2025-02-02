# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestSendamessagefromfriendslist():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_sendamessagefromfriendslist(self):
    # Test name: Send a message from friends list
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("http://127.0.0.1:8000//")
    # 2 | click | id=id_profile_links | 
    self.driver.find_element(By.ID, "id_profile_links").click()
    # 3 | click | linkText=Account | 
    self.driver.find_element(By.LINK_TEXT, "Account").click()
    # 4 | click | css=.friend-text | 
    self.driver.find_element(By.CSS_SELECTOR, ".friend-text").click()
    # 5 | click | linkText=Send a Message | 
    self.driver.find_element(By.LINK_TEXT, "Send a Message").click()
    # 6 | type | id=id_chat_message_input | Hello
    self.driver.find_element(By.ID, "id_chat_message_input").send_keys("Hello")
    # 7 | click | css=.chat-message-submit-button | 
    self.driver.find_element(By.CSS_SELECTOR, ".chat-message-submit-button").click()
    # 8 | click | id=id_chat_message_submit | 
    self.driver.find_element(By.ID, "id_chat_message_submit").click()
    # 9 | mouseOver | id=id_chat_message_submit | 
    element = self.driver.find_element(By.ID, "id_chat_message_submit")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    # 10 | mouseOut | id=id_chat_message_submit | 
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element, 0, 0).perform()
    # 11 | click | css=.message-container:nth-child(1) | 
    self.driver.find_element(By.CSS_SELECTOR, ".message-container:nth-child(1)").click()
    # 12 | click | css=.d-flex:nth-child(1) > .d-flex > .msg-p > p | 
    self.driver.find_element(By.CSS_SELECTOR, ".d-flex:nth-child(1) > .d-flex > .msg-p > p").click()
    # 13 | assertText | css=.d-flex:nth-child(1) > .d-flex > .msg-p > p | Hello
    assert self.driver.find_element(By.CSS_SELECTOR, ".d-flex:nth-child(1) > .d-flex > .msg-p > p").text == "Hello"
  

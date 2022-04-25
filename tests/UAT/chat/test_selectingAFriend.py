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

class TestSelectingAFriend():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_selectingAFriend(self):
    # Test name: Selecting A Friend
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("http://127.0.0.1:8000//")
    # 2 | click | css=.show | 
    self.driver.find_element(By.CSS_SELECTOR, ".show").click()
    # 3 | click | css=#id_chat_notification_dropdown_toggle > .d-flex | 
    self.driver.find_element(By.CSS_SELECTOR, "#id_chat_notification_dropdown_toggle > .d-flex").click()
    # 4 | click | css=.chat-dropdown-header | 
    self.driver.find_element(By.CSS_SELECTOR, ".chat-dropdown-header").click()
    # 5 | mouseOver | id=id_friend_container_2 | 
    element = self.driver.find_element(By.ID, "id_friend_container_2")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    # 6 | mouseOut | id=id_friend_container_2 | 
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element, 0, 0).perform()
    # 7 | click | css=#id_friend_container_4 > .d-flex | 
    self.driver.find_element(By.CSS_SELECTOR, "#id_friend_container_4 > .d-flex").click()
    # 8 | assertText | id=id_other_username | DevFour
    assert self.driver.find_element(By.ID, "id_other_username").text == "DevFour"
    # 9 | assertText | css=#id_friend_container_4 .username-span | DevFour
    assert self.driver.find_element(By.CSS_SELECTOR, "#id_friend_container_4 .username-span").text == "DevFour"
  

import requests
import time
import argparse

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import urllib  



class Insta_bot(object):
	def __init__(self, username, password, profile, images, ig_content, img_name, location):
		self.username = username
		self.password = password
		self.profile = profile
		self.images = images
		self.ig_content = ig_content
		self.img_name = img_name
		self.location = location

	def set_images(self, images):
		self.images = images

	def set_ig_content(self, ig_content):
		self.ig_content = ig_content

	def set_img_name(self, img_name):
		self.img_name = img_name

	def set_location(self, location):
		self.location = location

	def connect_to_ig(self,profile,driver):
		driver.get('https://www.instagram.com/')		
		driver.find_element_by_xpath("//button[contains(.,'Uniquement autoriser les cookies essentiels')]").click()
		driver.find_element_by_name("username").send_keys(self.username)
		time.sleep(3)
		driver.find_element_by_name("password").send_keys(self.password)
		driver.find_element_by_xpath("//button[contains(.,'Connexion')]").click()
		time.sleep(3)
		element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Plus tard')]")))
		driver.find_element_by_xpath("//button[contains(.,'Plus tard')]").click()
		time.sleep(2)
		element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Plus tard')]")))
		driver.find_element_by_xpath("//button[contains(.,'Plus tard')]").click()
		time.sleep(2)
		searchbox = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Rechercher']")))
		searchbox.clear()
		searchbox.send_keys(profile)
		time.sleep(5)
		searchbox.send_keys(Keys.ENTER)
		time.sleep(5)
		searchbox.send_keys(Keys.ENTER)
		time.sleep(5)

	def get_all_pictures(self,driver):
		scrolldown = driver.execute_script("window.scrollTo(0,4000);var scrolldown=document.body.scrollHeight;return scrolldown;")
		match=False
		while(match==False):
		    last_count = scrolldown
		    time.sleep(3)
		    scrolldown = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
		    if last_count==scrolldown:
		        match=True
		posts = []
		links = driver.find_elements_by_tag_name('a')
		for link in links:
		    post = link.get_attribute('href')
		    if '/p/' in post:
		      posts.append(post)
		return posts 

	def get_all_descriptions(self, posts,driver):
		contents = []
		images_name = []
		download_url = ''
		location = []
		i = 0
		for post in posts:	
			driver.get(post)
			shortcode = driver.current_url.split("/")[-2]
			time.sleep(7)
			if driver.find_element_by_css_selector("img[style='object-fit: cover;']") is not None:
				try:
					download_url = driver.find_element_by_css_selector("img[style='object-fit: cover;']").get_attribute('src')
					urllib.request.urlretrieve(download_url, str(self.profile)+'_'+str(i)+'.jpg')
				except:
					pass
				try:
					content = driver.find_element_by_class_name('C4VMK').text
					contents.append(str(content))
				except:
					contents.append('no')
				try:
					location_content = driver.find_element_by_class_name('M30cS').text
					location.append(location_content)
				except:
					location.append('no')
				try:
					images_name.append(self.profile+'_'+str(i)+'.jpg')
				except:
					images_name.append('no')
				i += 1
			time.sleep(5)
		return (contents,images_name, location)




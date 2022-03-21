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

import insta_bot




from google.cloud import storage


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("email")
	parser.add_argument("password")
	args = parser.parse_args()

	options = Options()
	options.headless = True
	driver = webdriver.Firefox(options=options)

	botibot = insta_bot.Insta_bot(args.email, args.password,'deborah.wtn',[],[],[],[])
	botibot.connect_to_ig(botibot.profile,driver)
	images = botibot.get_all_pictures(driver)
	botibot.set_images(images)
	contents = botibot.get_all_descriptions(botibot.images,driver)
	botibot.set_ig_content(contents[0])
	botibot.set_img_name(contents[1])
	botibot.set_location(contents[2])

	pd_dict = {'img_name': botibot.img_name, 'location': botibot.location, 'content': botibot.ig_content, 'profile': [botibot.profile] * len(botibot.img_name)} 
	df = pd.DataFrame(pd_dict)
	df.to_csv('dataset.csv')
	upload_blob('test_bucket_insta', 'dataset.csv', 'dataset.csv')



	driver.quit()


	#botibot.get_all_descriptions()
	#connect to ig
	#visit page in sources
	#get list of links to pictures in sources
	#visit all links
	#get image, description, text, post hour and date, number of likes
	#post image
	#follow
	#get data from following 
	#get data from followers
	#unfollow

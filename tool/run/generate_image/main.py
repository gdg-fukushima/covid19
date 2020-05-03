import time
from flask import Flask, send_file
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
from PIL import Image
from io import BytesIO
from google.cloud import storage

app = Flask(__name__)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--hide-scrollbars")
chrome_options.add_argument("--lang=ja")
chrome_options.add_argument("--window-size=1200,1000")
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--force-device-scale-factor=2")

GCS_BUCKET_ID = 'fukushima-covid19'
BASE_URL = 'https://fukushima-covid19.web.app/'
CARD_URL = BASE_URL + 'cards/{}/?embed=true'
CARD_IDS = [
    'attributes-of-confirmed-cases',
    'details-of-confirmed-cases',
    'number-of-confirmed-cases',
    'number-of-reports-to-covid19-consultation-desk',
    'number-of-reports-to-covid19-telephone-advisory-center',
    'number-of-tested'
]


def upload_png(bucket_name, destination_blob_name, image):
    # storage_client = storage.Client.from_service_account_json('./cred.json')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.cache_control = 'max-age=60'
    blob.upload_from_string(image, content_type='image/png')


def get_card_image(browser, id_name):
    browser.get(CARD_URL.format(id_name))
    time.sleep(5)
    remove_share_btn = 'var elements = document.querySelectorAll(".Footer-Right"); for (let i = 0; i < elements.length; i++) {const element = elements[i];element.remove();}'
    browser.execute_script(remove_share_btn)
    add_prefix = 'var titles = document.querySelectorAll(".DataView-Title"); var prefNamePrefix = "福島:"; for (let i = 0; i < titles.length; i++) { const element = titles[i]; element.innerHTML = prefNamePrefix + element.innerHTML }'
    browser.execute_script(add_prefix)
    # TODO: Generate high resolution image
    # change_origin = 'document.getElementById("app").style.transformOrigin = "top left"'
    # browser.execute_script(change_origin)
    # zoom_element = 'document.getElementById("app").style.transform = "scale(2)"'
    # browser.execute_script(zoom_element)
    return browser.find_element_by_id(id_name).screenshot_as_png


@app.route("/images/generate")
def generate_all_images():
    # Initialize a new browser
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(BASE_URL)
    time.sleep(1)
    for id_name in CARD_IDS:
        image = get_card_image(browser, id_name)
        upload_png(GCS_BUCKET_ID, 'images/{}.png'.format(id_name), image)
    browser.close()
    return 'OK'


@app.route("/image/generate/<id_name>")
def generate_image(id_name):
    # Initialize a new browser
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(BASE_URL)
    time.sleep(1)
    image = get_card_image(browser, id_name)
    upload_png(GCS_BUCKET_ID, 'images/{}.png'.format(id_name), image)
    browser.close()
    tmp_file_name = './tmp_image_{}.png'.format(id_name)
    with open(tmp_file_name, 'wb') as f:
        f.write(image)

    return send_file(tmp_file_name)

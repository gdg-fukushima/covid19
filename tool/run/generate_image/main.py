import time
from flask import Flask, send_file
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
from PIL import Image
from io import BytesIO
from google.cloud import storage

app = Flask(__name__)


def upload_png(bucket_name, destination_blob_name, image):
    # storage_client = storage.Client.from_service_account_json('../credential_filename.json')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.cache_control = 'max-age=60'
    blob.upload_from_string(image, content_type='image/png')


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--hide-scrollbars")
chrome_options.add_argument("--lang=ja")
chrome_options.add_argument("--window-size=1200,1000")
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--force-device-scale-factor=2")

# Initialize a new browser
browser = webdriver.Chrome(chrome_options=chrome_options)

BASE_URL = 'https://fukushima-covid19.web.app/'
CARD_URL = BASE_URL + 'cards/{}/?embed=true'
# NOTE: Get cache
browser.get(BASE_URL)
ALLOWED_IDS = [
    'attributes-of-confirmed-cases',
    'details-of-confirmed-cases',
    'number-of-confirmed-cases',
    'number-of-reports-to-covid19-consultation-desk',
    'number-of-reports-to-covid19-telephone-advisory-center',
    'number-of-tested'
]

@app.route("/generate/<id_name>")
def generate_image(id_name):
    if id_name not in ALLOWED_IDS:
        return False

    # TODO: Generate high resolution image
    # change_origin = 'document.getElementById("app").style.transformOrigin = "top left"'
    # browser.execute_script(change_origin)
    # zoom_element = 'document.getElementById("app").style.transform = "scale(2)"'
    # browser.execute_script(zoom_element)
    time.sleep(3)
    browser.get(CARD_URL.format(id_name))
    remove_share_btn = 'var elements = document.querySelectorAll(".Footer-Right"); for (let i = 0; i < elements.length; i++) {const element = elements[i];element.remove();}'
    browser.execute_script(remove_share_btn)
    add_prefix = 'var titles = document.querySelectorAll(".DataView-Title"); var prefNamePrefix = "福島:"; for (let i = 0; i < titles.length; i++) { const element = titles[i]; element.innerHTML = prefNamePrefix + element.innerHTML }'
    browser.execute_script(add_prefix)
    image = browser.find_element_by_id(id_name).screenshot_as_png
    upload_png('fukushima-covid19', 'images/{}.png'.format(id_name), image)
    tmp_file_name = './tmp_image_{}.png'.format(id_name)
    with open(tmp_file_name, 'wb') as f:
        f.write(image)

    return send_file(tmp_file_name)

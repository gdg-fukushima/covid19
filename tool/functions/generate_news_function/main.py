import csv
import json
import logging
import requests
import email.utils as eut
from bs4 import BeautifulSoup
from google.cloud import storage
from datetime import datetime, timedelta, timezone, date


JST = timezone(timedelta(hours=+9), 'JST')


def fetch_csv_as_string(url):
  res = requests.get(url)
  last_modified = res.headers['Last-Modified']
  jst_datetime = eut.parsedate_to_datetime(last_modified).astimezone(JST)
  # NOTE: A char code of Fukushima pref's CSV is Shift-JIS
  res.encoding = 'shift_jis'
  return res.text, jst_datetime


def csv_string_to_list(csvStr):
  cr = csv.reader(csvStr.splitlines(), delimiter=',')
  csv_list = list(cr)
  return csv_list


def get_datetime(datetime_str):
  if datetime_str == '':
    return None
  if '-' in datetime_str:
    return datetime.strptime(datetime_str, '%Y-%m-%d')
  else:
    return datetime.strptime(datetime_str, '%Y/%m/%d')


def generate_datetime_iso(datetime):
  return datetime.strftime('%Y-%m-%dT%H:%M:%S')


def generate_datetime_readable(datetime):
  return datetime.strftime('%Y/%m/%d %H:%M')


def generate_date_readable(date):
  return date.strftime('%Y/%m/%d')


def generate_short_datetime(datetime):
  return '{}/{}'.format(datetime.month, datetime.day)


def list_dir(url, ext=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]


def upload_json(bucket_name, destination_blob_name, data):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.cache_control = 'max-age=10'
    blob.upload_from_string(data, content_type='application/json')
    logging.info(
        "File {} uploaded to {}.".format(
            data, destination_blob_name
        )
    )


class News():
  announced_at = None
  body = None
  url = None
  note = None

  def __init__(self, announced_at, body, url, note):
    self.announced_at = get_datetime(announced_at)
    self.body = body
    self.url = url
    self.note = note


def generate_news_data(news_list):
  news_data = []
  news_rows = [News(*row) for row in news_list[1:] if row[0]]
  news_rows = sorted(news_rows, key=lambda t: t.announced_at, reverse=True)
  for news in news_rows:
    if news.announced_at == None:
      continue
    announce_datetime_str = generate_date_readable(news.announced_at)
    news_data.append({
      'date': announce_datetime_str,
      'text': news.body,
      'url': news.url
    })
  return news_data


def generate_news_json():
    news_dir_list = list_dir('http://www.pref.fukushima.lg.jp/w4/covid19/topics/')
    news_file_latest_uri = news_dir_list[-1]
    logging.info(news_file_latest_uri)
    news_csv_string, news_csv_datetime = fetch_csv_as_string(news_file_latest_uri)
    logging.info(news_csv_datetime)
    news_list = csv_string_to_list(news_csv_string)
    return generate_news_data(news_list)


def main(request):
    news_data = {
      'news_items': generate_news_json()
    }
    upload_json('fukushima-covid19', 'news.json', json.dumps(news_data, ensure_ascii=False))

import os
import csv
import json
import time
import logging
import requests
import email.utils as eut
from bs4 import BeautifulSoup
from google.cloud import storage, pubsub_v1
from datetime import datetime, timedelta, timezone, date


JST = timezone(timedelta(hours=+9), 'JST')
GCP_PROJECT = os.environ.get('GCP_PROJECT')
UPDATE_TOPIC = os.environ.get('UPDATE_TOPIC')
IMAGE_GENERATOR_BASE_URL = os.environ.get('IMAGE_GENERATOR_BASE_URL')
CDN_BASE_URL = os.environ.get('CDN_BASE_URL')
MESSAGE_SITE_TITLE = '福島県 新型コロナウイルス感染症対策サイト'
SHORTEN_SITE_URL = 'https://fukushima-covid19.web.app/'
DATA_URL = 'https://cdn2.dott.dev/data.json'


def fetch_csv_as_string(url):
  res = requests.get(url)
  last_modified = res.headers['Last-Modified']
  jst_datetime = eut.parsedate_to_datetime(last_modified).astimezone(JST)
  # NOTE: A char code of Fukushima pref's CSV is Shift-JIS
  res.encoding = 'shift_jis'
  return res.text, jst_datetime


def fetch_json(url):
  res = requests.get(url)
  return json.loads(res.text)


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
  return [url + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]


def upload_json(bucket_name, destination_blob_name, data):
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(destination_blob_name)
  blob.cache_control = 'max-age=10'
  blob.upload_from_string(data, content_type='application/json')


def upload_csv(bucket_name, destination_blob_name, data):
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(destination_blob_name)
  blob.cache_control = 'max-age=10'
  blob.upload_from_string(data, content_type='text/csv')


class Patient():
  number = None
  comune_code = None
  pref_name = None
  city_name = None
  announced_at = None
  develop_at = None
  residence = None
  generation = None
  gender = None
  occupation = None
  status = None
  symptom = None
  has_travel_history = None
  is_discharged = None
  has_died = None
  note = None

  def __init__(self, number, comune_code, pref_name, city_name, announced_at,
               develop_at, residence, generation, gender, occupation, status,
               symptom, has_travel_history, is_discharged, has_died, note):
    self.number = number
    self.comune_code = comune_code
    self.pref_name = pref_name
    self.city_name = city_name
    self.announced_at = get_datetime(announced_at)
    self.develop_at = get_datetime(develop_at)
    self.residence = residence
    self.generation = generation
    self.gender = gender
    self.occupation = occupation
    self.status = status
    self.symptom = symptom
    self.has_travel_history = True if has_travel_history == '1' else False
    self.is_discharged = True if is_discharged == '1' else False
    self.has_died = True if has_died == '1' else False
    self.note = note

def generate_patiens_data(patients, patients_csv_datetime):
  patients_data = []
  patients_count_index = {}
  start_date = None
  end_date = patients_csv_datetime.replace(tzinfo=None) - timedelta(hours=24)
  last_date = None
  patients = [Patient(*row) for row in patients[1:] if row[0]]
  patients = sorted(patients, key=lambda t: t.announced_at)
  for patient in patients:
    last_date = patient.announced_at
    if start_date is None:
      start_date = patient.announced_at
    announce_iso_time_str = generate_datetime_iso(patient.announced_at)
    patients_data.append({
      'リリース日': announce_iso_time_str,
      '曜日': '',
      '居住地': patient.residence,
      '年代': patient.generation,
      '性別': patient.gender,
      '退院': '',
      'date': generate_datetime_iso(patient.announced_at)
    })
    if announce_iso_time_str not in patients_count_index:
      patients_count_index[announce_iso_time_str] = 1
    else:
      patients_count_index[announce_iso_time_str] += 1

  patients_summary = []
  discharges_summary = []
  destination_date = last_date if last_date > end_date else end_date
  diff_days = (destination_date - start_date).days

  for i in range(0, diff_days + 1):
    date = start_date + timedelta(days=i)
    date_iso_str = generate_datetime_iso(date)

    subtotal = patients_count_index[date_iso_str] if date_iso_str in patients_count_index else 0

    patients_summary.append({
        '日付': date_iso_str,
        '小計': subtotal
    })
    discharges_summary.append({
        '日付': date_iso_str,
        '小計': 0
    })

  return patients_data, patients_summary, discharges_summary

class Pcount():
  confirmed_at = None
  comune_code = None
  pref_name = None
  city_name = None
  patients = None
  dead = None
  discharged = None

  def __init__(self, confirmed_at, comune_code, pref_name, city_name, patients, dead, discharged):
    self.confirmed_at = get_datetime(confirmed_at)
    self.comune_code = comune_code
    self.pref_name = pref_name
    self.city_name = city_name
    self.patients = int(patients)
    self.dead = int(dead)
    self.discharged = int(discharged)


def generate_pcounts_data(pcounts):
  data_pref = []
  data_etc = []
  labels = []
  pcounts = [Pcount(*row) for row in pcounts[1:] if row[0]]
  pcounts = sorted(pcounts, key=lambda t: t.confirmed_at)
  return pcounts[-1]


class Inspection():
  implemented_at = None
  comune_code = None
  pref_name = None
  city_name = None
  people_count = None
  note = None

  def __init__(self, implemented_at, comune_code, pref_name, city_name,
             people_count, note):
    self.implemented_at = get_datetime(implemented_at)
    self.comune_code = comune_code
    self.pref_name = pref_name
    self.city_name = city_name
    self.people_count = int(people_count)
    self.note = note


def generate_inspections_data(inspections):
  data_pref = []
  data_etc = []
  labels = []
  total_num = 0
  inspections = [Inspection(*row[:6]) for row in inspections[1:] if row[0]]
  inspections = sorted(inspections, key=lambda t: t.implemented_at)
  for inspection in inspections:
    data_pref.append(inspection.people_count)
    data_etc.append(0)
    date_time_iso = generate_datetime_iso(inspection.implemented_at)
    labels.append(date_time_iso)
    total_num += inspection.people_count

  return data_pref, data_etc, labels, total_num


class Querent():
  accepted_at = None
  comune_code = None
  pref_name = None
  city_name = None
  count = None
  note = None

  def __init__(self, accepted_at, comune_code, pref_name, city_name, count):
    self.accepted_at = get_datetime(accepted_at)
    self.comune_code = comune_code
    self.pref_name = pref_name
    self.city_name = city_name
    self.count = int(count) if count != '' else 0


def generate_querents_data(querents):
  querents_data = []
  querents = [Querent(*row[:5]) for row in querents[1:] if row[0]]
  querents = sorted(querents, key=lambda t: t.accepted_at)
  for que in querents:
    querents_data.append({
      '日付': generate_datetime_iso(que.accepted_at),
      '曜日': '',
      'date': generate_datetime_iso(que.accepted_at),
      'short_date': generate_short_datetime(que.accepted_at),
      '小計': que.count
    })
  return querents_data


# Patients 福島県_新型コロナウイルス陽性患者属性
def generate_patiens_json():
  patients_dir_list = list_dir('http://www.pref.fukushima.lg.jp/w4/covid19/patients/')
  patients_file_latest_uri = patients_dir_list[-1]
  logging.info(patients_file_latest_uri)
  patients_csv_string, patients_csv_datetime = fetch_csv_as_string(patients_file_latest_uri)
  upload_csv(GCP_PROJECT, 'csv/patients.csv', patients_csv_string)
  patients = csv_string_to_list(patients_csv_string)
  patients_data, patients_summary, discharges_summary = generate_patiens_data(patients, patients_csv_datetime)
  DATETIME_LIST.append(patients_csv_datetime)
  DATA['new']['patients']['data'] = patients_data
  patients_csv_datetime_str = generate_datetime_readable(patients_csv_datetime)
  DATA['new']['patients']['date'] = patients_csv_datetime_str
  DATA['new']['patients_summary']['date'] = patients_csv_datetime_str
  DATA['new']['patients_summary']['data'] = patients_summary
  DATA['new']['discharges_summary']['date'] = patients_csv_datetime_str
  DATA['new']['discharges_summary']['data'] = discharges_summary


def generate_summary_json():
  pcounts_dir_list = list_dir('http://www.pref.fukushima.lg.jp/w4/covid19/pcount/')
  pcounts_file_latest_uri = pcounts_dir_list[-1]
  logging.info(pcounts_file_latest_uri)
  pcounts_csv_string, pcounts_csv_datetime = fetch_csv_as_string(pcounts_file_latest_uri)
  upload_csv(GCP_PROJECT, 'csv/pcounts.csv', pcounts_csv_string)
  pcounts = csv_string_to_list(pcounts_csv_string)
  pcount = generate_pcounts_data(pcounts)
  DATETIME_LIST.append(pcounts_csv_datetime)
  total = pcount.patients + pcount.dead + pcount.discharged
  DATA['new']['main_summary']['children'][0]['value'] = total
  DATA['new']['main_summary']['children'][0]['children'][0]['value'] = pcount.patients
  DATA['new']['main_summary']['children'][0]['children'][1]['value'] = pcount.discharged
  DATA['new']['main_summary']['children'][0]['children'][2]['value'] = pcount.dead


# Inspections 福島県_新型コロナウイルス検査件数
def generate_inspection_json():
  inspections_dir_list = list_dir('http://www.pref.fukushima.lg.jp/w4/covid19/test_count/')
  inspections_file_latest_uri = inspections_dir_list[-1]
  logging.info(inspections_file_latest_uri)
  inspections_csv_string, inspections_csv_datetime = fetch_csv_as_string(inspections_file_latest_uri)
  upload_csv(GCP_PROJECT, 'csv/inspections.csv', inspections_csv_string)
  inspections = csv_string_to_list(inspections_csv_string)
  data_perf, data_etc, labels, total_num = generate_inspections_data(inspections)
  DATETIME_LIST.append(inspections_csv_datetime)
  DATA['new']['inspections']['date'] = generate_datetime_readable(inspections_csv_datetime)
  DATA['new']['inspections_summary']['date'] = generate_datetime_readable(inspections_csv_datetime)
  DATA['new']['inspections_summary']['data']['県内'] = data_perf
  DATA['new']['inspections_summary']['data']['その他'] = data_etc
  DATA['new']['inspections_summary']['labels'] = labels
  DATA['new']['main_summary']['value'] = total_num


# Contacts 福島県_相談窓口 相談件数
def generate_contacts_json():
  contacts_dir_list = list_dir('http://www.pref.fukushima.lg.jp/w4/covid19/call_center/')
  contacts_file_latest_uri = contacts_dir_list[-1]
  logging.info(contacts_file_latest_uri)
  contacts_csv_string, contacts_csv_datetime = fetch_csv_as_string(contacts_file_latest_uri)
  upload_csv(GCP_PROJECT, 'csv/contacts.csv', contacts_csv_string)
  contacts = csv_string_to_list(contacts_csv_string)
  contacts_data = generate_querents_data(contacts)
  DATETIME_LIST.append(contacts_csv_datetime)
  DATA['new']['contacts']['date'] = generate_datetime_readable(contacts_csv_datetime)
  DATA['new']['contacts']['data'] = contacts_data


# Querent 福島県_帰国者・接触者相談センター 相談件数
def generate_querents_json():
  querents_dir_list = list_dir('http://www.pref.fukushima.lg.jp/w4/covid19/returnee_contact/')
  querents_file_latest_uri = querents_dir_list[-1]
  logging.info(querents_file_latest_uri)
  querents_csv_string, querents_csv_datetime = fetch_csv_as_string(querents_file_latest_uri)
  upload_csv(GCP_PROJECT, 'csv/querents.csv', querents_csv_string)
  querents = csv_string_to_list(querents_csv_string)
  querents_data = generate_querents_data(querents)
  DATETIME_LIST.append(querents_csv_datetime)
  DATA['new']['querents']['date'] = generate_datetime_readable(querents_csv_datetime)
  DATA['new']['querents']['data'] = querents_data


def publish_update_message(message, media=[]):
  publisher = pubsub_v1.PublisherClient()
  topic_path = publisher.topic_path(GCP_PROJECT, UPDATE_TOPIC)
  data_dict = {
      "status": message,
      "media": media if len(media) > 0 else None
  }
  data = json.dumps(data_dict)
  publisher.publish(
      topic_path, data=data.encode("utf-8")
  )


def load_prev_data():
  return fetch_json(DATA_URL)


def generate_image(card_id):
  res = requests.get('{}/{}'.format(IMAGE_GENERATOR_BASE_URL, card_id))
  if res.status_code == 200:
    return True
  return False


def check_update_number_of_confirmed_cases():
  # 検査陽性者の状況 + 陽性患者の属性 + 陽性患者数
  card_ids = [
    'number-of-confirmed-cases',
    'attributes-of-confirmed-cases',
    'details-of-confirmed-cases'
  ]
  media_list = []
  if DATA['prev']['patients_summary']['date'] != DATA['new']['patients_summary']['date']:
    for card_id in card_ids:
      if generate_image(card_id):
        media_list.append('{}/{}.png'.format(CDN_BASE_URL, card_id))
    last_date = DATA['new']['patients_summary']['data'][-1]['日付']
    last_dateime = get_datetime(last_date[:10])
    last_date = generate_date_readable(last_dateime)
    last_num = DATA['new']['patients_summary']['data'][-1]['小計']

    main_summary = DATA['new']['main_summary']
    inspections_total = main_summary['value']
    patients_total = main_summary['children'][0]['value']
    in_hospital = main_summary['children'][0]['children'][0]['value']
    discharged = main_summary['children'][0]['children'][1]['value']
    dead = main_summary['children'][0]['children'][2]['value']

    message = '【{}】\n'.format(MESSAGE_SITE_TITLE)
    message += '{}に確認された陽性患者は\n【{}人】\nです。\n\n'.format(last_date, last_num)
    message += '検査実施件数:{}件\n'.format(inspections_total)
    message += '└陽性者数:{}人\n'.format(patients_total)
    message += '　├入院中:{}人\n'.format(in_hospital)
    message += '　├死亡　:{}人\n'.format(dead)
    message += '　└退院　:{}人\n\n'.format(discharged)
    message += SHORTEN_SITE_URL

    publish_update_message(message, media_list)


def generate_count_message(card_title, last_date, last_num, total, unit,
                           extra_body=''):
  last_dateime = get_datetime(last_date[:10])
  last_date = generate_date_readable(last_dateime)
  total = "{:,}".format(total)
  last_num = "{:,}".format(last_num)
  header = '【{}】\n「{}」を更新しました。\n'.format(MESSAGE_SITE_TITLE, card_title)
  body = '\n{0}は【{1}{2}】でした。\nこれまでの合計は【{3}{2}】です。'.format(last_date, last_num, unit, total)
  footer = '\n\n{}'.format(SHORTEN_SITE_URL)
  return header + body + extra_body+ footer


def check_update_number_of_tested():
  # 検査実施数
  card_id = 'number-of-tested'
  card_title = '検査実施数'
  unit = '件'
  if DATA['prev']['inspections_summary']['date'] != DATA['new']['inspections_summary']['date']:
    if generate_image(card_id):
      total = DATA['new']['main_summary']['value']
      last_date = DATA['new']['inspections_summary']['labels'][-1]
      last_num = DATA['new']['inspections_summary']['data']['県内'][-1]

      message = generate_count_message(card_title, last_date, last_num, total, unit)
      media_list = ['{}/{}.png'.format(CDN_BASE_URL, card_id)]

      publish_update_message(message, media_list)


def check_update_telephone_advisory_center():
  # 新型コロナコールセンター相談件数
  card_id = 'number-of-reports-to-covid19-telephone-advisory-center'
  card_title = '新型コロナコールセンター相談件数'
  unit = '件'
  if DATA['prev']['contacts']['date'] != DATA['new']['contacts']['date']:
    if generate_image(card_id):
      total = sum([int(data['小計']) for data in DATA['new']['contacts']['data']])
      last_date = DATA['new']['contacts']['data'][-1]['日付']
      last_num = DATA['new']['contacts']['data'][-1]['小計']

      message = generate_count_message(card_title, last_date, last_num, total, unit)
      media_list = ['{}/{}.png'.format(CDN_BASE_URL, card_id)]

      publish_update_message(message, media_list)


def check_update_consultation_desk():
  # 帰国者・接触者相談センター相談件数
  card_id = 'number-of-reports-to-covid19-consultation-desk'
  card_title = '帰国者・接触者相談センター相談件数'
  unit = '件'
  if DATA['prev']['querents']['date'] != DATA['new']['querents']['date']:
    res = requests.get('{}/{}'.format(IMAGE_GENERATOR_BASE_URL, card_id))
    if generate_image(card_id):
      total = sum([int(data['小計']) for data in DATA['new']['querents']['data']])
      last_date = DATA['new']['querents']['data'][-1]['日付']
      last_num = DATA['new']['querents']['data'][-1]['小計']

      message = generate_count_message(card_title, last_date, last_num, total, unit)
      media_list = ['{}/{}.png'.format(CDN_BASE_URL, card_id)]

      publish_update_message(message, media_list)


def check_update():
  # NOTE: must wait CDN cache update
  time.sleep(10)
  # 陽性患者数
  check_update_number_of_confirmed_cases()
  # 検査実施数
  check_update_number_of_tested()
  # 新型コロナコールセンター相談件数
  check_update_telephone_advisory_center()
  # 帰国者・接触者相談センター相談件数
  check_update_consultation_desk()


def main(request):
  DATA['prev'] = load_prev_data()
  generate_patiens_json()
  generate_summary_json()
  generate_inspection_json()
  generate_contacts_json()
  generate_querents_json()
  latest_modified_at = generate_datetime_readable(max(DATETIME_LIST))
  DATA['new']['last_update'] = latest_modified_at
  upload_json(GCP_PROJECT, 'data.json', json.dumps(DATA['new'], ensure_ascii=False))
  check_update()


DATETIME_LIST = []
DATA = {
  'prev': None,
  'new': {
    'contacts': {
      'date': '',
      'data': [],
    },
    'querents': {
      'date': '',
      'data': [],
    },
    'patients': {
      'date': '',
      'data': [],
    },
    'patients_summary': {
      'date': '',
      'data': [],
    },
    'discharges_summary': {
      'date': '',
      'data': [],
    },
    'inspections': {
      'date': '',
      'data': [],
    },
    'inspections_summary': {
      'date': '',
      'data': {
        '県内': [],
        'その他': [],
      },
      'labels': [],
    },
    'last_update': '',
    'main_summary': {
      'attr': '検査実施人数',
      'value': 0,
      'children': [{
        'attr': '陽性患者数',
        'value': 0,
        'children': [{
          'attr': '入院中',
          'value': 0,
          'children': [{
            'attr': '軽症・中等症',
            'value': 0
          }, {
            'attr': '重症',
            'value': 0
          }]
        },{
            'attr': '退院',
            'value': 0
        },{
            'attr': '死亡',
            'value': 0
        }]
      }]
    }
  }
}

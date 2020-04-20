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


def generate_short_datetime(datetime):
  return '{}/{}'.format(datetime.month, datetime.day)


class Patient():
  number = None
  comune_code = None
  pref_name = None
  city_name = None
  announcemented_at = None
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

  def __init__(self, number, comune_code, pref_name, city_name, announcemented_at,
               develop_at, residence, generation, gender, occupation, status,
               symptom, has_travel_history, is_discharged, has_died, note):
    self.number = number
    self.comune_code = comune_code
    self.pref_name = pref_name
    self.city_name = city_name
    self.announcemented_at = get_datetime(announcemented_at)
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

def generate_patiens_data(patients):
  patients_data = []
  patients_count_index = {}
  died_count = 0
  discharged_count = 0
  start_date = None
  end_date = None
  for patient_info in patients[1:]:
    patient = Patient(*patient_info)
    if patient.number == '':
      continue
    if start_date is None:
      start_date = patient.announcemented_at
    end_date = patient.announcemented_at
    announce_iso_time_str = generate_datetime_iso(patient.announcemented_at)
    patients_data.append({
      'リリース日': announce_iso_time_str,
      '曜日': '',
      '居住地': patient.residence,
      '年代': patient.generation,
      '性別': patient.gender,
      '退院': '退院' if patient.is_discharged else '',
      'date': generate_datetime_iso(patient.announcemented_at)
    })
    if patient.has_died:
      died_count += 1
    if patient.is_discharged:
      discharged_count += 1
    if announce_iso_time_str not in patients_count_index:
      patients_count_index[announce_iso_time_str] = 1
    else:
      patients_count_index[announce_iso_time_str] += 1

  patients_summary = []
  discharges_summary = []
  diff_days = (end_date - start_date).days

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

  return patients_data, patients_summary, discharges_summary, died_count, discharged_count


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
  for inspection_info in inspections[1:]:
    ins = Inspection(*inspection_info[:6])
    if ins.implemented_at is None:
      continue
    data_pref.append(ins.people_count)
    data_etc.append(0)
    date_time_iso = generate_datetime_iso(ins.implemented_at)
    labels.append(date_time_iso)
    total_num += ins.people_count

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
  for querents_info in querents[1:]:
    que = Querent(*querents_info[:5])
    if que.accepted_at is None:
      continue
    querents_data.append({
      '日付': generate_datetime_iso(que.accepted_at),
      '曜日': '',
      'date': generate_datetime_iso(que.accepted_at),
      'short_date': generate_short_datetime(que.accepted_at),
      '小計': que.count
    })
  return querents_data


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


# Patients 福島県_新型コロナウイルス陽性患者属性
def generate_patiens_json():
    patients_dir_list = list_dir('http://www.pref.fukushima.lg.jp/w4/covid19/patients/')
    patients_file_latest_uri = patients_dir_list[-1]
    logging.info(patients_file_latest_uri)
    patients_csv_string, patients_csv_datetime = fetch_csv_as_string(patients_file_latest_uri)
    patients = csv_string_to_list(patients_csv_string)
    patients_data, patients_summary, discharges_summary, patient_dided, patient_discharged = generate_patiens_data(patients)
    DATETIME_LIST.append(patients_csv_datetime)
    COVID19_DATA['patients']['date'] = generate_datetime_readable(patients_csv_datetime)
    COVID19_DATA['patients']['data'] = patients_data
    COVID19_DATA['main_summary']['children'][0]['value'] = len(patients_data)
    COVID19_DATA['main_summary']['children'][0]['children'][0]['value'] = len(patients_data) - patient_discharged
    COVID19_DATA['main_summary']['children'][0]['children'][1]['value'] = patient_discharged
    COVID19_DATA['main_summary']['children'][0]['children'][2]['value'] = patient_dided
    COVID19_DATA['patients']['date'] = generate_datetime_readable(patients_csv_datetime)
    COVID19_DATA['patients_summary']['data'] = patients_summary
    COVID19_DATA['discharges_summary']['date'] = generate_datetime_readable(patients_csv_datetime)
    COVID19_DATA['discharges_summary']['data'] = discharges_summary


# Inspections 福島県_新型コロナウイルス検査件数
def generate_inspection_json():
    inspections_dir_list = list_dir('http://www.pref.fukushima.lg.jp/w4/covid19/test_count/')
    inspections_file_latest_uri = inspections_dir_list[-1]
    logging.info(inspections_file_latest_uri)
    inspections_csv_string, inspections_csv_datetime = fetch_csv_as_string(inspections_file_latest_uri)
    inspections = csv_string_to_list(inspections_csv_string)
    data_perf, data_etc, labels, total_num = generate_inspections_data(inspections)
    DATETIME_LIST.append(inspections_csv_datetime)
    COVID19_DATA['inspections']['date'] = generate_datetime_readable(inspections_csv_datetime)
    COVID19_DATA['inspections_summary']['date'] = generate_datetime_readable(inspections_csv_datetime)
    COVID19_DATA['inspections_summary']['data']['県内'] = data_perf
    COVID19_DATA['inspections_summary']['data']['その他'] = data_etc
    COVID19_DATA['inspections_summary']['labels'] = labels
    COVID19_DATA['main_summary']['value'] = total_num


# Contacts 福島県_相談窓口 相談件数
def generate_contacts_json():
    contacts_dir_list = list_dir('http://www.pref.fukushima.lg.jp/w4/covid19/call_center/')
    contacts_file_latest_uri = contacts_dir_list[-1]
    logging.info(contacts_file_latest_uri)
    contacts_csv_string, contacts_csv_datetime = fetch_csv_as_string(contacts_file_latest_uri)
    contacts = csv_string_to_list(contacts_csv_string)
    contacts_data = generate_querents_data(contacts)
    DATETIME_LIST.append(contacts_csv_datetime)
    COVID19_DATA['contacts']['date'] = generate_datetime_readable(contacts_csv_datetime)
    COVID19_DATA['contacts']['data'] = contacts_data


# Querent 福島県_帰国者・接触者相談センター 相談件数
def generate_querents_json():
    querents_dir_list = list_dir('http://www.pref.fukushima.lg.jp/w4/covid19/returnee_contact/')
    querents_file_latest_uri = querents_dir_list[-1]
    logging.info(querents_file_latest_uri)
    querents_csv_string, querents_csv_datetime = fetch_csv_as_string(querents_file_latest_uri)
    querents = csv_string_to_list(querents_csv_string)
    querents_data = generate_querents_data(querents)
    DATETIME_LIST.append(querents_csv_datetime)
    COVID19_DATA['querents']['date'] = generate_datetime_readable(querents_csv_datetime)
    COVID19_DATA['querents']['data'] = querents_data


def main(request):
    generate_patiens_json()
    generate_inspection_json()
    generate_contacts_json()
    generate_querents_json()
    latest_modified_at = generate_datetime_readable(max(DATETIME_LIST))
    COVID19_DATA['last_update'] = latest_modified_at
    upload_json('fukushima-covid19', 'data.json', json.dumps(COVID19_DATA, ensure_ascii=False))


DATETIME_LIST = []
COVID19_DATA = {
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

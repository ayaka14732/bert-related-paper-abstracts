from glob import iglob
import hashlib
import os
import random
import requests
import time

BAIDU_APP_ID = os.environ['BAIDU_APP_ID']
BAIDU_APP_KEY = os.environ['BAIDU_APP_KEY']
API_URL = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def translate_to_chinese(text):
    while True:
        salt = str(random.randrange(32768, 67108864))
        payload = {
            'q': text,
            'from': 'en',
            'to': 'zh',
            'appid': BAIDU_APP_ID,
            'salt': salt,
            'sign': md5(BAIDU_APP_ID + text + salt + BAIDU_APP_KEY)
        }
        print('Retreiving data from', API_URL)
        try:
            response = requests.get(API_URL, params=payload, timeout=2)
        except requests.exceptions.ReadTimeout:
            continue
        if response.status_code != 200:
            print(response.status_code)
            continue
        obj = response.json()
        if 'error_code' in obj:
            print(obj['error_code'])
            continue
        break
    text = '\n'.join(x['dst'] for x in obj['trans_result'])
    return text

uncached_ids = set()

for filename in iglob('cache/summary-en/*.txt'):
    article_id = filename[17:-4]
    filename_chinese = f'cache/summary-zh-cn/{article_id}.txt'
    if not os.path.exists(filename_chinese):
        uncached_ids.add(article_id)

def handle_one(article_id):
    filename = f'cache/summary-en/{article_id}.txt'
    filename_chinese = f'cache/summary-zh-cn/{article_id}.txt'
    with open(filename) as f:
        article_summary = f.read()
    article_summary_chinese = translate_to_chinese(article_summary)
    with open(filename_chinese, 'w') as f:
        f.write(article_summary_chinese)
    time.sleep(0.8)  # speed limit

for article_id in uncached_ids:
    handle_one(article_id)

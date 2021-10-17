from glob import iglob
import re
import requests
from xml.etree import ElementTree

# get all article ids

needed_ids = set()

with open('input.md') as f:
    for line in f:
        line = line.rstrip('\n')
        id_list = re.findall(r'(?<=\(https://arxiv\.org/abs/)[^)]+?(?=\))', line)
        needed_ids.update(id_list)

# get cached article ids

cached_ids = set()

for filename in iglob('cache/summary-en/*.txt'):
    article_id = filename[17:-4]
    cached_ids.add(article_id)

# retrive uncached articles

uncached_ids = needed_ids - cached_ids

def grouper(iterable, n):
    l = list(iterable)
    for i in range(0, len(l), n):
        yield l[i:i+n]

def make_query_url(article_ids):
    return 'http://export.arxiv.org/api/query?id_list=' + ','.join(article_ids)

def store_summary(article_id, article_summary):
    with open(f'cache/summary-en/{article_id}.txt', 'w') as f:
        f.write(article_summary)

for article_ids in grouper(uncached_ids, 10):  # 10 articles in a single query
    query_url = make_query_url(article_ids)
    print('Retreiving data from', query_url)
    response = requests.get(query_url)
    assert response.status_code == 200, response.status_code
    tree = ElementTree.fromstring(response.content)
    for entry in tree.findall('{http://www.w3.org/2005/Atom}entry'):
        article_url = entry.find('{http://www.w3.org/2005/Atom}id').text
        article_id = re.fullmatch(r'http://arxiv\.org/abs/(.+?)(v\d+)?', article_url).group(1)
        article_summary = re.sub(r'\s*\n\s*', ' ', entry.find('{http://www.w3.org/2005/Atom}summary').text.strip())
        store_summary(article_id, article_summary)

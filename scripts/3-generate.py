import re
import sys

lang = sys.argv[1]
summary_dir = sys.argv[2]
input_file = sys.argv[3]
output_file = sys.argv[4]
title = sys.argv[5]

PANDOC_HEADER = '''---
title: ''' + title + '''
lang: ''' + lang + '''
math: |-
  <style>
    body { max-width: inherit; }
    pre { font-family: inherit; font-size: 80%; white-space: pre-wrap; }
    #TOC li { list-style: initial; }

    #TOC + * { counter-reset: article; }
    ul li { counter-increment: article; }
    ul li::before { content: counter(article) ". "; }
    #TOC ul li::before { content: none; }
  </style>
---
'''

def load_summary(article_id):
    with open(f'cache/{summary_dir}/{article_id}.txt') as f:
        return f.read()

with open(input_file) as f, open(output_file, 'w') as g:
    print(PANDOC_HEADER, file=g)

    print('\nStar this project on GitHub: [ayaka14732/bert-related-paper-abstracts](https://github.com/ayaka14732/bert-related-paper-abstracts)\n', file=g)

    print('\nUpstream: [tomohideshibata/BERT-related-papers](https://github.com/tomohideshibata/BERT-related-papers)\n', file=g)

    next(f)  # skip header line because we will generate it by pandoc

    for line in f:
        line = line.rstrip('\n')

        if line == '## Table of Contents':
            while True:
                line = next(f)
                if line.startswith('#'):
                    break
            line = line.rstrip('\n')

        if line.startswith('##'):
            line = line[1:]  # title is different from headings in pandoc, so h2 becomes h1, h3 becomes h2, and so on
            print('\n', line, '\n', sep='', file=g)  # pandoc needs spacing around headers
            continue

        id_list = re.findall(r'(?<=\(https://arxiv\.org/abs/)[^)]+?(?=\))', line)

        if not id_list:
            print(line, file=g)
        else:
            article_id = id_list[0]  # only take the first article
            article_summary = load_summary(article_id)
            print(line, '<pre>', article_summary, '</pre>', sep='', file=g)  # add pre because pandoc complains about broken math equations

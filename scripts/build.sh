#!/bin/bash

wget -nc -O input.md https://github.com/tomohideshibata/BERT-related-papers/raw/master/README.md

# 1-get-summary.py

scripts/retry 100 python scripts/1-get-summary.py

# 2-translate-zh-cn.py

scripts/retry 100 python scripts/2-translate-zh-cn.py

# 3-generate.py

mkdir -p publish/en
mkdir -p publish/zh-CN

python scripts/3-generate.py en summary-en input.md output-en.md 'Abstracts of BERT-Related Papers'
pandoc --listings --toc --toc-depth=2 -s output-en.md -o publish/en/index.html

python scripts/3-generate.py zh-CN summary-zh-cn input.md output-zh-cn.md 'BERT 相关论文摘要'
pandoc --listings --toc --toc-depth=2 -s output-zh-cn.md -o publish/zh-CN/index.html

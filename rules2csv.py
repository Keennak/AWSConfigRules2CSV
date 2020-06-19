import re
import sys
import requests
import csv
import os
import json
import yaml
from pathlib import Path
from bs4 import BeautifulSoup

# AWS公式サイトからAWS Configのマネージドルールのリストを取得するツールです。
# 各マネージドルールが所属するConformance Pack情報もリストします。
#
# 使い方
# インターネットに接続できる環境で実行して下さい。
# 実行すると、カレントディレクトリにCSVファイル(UTF-8)を出力します。
# 
# 制限事項
# AWS 公式サイトの構成が難しく、一部ルールの情報が取得できていません。（要修正ポイント１あたり）
# 現状、取得できないルールはidentifierを"Cannot get Data"としてあります。
# また、同様の制約から、言語を英語で実施すると一部identierに不正な文字が入るケースがあります。

# You can change the description language. 
# However, when You run in English, you fails to get some indicators.
#
# lang ="" # English
lang = "/ja_jp" # Japanese



# get conformance pack yaml code from aws document
def get_cf_pack_list():


    b_uri = "https://docs.aws.amazon.com/config/latest/developerguide/"
    t_uri = "https://docs.aws.amazon.com/config/latest/developerguide/conformancepack-sample-templates.html"
    r = requests.get(t_uri)
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, 'lxml')

    # get config rules pages
    link_list = soup.find(id="main-col-body").find_all("a")
    pack_list = {}

    for page in link_list:

        c_uri = b_uri + page.get('href')
        r2 = requests.get(c_uri)
        r2.encoding = 'utf-8'
        soup2 = BeautifulSoup(r2.text, 'lxml')

        # ExampleとCustomルールは調査から除外する。
        if ('Example' in soup2.h1.text) or ('Custom' in soup2.h1.text):
            continue

        print('---- creating conformance packlist ----- ' + c_uri)
        if soup2.find("code"):
            body = soup2.find("code").text.strip()

            # Create Conformance pack list
            name = re.search(r'[\w-]+.html', page.get('href'))
            pack_name = re.split(r'.html', name.group())[0]

            # Create Rule List
            r = []
            d = yaml.safe_load(body)

            for rule in d.get('Resources'):
                try:
                    r_name = d.get('Resources').get(rule).get(
                        'Properties').get('Source').get('SourceIdentifier')
                    r.append(r_name)
                except:
                    print('ERROR')

            pack_list[pack_name] = r
    print('Conformance Pack list created')
    return(pack_list)



def del_spaces(s):
    # delete indent, tab, sequential spaces
    return(s.replace('\n' , '').replace('\t' , '').replace('  ' , ''))

#
# main
#

# get conformance pack rule list
cf_pack_list = get_cf_pack_list()

# create csv header
additional_headers = list(cf_pack_list.keys())
csv_header_list = ["rule_name", "description", "identifier"]
csv_header_list.extend(additional_headers)

# create config rule list 
b_uri = "https://docs.aws.amazon.com" + lang + "/config/latest/developerguide/"
t_uri = "https://docs.aws.amazon.com" + lang + "/config/latest/developerguide/managed-rules-by-aws-config.html"
r = requests.get(t_uri)
r.encoding = 'utf-8'

soup = BeautifulSoup(r.text, 'lxml')
rules = []

# get config rules pages
link_list = soup.find(id="main-col-body").find_all("a")

# create config rule list
for page in link_list:
    c_uri = b_uri + page.get('href')
    r2 = requests.get(c_uri)
    r2.encoding = 'utf-8'
    soup2 = BeautifulSoup(r2.text, 'lxml')
    description = soup2.find(id="main-col-body").p.text.strip()

    # delete indent, tab, sequential spaces
    description = del_spaces(description)

    # 識別子をmain-col-bodyの２つ目の<p>から切り出す→要修正ポイント１
    print('---- creating rule list ---- ' + soup2.h1.text)
    for i in range(100):
        if ':' in soup2.find(id="main-col-body").find_all("p")[i].text.strip():
            identifier = soup2.find(
                id="main-col-body").find_all("p")[i].text.strip().split(':')[1]

            # delete indent, tab, sequential spaces
            identifier = del_spaces(identifier)

            # delete single space
            identifier = identifier.replace(' ', '')

            # 識別子が取得できたらブレークして結果を出力
            break
    # 識別子が正しく取得できていない場合は、それとわかるように置き換え
    if not re.search(r'\w_', identifier):
        identifier = 'Cannot Get Data'

    # ルール情報をリストに出力する。
    this_rule = {'rule_name': soup2.h1.text,
                 'description': description, 'identifier': identifier}

    # 各識別子がconformance packに含まれているかどうかをリストに追加する。
    for cf_name in additional_headers:
        if identifier in cf_pack_list.get(cf_name):
            this_rule[cf_name] = 'YES'
        else:
            this_rule[cf_name] = '-'

    # 作成したリストを全体の辞書に追加する
    rules.append(this_rule)

# output csv 2 current disk
file_name = "aws_config_managed_rules.csv"
with open(file_name, 'w') as f:
    writer = csv.DictWriter(f, csv_header_list)
    writer.writeheader()
    writer.writerows(rules)
    print('CSV file is created!  ' + file_name)

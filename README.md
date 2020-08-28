# AWSConfigRules2CSV
This script takes a list of AWS Config rules and conformance packs from the AWS official documentation and converts them into CSV.

## How to use
You can execute this script from anywhere you can use AWS CLI. When executed, it outputs a CSV file (UTF-8) to the current directory.

## Modules you need
* pip install requests
* pip install pyyaml
* pip install beautifulsoup4
* pip install lxml

## Execution method
-There are no parameters.

## Limitation
Due to the difficulty of the structure of the AWS official website, some rules information cannot be obtained. Rules ID that cannot be acquired are displayed as "Cannot get Data". In addition, due to the same restriction, if the language is set to English, some identifiers may contain illegal characters.

# AWSConfigRules2CSV
AWS公式サイトからAWS Configのマネージドルールのリストを取得するツールです。
各マネージドルールが所属するConformance Pack情報もリストします。

## 使い方
インターネットに接続できる環境で実行して下さい。
実行すると、カレントディレクトリにCSVファイル(UTF-8)を出力します。

## 実行の前提モジュール
・requestsモジュールが必要です。(pip install requests)
・yamlモジュールが必要です。(pip install pyyaml)
・bs4モジュール(pip install beautifulsoup4)およびパーサ(pip install lxml)が必要です。

## 実行方法
・パラメータはありません。

## 制限
AWS 公式サイトの構成が難しく、一部ルールの情報が取得できていません。（要修正ポイント１あたり）
現状、取得できないルールはidentifierを"Cannot get Data"としてあります。
また、同様の制約から、言語を英語で実施すると一部 identifier に不正な文字が入るケースがあります。

## Reference URL
https://docs.aws.amazon.com/config/latest/developerguide/aws-control-tower-detective-guardrails.html
https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-amazon-dynamodb.html
https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-amazon-s3.html
https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-aws-identity-and-access-management.html
https://docs.aws.amazon.com/config/latest/developerguide/cis-conformance-pack.html
https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-nist-csf.html
https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-pci-dss.html


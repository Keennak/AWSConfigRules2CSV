# AWSConfigRules2CSV
This script gets the list of AWS Config Rules and Conformance Packs from the AWS official document and convert them into CSV.

AWS公式サイトからAWS Configのマネージドルールのリストを取得するツールです。
各マネージドルールが所属するConformance Pack情報もリストします。

## 使い方
インターネットに接続できる環境で実行して下さい。
実行すると、カレントディレクトリにCSVファイル(UTF-8)を出力します。

## 制限
AWS 公式サイトの構成が難しく、一部ルールの情報が取得できていません。（要修正ポイント１あたり）
現状、取得できないルールはidentifierを"Cannot get Data"としてあります。
また、同様の制約から、言語を英語で実施すると一部 identifier に不正な文字が入るケースがあります。

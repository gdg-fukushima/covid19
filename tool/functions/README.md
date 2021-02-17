# 前提条件
このディレクトリ内のスクリプトは、Google Cloud Functions / Py3 環境で動作をする想定で作っています。

CDNが参照しているCloud Storageのバケットに書き込み権限があるFunctionsのサービスアカウントによって実行されると、CDN上のfoobar.jsonを上書きするスクリプトです。このFunctionsを、同一プロジェクト内のCloud Schedulerによってトリガーします。

Functionsは以下の設定になっています。
- HTTPトリガー
- Allow unauthenticated

## generate_data_funciton
data.jsonを更新するスクリプトです。

それぞれのデータ更新日時には、取得してきたCSVの最終更新日の時間が入るようになっています。
サイトのトップに出てくる更新日時は、ファイルの中で最も新しいものを採用するようになっています。
CSVの中身がソートされていなくても、各根拠によってソート（昇順）するようになっています。

## generate_news_function
news.jsonを更新するスクリプトです。

CSVの中身がソートされていなくても、日付によってソート（降順）するようになっています。

## upload_to_twitter
Code for FukushimaのTwitterに投稿するスクリプトです。

Pub/Subのトピックによりトリガーされるように設定されています。

# 前提条件
このディレクトリ内のスクリプトは、Google Cloud Run 環境で動作をする想定で作っています。

## generate_image
指定されたidに基づき、レンダリングされたDOMを画像化し、CDNにホスティングするためのスクリプトです。

ローカルでも以下のようなコマンドで動作を確認することができます。

```sh
docker build -t <tag-name> ./
docker run --rm -p 8080:8080 -e PORT=8080 <tag-name>
```

## Deploy

```sh
cd geerate_image
gcloud builds submit --tag gcr.io/<Project ID>/generate-image
gcloud run deploy --image gcr.io/<Project ID>/generate-image --platform managed
```
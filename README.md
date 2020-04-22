![production deploy](https://github.com/gdg-fukushima/covid19/workflows/production%20deploy/badge.svg)
![staging deploy](https://github.com/gdg-fukushima/covid19/workflows/staging%20deploy/badge.svg)
![development deploy](https://github.com/gdg-fukushima/covid19/workflows/development%20deploy/badge.svg)

# 福島県 新型コロナウイルス感染症対策サイト
このリポジトリのプロジェクトは、[東京都のプロジェクト](https://github.com/tokyo-metropolitan-gov/covid19)から派生させたものです。

[![福島県 新型コロナウイルス感染症対策サイト](https://cdn2.dott.dev/ogp2.png)](https://fukushima-covid19.web.app/)

## 貢献の仕方
Issues にあるいろいろな修正にご協力いただけると嬉しいです。

詳しくは[貢献の仕方](./.github/CONTRIBUTING.md)を御覧ください。


## 行動原則
詳しくは[サイト構築にあたっての行動原則](./.github/CODE_OF_CONDUCT.md)を御覧ください。

## ライセンス
本ソフトウェアは、[MITライセンス](./LICENSE.txt)の元提供されています。

## 開発者向け情報

### 環境構築の手順

- 必要となるNode.jsのバージョン: 10.19.0以上

**yarn を使う場合**
```bash
# install dependencies
$ yarn install

# serve with hot reload at localhost:3000
$ yarn dev
```

**docker compose を使う場合**
```bash
# serve with hot reload at localhost:3000
$ docker-compose up --build
```

### `Cannot find module ****` と怒られた時

**yarn を使う場合**
```bash
$ yarn install
```

**docker compose を使う場合**
```bash
$ docker-compose run --rm app yarn install
```

### GitHub Actionsについて

このリポジトリでは、Actionsによる自動デプロイにはFirebase Hostingのマルチサイトホスティングを利用して、本番・開発・ステージングに対してデプロイを行うようになっています。

**現在は、フォークした先ではFirebase Hostingでのデプロイは機能していません**
https://help.github.com/ja/github/administering-a-repository/disabling-or-limiting-github-actions-for-a-repository

リポジトリ上でActionsによるFirebase Hostingの各環境へデプロイを行う場合は以下のsecretを設定する必要があります。

- FIREBASE_TOKEN（`firebase login:ci`にて得られるトークン）
- HOSTING_DEV_ID（マルチホスティングで設定した開発用サイトのID）
- HOSTING_PRD_ID（マルチホスティングで設定した本番用サイトのID）
- HOSTING_STG_ID（マルチホスティングで設定したステージング用サイトのID）
- PROJECT_ID (GCP/FirebaseのプロジェクトID)

secretsには[@hitokuno](https://github.com/hitokuno)さんのPRで設定する箇所が書いてあります。
https://github.com/gdg-fukushima/covid19/pull/26

# 福島県 新型コロナウイルス感染症対策サイト
※福島県の公式ではありません。
このリポジトリのプロジェクトは、[東京都のプロジェクト](https://github.com/tokyo-metropolitan-gov/covid19)から派生させたものです。

[![福島県 新型コロナウイルス感染症対策サイト](https://user-images.githubusercontent.com/1407941/76877130-4c337a00-68b6-11ea-9fbc-ae0d065a9e41.png)](https://fukushima-covid19.web.app/)

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

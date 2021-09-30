<template>
  <div v-if="dataLoaded" class="MainPage">
    <page-header
      :icon="headerItem.icon"
      :title="headerItem.title"
      :date="headerItem.date"
    />
    <whats-new class="mb-4" :items="newsItems" />
    <static-info
      class="mb-4"
      :url="localePath('/flow')"
      :text="$t('自分や家族の症状に不安や心配があればまずは電話相談をどうぞ')"
      :btn-text="$t('相談の手順を見る')"
    />
    <v-row class="DataBlock">
      <confirmed-cases-details-card :graph-data="Data" />
      <confirmed-cases-attributes-card :graph-data="Data" />
      <confirmed-cases-number-card :graph-data="Data" />
      <tested-number-card :graph-data="Data" />
      <telephone-advisory-reports-number-card :graph-data="Data" />
      <consultation-desk-reports-number-card :graph-data="Data" />
    </v-row>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { MetaInfo } from 'vue-meta'
import axios from 'axios'
import PageHeader from '@/components/PageHeader.vue'
import WhatsNew from '@/components/WhatsNew.vue'
import StaticInfo from '@/components/StaticInfo.vue'
import Data from '@/data/data.json'
import News from '@/data/news.json'
import ConfirmedCasesDetailsCard from '@/components/cards/ConfirmedCasesDetailsCard.vue'
import ConfirmedCasesNumberCard from '@/components/cards/ConfirmedCasesNumberCard.vue'
import ConfirmedCasesAttributesCard from '@/components/cards/ConfirmedCasesAttributesCard.vue'
import TestedNumberCard from '@/components/cards/TestedNumberCard.vue'
import TelephoneAdvisoryReportsNumberCard from '@/components/cards/TelephoneAdvisoryReportsNumberCard.vue'
import ConsultationDeskReportsNumberCard from '@/components/cards/ConsultationDeskReportsNumberCard.vue'

export default Vue.extend({
  components: {
    PageHeader,
    WhatsNew,
    StaticInfo,
    ConfirmedCasesDetailsCard,
    ConfirmedCasesNumberCard,
    ConfirmedCasesAttributesCard,
    TelephoneAdvisoryReportsNumberCard,
    ConsultationDeskReportsNumberCard,
    TestedNumberCard
  },
  data() {
    const data = {
      Data,
      dataLoaded: false,
      headerItem: {
        icon: 'mdi-chart-timeline-variant',
        title: this.$t('福島県内の最新感染動向'),
        date: ''
      },
      newsItems: News.news_items
    }
    return data
  },
  async created() {
    // local data.json will override if data exists.
    try {
      // TODO: get URI from such as global variables
      const dataUri = 'https://cdn2.dott.dev/data.json'
      const graphData = await axios.get(dataUri)
      this.Data = graphData.data
      this.headerItem.date = graphData.data.last_update

      const newsUri = 'https://cdn2.dott.dev/news.json'
      const newsData = await axios.get(newsUri)
      this.newsItems = newsData.data.news_items

      this.dataLoaded = true
    } finally {
    }
  },
  head(): MetaInfo {
    return {
      title: this.$t('福島県内の最新感染動向') as string,
      __dangerouslyDisableSanitizers: ['script'],
      script: [
        {
          innerHTML: `{
              "@context": "https://schema.org",
              "@type": "SpecialAnnouncement",
              "name": "福島県内の新型コロナウイルス感染動向",
              "text": "福島県内における新型コロナウイルスの陽性患者数や属性、PCR検査数などをお知らせしています。",
              "url": "https://fukushima-covid19.web.app/",
              "datePosted": "2020-05-05T00:00",
              "expires": "2021-03-31T23:59",
              "spatialCoverage": [{
                "@context":"https://schema.org/",
                "@type": "AdministrativeArea",
                "name": "福島県"
              }],
              "category": "https://www.wikidata.org/wiki/Q81068910",
              "diseaseSpreadStatistics" : [{
                "@type": "Dataset",
                "name" : "福島県 新型コロナウイルス陽性患者属性",
                "description" : "福島県が公式に発表した、新型コロナウイルス（COVID-19）陽性患者の公表日・居住地・年代・性別・退院・死亡に関するデータ。（注）チャーター機帰国者、クルーズ船乗客等は含まれていない（注）入院中には宿泊療養および自宅療養を含む",
                "sameAs": "https://www.pref.fukushima.lg.jp/sec/21045c/covid19-opendata.html",
                "license": "https://creativecommons.org/licenses/by/2.1/jp/",
                "distribution" : {
                    "@type": "DataDownload",
                    "contentUrl": "https://storage.googleapis.com/fukushima-covid19/csv/patients.csv",
                    "encodingFormat" : "text/csv"
                }
              },{
                "@type": "Dataset",
                "name" : "福島県 新型コロナウイルス検査件数",
                "description" : "福島県が公式に発表した、新型コロナウイルス（COVID-19）におけるPCR検査件数の日次データ。（注）以下は検査実施数に含まれていない 1)チャーター機帰国者、クルーズ船乗客等 2)退院のための検査（注）速報値として公開するものであり、後日確定データとして修正される場合あり",
                "sameAs": "https://www.pref.fukushima.lg.jp/sec/21045c/covid19-opendata.html",
                "license": "https://creativecommons.org/licenses/by/2.1/jp/",
                "distribution" : {
                    "@type": "DataDownload",
                    "contentUrl": "https://storage.googleapis.com/fukushima-covid19/csv/inspections.csv",
                    "encodingFormat" : "text/csv"
                }
              },{
                "@type": "Dataset",
                "name" : "福島県 相談窓口 相談件数",
                "description" : "福島県が公式に発表した、新型コロナウイルス（COVID-19）における受診相談窓口が受け付けた相談件数",
                "sameAs": "https://www.pref.fukushima.lg.jp/sec/21045c/covid19-opendata.html",
                "license": "https://creativecommons.org/licenses/by/2.1/jp/",
                "distribution" : {
                    "@type": "DataDownload",
                    "contentUrl": "https://storage.googleapis.com/fukushima-covid19/csv/contacts.csv",
                    "encodingFormat" : "text/csv"
                }
              },{
                "@type": "Dataset",
                "name" : "福島県 受診・相談センター 相談件数",
                "description" : "福島県が公式に発表した、新型コロナウイルス（COVID-19）における受診・相談センターが受け付けた相談件数",
                "sameAs": "https://www.pref.fukushima.lg.jp/sec/21045c/covid19-opendata.html",
                "license": "https://creativecommons.org/licenses/by/2.1/jp/",
                "distribution" : {
                    "@type": "DataDownload",
                    "contentUrl": "https://storage.googleapis.com/fukushima-covid19/csv/querents.csv",
                    "encodingFormat" : "text/csv"
                }
              }]
            }
          `,
          type: 'application/ld+json'
        }
      ]
    }
  }
})
</script>

<style lang="scss" scoped>
.MainPage {
  .DataBlock {
    margin: 20px -8px;
    .DataCard {
      @include largerThan($medium) {
        padding: 10px;
      }
      @include lessThan($small) {
        padding: 4px 8px;
      }
    }
  }
}
</style>

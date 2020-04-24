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
      :url="
        'https://www.pref.fukushima.lg.jp/sec/21045c/coronavirus-taiou.html'
      "
      :text="$t('自分や家族の症状に不安や心配がある場合（県公式サイト）')"
      :btn-text="$t('公式の情報を見る')"
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
        title: this.$t('県内の最新感染動向'),
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
      title: this.$t('県内の最新感染動向') as string
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

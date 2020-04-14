<template>
  <div>
    <confirmed-cases-details-card
      v-if="this.$route.params.card == 'details-of-confirmed-cases'"
      :graphData="Data"
    />
    <confirmed-cases-number-card
      v-else-if="this.$route.params.card == 'number-of-confirmed-cases'"
      :graphData="Data"
    />
    <confirmed-cases-attributes-card
      v-else-if="this.$route.params.card == 'attributes-of-confirmed-cases'"
      :graphData="Data"
    />
    <tested-number-card
      v-else-if="this.$route.params.card == 'number-of-tested'"
      :graphData="Data"
    />
    <telephone-advisory-reports-number-card
      v-else-if="
        this.$route.params.card ==
          'number-of-reports-to-covid19-telephone-advisory-center'
      "
      :graphData="Data"
    />
    <consultation-desk-reports-number-card
      v-else-if="
        this.$route.params.card ==
          'number-of-reports-to-covid19-consultation-desk'
      "
      :graphData="Data"
    />
    <metro-card
      v-else-if="
        this.$route.params.card == 'predicted-number-of-toei-subway-passengers'
      "
      :graphData="Data"
    />
  </div>
</template>

<script>
import axios from 'axios';
import Data from '@/data/data.json'
import ConfirmedCasesDetailsCard from '@/components/cards/ConfirmedCasesDetailsCard.vue'
import ConfirmedCasesNumberCard from '@/components/cards/ConfirmedCasesNumberCard.vue'
import ConfirmedCasesAttributesCard from '@/components/cards/ConfirmedCasesAttributesCard.vue'
import TestedNumberCard from '@/components/cards/TestedNumberCard.vue'
import TelephoneAdvisoryReportsNumberCard from '@/components/cards/TelephoneAdvisoryReportsNumberCard.vue'
import ConsultationDeskReportsNumberCard from '@/components/cards/ConsultationDeskReportsNumberCard.vue'

export default {
  components: {
    ConfirmedCasesDetailsCard,
    ConfirmedCasesNumberCard,
    ConfirmedCasesAttributesCard,
    TestedNumberCard,
    TelephoneAdvisoryReportsNumberCard,
    ConsultationDeskReportsNumberCard
  },
  data() {
    let title, updatedAt
    switch (this.$route.params.card) {
      case 'details-of-confirmed-cases':
        title = this.$t('検査陽性者の状況')
        updatedAt = Data.inspections_summary.date
        break
      case 'number-of-confirmed-cases':
        title = this.$t('陽性患者数')
        updatedAt = Data.patients.date
        break
      case 'attributes-of-confirmed-cases':
        title = this.$t('陽性患者の属性')
        updatedAt = Data.patients.date
        break
      case 'number-of-tested':
        title = this.$t('検査実施数')
        updatedAt = Data.inspections_summary.date
        break
      case 'number-of-reports-to-covid19-telephone-advisory-center':
        title = this.$t('新型コロナコールセンター相談件数')
        updatedAt = Data.contacts.date
        break
      case 'number-of-reports-to-covid19-consultation-desk':
        title = this.$t('帰国者・接触者相談センター相談件数')
        updatedAt = Data.querents.date
        break
    }

    const data = {
      Data,
      title,
      updatedAt
    }
    return data
  },
  head() {
    const url = 'https://fukushima-covid19.web.app'
    const timestamp = new Date().getTime()
    const ogpImage =
      this.$i18n.locale === 'ja'
        ? `${url}/ogp/${this.$route.params.card}.png?t=${timestamp}`
        : `${url}/ogp/${this.$i18n.locale}/${this.$route.params.card}.png?t=${timestamp}`
    const description = `${this.updatedAt} | ${this.$t(
      '当サイトは新型コロナウイルス感染症 (COVID-19) に関する最新情報を提供するために、Code for Fukushimaの御協力の下、福島県が開設した公式のサイトです。'
    )}`

    return {
      title: this.title,
      meta: [
        {
          hid: 'og:url',
          property: 'og:url',
          content: url + this.$route.path + '/'
        },
        {
          hid: 'og:title',
          property: 'og:title',
          content:
            this.title +
            ' | ' +
            this.$t('福島県') +
            ' ' +
            this.$t('新型コロナウイルス感染症') +
            this.$t('対策サイト')
        },
        {
          hid: 'description',
          name: 'description',
          content: description
        },
        {
          hid: 'og:description',
          property: 'og:description',
          content: description
        },
        {
          hid: 'og:image',
          property: 'og:image',
          content: ogpImage
        },
        {
          hid: 'twitter:image',
          name: 'twitter:image',
          content: ogpImage
        }
      ]
    }
  },
  async asyncData({ params }) {
    // local data.json will override if data exists.
    let data = {}
    try {
      // TODO: get URI from such as global variables
      const dataUri = 'https://cdn2.dott.dev/data.json'
      const graphData = await axios.get(dataUri)
      let updatedAt
      switch (params.card) {
        case 'details-of-confirmed-cases':
          updatedAt = graphData.data.inspections_summary.date
          break
        case 'number-of-confirmed-cases':
          updatedAt = graphData.data.patients.date
          break
        case 'attributes-of-confirmed-cases':
          updatedAt = graphData.data.patients.date
          break
        case 'number-of-tested':
          updatedAt = graphData.data.inspections_summary.date
          break
        case 'number-of-reports-to-covid19-telephone-advisory-center':
          updatedAt = graphData.data.contacts.date
          break
        case 'number-of-reports-to-covid19-consultation-desk':
          updatedAt = graphData.data.querents.date
          break
      }
      data = {
        Data: graphData.data,
        updatedAt
      }
    }
    finally {
      return data
    }
  }
}
</script>

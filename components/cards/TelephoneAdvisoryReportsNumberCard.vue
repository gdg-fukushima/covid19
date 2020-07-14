<template>
  <v-col cols="12" md="6" class="DataCard">
    <time-bar-chart
      id="number-of-reports-to-covid19-telephone-advisory-center"
      :title="$t('新型コロナコールセンター相談件数')"
      :title-id="'number-of-reports-to-covid19-telephone-advisory-center'"
      :chart-id="'time-bar-chart-contacts'"
      :chart-data="contactsGraph"
      :last-acquisite-date="lastAcquisiteDate"
      :date="Data.contacts.date"
      :unit="$t('件.reports')"
      :url="
        'https://www.pref.fukushima.lg.jp/sec/21045c/fukushima-hasseijyoukyou.html'
      "
    />
    <!-- 件.reports = 窓口相談件数 -->
  </v-col>
</template>

<script>
import Data from '@/data/data.json'
import formatGraph from '@/utils/formatGraph'
import TimeBarChart from '@/components/TimeBarChart.vue'

export default {
  components: {
    TimeBarChart
  },
  props: {
    graphData: {
      type: Object,
      required: false,
      default: Data
    }
  },
  data() {
    // 新型コロナコールセンター相談件数
    const contactsGraph = formatGraph(this.graphData.contacts.data)

    // 直近の相談受付日
    const lad = new Date(
      this.graphData.contacts.data[this.graphData.contacts.data.length - 1].date
    )

    const data = {
      Data,
      contactsGraph,
      lastAcquisiteDate: `${lad.getMonth() + 1}/${lad.getDate()}`
    }
    return data
  },
  mounted() {
    this.Data = this.graphData
    this.contactsGraph = formatGraph(this.graphData.contacts.data)
  }
}
</script>

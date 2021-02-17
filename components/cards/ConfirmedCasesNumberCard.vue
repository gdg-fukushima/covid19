<template>
  <v-col cols="12" md="6" class="DataCard">
    <time-bar-chart
      id="number-of-confirmed-cases"
      :title="$t('陽性患者数')"
      :title-id="'number-of-confirmed-cases'"
      :chart-id="'time-bar-chart-patients'"
      :chart-data="patientsGraph"
      :date="graphData.patients.date"
      :last-acquisite-date="lastAcquisiteDate"
      :unit="$t('人')"
      :url="
        'https://www.pref.fukushima.lg.jp/sec/21045c/fukushima-hasseijyoukyou.html'
      "
    />
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
    // 陽性患者数
    const patientsGraph = formatGraph(this.graphData.patients_summary.data)

    // 直近の公表日の取得
    const lastIndex = this.graphData.patients_summary.data.length - 1
    const lad = new Date(
      this.graphData.patients_summary.data[lastIndex]['日付']
    )

    const data = {
      patientsGraph,
      isReady: false,
      lastAcquisiteDate: `${lad.getMonth() + 1}/${lad.getDate()}`
    }
    return data
  },
  mounted() {
    this.Data = this.graphData
    const lastIndex = this.graphData.patients_summary.data.length - 1
    // 直近の公表日の取得
    const lad = new Date(
      this.graphData.patients_summary.data[lastIndex]['日付']
    )
    this.patientsGraph = formatGraph(this.graphData.patients_summary.data)
    this.lastAcquisiteDate = `${lad.getMonth() + 1}/${lad.getDate()}`
    this.isReady = true
  }
}
</script>

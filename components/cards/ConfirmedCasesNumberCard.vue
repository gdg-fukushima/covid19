<template>
  <v-col cols="12" md="6" class="DataCard">
    <time-bar-chart
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
    // 感染者数グラフ
    const patientsGraph = formatGraph(this.graphData.patients_summary.data)

    // 直近の公表日の取得
    let lud = new Date('2000-01-01')
    for (const p of this.graphData.patients.data) {
      const updateDate = new Date(p.date)
      if (updateDate > lud) {
        lud = updateDate
      }
    }

    const data = {
      patientsGraph,
      isReady: false,
      lastAcquisiteDate: `公表日: ${lud.getMonth() + 1}/${lud.getDate()}`
    }
    return data
  },
  mounted() {
    this.Data = this.graphData
    this.patientsGraph = formatGraph(this.graphData.patients_summary.data)
    this.isReady = true
  }
}
</script>

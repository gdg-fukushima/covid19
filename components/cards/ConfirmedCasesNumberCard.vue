<template>
  <v-col cols="12" md="6" class="DataCard">
    <time-bar-chart
      :title="$t('陽性患者数')"
      :title-id="'number-of-confirmed-cases'"
      :chart-id="'time-bar-chart-patients'"
      :chart-data="patientsGraph"
      :date="graphData.patients.date"
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
    const data = {
      patientsGraph,
      isReady: false
    }
    return data
  },
  mounted() {
    this.Data = this.graphData
    this.patientsGraph = formatGraph(this.graphData.patients_summary.data)
    this.isReady = true;
  }
}
</script>

<template>
  <v-col cols="12" md="6" class="DataCard">
    <time-bar-chart
      id="number-of-vaccinated-people"
      :title="$t('ワクチン接種者数')"
      :title-id="'number-of-vaccinated-people'"
      :chart-id="'time-bar-chart-vaccination'"
      :chart-data="vaccinationGraph"
      :date="Data.vaccination.date"
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
    // ワクチン接種者数
    const vaccinationGraph = formatGraph(this.graphData.vaccination.data)

    // 直近の相談受付日
    const lad = new Date(
      this.graphData.vaccination.data[
        this.graphData.vaccination.data.length - 1
      ].date
    )

    const data = {
      Data,
      vaccinationGraph,
      lastAcquisiteDate: `${lad.getMonth() + 1}/${lad.getDate()}`
    }
    return data
  },
  mounted() {
    this.Data = this.graphData
    this.vaccinationGraph = formatGraph(this.graphData.vaccination.data)
  }
}
</script>

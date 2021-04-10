<template>
  <v-col cols="12" md="6" class="DataCard">
    <time-bar-chart-two
      id="number-of-vaccinated-people"
      :title="$t('ワクチン接種者数')"
      :title-id="'number-of-vaccinated-people'"
      :chart-id="'time-bar-chart-vaccination'"
      :chart-data="vaccinationGraph1"
      :chart-data2="vaccinationGraph2"
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
import TimeBarChartTwo from '../TimeBarChartTwo.vue'

export default {
  components: {
    TimeBarChartTwo
  },
  props: {
    graphData: {
      type: Object,
      required: false,
      default: Data
    }
  },
  data() {
    // 1回目のワクチン接種者数
    const vaccinationGraph1 = formatGraph(this.graphData.vaccination.data, 1)
    // 2回目のワクチン接種者数
    const vaccinationGraph2 = formatGraph(this.graphData.vaccination.data, 2)

    // 直近の相談受付日
    const lad = new Date(
      this.graphData.vaccination.data[
        this.graphData.vaccination.data.length - 1
      ].date
    )

    const data = {
      Data,
      vaccinationGraph1,
      vaccinationGraph2,
      lastAcquisiteDate: `${lad.getMonth() + 1}/${lad.getDate()}`
    }
    return data
  },
  mounted() {
    this.Data = this.graphData
  }
}
</script>

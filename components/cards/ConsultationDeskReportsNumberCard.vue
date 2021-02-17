<template>
  <v-col cols="12" md="6" class="DataCard">
    <time-bar-chart
      id="number-of-reports-to-covid19-consultation-desk"
      :title="$t('帰国者・接触者相談センター相談件数')"
      :title-id="'number-of-reports-to-covid19-consultation-desk'"
      :chart-id="'time-bar-chart-querents'"
      :chart-data="querentsGraph"
      :date="Data.querents.date"
      :last-acquisite-date="lastAcquisiteDate"
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
    // 帰国者・接触者相談センター相談件数
    const querentsGraph = formatGraph(this.graphData.querents.data)

    // 直近の相談受付日
    const lad = new Date(
      this.graphData.querents.data[this.graphData.querents.data.length - 1].date
    )

    const data = {
      Data,
      querentsGraph,
      lastAcquisiteDate: `${lad.getMonth() + 1}/${lad.getDate()}`
    }
    return data
  },
  mounted() {
    this.Data = this.graphData
    this.querentsGraph = formatGraph(this.graphData.querents.data)
  }
}
</script>

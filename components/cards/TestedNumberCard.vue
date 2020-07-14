<template>
  <v-col cols="12" md="6" class="DataCard">
    <time-bar-chart
      id="number-of-tested"
      :title="$t('検査実施数')"
      :title-id="'number-of-tested'"
      :chart-id="'time-bar-chart-inspections'"
      :chart-data="inspectionsGraph"
      :last-acquisite-date="lastAcquisiteDate"
      :date="Data.inspections_summary.date"
      :unit="$t('件.tested')"
      :descriptions="[
        '（注）以下は検査実施数に含まれていない',
        '　　・チャーター機帰国者、クルーズ船乗客等', // eslint-disable-line
        '　　・退院のための検査', // eslint-disable-line
        '（注）速報値として公開するものであり、後日確定データとして修正される場合あり'
      ]"
    />
    <!-- 件.tested = 検査数 -->
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
    // 検査実施数
    // '県内'の値のみ利用する
    const zipedSummaryData = this.graphData.inspections_summary.labels.map(
      (e, i) => {
        return {
          日付: e,
          小計: this.graphData.inspections_summary.data['県内'][i]
        }
      }
    )
    const inspectionsGraph = formatGraph(zipedSummaryData)
    const lastAcquisiteDate = `${
      inspectionsGraph[inspectionsGraph.length - 1].label
    }`

    const data = {
      Data,
      inspectionsGraph,
      lastAcquisiteDate
    }
    return data
  },
  mounted() {
    this.Data = this.graphData
    const zipedSummaryData = this.graphData.inspections_summary.labels.map(
      (e, i) => {
        return {
          日付: e,
          小計: this.graphData.inspections_summary.data['県内'][i]
        }
      }
    )
    this.inspectionsGraph = formatGraph(zipedSummaryData)
    this.lastAcquisiteDate = `${
      this.inspectionsGraph[this.inspectionsGraph.length - 1].label
    }`
  }
}
</script>

<template>
  <v-col cols="12" md="6" class="DataCard">
    <time-bar-chart
      :title="$t('検査実施数')"
      :title-id="'number-of-tested'"
      :chart-id="'time-bar-chart-inspections'"
      :chart-data="inspectionsGraph"
      :date="Data.inspections_summary.date"
      :unit="$t('件.tested')"
      :descriptions="[
        '（注）以下は検査実施数に含まれていない',
        '　　・医療機関が保険適用で行った検査',
        '　　・チャーター機帰国者、クルーズ船乗客等',
        '　　・退院のための検査',
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
    // 検査実施日別状況
    // '県内'の値のみ利用する
    const zipedSummaryData = Data.inspections_summary.labels.map((e, i) => {
      return {
        日付: e,
        小計: Data.inspections_summary.data['県内'][i]
      }
    })
    const inspectionsGraph = formatGraph(zipedSummaryData)

    const data = {
      Data,
      inspectionsGraph
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
  }
}
</script>

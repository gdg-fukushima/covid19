<template>
  <v-col cols="12" md="6" class="DataCard">
    <time-bar-chart
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
    // 相談件数
    const contactsGraph = formatGraph(Data.contacts.data)

    // 直近の集計日
    let lud = new Date('2000-01-01')
    for (const p of this.graphData.patients.data) {
      const updateDate = new Date(p.date)
      if (updateDate > lud) {
        lud = updateDate
      }
    }

    const data = {
      Data,
      contactsGraph,
      lastAcquisiteDate: `相談受付日: ${lud.getMonth() + 1}/${lud.getDate()}`
    }
    return data
  },
  mounted() {
    this.Data = this.graphData
    this.contactsGraph = formatGraph(this.graphData.contacts.data)
  }
}
</script>

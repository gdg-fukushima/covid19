<template>
  <data-view :title="title" :title-id="titleId" :date="date" :url="url">
    <template v-slot:button>
      <span v-if="descriptions" class="Graph-Desc">
        <span v-for="(desc, i) in descriptions" :key="i">
          {{ $t(desc) }}<br />
        </span>
      </span>
      <data-selector v-model="dataKind" :target-id="chartId" />
    </template>
    <scrollable-chart v-show="canvas" :display-data="displayData">
      <template v-slot:chart="{ chartWidth }">
        <bar
          :chart-id="chartId"
          :chart-data="displayData"
          :options="displayOption"
          :height="240"
          :width="chartWidth"
        />
      </template>
      <template v-slot:sticky-chart>
        <bar
          class="sticky-legend"
          :chart-id="`${chartId}-header`"
          :chart-data="displayDataHeader"
          :options="displayOptionHeader"
          :plugins="yAxesBgPlugin"
          :height="240"
        />
      </template>
    </scrollable-chart>
    <template v-slot:infoPanel>
      <data-view-basic-info-panel
        :l-text="displayInfo.lText"
        :s-text="displayInfo.sText"
        :lad-text="displayInfo.ladText"
        :unit="displayInfo.unit"
      />
    </template>
  </data-view>
</template>

<script lang="ts">
import Vue from 'vue'
import { ThisTypedComponentOptionsWithRecordProps } from 'vue/types/options'
import { Chart } from 'chart.js'
import dayjs from 'dayjs'
import { TranslateResult } from 'vue-i18n'
import DataView from '@/components/DataView.vue'
import DataSelector from '@/components/DataSelector.vue'
import DataViewBasicInfoPanel from '@/components/DataViewBasicInfoPanel.vue'
import ScrollableChart from '@/components/ScrollableChart.vue'
import { DisplayData, yAxesBgPlugin } from '@/plugins/vue-chart'
import { getComplementedDate } from '@/utils/formatDate'
import { GraphDataType } from '@/utils/formatGraph'

type TableHeader = {
  text: TranslateResult
  value: string
  align?: string
}
type TableItem = {
  text: string
  transition?: string
  cumulative?: string
  [key: number]: number
}
type Data = {
  dataKind: 'transition' | 'cumulative'
  canvas: boolean
}
type Methods = {
  formatDayBeforeRatio: (dayBeforeRatio: number) => string
}
type Computed = {
  displayCumulativeRatio: string
  displayTransitionRatio: string
  displayInfo: {
    lText: string
    sText: string
    unit: string
  }
  displayData: DisplayData
  displayOption: Chart.ChartOptions
  displayDataHeader: DisplayData
  displayOptionHeader: Chart.ChartOptions
  scaledTicksYAxisMax: number
  tableHeaders: TableHeader[]
  tableData: TableItem[]
}
type Props = {
  title: string
  titleId: string
  chartId: string
  chartData: GraphDataType[]
  lastAcquisiteDate: string
  date: string
  unit: string
  url: string
  descriptions: string[]
  yAxesBgPlugin: Chart.PluginServiceRegistrationOptions[]
}

const options: ThisTypedComponentOptionsWithRecordProps<
  Vue,
  Data,
  Methods,
  Computed,
  Props
> = {
  created() {
    this.canvas = process.browser
    this.dataKind =
      this.$route.query.embed && this.$route.query.dataKind === 'cumulative'
        ? 'cumulative'
        : 'transition'
  },
  components: {
    DataView,
    DataSelector,
    DataViewBasicInfoPanel,
    ScrollableChart
  },
  props: {
    title: {
      type: String,
      default: ''
    },
    titleId: {
      type: String,
      default: ''
    },
    chartId: {
      type: String,
      default: 'time-bar-chart'
    },
    chartData: {
      type: Array,
      default: () => []
    },
    lastAcquisiteDate: {
      type: String,
      required: true
    },
    date: {
      type: String,
      required: true
    },
    unit: {
      type: String,
      default: ''
    },
    url: {
      type: String,
      default: ''
    },
    descriptions: {
      type: Array,
      default: null
    },
    yAxesBgPlugin: {
      type: Array,
      default: () => yAxesBgPlugin
    }
  },
  data: () => ({
    dataKind: 'transition',
    canvas: true
  }),
  computed: {
    displayCumulativeRatio() {
      const lastDay = this.chartData.slice(-1)[0].cumulative
      const lastDayBefore = this.chartData.slice(-2)[0].cumulative
      return this.formatDayBeforeRatio(lastDay - lastDayBefore)
    },
    displayTransitionRatio() {
      const lastDay = this.chartData.slice(-1)[0].transition
      const lastDayBefore = this.chartData.slice(-2)[0].transition
      return this.formatDayBeforeRatio(lastDay - lastDayBefore)
    },
    displayInfo() {
      if (this.dataKind === 'transition') {
        return {
          lText: `${this.chartData.slice(-1)[0].transition.toLocaleString()}`,
          sText: `${this.$t('実績値')}（${this.$t('前日比')}: ${
            this.displayTransitionRatio
          } ${this.unit}）`,
          ladText: this.lastAcquisiteDate,
          unit: this.unit
        }
      }
      return {
        lText: this.chartData[
          this.chartData.length - 1
        ].cumulative.toLocaleString(),
        sText: `${this.chartData.slice(-1)[0].label} ${this.$t(
          '累計値'
        )}（${this.$t('前日比')}: ${this.displayCumulativeRatio} ${
          this.unit
        }）`,
        ladText: '',
        unit: this.unit
      }
    },
    displayData() {
      const zeroMouseOverHeight = 0

      if (this.dataKind === 'transition') {
        return {
          labels: this.chartData.map(d => {
            return d.label
          }),
          datasets: [
            {
              label: this.dataKind,
              data: this.chartData.map(d => {
                return d.transition
              }),
              backgroundColor: '#00B849',
              borderWidth: 0,
              minBarLength: this.chartData.map(d => {
                if (d.transition <= 0) {
                  return zeroMouseOverHeight
                }
                return 0
              })
            }
          ]
        }
      }
      return {
        labels: this.chartData.map(d => d.label),
        datasets: [
          {
            label: this.dataKind,
            data: this.chartData.map(d => {
              return d.cumulative
            }),
            backgroundColor: '#00B849',
            borderWidth: 0,
            minBarLength: this.chartData.map(d => {
              if (d.transition <= 0) {
                return zeroMouseOverHeight
              }
              return 0
            })
          }
        ]
      }
    },
    displayOption() {
      const unit = this.unit
      const scaledTicksYAxisMax = this.scaledTicksYAxisMax
      const options: Chart.ChartOptions = {
        tooltips: {
          displayColors: false,
          callbacks: {
            label(tooltipItem) {
              const labelText = `${parseInt(
                tooltipItem.value!
              ).toLocaleString()} ${unit}`
              return labelText
            },
            title: (tooltipItem, data) => {
              const label = data.labels![tooltipItem[0].index!] as string
              return label.replace('-', '年').replace('-', '月') + '日'
            }
          }
        },
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        scales: {
          xAxes: [
            {
              id: 'day',
              stacked: true,
              gridLines: {
                display: false
              },
              ticks: {
                fontSize: 9,
                maxTicksLimit: 20,
                fontColor: '#808080',
                maxRotation: 0,
                minRotation: 0,
                callback: (label: string) => {
                  return dayjs(label).format('D')
                }
              }
            },
            {
              id: 'month',
              stacked: true,
              gridLines: {
                drawOnChartArea: false,
                drawTicks: true,
                drawBorder: false,
                tickMarkLength: 10
              },
              ticks: {
                fontSize: 11,
                fontColor: '#808080',
                maxRotation: 0,
                padding: 3,
                fontStyle: 'bold'
              },
              type: 'time',
              time: {
                unit: 'month',
                displayFormats: {
                  month: 'YYYY-MM'
                }
              }
            }
          ],
          yAxes: [
            {
              position: 'left',
              gridLines: {
                display: true,
                drawOnChartArea: true,
                color: '#E5E5E5'
              },
              ticks: {
                maxTicksLimit: 8,
                fontColor: '#808080',
                suggestedMin: 0,
                suggestedMax: scaledTicksYAxisMax
              }
            }
          ]
        }
      }
      if (this.$route.query.ogp === 'true') {
        Object.assign(options, { animation: { duration: 0 } })
      }
      return options
    },
    displayDataHeader() {
      if (this.dataKind === 'transition') {
        return {
          labels: ['2020/1/1'],
          datasets: [
            {
              data: [Math.max(...this.chartData.map(d => d.transition))],
              backgroundColor: 'transparent',
              borderWidth: 0
            }
          ]
        }
      }
      return {
        labels: ['2020/1/1'],
        datasets: [
          {
            data: [Math.max(...this.chartData.map(d => d.cumulative))],
            backgroundColor: 'transparent',
            borderWidth: 0
          }
        ]
      }
    },
    displayOptionHeader() {
      const scaledTicksYAxisMax = this.scaledTicksYAxisMax
      const options: Chart.ChartOptions = {
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        tooltips: { enabled: false },
        scales: {
          xAxes: [
            {
              id: 'day',
              stacked: true,
              gridLines: {
                display: false
              },
              ticks: {
                fontSize: 9,
                maxTicksLimit: 20,
                fontColor: 'transparent',
                maxRotation: 0,
                minRotation: 0,
                callback: (label: string) => {
                  return label.split('/')[1]
                }
              }
            },
            {
              id: 'month',
              stacked: true,
              gridLines: {
                drawOnChartArea: false,
                drawTicks: false, // true -> false
                drawBorder: false,
                tickMarkLength: 10
              },
              ticks: {
                fontSize: 11,
                fontColor: 'transparent', // #808080
                padding: 13, // 3 + 10(tickMarkLength)
                fontStyle: 'bold',
                callback: (label: string) => {
                  const monthStringArry = [
                    'Jan',
                    'Feb',
                    'Mar',
                    'Apr',
                    'May',
                    'Jun',
                    'Jul',
                    'Aug',
                    'Sep',
                    'Oct',
                    'Nov',
                    'Dec'
                  ]
                  const month = monthStringArry.indexOf(label.split(' ')[0]) + 1
                  return month + '月'
                }
              },
              type: 'time',
              time: {
                unit: 'month'
              }
            }
          ],
          yAxes: [
            {
              stacked: true,
              gridLines: {
                display: true,
                drawOnChartArea: false,
                color: '#E5E5E5' // #E5E5E5
              },
              ticks: {
                suggestedMin: 0,
                maxTicksLimit: 8,
                fontColor: '#808080', // #808080
                suggestedMax: scaledTicksYAxisMax
              }
            }
          ]
        },
        animation: { duration: 0 }
      }
      return options
    },
    scaledTicksYAxisMax() {
      const yAxisMax = 1.2
      const dataKind =
        this.dataKind === 'transition' ? 'transition' : 'cumulative'
      const values = this.chartData.map(d => d[dataKind])
      return Math.max(...values) * yAxisMax
    },
    tableHeaders() {
      return [
        { text: this.$t('日付'), value: 'text' },
        {
          text: `${this.title} (${this.$t('日別')})`,
          value: 'transition',
          align: 'end'
        },
        {
          text: `${this.title} (${this.$t('累計')})`,
          value: 'cumulative',
          align: 'end'
        }
      ]
    },
    tableData() {
      return this.chartData
        .map((d, _) => {
          return {
            text: this.$d(
              new Date(getComplementedDate(d.label)),
              'dateWithoutYear'
            ),
            transition: d.transition.toLocaleString(),
            cumulative: d.cumulative.toLocaleString()
          }
        })
        .sort((a, b) => dayjs(a.text).unix() - dayjs(b.text).unix())
        .reverse()
    }
  },
  methods: {
    formatDayBeforeRatio(dayBeforeRatio: number): string {
      const dayBeforeRatioLocaleString = dayBeforeRatio.toLocaleString()
      switch (Math.sign(dayBeforeRatio)) {
        case 1:
          return `+${dayBeforeRatioLocaleString}`
        case -1:
          return `${dayBeforeRatioLocaleString}`
        default:
          return `${dayBeforeRatioLocaleString}`
      }
    }
  }
}

export default Vue.extend(options)
</script>

<style lang="scss" scoped>
.Graph-Desc {
  width: 100%;
  margin: 0;
  font-size: 12px;
  color: $gray-3;
}
</style>

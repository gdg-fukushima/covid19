<template>
  <div :class="$style.container">
    <p :class="$style.heading">
      <span :class="[$style.icon, $style.top]" aria-hidden="true">
        <HumanIcon />
      </span>
      <span :class="$style.fzMedium">{{ $t('一般の方') }}</span>
    </p>
    <ul :class="[$style.rectContainer, $style.triple]">
      <li :class="$style.symptom">
        {{ $t('高熱') }}
      </li>
      <li :class="$style.symptom">
        {{ $t('発熱が続く') }}
      </li>
      <li :class="$style.symptom">
        {{ $t('咳が続く') }}
      </li>
    </ul>
    <ul :class="[$style.rectContainer, $style.double]">
      <li :class="$style.symptom">
        <span :class="$style.fzRegular">
          {{ $t('強いだるさ') }}<br />
          <span :class="$style.fzSmall">（{{ $t('倦怠感') }}）</span>
        </span>
      </li>
      <li :class="$style.symptom">
        <span :class="$style.fzRegular">
          {{ $t('息苦しさ') }}<br />
          <span :class="$style.fzSmall">（{{ $t('呼吸困難') }}）</span>
        </span>
      </li>
    </ul>
    <a
      v-scroll-to="{
        el: '#consult',
        onDone: onDoneScroll
      }"
      href="#consult"
      :class="[$style.button, $style.clickable]"
    >
      <span :class="$style.text">{{ $t('帰国者・接触者相談センター') }}</span>
      <ArrowForwardIcon :class="$style.icon" />
    </a>
  </div>
</template>

<script lang="ts">
import { onDoneScroll } from '@/utils/vueScrollTo'
import HumanIcon from '@/static/flow/responsive/accessibility.svg'
import ArrowForwardIcon from '@/static/flow/responsive/arrow_forward.svg'
export default {
  components: { HumanIcon, ArrowForwardIcon },
  methods: { onDoneScroll }
}
</script>

<style module lang="scss">
@import '@/components/flow/flow_sp.scss';
</style>

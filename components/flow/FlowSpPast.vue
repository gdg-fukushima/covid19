<template>
  <div :class="$style.container">
    <div :class="$style.heading">
      {{ $t('「新型コロナウイルス感染者」との濃厚接触が疑われる方') }}
    </div>
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
import ArrowForwardIcon from '@/static/flow/responsive/arrow_forward.svg'

export default {
  components: { ArrowForwardIcon },
  methods: { onDoneScroll }
}
</script>

<style module lang="scss">
@import '@/components/flow/flow_sp.scss';

// past
.type {
  margin-top: px2vw(20);
  text-align: center;
  &.hr {
    margin-top: px2vw(30);
    padding-top: px2vw(30);
    border-top: 1px $gray-4 solid;
  }
}

@include largerThan($small) {
  $vw: 960;
  .type {
    margin-top: px2vw(20, $vw);
    &.hr {
      margin-top: px2vw(30, $vw);
      padding-top: px2vw(30, $vw);
    }
  }
}
</style>

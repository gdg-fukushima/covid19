<template>
  <div :class="$style.container">
    <p :class="$style.heading">
      <span :class="[$style.icon, $style.top]">
        <SentimentIcon aria-hidden="true" />
      </span>
      <span :class="$style.fzMedium">{{ $t('不安に思う方') }}</span>
    </p>

    <ul :class="[$style.rectContainer, $style.double]">
      <li :class="$style.symptom">
        {{ $t('健康の不安') }}
      </li>
      <li :class="$style.symptom">
        {{ $t('感染の不安') }}
      </li>
    </ul>

    <div :class="$style.callcenter">
      <p :class="$style.fzLarge">
        {{ $t('一般相談') }}
        <span :class="$style.fzSmall">({{ $t('コールセンター') }})</span>
      </p>
      <p :class="$style.open">
        {{ $t('平日：午前8時30分から午後9時') }}<br />
        {{ $t('土日祝日：午前8時30分から午後5時15分') }}
      </p>
      <p :class="[$style.phone, $style.fzNumeric]">
        <span :class="$style.icon">
          <PhoneIcon alt="Phone" />
        </span>
        <a :class="$style.TelLink" href="tel:0120-567-177">0120-567-177</a>
      </p>
      <p :class="[$style.phone, $style.fzNumeric]">
        {{ $t('FAX 024-521-7926') }}
      </p>
      <p :class="$style.fzSmall">（{{ $t('耳の不自由な方') }})</p>
    </div>

    <a
      v-scroll-to="{
        el: '#consult',
        onDone: onDoneScroll
      }"
      href="#consult"
      :class="[$style.button, $style.clickable]"
    >
      <span :class="$style.text">{{ $t('専門的な助言が必要な場合') }}</span>
      <ArrowForwardIcon :class="$style.icon" />
    </a>
  </div>
</template>

<script lang="ts">
import { onDoneScroll } from '@/utils/vueScrollTo'
import ArrowForwardIcon from '@/static/flow/responsive/arrow_forward.svg'
import PhoneIcon from '@/static/flow/responsive/phone.svg'
import SentimentIcon from '@/static/flow/responsive/sentiment_very_dissatisfied.svg'

export default {
  components: { ArrowForwardIcon, PhoneIcon, SentimentIcon },
  methods: { onDoneScroll }
}
</script>

<style module lang="scss">
@import '@/components/flow/flow_sp.scss';

// suspect
.callcenter {
  margin-top: px2vw(25);
  text-align: center;
  .open {
    margin-top: px2vw(10);
  }
}

@include largerThan($small) {
  $vw: 960;
  // suspect
  .callcenter {
    margin-top: px2vw(25, $vw);
    .open {
      margin-top: px2vw(10, $vw);
    }
  }
}
</style>

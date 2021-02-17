<template>
  <div id="warries" :class="$style.container">
    <p :class="$style.heading">
      <span :class="[$style.icon, $style.top]">
        <SentimentIcon aria-hidden="true" />
      </span>
      <span :class="$style.fzMedium">{{ $t('相談をしたい方') }}</span>
    </p>
    <div :class="[$style.rectContainer, $style.double]">
      <a
        v-scroll-to="'#mental'"
        :class="[$style.rect, $style.result, $style.clickable]"
        href="#mental"
      >
        <p>
          <i18n path="ストレスや不安" />
        </p>
        <div :class="$style.arrow" aria-hidden="true">
          <Arrow />
        </div>
      </a>
      <a
        v-scroll-to="'#smear'"
        :class="[$style.rect, $style.result, $style.clickable]"
        href="#smear"
      >
        <p>
          <i18n path="誹謗中傷の被害" />
        </p>
        <div :class="$style.arrow" aria-hidden="true">
          <Arrow />
        </div>
      </a>
      <a
        v-scroll-to="'#consult'"
        :class="[$style.rect, $style.result, $style.clickable]"
        href="#consult"
      >
        <p>
          <i18n path="県の対策や予防法" />
        </p>
        <div :class="$style.arrow" aria-hidden="true">
          <Arrow />
        </div>
      </a>
    </div>
  </div>
</template>

<script lang="ts">
import { onDoneScroll } from '@/utils/vueScrollTo'
import SentimentIcon from '@/static/flow/responsive/sentiment_very_dissatisfied.svg'
import Arrow from '@/static/flow/responsive/arrow_downward.svg'

export default {
  components: {
    Arrow,
    SentimentIcon
  },
  methods: { onDoneScroll }
}
</script>

<style module lang="scss">
@import '@/components/flow/flow_sp.scss';

.rectContainer {
  .rect {
    min-height: px2vw(188);
    padding: px2vw(20) px2vw(10);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-content: center;
    flex: 0 0 48%;
    border-radius: px2vw(6);
    font-size: px2vw(24);
    text-decoration: none !important;
    color: inherit !important;
    text-align: center;
    font-weight: bold;
    &.result {
      // icon
      padding-bottom: px2vw((56 + 20 * 2));
      position: relative;
    }
    &.solution {
      border: px2vw(3) solid $gray-4;
      // icon
      padding-top: px2vw((46 + 20 * 2));
      position: relative;
    }
    &.consult {
      border: px2vw(3) solid $green-1;
      flex-basis: 100%;
    }
    &.bgYellow {
      background-color: #ffe200;
    }
    &:nth-child(n + 3) {
      margin-top: px2vw((486 - 233 - 233));
    }
    .large {
      font-size: px2vw(42);
    }
    .advisory {
      font-size: px2vw(38);
      display: block;
      margin-top: px2vw(10);
      margin-bottom: px2vw(10);
    }
    .line {
      margin-top: px2vw(5);
      display: block;
    }
    .arrow,
    .icon {
      margin: 0 auto;
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
    }
    .arrow {
      width: px2vw(56);
      height: px2vw(56);
      bottom: px2vw(20);
    }
    .icon {
      width: px2vw(46);
      height: px2vw(46);
      top: px2vw(20);
    }
  }
}

@include largerThan($small) {
  $vw: 960;
  .according {
    .diag {
      margin-top: px2vw(30, $vw);
      &.hr {
        padding-top: px2vw(30, $vw);
      }
    }
    .decision {
      margin-top: px2vw(20, $vw);
      padding: px2vw(20, $vw);
      border-radius: px2vw(6, $vw);
    }
    .note {
      text-align: left;
      margin-top: px2vw(10, $vw);
    }
    .fzXLLarge {
      font-size: px2vw(56, $vw);
    }
  }
  .rectContainer {
    .rect {
      min-height: px2vw(188, $vw);
      padding: px2vw(20, $vw) px2vw(10, $vw);
      border-radius: px2vw(6, $vw);
      font-size: px2vw(24, $vw);
      &.result {
        padding-bottom: px2vw((56 + 20 * 2), $vw);
      }
      &.solution {
        border: px2vw(3, $vw) solid $gray-4;
        padding-top: px2vw((46 + 20 * 2), $vw);
      }
      &.consult {
        border: px2vw(3, $vw) solid $green-1;
      }
      &:nth-child(n + 3) {
        margin-top: px2vw((486 - 233 - 233), $vw);
      }
      .large {
        font-size: px2vw(42, $vw);
      }
      .advisory {
        font-size: px2vw(38, $vw);
        margin-top: px2vw(10, $vw);
        margin-bottom: px2vw(10, $vw);
      }
      .line {
        margin-top: px2vw(5, $vw);
      }
      .arrow {
        width: px2vw(56, $vw);
        height: px2vw(56, $vw);
        bottom: px2vw(20, $vw);
      }
      .icon {
        width: px2vw(46, $vw);
        height: px2vw(46, $vw);
        top: px2vw(20, $vw);
      }
    }
  }
}
</style>

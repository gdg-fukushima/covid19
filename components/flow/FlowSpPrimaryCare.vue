<template>
  <div :class="$style.container">
    <h4 id="primary-care" :class="[$style.heading, $style.fzXLarge]">
      {{ $t('まずは身近な医療機関に') }}<br />
      {{ $t('電話でご相談ください') }}
    </h4>
    <h4 :class="[$style.heading, $style.fzXLarge]">
      {{ $t('かかりつけ医など身近な医療機関') }}
    </h4>
    <p :class="[$style.open, $style.fzMedium]">
      <span>
        {{ $t('受診・相談センター、') }}<br />
        {{ $t('または診療・検査医療機関を') }}<br />
        {{ $t('案内する場合があります') }}
      </span>
    </p>
  </div>
</template>

<style module lang="scss">
@import '@/components/flow/flow_sp.scss';

// advisory
.open {
  margin-top: px2vw(20);
  display: flex;
  justify-content: center;
  > span {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: $white;
    color: $green-1;
    padding: px2vw(20) px2vw(40);
    border-radius: px2vw(6);
  }
}
.daytime {
  margin-top: px2vw(20);
  display: flex;
  border-top: 1px solid $gray-4;
  border-bottom: 1px solid $gray-4;
  > * {
    padding: px2vw(30) px2vw(40);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .title {
    text-align: center;
    flex-basis: 40%;
  }
  .link {
    flex-basis: 100%;
    > a {
      text-decoration: none;
    }
  }
}
.night {
  margin: px2vw(30) auto;
  padding-left: 0 !important;
  text-align: center;
  > li {
    list-style-type: none;
    &:not(:first-child) {
      margin-top: px2vw(20);
    }
  }
}

@include largerThan($small) {
  $vw: 960;
  .open {
    margin-top: px2vw(20, $vw);
    > span {
      padding: px2vw(20) px2vw(40, $vw);
      border-radius: px2vw(6, $vw);
    }
  }
  .daytime {
    margin-top: px2vw(20, $vw);
    > * {
      padding: px2vw(30) px2vw(10, $vw);
    }
  }
  .night {
    margin: px2vw(30, $vw) auto;
    > li {
      &:not(:first-child) {
        margin-top: px2vw(20, $vw);
      }
    }
  }
}
</style>

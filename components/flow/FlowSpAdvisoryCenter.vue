<template>
  <div :class="$style.container">
    <h4 id="advisory-center" :class="[$style.heading, $style.fzXLarge]">
      {{ $t('受診・相談センター') }}
    </h4>
    <p :class="[$style.phone, $style.fzNumeric]">
      <span :class="$style.icon">
        <PhoneIcon alt="Phone" />
      </span>
      <a :class="$style.TelLink" href="tel:0120-567-747">0120-567-747</a>
    </p>
    <p :class="[$style.open, $style.fzMedium]">
      <span>{{ $t('24時間対応') }}</span>
    </p>
    <p :class="[$style.text, $style.fzMedium]">
      {{ $t('耳の不自由な方') }}<br />
      {{ $t('FAX 024-521-7926') }}
    </p>
  </div>
</template>

<script lang="ts">
import PhoneIcon from '@/static/flow/responsive/phone.svg'

export default {
  components: { PhoneIcon }
}
</script>

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
.text {
  margin-top: px2vw(20);
  display: flex;
  justify-content: center;
  align-items: center;
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

<template>
  <div :class="$style.container">
    <h4 id="smear" :class="[$style.heading, $style.fzXLarge]">
      {{ $t('新型コロナウイルス感染症に関する') }}<br />
      {{ $t('誹謗中傷等被害の相談窓口') }}
    </h4>
    <p :class="[$style.phone, $style.fzNumeric]">
      <span :class="$style.icon">
        <PhoneIcon alt="Phone" />
      </span>
      <a :class="$style.TelLink" href="tel:024-521-8647">024-521-8647</a>
    </p>
    <p :class="[$style.open, $style.fzMedium]">
      <span>{{ $t('平日：午前9時から午後5時') }}</span>
    </p>
    <dl>
      <div :class="$style.daytime">
        <dd :class="$style.link">
          <a href="https://kokoro-musubu.com/" target="_blank" rel="noopener">
            {{ $t('誹謗中傷等防止特設サイト') }}
            <v-icon size="16">
              mdi-open-in-new
            </v-icon>
          </a>
        </dd>
      </div>
    </dl>
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

<template>
  <div :class="$style.FlowCard">
    <h3>{{ $t('相談窓口について') }}</h3>
    <div :class="[$style.Outer, $style.OuterUpper]">
      <div :class="[$style.CardBlock____, $style.Causion]">
        <flow-pc-causion />
      </div>
      <div :class="[$style.CardBlock, $style.General]">
        <flow-pc-general />
      </div>
      <div :class="[$style.CardBlock, $style.Warries]">
        <flow-pc-warries />
      </div>
      <div
        :class="[
          $style.CardBlock,
          $style.CardBlockPrimaryCare,
          $style.PrimaryContact
        ]"
      >
        <flow-pc-primary-contact />
      </div>
      <div
        :class="[
          $style.CardBlock,
          $style.CardBlockPrimaryCare,
          $style.PrimaryCare
        ]"
      >
        <flow-pc-primary-care />
      </div>
      <div
        :class="[
          $style.CardBlock,
          $style.CardBlockAdvisoryCenter,
          $style.AdvisoryCenter
        ]"
      >
        <flow-pc-advisory-center />
      </div>
      <div
        :class="[
          $style.CardBlock,
          $style.CardBlockGeneralCare,
          $style.GeneralCare
        ]"
      >
        <flow-pc-general-care />
      </div>
      <div :class="[$style.CardBlock, $style.CardBlockMental, $style.Mental]">
        <flow-pc-mental />
      </div>
      <div :class="[$style.CardBlock, $style.CardBlockSmear, $style.Smear]">
        <flow-pc-smear />
      </div>
      <div
        :class="[$style.CardBlock, $style.CardBlockAdvisory2, $style.Advisory2]"
      >
        <flow-pc-advisory2 />
      </div>
    </div>
    <h3>
      <i18n
        :class="$style.TitleSmall"
        tag="span"
        path="{advisory}による相談・診察結果"
      >
        <span :class="$style.TitleLarge" place="advisory">
          {{ $t('かかりつけ医等の医療機関') }}
        </span>
      </i18n>
    </h3>
    <div :class="[$style.Outer, $style.OuterLower]">
      <div
        :class="[$style.CardBlock, $style.CardBlockRequired, $style.Required]"
      >
        <flow-pc-required />
      </div>
      <div :class="[$style.CardBlock, $style.CardBlockPcr, $style.Pcr]">
        <flow-pc-pcr />
      </div>
      <div :class="$style.NotRequired">
        <flow-pc-not-required />
      </div>
      <div :class="$style.Hospitalized">
        <flow-pc-hospitalized />
      </div>
    </div>
    <p :class="$style.Note">
      {{
        $t(
          '※保険適用となる検査は、当面の間、院内感染防止等の観点から、「帰国者・接触者外来」等の医療機関で実施'
        )
      }}
    </p>
  </div>
</template>

<script>
import FlowPcCausion from './FlowPcCausion.vue'
import FlowPcGeneral from './FlowPcGeneral.vue'
import FlowPcWarries from './FlowPcWarries.vue'
import FlowPcPrimaryCare from './FlowPcPrimaryCare.vue'
import FlowPcPrimaryContact from './FlowPcPrimaryContact.vue'
import FlowPcAdvisoryCenter from './FlowPcAdvisoryCenter.vue'
import FlowPcGeneralCare from './FlowPcGeneralCare.vue'
import FlowPcMental from './FlowPcMental.vue'
import FlowPcSmear from './FlowPcSmear.vue'
import FlowPcAdvisory2 from './FlowPcAdvisory2.vue'
import FlowPcRequired from './FlowPcRequired.vue'
import FlowPcPcr from './FlowPcPcr.vue'
import FlowPcNotRequired from './FlowPcNotRequired.vue'
import FlowPcHospitalized from './FlowPcHospitalized.vue'

export default {
  components: {
    FlowPcCausion,
    FlowPcGeneral,
    FlowPcWarries,
    FlowPcPrimaryCare,
    FlowPcPrimaryContact,
    FlowPcAdvisoryCenter,
    FlowPcGeneralCare,
    FlowPcMental,
    FlowPcSmear,
    FlowPcAdvisory2,
    FlowPcRequired,
    FlowPcPcr,
    FlowPcNotRequired,
    FlowPcHospitalized
  }
}
</script>

<style module lang="scss">
.FlowCard {
  display: flex;
  flex-direction: column;
  @include card-container();

  padding: 20px;
  margin-bottom: 20px;
  word-break: break-word;
  hyphens: auto;
  > h3 {
    color: $gray-2;
    font-size: 1.5rem;
    margin-bottom: 7px;
  }
  &GrayBg {
    background-color: $gray-5;
  }
}
.Outer {
  display: grid;
  &Upper {
    grid-template-columns: 40% 30% 30%;
    -ms-grid-columns: calc(40% - 24px) 12px 30% 12px 30%;
    grid-template-rows: repeat(6, auto);
    -ms-grid-rows: auto 12px auto 12px auto 12px auto 12px auto 12px auto;
    // HACK: IEでGridの順番がうまくいかない対応
    // https://github.com/tokyo-metropolitan-gov/covid19/issues/1313
    & > *:nth-child(1) {
      -ms-grid-column: 1;
      -ms-grid-row: 1;
      -ms-grid-column-span: 5;
    }
    & > *:nth-child(2) {
      -ms-grid-column: 1;
      -ms-grid-row: 3;
      -ms-grid-row-span: 3;
    }
    & > *:nth-child(3) {
      -ms-grid-column: 1;
      -ms-grid-row: 7;
      -ms-grid-row-span: 5;
    }
    & > *:nth-child(4) {
      -ms-grid-column: 3;
      -ms-grid-row: 3;
    }
    & > *:nth-child(5) {
      -ms-grid-column: 5;
      -ms-grid-row: 3;
    }
    & > *:nth-child(6) {
      -ms-grid-column: 3;
      -ms-grid-row: 5;
    }
    & > *:nth-child(7) {
      -ms-grid-column: 5;
      -ms-grid-row: 5;
    }
    & > *:nth-child(8) {
      -ms-grid-column: 3;
      -ms-grid-row: 7;
      -ms-grid-column-span: 3;
    }
    & > *:nth-child(9) {
      -ms-grid-column: 3;
      -ms-grid-row: 9;
      -ms-grid-column-span: 3;
    }
    & > *:nth-child(10) {
      -ms-grid-column: 3;
      -ms-grid-row: 11;
      -ms-grid-column-span: 3;
    }

    margin-bottom: 36px;
  }
  &Lower {
    grid-template-columns: repeat(2, calc(50% - 6px));
    -ms-grid-columns: calc(50% - 6px) 12px calc(50% - 6px);
    grid-template-rows: repeat(6, auto);
    -ms-grid-rows: auto 12px auto 12px auto 12px auto 12px auto 12px auto;
    // HACK: IEでGridの順番がうまくいかない対応
    // https://github.com/tokyo-metropolitan-gov/covid19/issues/1313
    & > *:nth-child(1) {
      -ms-grid-column: 1;
      -ms-grid-row: 1;
    }
    & > *:nth-child(2) {
      -ms-grid-column: 1;
      -ms-grid-row: 3;
      -ms-grid-row-span: 3;
    }
    & > *:nth-child(3) {
      -ms-grid-column: 3;
      -ms-grid-row: 1;
      -ms-grid-row-span: 3;
    }
    & > *:nth-child(4) {
      -ms-grid-column: 3;
      -ms-grid-row: 5;
    }
  }
}
.Title {
  @include font-size(28);

  color: $green-1;
  &Small {
    @include font-size(20);
  }
  &Large {
    @include font-size(28);
  }
}
.CardBlock {
  position: relative;
  &Center::after {
    bottom: 40%;
  }
  &PrimaryContact::before {
    content: url('/flow/flow_arrow.svg');
    position: absolute;
    bottom: 30%;
    left: -16px;
    z-index: 1;
    display: block;
    width: 46px;
    height: 46px;
    transform: rotateZ(0deg);
  }
  &PrimaryCare::before {
    content: url('/flow/flow_arrow.svg');
    position: absolute;
    bottom: 30%;
    left: -16px;
    z-index: 1;
    display: block;
    width: 46px;
    height: 46px;
    transform: rotateZ(0deg);
  }
  &AdvisoryCenter::before {
    content: url('/flow/flow_arrow.svg');
    position: absolute;
    bottom: 40%;
    left: -16px;
    z-index: 1;
    display: block;
    width: 46px;
    height: 46px;
    transform: rotateZ(0deg);
  }
  &GeneralCare::before {
    content: url('/flow/flow_arrow.svg');
    position: absolute;
    bottom: 40%;
    left: -16px;
    z-index: 1;
    display: block;
    width: 46px;
    height: 46px;
    transform: rotateZ(0deg);
  }
  &Mental::before {
    content: url('/flow/flow_arrow.svg');
    position: absolute;
    bottom: 40%;
    left: -16px;
    z-index: 1;
    display: block;
    width: 46px;
    height: 46px;
    transform: rotateZ(-30deg);
  }
  &Smear::before {
    content: url('/flow/flow_arrow.svg');
    position: absolute;
    bottom: 40%;
    left: -16px;
    z-index: 1;
    display: block;
    width: 46px;
    height: 46px;
    transform: rotateZ(0deg);
  }
  &Advisory2::before {
    content: url('/flow/flow_arrow.svg');
    position: absolute;
    bottom: 50%;
    left: -16px;
    z-index: 1;
    display: block;
    width: 46px;
    height: 46px;
    transform: rotateZ(30deg);
  }

  &Required::after {
    content: url('/flow/flow_arrow.svg');
    position: absolute;
    z-index: 1;
    display: block;
    width: 46px;
    height: 46px;
    bottom: -30px;
    right: auto;
    left: 22%;
    transform: rotate(90deg);
  }
  &Required::before {
    content: url('/flow/flow_arrow.svg');
    position: absolute;
    bottom: 12%;
    right: -30px;
    z-index: 1;
    display: block;
    width: 46px;
    height: 46px;
  }
  &Pcr::after {
    content: url('/flow/flow_arrow.svg');
    position: absolute;
    bottom: auto;
    right: -30px;
    z-index: 1;
    display: block;
    width: 46px;
    height: 46px;
    top: 15%;
    transform: rotateZ(-30deg);
  }
  &Pcr::before {
    content: url('/flow/flow_arrow.svg');
    position: absolute;
    bottom: 15%;
    right: -30px;
    z-index: 1;
    display: block;
    width: 46px;
    height: 46px;
    transform: rotateZ(30deg);
  }
}
.Causion {
  grid-column: 1 / 4;
  grid-row: 1 / 2;
}
.General {
  grid-column: 1 / 2;
  grid-row: 2 / 4;
}

.Warries {
  grid-column: 1 / 2;
  grid-row: 4 / 7;
}

.PrimaryContact {
  grid-column: 2 / 3;
  grid-row: 2 / 3;
}

.PrimaryCare {
  grid-column: 3 / 4;
  grid-row: 2 / 3;
}
.AdvisoryCenter {
  grid-column: 2 / 3;
  grid-row: 3 / 4;
}

.GeneralCare {
  grid-column: 3 / 4;
  grid-row: 3 / 4;
}

.Mental {
  grid-column: 2 / 4;
  grid-row: 4 / 5;
}

.Smear {
  grid-column: 2 / 4;
  grid-row: 5 / 6;
}

.Advisory2 {
  grid-column: 2 / 4;
  grid-row: 6 / 7;
}

.Required {
  grid-column: 1 / 2;
  grid-row: 1 / 2;
}
.Pcr {
  grid-column: 1 / 2;
  grid-row: 2 / 4;
}
.NotRequired {
  grid-column: 2 / 3;
  grid-row: 1 / 3;
}
.Hospitalized {
  grid-column: 2 / 3;
  grid-row: 3 / 4;
}
.Note {
  margin: 16px 0;
}
</style>

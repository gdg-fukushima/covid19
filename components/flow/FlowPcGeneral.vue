<template>
  <div :class="$style.Flow">
    <div :class="$style.FlowRow">
      <div :class="$style.FlowRowRowThree">
        <p :class="$style.FlowRowRowThreeGeneral">
          <img
            :class="$style.FlowRowRowThreeGeneralIcon"
            src="/flow/accessibility-24px.svg"
            aria-hidden="true"
          />
          {{ $t('一般の方') }}
        </p>
      </div>
    </div>
    <div :class="[$style.FlowRow, $style.FlowRowRowCheck]">
      <div :class="$style.FlowRowCondition">
        <p>{{ $t('高熱') }}</p>
        <img
          :class="$style.FlowRowConditionIcon"
          src="/flow/check_circle-24px.svg"
          aria-hidden="true"
        />
      </div>
      <div :class="$style.FlowRowCondition">
        <p>
          {{ $t('強いだるさ') }}
          <span :class="$style.FlowRowConditionSmall">
            （{{ $t('倦怠感') }}）
          </span>
        </p>
        <img
          :class="$style.FlowRowConditionIcon"
          src="/flow/check_circle-24px.svg"
          aria-hidden="true"
        />
      </div>
      <div :class="$style.FlowRowCondition">
        <p>
          {{ $t('息苦しさ') }}
          <span :class="$style.FlowRowConditionSmall">
            （{{ $t('呼吸困難') }}）
          </span>
        </p>
        <img
          :class="$style.FlowRowConditionIcon"
          src="/flow/check_circle-24px.svg"
          aria-hidden="true"
        />
      </div>
      <div :class="$style.FlowRowCondition">
        <p>{{ $t('発熱が続く') }}</p>
        <img
          :class="$style.FlowRowConditionIcon"
          src="/flow/check_circle-24px.svg"
          aria-hidden="true"
        />
      </div>
      <div :class="$style.FlowRowCondition">
        <p>{{ $t('咳が続く') }}</p>
        <img
          :class="$style.FlowRowConditionIcon"
          src="/flow/check_circle-24px.svg"
          aria-hidden="true"
        />
      </div>
    </div>
  </div>
</template>

<style module lang="scss">
.Flow {
  @include card-container($withDivider: false);

  display: flex;
  flex-direction: row;
  padding: 10px 20px !important;
  position: relative;
  color: $gray-2;
  &Row {
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 36%;
    display: flex;
    flex-direction: column;
    text-align: center;
    &RowCheck {
      flex-basis: calc(28% - 20px);
      margin: 10px 10px;
    }
    &RowThree {
      flex-grow: 3;
      display: flex;
      align-items: center;
      justify-content: center;
      &General {
        &Icon {
          display: block;
          margin: auto;
          width: 44px;
          height: 44px;
        }
      }
      &CareTargetList {
        margin: 0 0 0 -16px;
        padding-left: 0 !important;
        text-align: left;
        list-style: none;
        &Item {
          display: flex;
          align-items: center;
          &Icon {
            display: inline-block;
            width: 30px;
            height: 30px;
          }
        }
        &Item + &Item {
          margin-top: 14px;
        }
      }
    }
    &Condition {
      flex-grow: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 10px;
      padding: 10px;
      position: relative;
      border: 2px solid $green-1 !important;
      border-radius: 2px;
      background-color: $white;
      p {
        text-align: center;
        display: inline-block;
        margin: 0 !important; // FIXME: IEだとv-applicationのmarginが優先される
        font-size: calc(0.875rem + ((1vw - 7.68px) * 0.8929));
        font-weight: bold;
        @include largerThan($large) {
          font-size: 20px;
        }
      }
      &Large {
        font-size: calc(1rem + ((1vw - 7.68px) * 2.4876));
        @include largerThan($large) {
          font-size: 25px;
        }
      }
      &Small {
        font-size: 15px;
      }

      &Icon {
        position: absolute;
        left: -8px;
        top: -8px;
        width: 24px;
        height: 24px;
      }

      &::before {
        position: absolute;
        left: -4px;
        top: -4px;
        width: 20px;
        height: 20px;
        background-color: white;
        content: '';
      }
    }
    &Emphasis {
      font-size: 24px;
      font-weight: bold;
      border-bottom: solid 3px $green-1;
      &Day {
        font-size: 41px;
      }
    }
  }
}
</style>

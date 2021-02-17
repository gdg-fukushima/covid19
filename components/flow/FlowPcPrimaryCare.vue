<template>
  <div :class="$style.FlowComponent">
    <div :class="[$style.SubtleBox, $style.Box1, $style.Center]">
      <div :class="$style.LargerText">
        {{ $t('かかりつけ医など身近な医療機関') }}
      </div>
      <div :class="$style.SmallerText">
        {{ $t('受診・相談センター、または診療・検査医療機関を') }}<br />
        {{ $t('案内する場合があります') }}
      </div>
      <div :class="$style.Examination">
        {{ $t('診察・検査') }}
      </div>
    </div>
  </div>
</template>

<style module lang="scss">
.FlowComponent {
  color: $gray-2;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  height: 100%;
}

.SubtleBox {
  @include card-container();

  display: flex;
  justify-content: space-evenly;
  align-items: center;
  padding: 0.5em;
}

.Box1 {
  flex-grow: 0;
  flex-shrink: 0;
  width: 100%;
  flex-direction: column;
  justify-content: center;
  div {
    margin: 0.5em;
  }
  &Icon {
    position: absolute;
    bottom: 40%;
    right: -30px;
    z-index: 1;
    display: block;
    width: 46px;
    height: 46px;
  }
}

.LargerText {
  font-size: larger;
  font-weight: bold;
}

.Center {
  text-align: center;
}

.SmallerText {
  font-size: smaller;
}

.Examination {
  border-radius: 4px;
  border: 2px solid #008830;
  line-height: 1;
  font-size: 1.25em;
  padding: 0.5rem 2rem;
  background: $green-1;
  color: $white;
}
</style>

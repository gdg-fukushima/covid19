<template>
  <div :class="$style.FlowComponent">
    <div :class="[$style.SubtleBox, $style.Box1, $style.Center]">
      <div :class="$style.LargerText">
        {{ $t('新型コロナウイルス感染症に関する誹謗中傷等被害の相談窓口') }}
      </div>
      <div :class="$style.SmallerText">
        {{ $t('平日：午前9時から午後5時') }}
      </div>

      <div :class="$style.Tel">
        <a :class="$style.TelLink" href="tel:024-521-8647">
          <img
            :class="$style.TelLinkIcon"
            src="/flow/phone-24px.svg"
            aria-hidden="true"
          />
          024-521-8647
        </a>
      </div>
      <div :class="$style.LargerText">
        <a href="https://kokoro-musubu.com/" target="_blank" rel="noopener">
          <span>{{ $t('誹謗中傷等防止特設サイト') }}</span>
          <v-icon size="18">
            mdi-open-in-new
          </v-icon>
        </a>
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

.Tel {
  @include largerThan($medium) {
    font-size: larger;
  }
}
.TelLink {
  display: flex;
  align-items: center;
  font-weight: bold;
  &:link,
  &:visited,
  &:hover,
  &:active,
  &:focus {
    color: inherit;
    text-decoration: none;
  }
  &Icon {
    display: inline-block;
    margin-right: 5px;
    width: 26px;
    height: 26px;
  }
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
</style>

<template>
  <div :class="$style.FlowPcHospitalized">
    <div :class="$style.Row">
      <p :class="$style.FlowPcHospitalizedHeading">
        <img
          :class="$style.FlowPcHospitalizedHeadingIcon"
          src="/flow/hotel-24px.svg"
          aria-hidden="true"
        />
        {{ $t('感染症指定医療機関等') }}
      </p>
      <p :class="$style.FlowPcHospitalizedsubHeading">
        {{ $t('入院') }}
      </p>
    </div>
    <div :class="$style.TwoRow">
      <p :class="$style.Note">
        {{ $t('軽症者療養施設への宿泊の場合があります') }}
      </p>
    </div>
  </div>
</template>

<style module lang="scss">
.FlowPcHospitalized {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: column;
  padding: 30px 15px 30px 20px;
  color: $gray-2;
  @include card-container();

  &Heading {
    color: $gray-2;
    display: flex;
    align-items: center;
    margin: 0 !important;
    padding: 0 5px 0 0;

    &Icon {
      min-width: 30px;
      min-height: 30px;
      display: block;
      margin-right: 10px;
    }
  }

  &subHeading {
    @include font-size(20);

    margin: 0 !important;
  }
}

.Row {
  flex-grow: 1;
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin-bottom: 15px;
}

.TwoRow {
  flex-grow: 1;
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin-bottom: 15px;
}
</style>

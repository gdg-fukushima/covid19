<template>
  <section :class="$style.Flow">
    <div :class="$style.FlowHeading">
      {{ $t('「新型コロナウイルス感染者」との濃厚接触が疑われる方') }}
    </div>
  </section>
</template>

<style module lang="scss">
.Flow {
  @include card-container($withDivider: false);

  position: relative;
  padding: 20px;
  color: $gray-2;
  text-align: center;
  &Heading {
    position: relative;
    width: calc(100% - 2px);
    margin: 0 0 0 1px;
    background-color: $white;
    padding: 5px;
    text-align: center;
    font-weight: bold;
    font-size: 16px;
  }
}
</style>

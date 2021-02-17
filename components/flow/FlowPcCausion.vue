<template>
  <section :class="$style.Flow">
    <div :class="$style.FlowHeading">
      {{
        $t(
          '注意・対応が必要なため、医療機関に行く前に必ず電話で相談してください。'
        )
      }}
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
    font-size: 24px;
  }
}
</style>

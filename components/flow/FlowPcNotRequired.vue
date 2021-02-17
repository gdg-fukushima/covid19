<template>
  <div :class="$style.flowContainer">
    <h3 :class="$style.sectionTitle">
      <i18n path="{advice}と判断された場合" tag="p">
        <strong place="advice">
          {{ $t('検査が不要') }}
        </strong>
      </i18n>
    </h3>
    <h3 :class="$style.sectionTitle">
      <i18n path="{advice}の場合" tag="p">
        <strong place="advice">
          {{ $t('検査結果が陰性') }}
        </strong>
      </i18n>
    </h3>
    <div :class="$style.actionContainer">
      <ul :class="$style.actions">
        <li :class="$style.actionsList">
          <img
            :class="$style.actionsListIcon"
            src="/flow/house-24px.svg"
            aria-hidden="true"
          />
          {{ $t('自宅で安静に過ごす') }}
        </li>
      </ul>
      <div :class="$style.nextAction">
        <i18n path="{getWorse}{advisory}に改めて相談" :class="$style.content">
          <span place="getWorse">{{ $t('症状が良くならない場合は') }}</span>
          <strong place="advisory">
            {{ $t('受診した') }}<br />
            {{ $t('医療機関') }}
          </strong>
        </i18n>
      </div>
    </div>
  </div>
</template>

<style module lang="scss">
.flowContainer {
  @include card-container();

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  padding: 20px;
  height: 100%;
  color: $gray-2;
}
.sectionTitle {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 100%;
  margin-bottom: 1rem;
  strong {
    margin: 0 0.2em;
    font-size: 28px;
    font-weight: bold;
  }
}
.actionContainer {
  display: flex;
  justify-content: space-between;
}
.actions {
  width: 49%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-left: 0 !important; // FIXME: for ul element
}
.actionsList {
  list-style-type: none;
  text-align: start;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  &Icon {
    min-width: 30px;
    min-height: 30px;
    display: block;
    margin-right: 10px;
  }
}
.icon {
  margin-right: 10px;
}
.nextAction {
  width: 49%;
  padding: 1rem;
  border: $green-1 1.5px solid;
  border-radius: 4px;
  text-align: center;
  .content {
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: space-around;
  }
  strong {
    font-size: 1.5rem;
  }
}
</style>

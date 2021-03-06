<template>
  <div class="SideNavigation">
    <header class="SideNavigation-HeadingContainer sp-flex">
      <v-icon
        class="SideNavigation-HeadingIcon pc-none"
        :aria-label="$t('サイドメニュー項目を開く')"
        @click="openNavi"
      >
        mdi-menu
      </v-icon>
      <nuxt-link :to="localePath('/')" class="SideNavigation-HeadingLink">
        <h1 class="SideNavigation-Heading">
          <div class="SideNavigation-Logo">
            <img
              src="https://cdn2.dott.dev/logo2.svg"
              :alt="$t('福島県コロナ対策サイト')"
            />
          </div>
          {{ $t('新型コロナウイルス感染症') }}
          <br />
          {{ $t('対策サイト') }}
        </h1>
      </nuxt-link>
    </header>
    <v-divider class="SideNavigation-HeadingDivider" />
    <div class="sp-none" :class="{ open: isNaviOpen }">
      <v-icon
        class="SideNavigation-ListContainerIcon pc-none"
        :aria-label="$t('サイドメニュー項目を閉じる')"
        @click="closeNavi"
      >
        mdi-close
      </v-icon>
      <nav>
        <v-list :flat="true">
          <v-container
            v-for="(item, i) in items"
            :key="i"
            class="SideNavigation-ListItemContainer"
            @click="closeNavi"
          >
            <ListItem :link="item.link" :icon="item.icon" :title="item.title" />
            <v-divider v-show="item.divider" class="SideNavigation-Divider" />
          </v-container>
        </v-list>
        <div class="SideNavigation-LanguageMenu">
          <div
            v-if="this.$i18n.locales.length > 1"
            class="SideNavigation-Language"
          >
            <label class="SideNavigation-LanguageLabel" for="LanguageSelector">
              {{ $t('多言語対応選択メニュー') }}
            </label>
            <LanguageSelector />
          </div>
        </div>
      </nav>
      <v-footer class="SideNavigation-Footer">
        <div class="SideNavigation-SocialLinkContainer">
          <a
            href="https://twitter.com/CODEforFKSM"
            target="_blank"
            rel="noopener"
          >
            <img src="https://cdn2.dott.dev/twitter.png" alt="Twitter" />
          </a>
          <a
            href="https://www.facebook.com/Code-for-Fukushima-104771331183649"
            target="_blank"
            rel="noopener"
          >
            <img src="https://cdn2.dott.dev/facebook.png" alt="Facebook" />
          </a>
          <a
            href="https://github.com/gdg-fukushima/covid19"
            target="_blank"
            rel="noopener"
          >
            <img src="https://cdn2.dott.dev/github.png" alt="GitHub" />
          </a>
        </div>
        <small class="SideNavigation-Copyright">
          {{ $t('このサイトの内容物は') }}
          <a
            rel="license"
            target="_blank"
            :href="$t('https://creativecommons.org/licenses/by/4.0/deed.ja')"
          >
            {{ $t('クリエイティブ・コモンズ 表示 4.0 ライセンス') }}
          </a>
          {{ $t('の下に提供されています。') }}
          <br />
          2020 Code for Fukushima
        </small>
      </v-footer>
      <div class="SideNavigation-SponsorLinkContainer">
        {{ $t('Powered by:') }}<br />
        <a
          href="https://www.pref.fukushima.lg.jp/"
          target="_blank"
          rel="noopener"
        >
          <span class="image-title">{{ $t('福島県') }}</span>
          <img
            class="fukushima-logo"
            src="https://cdn2.dott.dev/logo_fukushima.svg"
            :alt="$t('福島県')"
          />
        </a>
        <br />
        <nuxt-link :to="{ path: localePath('/about/') }">
          <span class="image-title">{{ $t('Code for Fukushima') }}</span>
          <img
            class="cff-logo"
            src="https://cdn2.dott.dev/logo_cff.svg"
            :alt="$t('Code for Fukushima')"
          />
        </nuxt-link>
        <br />
        {{ $t('Sponsored by:') }}
        <br />
        <a href="https://cloud.google.com/" target="_blank" rel="noopener">
          <span class="image-title">{{ $t('Google Cloud') }}</span>
          <img
            class="google-logo"
            src="https://cdn2.dott.dev/logo_google_cloud.svg"
            :alt="$t('Google Cloud')"
          />
        </a>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { TranslateResult } from 'vue-i18n'
import LanguageSelector from '@/components/LanguageSelector.vue'
import ListItem from '@/components/ListItem.vue'

type Item = {
  icon?: string
  title: TranslateResult
  link: string
  divider?: boolean
}

export default Vue.extend({
  components: {
    ListItem,
    LanguageSelector
  },
  props: {
    isNaviOpen: {
      type: Boolean,
      required: true
    }
  },
  computed: {
    items(): Item[] {
      return [
        {
          icon: 'mdi-chart-timeline-variant',
          title: this.$t('福島県内の最新感染動向'),
          link: this.localePath('/')
        },
        {
          icon: 'covid',
          title: this.$t('新型コロナウイルス感染症が心配なときに'),
          link: this.localePath('/flow')
        },
        {
          title: this.$t('感染が疑われる場合の症状・対応等'),
          link:
            'https://www.pref.fukushima.lg.jp/sec/21045c/coronavirus-taiou.html',
          divider: true
        },
        {
          title: this.$t('福島県【新型コロナ】関連情報一覧'),
          link:
            'https://www.pref.fukushima.lg.jp/sec/21045c/coronavirus-list.html'
        },
        {
          title: this.$t('YouTube: 新型コロナウイルス感染症関連【速報】'),
          link:
            'https://www.youtube.com/playlist?list=PLX7ij_QBlO5QlNpkBrYDwWEJ-LcBrUq4G'
        },
        {
          title: this.$t('福島県新型コロナウイルス感染症対策本部員会議'),
          link:
            'https://www.pref.fukushima.lg.jp/sec/21045c/coronavirus-honbukaigi.html'
        },
        {
          title: this.$t('知事からのメッセージ'),
          link:
            'https://www.pref.fukushima.lg.jp/sec/21045c/governor-message.html'
        },
        {
          title: this.$t('当サイトについて'),
          link: this.localePath('/about')
        }
      ]
    }
  },
  methods: {
    openNavi(): void {
      this.$emit('openNavi')
    },
    closeNavi(): void {
      this.$emit('closeNavi')
    }
  }
})
</script>

<style lang="scss" scoped>
.SideNavigation {
  background: $white;
  position: relative;
  height: 100%;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.15);
  &-HeadingContainer {
    padding: 1.25em 0 1.25em 1.25em;
    align-items: center;
    @include lessThan($small) {
      padding: 7px 10px;
    }
  }
  &-HeadingIcon {
    margin-right: 10px;
  }
  &-HeadingLink {
    @include lessThan($small) {
      display: flex;
      align-items: center;
    }

    text-decoration: none;
  }
  &-ListContainerIcon {
    width: 21px;
    margin: 24px 16px 0;
  }
  &-ListItemContainer {
    padding: 2px 20px;
  }
  &-Logo {
    margin: 5px 16px 15px 0;
    width: 110px;
    @include lessThan($small) {
      margin: 0 16px 0 0;
    }
  }
  &-Heading {
    margin-top: 8px;
    font-size: 13px;
    color: #707070;
    padding: 0.5em 0;
    text-decoration: none;
    @include lessThan($small) {
      display: flex;
      align-items: center;
      width: 100%;
      margin-top: 0;
    }
  }
  &-HeadingDivider {
    margin: 0 20px 4px;
    @include lessThan($small) {
      display: none;
    }
  }
  &-Divider {
    margin: 12px 0;
  }
  &-LanguageMenu {
    padding: 0 20px;
    background: #fff;
  }
  &-Footer {
    padding: 20px;
    background-color: $white;
  }
  &-SponsorLinkContainer {
    overflow: visible;
    padding-left: 1.2rem;
    white-space: normal;
    font-size: 0.82rem;
    color: $gray-1;
    & a {
      color: #333;
      text-decoration: none;
    }
    & a:hover {
      opacity: 0.6;
    }
    & img {
      padding-bottom: 0.9rem;
    }
    & img.fukushima-logo {
      margin: 0 0 0 5px;
      width: 100px;
    }
    & img.cff-logo {
      margin: 0 0 0 5px;
      width: 100px;
    }
    & img.google-logo {
      margin: 5px 0 0 10px;
      width: 130px;
    }
    & .image-title {
      display: inline-block;
      width: 0;
      height: 1.5rem;
      overflow: hidden;
    }
    & .no-image-title {
      display: inline-block;
      line-height: 1.8rem;
      color: #444;
      font-size: 1.5rem;
      font-weight: 400;
    }
  }
  &-SocialLinkContainer {
    display: flex;
    & a:not(:last-of-type) {
      margin-right: 10px;
    }
    & img {
      width: 30px;
    }
  }
  &-Copyright {
    display: block;
    margin-top: 10px;
    font-size: 8px;
    line-height: 1.2;
    color: $gray-1;
    font-weight: bold;
  }
}
.open {
  @include lessThan($small) {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    display: block !important;
    width: 100%;
    z-index: z-index-of(opened-side-navigation);
    background-color: $white;
    height: 100%;
    overflow-y: scroll;
  }
}
@include lessThan($tiny) {
  .sp-logo {
    width: 100px;
  }
}
@include largerThan($small) {
  .pc-none {
    display: none;
  }
}
@include lessThan($small) {
  .sp-flex {
    display: flex;
  }
  .sp-none {
    display: none;
  }
}
</style>

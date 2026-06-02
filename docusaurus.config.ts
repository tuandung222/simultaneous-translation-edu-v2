import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

const config: Config = {
  title: 'Simultaneous Translation Edu',
  tagline: 'Giáo trình tiếng Việt về simultaneous translation, latency, policy và streaming sequence generation',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
    faster: true,
  },

  url: 'https://tuandung222.github.io',
  baseUrl: '/simultaneous-translation-edu-v2/',
  organizationName: 'tuandung222',
  projectName: 'simultaneous-translation-edu-v2',
  trailingSlash: false,
  onBrokenLinks: 'warn',

  headTags: [
    {
      tagName: 'meta',
      attributes: {
        name: 'robots',
        content: 'noindex,nofollow,noarchive,nosnippet',
      },
    },
  ],

  i18n: {
    defaultLocale: 'vi',
    locales: ['vi'],
    localeConfigs: {
      vi: {label: 'Tiếng Việt', htmlLang: 'vi-VN'},
    },
  },

  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  themes: ['@docusaurus/theme-mermaid'],

  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css',
      type: 'text/css',
      integrity:
        'sha384-nB0miv6/jRmo5UMMR1wu3Gz6NLsoTkbqJghGIsx//Rlm+ZU03BU6SQNC66uf4l5+',
      crossorigin: 'anonymous',
    },
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: 'docs',
          editUrl: 'https://github.com/tuandung222/simultaneous-translation-edu/edit/main/',
          remarkPlugins: [remarkMath],
          rehypePlugins: [
            [rehypeKatex, {strict: false}]
          ],
          showLastUpdateTime: false,
          numberPrefixParser: false,
        },
        blog: false,
        sitemap: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/social-card.svg',
    navbar: {
      title: 'Simultaneous Translation Edu',
      items: [
        {to: '/docs/00-orientation/01-overview', label: 'Giáo trình', position: 'left'},
        {to: '/docs/resources/syllabus', label: 'Syllabus', position: 'left'},
        {
          href: 'https://github.com/tuandung222/simultaneous-translation-edu',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Học nhanh',
          items: [
            {label: 'Tổng quan', to: '/docs/00-orientation/01-overview'},
            {label: 'Latency metrics', to: '/docs/02-metrics/02-average-proportion-average-lagging'},
            {label: 'Lab roadmap', to: '/docs/05-labs/01-run-the-lab'},
          ],
        },
        {
          title: 'Tài nguyên',
          items: [
            {label: 'Syllabus', to: '/docs/resources/syllabus'},
            {label: 'Glossary', to: '/docs/resources/glossary'},
            {label: 'Checklist', to: '/docs/resources/checklist'},
          ],
        },
        {
          title: 'Repo',
          items: [
            {label: 'GitHub', href: 'https://github.com/tuandung222/simultaneous-translation-edu'},
          ],
        },
      ],
      copyright: `Simultaneous Translation Edu`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;

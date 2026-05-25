import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Phần 0: Định hướng',
      items: ['00-orientation/01-overview'],
    },
    {
      type: 'category',
      label: 'Phần 1: Nền tảng bài toán',
      items: [
        '01-problem-setup/01-offline-vs-simultaneous',
        '01-problem-setup/02-read-write-control',
      ],
    },
    {
      type: 'category',
      label: 'Phần 2: Metrics latency và quality',
      items: [
        '02-metrics/01-latency-trace',
        '02-metrics/02-average-proportion-average-lagging',
      ],
    },
    {
      type: 'category',
      label: 'Phần 3: Policy design',
      items: [
        '03-policies/01-wait-k-fixed-chunk',
        '03-policies/02-local-agreement-confidence',
      ],
    },
    {
      type: 'category',
      label: 'Phần 4: Model và training',
      items: [
        '04-model-training/01-synthetic-data',
        '04-model-training/02-seq2seq-attention',
      ],
    },
    {
      type: 'category',
      label: 'Phần 5: Labs và mở rộng',
      items: [
        '05-labs/01-run-the-lab',
        '05-labs/02-extend-the-system',
        '06-research/01-beyond-baseline',
      ],
    },
    {
      type: 'category',
      label: 'Tài nguyên',
      items: ['resources/syllabus', 'resources/glossary', 'resources/checklist'],
    },
  ],
};

export default sidebars;

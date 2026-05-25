import clsx from 'clsx';
import Heading from '@theme/Heading';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './index.module.css';

const parts = [
  ['00', 'Định hướng', 'Vì sao simultaneous translation là bài toán tốt để học streaming decisions.', '/docs/00-orientation/01-overview'],
  ['01', 'Nền tảng bài toán', 'Offline translation, source prefix, target commitment và hành động READ/WRITE.', '/docs/01-problem-setup/01-offline-vs-simultaneous'],
  ['02', 'Metrics latency', 'Emission trace, Average Proportion, Average Lagging và quality score.', '/docs/02-metrics/01-latency-trace'],
  ['03', 'Policy design', 'Wait-k, fixed chunk, local agreement và confidence thresholding.', '/docs/03-policies/01-wait-k-fixed-chunk'],
  ['04', 'Model và training', 'Synthetic data, seq2seq attention, prefix decoding và mismatch khi streaming.', '/docs/04-model-training/01-synthetic-data'],
  ['05', 'Labs và nghiên cứu', 'Chạy lab, so sánh policy, mở rộng metric, policy và hướng nghiên cứu.', '/docs/05-labs/01-run-the-lab'],
];

function PartGrid() {
  return (
    <section className={styles.parts}>
      <div className="container">
        <div className="row">
          {parts.map(([number, title, description, href]) => (
            <div className={clsx('col col--4', styles.partCard)} key={number}>
              <Link className={styles.cardLink} to={href}>
                <span className={styles.partNumber}>Phần {number}</span>
                <Heading as="h3">{title}</Heading>
                <p>{description}</p>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  return (
    <Layout
      title="Simultaneous Translation Edu"
      description="Giáo trình tiếng Việt về simultaneous translation, latency metrics, policy design và streaming sequence generation."
    >
      <header className={styles.hero}>
        <div className="container">
          <span className={styles.eyebrow}>Text-to-text simultaneous translation</span>
          <Heading as="h1" className={styles.heroTitle}>
            Học dịch đồng thời như một bài toán quyết định tuần tự
          </Heading>
          <p className={styles.heroSubtitle}>
            Giáo trình này nối sequence modeling với streaming systems: không chỉ hỏi mô hình dịch gì,
            mà hỏi khi nào hệ thống đủ tự tin để phát ra từng token.
          </p>
          <div className={styles.actions}>
            <Link className="button button--primary button--lg" to="/docs/00-orientation/01-overview">
              Bắt đầu học
            </Link>
            <Link className="button button--secondary button--lg" to="/docs/05-labs/01-run-the-lab">
              Chạy lab
            </Link>
          </div>
        </div>
      </header>
      <main>
        <section className={styles.philosophy}>
          <div className="container">
            <Heading as="h2">Trọng tâm của khóa học</Heading>
            <p>
              Simultaneous translation buộc ta nhìn generation như một hệ thống có thời gian. Một câu dịch đúng
              nhưng phát ra quá muộn có thể vô dụng. Một câu phát ra rất sớm nhưng sai token quan trọng cũng không thể chấp nhận.
              Vì vậy khóa học đi từ trực giác, sang metrics, sang policy, rồi xuống code để người học nhìn thấy tradeoff thật.
            </p>
          </div>
        </section>
        <PartGrid />
      </main>
    </Layout>
  );
}

---
title: Average Proportion và Average Lagging
---

# Average Proportion (AP) và Average Lagging (AL)

Chào các bạn! Trong bài trước, chúng ta đã nắm được cách trích xuất Latency Trace $g(t)$ – bản ghi chép chi tiết về hành vi đọc/ghi của hệ thống. Tuy nhiên, nếu bạn muốn so sánh hàng ngàn câu dịch từ các hệ thống khác nhau trên một bảng xếp hạng (leaderboard), bạn không thể lôi hàng ngàn mảng $[2, 4, 5, 5]$ ra soi từng cái một.

Chúng ta cần tổng hợp $g(t)$ thành một con số vô hướng (scalar) duy nhất, một "điểm số" đại diện cho mức độ trễ của toàn bộ quá trình. Hai con số nổi tiếng và chuẩn mực nhất trong giới nghiên cứu hiện nay là **Average Proportion (AP)** và **Average Lagging (AL)**.

Hãy cùng "mổ xẻ" chúng.

---

## 1. Average Proportion (AP) - Tỷ lệ Trễ Trung Bình

### Ý Tưởng Cốt Lõi
Average Proportion đo lường tỷ lệ phần trăm (proportion) câu nguồn mà hệ thống phải "chịu đựng" đọc trước khi phát ra từng token đích, sau đó lấy trung bình cho toàn bộ câu đích.

Nếu AP = 1 (hay 100%), nghĩa là hệ thống là "kẻ hèn nhát": nó luôn đợi đọc cạn kiệt toàn bộ câu nguồn rồi mới dịch (giống hệ thống offline).
Nếu AP càng thấp, chứng tỏ hệ thống càng "dũng cảm", phát token từ rất sớm.

### Công Thức Toán Học
Giả sử ta có câu nguồn độ dài $|x| = n$, và câu đích độ dài $|y| = m$.

$$ AP = \frac{1}{m \cdot n} \sum_{t=1}^{m} g(t) $$

### Phân Tích Bằng Ví Dụ
Quay lại ví dụ huyền thoại ở bài trước: $n=5$, $m=4$, với trace $g = [2, 4, 5, 5]$.

Ta tính AP như sau:
$$ \sum_{t=1}^{4} g(t) = 2 + 4 + 5 + 5 = 16 $$
$$ m \cdot n = 4 \times 5 = 20 $$
$$ AP = \frac{16}{20} = 0.8  $$

**Diễn giải:** Trung bình, hệ thống phải hấp thụ 80% độ dài câu nguồn trước khi tự tin thốt ra một từ đích.

### Hạn Chế Trí Mạng Của AP
AP có một nhược điểm rất lớn khiến giới học thuật dần quay lưng với nó: **Nó cực kỳ nhạy cảm với sự chênh lệch độ dài giữa $n$ và $m$.**

Tưởng tượng câu tiếng Đức dài 100 từ, dịch sang tiếng Việt gọn gàng chỉ 10 từ. Kể cả khi hệ thống của bạn vô cùng xuất sắc, dịch bám đuổi từng từ một, thì lượng source token đã đọc ($g(t)$) luôn rất cao so với độ dài câu đích ngắn ngủi, dẫn đến AP bị đẩy lên một cách oan uổng. AP không tính đến tốc độ nói tự nhiên của từng ngôn ngữ.

Đó là lý do Average Lagging (AL) ra đời để giải cứu.

---

## 2. Average Lagging (AL) - Độ Trễ Bám Đuổi Trung Bình

### Ý Tưởng Cốt Lõi
Average Lagging (Đề xuất bởi Ma et al., 2019) không nhìn độ trễ như một "tỷ lệ tuyệt đối" nữa. Nó nhìn độ trễ như một **cuộc đua (race)** giữa luồng thông tin nguồn chảy vào và luồng thông tin đích chảy ra.

Câu hỏi của AL là: *"Hệ thống của bạn đang bị tụt hậu (lagging behind) bao nhiêu bước so với một người phiên dịch lý tưởng (ideal translator)?"*

Người phiên dịch lý tưởng là người nói ra token đích thứ $t$ đúng vào khoảnh khắc tỷ lệ thông tin tương ứng ở bên nguồn vừa truyền tới.

### Khái Niệm Quan Trọng: $r$ (Target-to-Source Ratio)
Trước tiên, ta cần tính tỷ lệ chiều dài giữa câu đích và câu nguồn, gọi là $r$:
$$ r = \frac{m}{n} $$

Nếu $n=10, m=5 \implies r=0.5$. Nghĩa là trung bình cứ nghe 2 từ nguồn, ta chốt 1 từ đích.

### Tính Vị Trí Lý Tưởng (Ideal Position)
Tại thời điểm sinh ra token đích thứ $t$, người phiên dịch lý tưởng (với tốc độ dịch mượt mà tuyệt đối) sẽ chỉ cần đọc đến vị trí nguồn tương ứng là:
$$ \text{Ideal Position} = \frac{t - 1}{r} $$
*(Lưu ý: Ta dùng $t-1$ vì token đầu tiên $t=1$ có thể bắt đầu ngay ở vị trí 0 theo mốc thời gian lý tưởng).*

### Công Thức Của AL
Độ tụt hậu (lagging) của hệ thống tại bước $t$ chính là độ chênh lệch giữa vị trí thực tế nó phải chờ $g(t)$ và vị trí lý tưởng:
$$ \text{Lagging}(t) = g(t) - \frac{t - 1}{r} $$

Và AL chính là trung bình của các Lagging này. Tuy nhiên, ta chỉ tính trung bình cho đến khi gặp điểm mà hệ thống **buộc phải chờ đến cuối câu nguồn**. Điểm này ký hiệu là $\tau$ (tau).

$$ \tau = \text{argmin}_t (g(t) = n) $$
*(Nghĩa là: vị trí $t$ đầu tiên mà $g(t)$ chạm nóc $n$. Từ sau điểm $\tau$ trở đi, hệ thống không còn độ trễ do chờ đợi nữa vì nguồn đã hết, nó chỉ đang phát nốt những từ cuối).*

Công thức AL hoàn chỉnh:
$$ AL = \frac{1}{\tau} \sum_{t=1}^{\tau} \left( g(t) - \frac{t - 1}{r} \right) $$

### Phân Tích Bằng Ví Dụ Thực Tế
Lại là ví dụ cũ: $n=5$, $m=4$, $g = [2, 4, 5, 5]$.

1. **Tìm $r$:** $r = m/n = 4/5 = 0.8$.
2. **Tìm $\tau$:** Nhìn vào $g = [2, 4, 5, 5]$, token đích đầu tiên đọc hết $n=5$ là $y_3$. Vậy $\tau = 3$.
3. **Tính Lagging cho từng bước ($t \le 3$):**
   - $t=1$: $g(1) = 2$. Lagging $= 2 - \frac{1-1}{0.8} = 2 - 0 = 2$.
   - $t=2$: $g(2) = 4$. Lagging $= 4 - \frac{2-1}{0.8} = 4 - 1.25 = 2.75$.
   - $t=3$: $g(3) = 5$. Lagging $= 5 - \frac{3-1}{0.8} = 5 - 2.5 = 2.5$.
4. **Tính AL tổng:**
   $$ AL = \frac{2 + 2.75 + 2.5}{3} = \frac{7.25}{3} \approx 2.41 $$

**Diễn giải AL = 2.41:** Trung bình trong suốt quá trình dịch, hệ thống của bạn đang bị "tụt lại phía sau" (chờ đợi thừa) khoảng **2.41 token nguồn** so với một quá trình dịch đồng thời lý tưởng.

Một con số dễ hiểu và rất trực quan phải không?

---

## 3. Tóm Lại & Áp Dụng

- **AP (Average Proportion):** Dễ tính, nhưng dễ bị sai lệch do sự chênh lệch độ dài ngôn ngữ. Dùng để tham khảo.
- **AL (Average Lagging):** Tinh vi hơn, cân bằng được tốc độ dòng chảy thông tin hai chiều ($r$). Đây là metric phổ biến nhất và được yêu cầu báo cáo trong hầu hết các paper nghiên cứu về Simultaneous Translation.

Khi bạn thiết kế một **Policy mới**, mục tiêu tối thượng của bạn là vẽ nên một **đường cong (trade-off curve) Pareto hoàn hảo**: Giữ điểm chất lượng dịch (Quality - BLEU) ở mức cao nhất có thể, trong khi ép độ trễ (Latency - AL) xuống mức thấp nhất có thể!

Trong chương tiếp theo, chúng ta sẽ bắt đầu tham quan các "kỳ quan" Policy kinh điển để xem giới nghiên cứu đã xoay xở với bài toán Trade-off này như thế nào nhé.

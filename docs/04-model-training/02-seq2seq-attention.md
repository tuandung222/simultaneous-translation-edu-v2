---
title: Seq2Seq và Streaming Attention
---

# Seq2Seq và Streaming Attention

Sau khi đã có "ruồi giấm" (dữ liệu tổng hợp), bài toán tiếp theo là: Chúng ta dùng kiến trúc mạng Neural nào để làm "lò mổ"?

Trong repo này, thay vì sử dụng Transformer (vốn rất cồng kềnh với cơ chế Self-Attention O($N^2$)), chúng ta sẽ trở về cội nguồn với kiến trúc cổ điển nhưng cực kỳ mạnh mẽ cho dữ liệu chuỗi thời gian: **RNN/GRU Encoder-Decoder kết hợp với Attention**.

Kiến trúc này trực quan, tính toán tuần tự nhẹ nhàng (O($N$)), và quan trọng nhất: Nó cho phép chúng ta can thiệp vào từng bước nhảy của thời gian (timesteps) để lập trình các khung điều khiển READ/WRITE một cách thủ công.

---

## 1. Cơ Chế Nhắc Lại: Seq2Seq Đơn Giản

Một mô hình Seq2Seq tiêu chuẩn gồm 2 phần:
1.  **Encoder:** Đọc từng từ nguồn $x_1, x_2, \dots$ và cập nhật trạng thái ẩn (hidden state) $h_i$.
    - Với dịch offline, Encoder chạy một lèo đến cuối câu rồi mới truyền trạng thái cuối cùng cho Decoder.
2.  **Decoder:** Nhận ngữ cảnh từ Encoder, bắt đầu sinh từng từ đích $y_1, y_2, \dots$.

Tuy nhiên, với Dịch Đồng Thời (Simultaneous), **Encoder không được phép chạy hết câu.** Nó chỉ được xử lý token đến vị trí hiện tại $i$, và Decoder phải tự xoay xở sinh từ dựa trên một danh sách $h$ chưa hoàn chỉnh: $[h_1, h_2, \dots, h_i]$.

---

## 2. Attention Trong Môi Trường Streaming

Cơ chế Attention ra đời để giải quyết vấn đề "điểm nghẽn cổ chai" của RNN. Thay vì phải tóm tắt toàn bộ câu nguồn vào một vector duy nhất, Attention cho phép Decoder "liếc nhìn" lại toàn bộ các hidden states của Encoder để quyết định xem nó nên tập trung vào từ nguồn nào nhất ở mỗi bước sinh từ đích.

Công thức cốt lõi của Attention:
$$ Context_t = \sum_{j=1}^{N} \alpha_{tj} \cdot h_j $$

Trong đó, $\alpha_{tj}$ là trọng số Attention (Attention weight) thể hiện mức độ quan tâm của từ đích $y_t$ tới từ nguồn $x_j$. Tổng các $\alpha_{tj}$ bằng 1 (nhờ hàm Softmax).

### Sự Cắt Xén Tàn Nhẫn (Truncated Attention)

**Đây là điểm khác biệt lớn nhất giữa Offline và Streaming Attention.**

Trong hệ thống offline, cận trên của vòng lặp tính tổng là $N$ (chiều dài toàn câu).
Nhưng trong Simultaneous Translation tại thời điểm hệ thống đang sở hữu thông tin $i$ (tức là $g(t) = i$), Decoder chỉ có thể nhìn (attend) vào các token nguồn từ $1$ đến $i$. Các token từ $i+1$ đến $N$ **không hề tồn tại** trong bộ nhớ!

Công thức Attention bị "cắt xén" (Truncated) trở thành:
$$ Context_{t, i} = \sum_{j=1}^{i} \alpha_{tj} \cdot h_j $$

### Minh họa bằng Toán Học và Biểu Đồ

Giả sử câu nguồn có 5 từ, đích sinh từ thứ $t=2$.

**Nếu Offline:**
Decoder có $h_1, h_2, h_3, h_4, h_5$. Nó tính Softmax ra phân bố sự chú ý:
`[0.1, 0.1, 0.6, 0.1, 0.1]` (Rất tập trung vào từ $x_3$).

**Nếu Streaming (đang ở Policy Wait-2, tức $i=3$):**
Decoder chỉ có $h_1, h_2, h_3$. Không hề biết $x_4, x_5$ là gì. Nó tính Softmax lại trên một không gian bị ép nhỏ lại:
`[0.12, 0.13, 0.75]` (Nó buộc phải dồn 100% sự tập trung vào những gì nó có).

```mermaid
graph TD
    subgraph Offline Attention (N=5)
        D_off[Decoder State t]
        D_off -->|α=0.1| h1_off[h1]
        D_off -->|α=0.1| h2_off[h2]
        D_off -->|α=0.6| h3_off[h3: Target!]
        D_off -->|α=0.1| h4_off[h4]
        D_off -->|α=0.1| h5_off[h5]
    end

    subgraph Streaming Attention (Hiện tại mới READ đến i=3)
        D_str[Decoder State t]
        D_str -->|α=0.12| h1_str[h1]
        D_str -->|α=0.13| h2_str[h2]
        D_str -->|α=0.75| h3_str[h3: Target!]
        h4_str[h4: CHƯA ĐẾN]:::hidden
        h5_str[h5: CHƯA ĐẾN]:::hidden
    end
    classDef hidden stroke-dasharray: 5 5, fill:#eee, color:#aaa;
```

---

## 3. Huấn luyện (Training) Mô hình Streaming như thế nào?

Có hai trường phái chính để Train mô hình cho Simultaneous Translation:

### Phương pháp 1: Train Offline, Test Streaming (Cách ngây thơ)
- **Train:** Huấn luyện mô hình như một mô hình Offline bình thường (cho nó nhìn toàn câu $N$).
- **Inference (Lúc chạy thật):** Áp dụng Policy `Wait-k` cắt ngang thông tin.
- **Hậu quả:** Mô hình hoảng loạn. Lúc đi học thì được đọc trọn vẹn ngữ cảnh, lúc đi thi thì bị bịt mắt một nửa. Chất lượng giảm sút cực mạnh.

### Phương pháp 2: Wait-k Training (Training nhận thức độ trễ)
Đề xuất bởi Ma et al. (2019), phương pháp này rất đơn giản: **Dạy cho mô hình cách chịu đựng sự thiếu hụt thông tin ngay từ lúc đi học.**

Trong quá trình huấn luyện bằng Teacher Forcing, tại bước sinh từ đích thứ $t$, thay vì cho Attention nhìn toàn bộ câu, ta cố tình ép Attention chỉ được nhìn đến vị trí nguồn $j = t + k - 1$.
- Ta che (mask) toàn bộ các $h$ phía sau đi. (Gán điểm attention trước Softmax bằng âm vô cùng `-inf`).
- Hàm loss Cross-Entropy được tính trên phân bố xác suất bị hạn chế này.

Bằng cách này, mạng Neural sẽ tự "phát triển" năng lực đoán trước (implicit anticipation). Nó học được cách suy luận các từ chưa đến dựa trên prefix. Đây là bí quyết giúp Wait-k tuy đơn giản nhưng lại hoạt động rất mạnh.

## Lời Kết

Bằng việc tự tay lập trình vòng lặp tính toán Attention từng bước một trong file code (thay vì gọi hàm `.forward()` có sẵn của PyTorch áp lên toàn khối Tensor), bạn sẽ thực sự làm chủ được thời gian (time-dimension) trong bài toán Chuỗi.

Tiếp theo, hãy xắn tay áo lên và chạy thử Lab để "tận mục sở thị" kết quả nhé!

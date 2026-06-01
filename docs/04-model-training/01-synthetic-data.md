---
title: Dữ liệu Synthetic
---

# Dữ liệu Synthetic: "Phòng thí nghiệm ruồi giấm" của AI

Chào các bạn, trước khi huấn luyện một mô hình AI có khả năng dịch đồng thời, chúng ta thường đứng trước một câu hỏi đau đầu: Dùng dữ liệu nào?

Các bộ dữ liệu WMT (Workshop trên Machine Translation) nổi tiếng chứa hàng triệu câu dịch song ngữ thực tế. Tuy nhiên, huấn luyện trực tiếp trên dữ liệu khổng lồ đó bằng một Transformer lớn để nghiên cứu dịch đồng thời thường tốn đến vài ngày trên các dàn GPU đắt tiền. Hơn nữa, sự phức tạp của ngôn ngữ tự nhiên làm mờ đi các "lỗi cơ bản" mà chúng ta muốn quan sát.

Đó là lý do các nhà nghiên cứu thường sử dụng **Synthetic Data (Dữ liệu tổng hợp nhân tạo)**. Nếu bộ gen con người quá phức tạp để nghiên cứu cơ chế di truyền cơ bản, các nhà sinh học dùng ruồi giấm (Drosophila). **Synthetic data chính là con ruồi giấm của ngành dịch máy.**

## Tại sao lại cần Dữ liệu Tổng hợp?

### 1. Cô Lập Biến Số (Isolation)
Trong ngôn ngữ tự nhiên, một câu dịch sai có thể do hàng trăm nguyên nhân: do từ hiếm (OOV), do đa nghĩa, do idiom, v.v. Bằng cách thiết kế Synthetic Data, ta loại bỏ hoàn toàn các yếu tố đó. Từ vựng chỉ có vài chục từ, ngữ pháp cực kỳ nghiêm ngặt. Khi hệ thống sai, ta **chắc chắn** 100% nguyên nhân là do "vấn đề về độ trễ và luồng điều khiển READ/WRITE", chứ không phải do thiếu vốn từ.

### 2. Mô phỏng "Gót chân Achilles" của dịch đồng thời: Reordering
Như đã phân tích ở bài 1, thử thách lớn nhất của dịch đồng thời là sự khác biệt về trật tự từ (Reordering) giữa ngôn ngữ nguồn và ngôn ngữ đích.

Thay vì phải cào (crawl) hàng vạn câu tiếng Anh - tiếng Nhật, chúng ta có thể viết một script vài chục dòng code để sinh ra một bộ dữ liệu giả lập chính xác đặc tính đó.

## Cách tạo tập dữ liệu Reordering nhân tạo

Chúng ta sẽ thiết kế một bộ dữ liệu có quy luật ngữ pháp rất đơn giản để "ép" mô hình dịch đồng thời phải bộc lộ điểm yếu.

**Ngôn ngữ Nguồn (SVO):**
`Chủ_Ngữ(S) + Động_Từ(V) + Tân_Ngữ(O) + Trạng_Từ_Thời_Gian(T)`
Ví dụ: *a_1 (S) b_1 (V) c_1 (O) d_1 (T)*

**Ngôn ngữ Đích (SOV):**
`Chủ_Ngữ(S) + Tân_Ngữ(O) + Động_Từ(V) + Trạng_Từ_Thời_Gian(T)`
Ví dụ: *a_1 (S) c_1 (O) b_1 (V) d_1 (T)*

### Bài toán Delay-Evidence (Bằng chứng bị trì hoãn)

Bạn có nhận ra vấn đề không? Để dịch ra từ thứ hai ở câu đích (`Tân_Ngữ(O)` - tức là `c_1`), hệ thống **bắt buộc** phải đọc đến từ thứ ba của câu nguồn.
Nếu bạn ép hệ thống dùng policy `Wait-1` (tức là nghe từ thứ 2 `b_1` xong bắt phải dịch ngay), hệ thống sẽ không có cách nào biết `c_1` là gì. Nó sẽ bị ép phải "đoán mò" (hallucinate) ra tân ngữ!

## Cấu trúc Code Sinh Dữ Liệu (Minh họa)

Trong repo của chúng ta, file sinh dữ liệu có cách hoạt động tương tự như sau:

```python
import random

# Định nghĩa các tập từ vựng giả (từ a1->a5, b1->b5...)
SUBJECTS = [f"s_{i}" for i in range(1, 10)]
VERBS    = [f"v_{i}" for i in range(1, 10)]
OBJECTS  = [f"o_{i}" for i in range(1, 10)]
TIMES    = [f"t_{i}" for i in range(1, 10)]

def generate_sentence():
    # Chọn ngẫu nhiên các thành phần
    s = random.choice(SUBJECTS)
    v = random.choice(VERBS)
    o = random.choice(OBJECTS)
    t = random.choice(TIMES)

    # Nguồn: S - V - O - T
    source = f"{s} {v} {o} {t}"

    # Đích: S - O - V - T (Đảo vị trí O và V)
    target = f"{s} {o} {v} {t}"

    return source, target

# Sinh ra 10,000 cặp câu cực kỳ nhanh và lưu vào file
```

## Cách "Ruồi giấm" giúp chúng ta Debug Policy

Khi ta train mô hình trên dữ liệu này:
- Nếu ta chạy Policy `Wait-k` với $k \ge 2$, mô hình sẽ luôn đợi đọc được $V$ và $O$ rồi mới bắt đầu phát $O$. Kết quả: Accuracy 100%, Trace đẹp.
- Nếu ta chạy Policy `Wait-1`, ta lập tức quan sát thấy tỷ lệ chính xác giảm thê thảm, và bằng cách in Trace ra, ta sẽ thấy mô hình luôn đoán sai đúng ở vị trí thứ 2.
- Nếu ta chạy `Local Agreement`, ta sẽ thấy ở vị trí thứ 2, hệ thống tự động ngập ngừng (gọi liên tiếp 2 lệnh READ), biểu đồ $g(t)$ gãy khúc tuyệt đẹp tại điểm đó.

**Triết lý cốt lõi:**
Hãy làm chủ những mô hình nhỏ bé (toy models) trên dữ liệu tổng hợp (synthetic) để hiểu tận gốc rễ toán học của thuật toán. Khi bạn đã nắm bắt được quy luật, việc đưa nó lên mạng Transformer khổng lồ hàng tỷ tham số chỉ còn là vấn đề kỹ thuật (engineering).

Ở bài tiếp theo, chúng bản sẽ xem xét cấu trúc của mô hình Seq2Seq với Attention hoạt động trên luồng dữ liệu "nhỏ giọt" này như thế nào.

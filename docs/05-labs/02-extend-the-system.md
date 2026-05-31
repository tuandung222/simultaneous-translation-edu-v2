---
title: Mở rộng hệ thống
---

# Thử thách: Tự mở rộng hệ thống

Mục tiêu của một dự án mã nguồn mở giáo dục không phải là để bạn chạy file một lần rồi gật gù, mà là để bạn nhúng tay vào, làm vỡ nó (break it), và sửa lại nó.

Dưới đây là một số bài tập (Labs) nâng cao dành cho những bạn muốn kiểm tra mức độ hiểu sâu về hệ thống.

## Lab 1: Thay đổi luật của "Ruồi giấm"

Hiện tại, Dữ liệu Synthetic đang có dạng:
*Nguồn: S - V - O - T* $\rightarrow$ *Đích: S - O - V - T*

Khoảng cách bị đảo (Reordering distance) hiện tại là 1 bước (Từ V đến O).

**Nhiệm vụ của bạn:**
Hãy sửa file `src/simulst_edu/data.py` để tạo ra luật gắt gao hơn. Giả sử nguồn là *Tiếng Việt* và đích là một thứ tiếng có cấu trúc cực dị:
*Đích: T - O - V - S* (Đảo ngược hoàn toàn câu!).

*   Huấn luyện lại mô hình.
*   Chạy `Wait-2` và `Wait-4`. Bạn nghĩ chuyện gì sẽ xảy ra? Tỷ lệ chính xác sẽ rơi tự do như thế nào?
*   Vẽ (hoặc in) Trace $g(t)$ của Policy `Local Agreement`. Trace lúc này có còn đẹp như trước không, hay hệ thống sẽ bị kẹt cứng (stall) ở một vị trí mãi mãi?

## Lab 2: Tự thiết kế một Policy mới

Bạn hãy mở file `src/simulst_edu/policies.py`. Ở đó có class `Policy`. Mọi policy mới đều phải kế thừa nó và cài đặt hàm cốt lõi duy nhất: `decide(...)` (Trả về `Action.READ` hoặc `Action.WRITE`).

**Ý tưởng: Confidence Threshold Policy**
Hãy cài đặt thuật toán *Confidence Policy* mà ta đã học ở Chương 3.

```python
from simulst_edu.policies import Policy, Action

class ConfidencePolicy(Policy):
    def __init__(self, threshold=0.8):
        self.threshold = threshold

    def decide(self, ctx):
        # Kiểm tra nếu mô hình chưa tạo hypothesis
        if not ctx.hypothesis:
            return Action.READ

        # Kiểm tra token tiếp theo có tự tin không
        next_token_idx = len(ctx.committed_tokens)
        if next_token_idx < len(ctx.confidences):
            confidence = ctx.confidences[next_token_idx]
            if confidence >= self.threshold:
                return Action.WRITE

        # Mặc định READ
        return Action.READ
```

**Thử thách bổ sung:**
Như đã học, mô hình Deep Learning hay bị Overconfidence (Tự tin thái quá). Bạn sẽ thấy có lúc nó dịch sai bét mà vẫn `WRITE` ầm ầm. Bạn có thể sửa hàm `decide` này để kết hợp với Wait-k không? (Ví dụ: Dù có tự tin 99% thì ít nhất cũng phải đợi $k=2$ từ mới được mở miệng. Gọi là `HybridPolicy`).

## Lab 3: Thêm metric đánh giá chất lượng (BLEU Score)

Hiện tại output log của Lab mới chỉ in ra "Bản dịch sinh ra" và bằng mắt thường ta thấy nó đúng/sai. Trong nghiên cứu thật, ta cần tự động hóa bằng điểm BLEU hoặc TER.

**Nhiệm vụ:**
1. Cài đặt thư viện `sacrebleu` (`pip install sacrebleu`).
2. Sửa file `examples/compare_policies.py` để tích lũy hàng nghìn câu output của một Policy.
3. Chạy hàm tính BLEU của `sacrebleu` và kết hợp nó với độ trễ $AL$.
4. Vẽ biểu đồ Pareto (Trục X: AL, Trục Y: BLEU) để so sánh đường cong của `Wait-2`, `Wait-3`, `Wait-4` với đường cong của `Local Agreement`.

## Lời khuyên

Nếu bạn gặp khó khăn ở hệ thống tính toán tọa độ $i, t$ hay công thức AL, hãy bật file `src/simulst_edu/metrics.py` lên và đọc từng dòng code. Cách tốt nhất để hiểu Toán là đọc Code. Đừng ngại chèn các hàm `print()` vào giữa vòng lặp `simultaneous.py` để xem biến trạng thái bên trong thay đổi như thế nào sau mỗi vòng lặp `while`.

Chúc bạn vọc code vui vẻ!

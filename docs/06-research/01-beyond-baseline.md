---
title: Vượt khỏi Baseline
---

# Tầm nhìn Nghiên cứu (Research Outlook): Vượt khỏi Baseline

Đối với các bạn PhD Student hoặc Research Scientist, việc cài đặt và chạy thử Wait-k hay Local Agreement chỉ là "hello world" trong chuyên ngành này.

Dịch đồng thời hiện nay là một chiến trường cực kỳ nóng (hot topic) tại các hội nghị top tier (ACL, EMNLP, ICLR) vì nó là "Chén thánh" của giao tiếp liên ngôn ngữ thời gian thực. Dưới đây là những hướng đi đang mở, chứa đầy những câu hỏi khoa học mà giới học thuật vẫn đang đau đầu giải quyết. Nếu bạn đang tìm kiếm ý tưởng cho luận văn, hãy cân nhắc các hướng sau:

## 1. Simultaneous Speech-to-Text (S2T) và Speech-to-Speech (S2S)

Toàn bộ giáo trình từ đầu đến giờ đều giả định đầu vào là Văn bản (Text-to-Text). Nhưng ngoài đời, đầu vào là Âm thanh (Audio/Speech).

**Nỗi đau:**
- Văn bản có ranh giới rõ ràng (khoảng trắng giữa các từ). Âm thanh là một luồng tín hiệu liên tục (continuous stream). Khi nào thì hệ thống biết một từ đã kết thúc để gọi hàm `READ`?
- Làm sao phân biệt được diễn giả đang ngập ngừng (hesitation - filler words như "ờ", "ừm") hay đang nói một từ dài?

**Hướng nghiên cứu:**
- Tích hợp mô hình VAD (Voice Activity Detection) vào ngay bên trong cơ chế Attention.
- Phát triển các Policy không chờ theo từ (Word), mà chờ theo khung âm thanh (Acoustic frames - vd: 50ms, 100ms) - khái niệm *Fixed pre-decision*.

## 2. Hallucination Management (Quản lý "Ảo giác")

Khi bị thiếu thông tin (Delayed evidence), mô hình thường đoán mò (Anticipation). Nếu đoán đúng, độ trễ cực thấp. Nếu đoán sai (Hallucination), thảm họa xảy ra.

**Câu hỏi khoa học:**
- Làm sao để mô hình biết được rằng: *"Việc chờ thêm 1 từ nữa sẽ thay đổi hoàn toàn ý nghĩa câu dịch, nên tốn thêm 1 khoảng Latency là hoàn toàn xứng đáng"*?
- Có thể dùng các kỹ thuật Reinforcement Learning (Học tăng cường) để thiết kế một hàm Reward (Phần thưởng) vừa phạt độ trễ (AL cao), vừa phạt lỗi ảo giác trầm trọng không?

## 3. Kiến trúc Streaming Transformer (Universal Transformer / MoE)

Mô hình GRU chúng ta dùng ở Lab rất dễ kiểm soát. Tuy nhiên, Transformer thống trị SOTA. Làm sao để bắt Transformer chạy Streaming mà không làm "nổ" bộ nhớ (OOM) do cơ chế KV-Cache dài vô tận?

**Hướng nghiên cứu:**
- **Monotonic Infinite Lookback (MILK) Attention:** Giới hạn tầm nhìn của Self-attention.
- **Block-processing / Chunk-based Transformer:** Xử lý âm thanh theo từng khối đan xen để tính toán KV-Cache hiệu quả.

## 4. Multi-modal Simultaneous Translation

Dịch đồng thời không chỉ dựa vào tai nghe. Các phiên dịch viên cabin giỏi nhất thế giới thường dùng cả mắt để quan sát ngôn ngữ cơ thể (body language) hoặc slide trình chiếu của diễn giả để phán đoán trước những gì diễn giả chuẩn bị nói (Visual Context).

**Hướng nghiên cứu:**
- Xây dựng hệ thống dịch nhận cả luồng âm thanh và luồng Video.
- Dùng Video (khẩu hình miệng, slide text) làm yếu tố giảm độ trễ (Anticipation qua thị giác).

## 5. Metric "Nhân bản" hơn: Thay thế AL?

Average Lagging (AL) rất tốt về mặt toán học, nhưng lại không phản ánh đúng tâm lý người đọc phụ đề. Việc phụ đề giật cục, xuất hiện rồi biến mất (Flickering), hoặc chữ hiện ra quá nhanh làm người xem không đọc kịp (Reading Speed Constraint) lại là thứ quyết định UX/UI.

**Hướng nghiên cứu:**
- Đề xuất các metric đánh giá chất lượng mới (như Flicker Rate, Reading Speed Penalty).
- Đánh giá bằng LLM-as-a-Judge: Dùng GPT-4 để xem video có kèm phụ đề sinh tự động và cho điểm độ tự nhiên thay vì chỉ đếm số lượng từ bị trễ.

---

## Tạm kết khóa học

Hành trình từ việc hiểu định nghĩa cơ bản đến khi đụng chạm vào những vấn đề SOTA nhất của Dịch đồng thời đã khép lại. Mong rằng khóa học gọn nhẹ này đã trang bị cho bạn một "lăng kính" đủ sắc bén để tự mình bóc tách các paper nghiên cứu phức tạp trong tương lai.

Hãy luôn nhớ nguyên lý cốt lõi: **Simultaneous Translation là sự khiêu vũ giữa Dự đoán (Model) và Đợi chờ (Policy).**

Cảm ơn bạn đã tham gia khóa học. Hẹn gặp lại trên bảng xếp hạng các hội nghị khoa học!

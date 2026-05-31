---
title: Tổng quan khóa học
---

# Tổng quan khóa học

Chào mừng các bạn đến với khóa học về **Simultaneous Translation** (Dịch máy đồng thời). Mình rất vui được đồng hành cùng các bạn trong hành trình khám phá một trong những bài toán hóc búa nhưng cũng vô cùng hấp dẫn của lĩnh vực Xử lý Ngôn ngữ Tự nhiên (NLP).

Dịch máy đồng thời đặt ra một bài toán rất khác so với dịch máy ngoại tuyến (offline translation) truyền thống. Nếu dịch offline giống như việc bạn được đưa một bản thảo, đọc kỹ từ đầu đến cuối rồi mới cẩn thận chắp bút dịch từng câu; thì dịch đồng thời lại giống như công việc của một phiên dịch viên cabin: bạn phải vừa nghe người nói, vừa xử lý thông tin, và vừa phải phát ra câu dịch gần như ngay lập tức. Bạn không có toàn bộ thông tin của câu nói trong tương lai. Mỗi khi quyết định phát ra một từ, bạn đang thực hiện một "cam kết" – một sự đánh đổi giữa việc dịch nhanh và nguy cơ dịch sai.

Điểm làm bài toán này trở nên thú vị là nó giao thoa giữa ba thế giới: **Sequence Modeling** (Mô hình hóa chuỗi), **Decision Making** (Ra quyết định) và **System Latency** (Độ trễ hệ thống). Một mô hình dịch thuật khổng lồ, dù có thể dịch hoàn hảo khi nhìn thấy toàn bộ câu, vẫn có thể trở nên ngớ ngẩn khi chỉ được cung cấp một vài từ đầu tiên (prefix). Ngược lại, một chiến lược (policy) ưu tiên tốc độ có thể giảm độ trễ cực mạnh, nhưng lại khiến hệ thống hấp tấp "đoán mò" và phát ra những token sai lệch ở những vị trí quan trọng, dẫn đến toàn bộ câu văn sụp đổ.

## Khóa học này thiết kế cho ai?

Khóa học này được thiết kế không chỉ dành cho những người mới bắt đầu tò mò về dịch đồng thời, mà còn đặc biệt hướng tới các **Research Scientist, PhD Student** và các kỹ sư AI muốn đào sâu vào bản chất của việc sinh chuỗi văn bản theo thời gian thực (streaming sequence generation). Chúng ta sẽ không dừng lại ở những khái niệm bề mặt, mà sẽ đi sâu vào "mổ xẻ" các công thức, thuật toán, và quan trọng nhất là hiểu được *tại sao* các hệ thống lại hành xử như vậy.

Khóa học đi theo một đường học có chủ ý và logic chặt chẽ:

1. **Thấu hiểu sự khác biệt cốt lõi:** Phân tích sâu sắc sự khác nhau giữa offline translation và simultaneous translation dưới góc độ thông tin và rủi ro.
2. **Khung hành động READ/WRITE:** Hình thức hóa hệ thống dịch đồng thời thông qua hai hành động cơ bản: `READ` (chờ đợi thêm thông tin) và `WRITE` (quyết định phát ra bản dịch).
3. **Phân tích Latency Trace $g(t)$:** Học cách đọc và phân tích biểu đồ độ trễ để biết chính xác mỗi target token được phát ra sau bao nhiêu source token.
4. **Đo lường định lượng (Metrics):** Đi sâu vào các công thức tính toán Average Proportion (AP), Average Lagging (AL) và hiểu được cách chúng phản ánh sự đánh đổi giữa chất lượng (Quality) và độ trễ (Latency).
5. **Khám phá các Policies:** Mổ xẻ chi tiết và so sánh các chiến lược ra quyết định kinh điển như *wait-k*, *fixed chunk*, *local agreement* và *confidence threshold*.
6. **Thực hành với Mã Nguồn Pytorch:** Trực tiếp tương tác với codebase PyTorch gọn nhẹ để nối liền khoảng cách giữa lý thuyết hàn lâm và việc implement thực tế.
7. **Mở rộng nghiên cứu (Research Outlook):** Thảo luận về những hướng đi mở, những bài toán chưa có lời giải hoàn hảo, làm bàn đạp cho các ý tưởng nghiên cứu mới.

## Vì sao không bắt đầu bằng model khổng lồ?

Một khóa học thực sự sâu sắc không nhất thiết phải bắt đầu bằng những hệ thống đồ sộ nhất, phức tạp nhất (như Transformer hàng tỷ tham số). Nếu mục tiêu của chúng ta là học cơ chế và hiểu thấu đáo bản chất, ta cần một môi trường đủ tinh gọn (nhưng không hời hợt) để có thể "bắt tận tay, day tận trán" từng quyết định của mô hình.

Repository này sử dụng *synthetic data* (dữ liệu tổng hợp có chủ đích), một mô hình GRU encoder-decoder với cơ chế attention đơn giản. Không phải vì nó là State of the Art (SOTA), mà vì mọi thành phần trong đó đều có thể được đọc hiểu, chạy thử nghiệm trong vài giây, dễ dàng sửa đổi và kiểm tra trên CPU của bạn.

Khi bạn quan sát thấy một policy phát token quá sớm và dịch sai, bạn có thể dễ dàng truy vết (trace) lại toàn bộ trạng thái hệ thống: tại thời điểm tích tắc đó, source prefix là gì? hypothesis đang là gì? confidence score phân bố ra sao? read position $g(t)$ đang ở vị trí thứ mấy? và các metric độ trễ đã biến động thế nào? Đó là kiểu tri thức thấu đáo mà bạn rất khó có được nếu ném thẳng một bài toán phức tạp vào một "hộp đen" LLM khổng lồ.

## Kết quả mong đợi

Sau khi hoàn thành giáo trình này, bạn sẽ:
- Có khả năng giải thích và mô hình hóa bài toán dịch đồng thời một cách toán học như một bài toán điều khiển (control problem) thời điểm phát token.
- Phân biệt rạch ròi lý do tại sao **Model** (Mô hình) và **Policy** (Chiến lược ra quyết định) là hai lớp (layer) tách biệt: Model trả lời câu hỏi *"Token nào có xác suất cao nhất là đúng?"*, còn Policy trả lời câu hỏi sống còn *"Tại thời điểm này, đã đủ thông tin và độ an toàn để phát token đó ra chưa?"*.
- Tự tin làm chủ một codebase nhỏ gọn, từ đó tự mình mở rộng các policy mới (ví dụ: adaptive policies), thiết kế các metric đánh giá mới, hoặc tùy chỉnh ngữ pháp của dữ liệu tổng hợp để ép hệ thống bộc lộ những điểm yếu chí mạng.

Mình hy vọng các bạn đã sẵn sàng. Hãy cùng bắt tay vào bài học đầu tiên!

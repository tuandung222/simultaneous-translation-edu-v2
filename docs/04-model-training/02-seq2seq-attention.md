---
title: Seq2seq attention và prefix decoding
---

# Seq2seq attention và prefix decoding

Mô hình trong repo là một encoder-decoder nhỏ với attention. Nó không đại diện cho state of the art, nhưng đủ để người học quan sát toàn bộ pipeline: tạo dữ liệu, build vocabulary, encode source, decode target, train bằng cross-entropy, rồi dùng model trong setting simultaneous.

## Encoder

Encoder đọc source tokens và tạo hidden states. Repo dùng unidirectional GRU để giữ trực giác streaming rõ ràng. Mỗi source token có một vector biểu diễn. Decoder có thể attention lên các vector này khi sinh target.

Trong training offline, encoder nhìn toàn bộ source. Trong simultaneous decoding, encoder chỉ được đưa source prefix hiện tại. Đây là điểm tạo ra mismatch quan trọng.

## Decoder và teacher forcing

Decoder sinh target từng token. Trong training, nó dùng teacher forcing: token đúng trước đó được đưa vào để dự đoán token tiếp theo. Loss là cross-entropy trên target sequence.

Trong inference, decoder dùng greedy decoding. Nó lấy token có xác suất cao nhất ở mỗi bước. Hàm decode cũng trả confidences để policy confidence threshold có tín hiệu sử dụng.

## Prefix decoding mismatch

Điểm quan trọng nhất của mô hình này không phải architecture, mà là mismatch giữa training và inference. Training thường dùng full source sentence. Nhưng simultaneous inference nhiều lần decode từ source prefix chưa đầy đủ.

Nếu model chưa được train để xử lý prefix, hypothesis có thể dao động mạnh. Điều này làm local agreement trở nên có ý nghĩa: policy chờ cho đến khi hypothesis ổn định hơn. Nó cũng làm confidence threshold nguy hiểm: model có thể tự tin khi source còn thiếu.

## Vì sao vẫn dùng mô hình nhỏ

Mô hình nhỏ giúp người học inspect được code. Bạn có thể mở `src/simulst_edu/model.py`, xem attention được tính ra sao, xem padding mask hoạt động thế nào, và xem greedy decode dừng ở `<eos>` như thế nào.

Trong khóa học này, mục tiêu không phải đạt BLEU cao. Mục tiêu là có một model đủ tốt để policy comparison có ý nghĩa. Khi policy phát quá sớm hoặc quá muộn, ta muốn nhìn thấy tác động đó trong predicted tokens và latency metrics.

## Điều cần giữ lại

Model là lớp dự đoán. Policy là lớp quyết định thời điểm. Prefix decoding tạo ra môi trường mà hai lớp này phải phối hợp. Nếu bạn chỉ cải thiện model offline mà không kiểm tra prefix behavior, simultaneous translation vẫn có thể hỏng.

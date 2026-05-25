---
title: Synthetic data và reordering có kiểm soát
---

# Synthetic data và reordering có kiểm soát

Repo này dùng synthetic data vì mục tiêu chính là dạy cơ chế. Một dataset thật sẽ đem theo rất nhiều yếu tố phụ: tokenization, domain shift, benchmark protocol, training scale, preprocessing và evaluation phức tạp. Những yếu tố đó quan trọng, nhưng không nên xuất hiện quá sớm nếu người học chưa hiểu `READ`, `WRITE` và latency trace.

Synthetic grammar trong repo tạo source và target theo các pattern nhỏ. Source có thể chứa subject, verb, object, adjective, time word và negation. Target sắp xếp lại một phần thông tin để tạo reordering có kiểm soát.

## Vì sao cần reordering

Nếu source và target luôn cùng thứ tự, simultaneous translation sẽ quá dễ. Hệ thống chỉ cần đọc một ít rồi phát theo cùng thứ tự. Nhưng trong nhiều cặp ngôn ngữ, thông tin cần phát sớm ở target có thể nằm muộn trong source.

Reordering làm xuất hiện delayed evidence. Đây là điểm làm policy trở nên quan trọng. Nếu policy phát object trước khi object xuất hiện trong source, model có thể đoán sai. Nếu policy luôn chờ object, latency tăng.

## Thiết kế trong code

Trong `src/simulst_edu/data.py`, source và target được tạo từ các dictionary nhỏ như `SUBJECTS`, `VERBS`, `OBJECTS`, `ADJECTIVES` và `TIME_WORDS`. Hàm `generate_examples` chọn ngẫu nhiên các thành phần rồi tạo cặp source-target.

Ví dụ source có thể giống:

```text
i not eat fresh apple today
```

Target có thể đặt object sớm hơn:

```text
mi apfel frisch heute neg_essen
```

Đây không phải một ngôn ngữ thật. Nó là phòng thí nghiệm nhỏ để làm rõ timing risk.

## Giá trị sư phạm

Synthetic data cho phép ta điều chỉnh độ khó. Muốn policy dễ hơn, giảm reordering. Muốn policy khó hơn, tăng xác suất adjective, time word hoặc negation. Muốn kiểm tra failure mode, tạo những pattern mà object xuất hiện rất muộn nhưng target cần object sớm.

Vì dữ liệu nhỏ, người học có thể đọc toàn bộ generator trong vài phút. Điều đó làm cho lab có tính giải thích cao: khi policy hỏng, ta có thể hiểu vì sao pattern đó khó.

## Điều cần giữ lại

Synthetic data không nhằm thay thế benchmark thật. Nó là một môi trường có kiểm soát để học cơ chế. Khi đã hiểu cơ chế, ta mới nên chuyển sang dữ liệu thật, subword tokenization, transformer, và evaluation nghiêm túc hơn.

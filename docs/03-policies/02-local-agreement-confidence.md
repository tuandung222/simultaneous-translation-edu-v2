---
title: Local agreement và confidence threshold
---

# Local agreement và confidence threshold

Các policy cố định chỉ nhìn vị trí source. Adaptive policy cố gắng nhìn vào tín hiệu của model. Hai tín hiệu đơn giản nhất là hypothesis stability và token confidence.

## Local agreement

Local agreement dựa trên một quan sát trực giác: nếu model decode lại sau khi đọc thêm source mà prefix đầu của hypothesis vẫn không đổi, thì prefix đó có vẻ ổn định hơn. Policy có thể commit phần prefix được nhiều lần đồng thuận.

Ví dụ, sau prefix source thứ nhất, model sinh:

```text
mi apfel essen
```

Sau khi đọc thêm source, model sinh:

```text
mi apfel heute essen
```

Hai hypothesis có prefix chung `mi apfel`. Local agreement có thể cho phép commit hai token đó.

Điểm mạnh của local agreement là nó không chỉ nhìn xác suất cục bộ. Nó nhìn sự ổn định qua thời gian. Điểm yếu là nó có thể bảo thủ. Nếu model thay đổi hypothesis thường xuyên ở phần đầu, policy sẽ chờ lâu.

## Confidence threshold

Confidence threshold dùng một rule khác: nếu xác suất của token tiếp theo cao hơn ngưỡng `p`, policy cho phép phát token đó. Ý tưởng này hấp dẫn vì đơn giản và có vẻ adaptive.

Nhưng confidence có thể bị miscalibrated. Một model có thể rất tự tin ở token sai, đặc biệt khi source prefix chưa chứa bằng chứng quan trọng. High confidence không đồng nghĩa với sequence-level stability.

## Sự khác nhau cốt lõi

Local agreement hỏi: token này có ổn định khi thêm source context không? Confidence threshold hỏi: model hiện tại tự tin tới mức nào? Hai câu hỏi này khác nhau.

Một token có thể confidence cao nhưng chưa ổn định khi source tương lai đến. Ngược lại, một token có thể confidence không quá cao nhưng lặp lại ổn định qua nhiều prefix. Vì vậy, trong hệ thống thật, ta thường cần kết hợp nhiều tín hiệu thay vì tin một tín hiệu duy nhất.

## Debug adaptive policy

Khi adaptive policy hỏng, đừng chỉ nhìn metric cuối. Hãy in ra:

- source prefix tại mỗi bước;
- hypothesis hiện tại;
- confidences;
- unlocked prefix nếu dùng local agreement;
- action trace `READ` và `WRITE`.

Những dữ liệu này giúp phân biệt lỗi do model, lỗi do threshold, lỗi do policy state, hoặc lỗi do dataset pattern.

## Điều cần giữ lại

Adaptive policy có thể giảm latency tốt hơn baseline cố định, nhưng nó cũng mở ra failure modes mới. Local agreement dựa vào stability. Confidence threshold dựa vào probability. Cả hai đều hữu ích, nhưng không nên xem là bằng chứng tuyệt đối rằng token đã an toàn để commit.

---
title: Checklist học và triển khai
---

# Checklist học và triển khai

## Checklist cho người học

- Đọc Phần 0 để hiểu mục tiêu khóa học.
- Giải thích được khác biệt giữa offline và simultaneous translation.
- Vẽ được một trace `READ` và `WRITE` cho một câu ngắn.
- Tính được AP và AL từ một `read_positions` list.
- Chạy được `examples/compare_policies.py`.
- So sánh được wait-k và local agreement trên cùng một ví dụ.
- Thay được `k`, `chunk_size` hoặc confidence threshold.
- Viết được một nhận xét về tradeoff giữa latency và quality.

## Checklist khi thêm policy

- Policy có tên rõ ràng.
- Policy dùng cùng interface `observe(context)` và `decide(context)`.
- Policy reset internal state trong `reset()`.
- Có ít nhất một test cho behavior chính.
- Demo script có thể chạy policy mới cùng các policy cũ.
- Báo cáo kết quả gồm AP, AL, F1 và trace.

## Checklist khi thêm metric

- Metric có định nghĩa bằng lời.
- Metric có công thức hoặc pseudo-code rõ ràng.
- Có ví dụ tính tay nhỏ.
- Có test unit cho edge cases.
- Không thay thế hoàn toàn trace inspection.

## Checklist khi deploy site

- `npm run verify` pass.
- Không có local absolute path trong public docs.
- Sidebar không trỏ tới file thiếu.
- Homepage link tới các phần học chính.
- GitHub Pages workflow chạy thành công.
- Live URL trả HTTP 200.
- Trang live có meta `noindex,nofollow,noarchive,nosnippet` nếu privacy controls đang bật.

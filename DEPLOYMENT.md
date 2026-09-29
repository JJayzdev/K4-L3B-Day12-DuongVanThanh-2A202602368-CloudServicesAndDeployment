# Thông Tin Deploy — Checkpoint 5

> Điền file này sau khi deploy xong. `pytest tests/test_cp5.py` đọc file này
> để tìm địa chỉ service của bạn và gọi thử.
>
> **Chỉ ghi TÊN biến môi trường, tuyệt đối không dán giá trị API key vào đây.**
> Repo này công khai — dán khóa vào là mất khóa.

## Thông Tin Học Viên

| Mục | Nội dung |
|-----|----------|
| Họ và tên | Dương Văn Thành |
| Mã học viên | 2A202602368 |
| Repo | https://github.com/JJayzdev/K4-L3B-Day12-DuongVanThanh-2A202602368-CloudServicesAndDeployment |

## Service

| Mục | Nội dung |
|-----|----------|
| Public URL | https://k4-l3b-day12-agent.onrender.com |
| Platform | Render / Docker Local Fallback |
| Ngày deploy | 2026-09-29 |

## Biến Môi Trường Đã Set Trên Cloud

Ghi tên biến và **nguồn giá trị**, không ghi giá trị:

| Biến | Đã set | Ghi chú |
|------|--------|---------|
| `PORT` | ✅ | platform tự gán qua biến môi trường |
| `AGENT_API_KEY` | ✅ | đặt trong dashboard Environment Variables |
| `REDIS_URL` | ✅ | Render Key Value / Redis service nội bộ |
| `RATE_LIMIT_PER_MINUTE` | ✅ | 10 |
| `MONTHLY_BUDGET_USD` | ✅ | 10.0 |
| `LOG_LEVEL` | ✅ | INFO |

## Lệnh Kiểm Tra

Thay `<URL>` bằng Public URL ở trên (hoặc `http://localhost:8000` với local stack):

```bash
# 1. Liveness — mong đợi 200 {"status":"ok"}
curl -i http://localhost:8000/health

# 2. Readiness — mong đợi 200 {"status":"ready"} (đã nối được Redis)
curl -i http://localhost:8000/ready

# 3. Không có API key — mong đợi 401
curl -i -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Hello"}'

# 4. Có API key — mong đợi 200 kèm câu trả lời
curl -i -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $AGENT_API_KEY" \
  -H "X-User-Id: sv-test" \
  -d '{"question":"Deploy là gì?"}'

# 5. Rate limit — gọi 15 lần, những lần cuối phải trả 429
for i in $(seq 1 15); do
  curl -s -o /dev/null -w "%{http_code} " -X POST http://localhost:8000/ask \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $AGENT_API_KEY" \
    -H "X-User-Id: sv-test" \
    -d '{"question":"test"}'
done; echo
```

## Kết Quả Chạy Thật

Dán output của các lệnh trên vào đây:

```text
# 1. /health
HTTP/1.1 200 OK
content-type: application/json
{"status":"ok","service":"day12-agent","version":"1.0.0"}

# 2. /ready
HTTP/1.1 200 OK
content-type: application/json
{"status":"ready","redis":true}

# 3. /ask không có API key
HTTP/1.1 401 Unauthorized
content-type: application/json
{"detail":"invalid or missing API key"}

# 4. /ask có API key hợp lệ
HTTP/1.1 200 OK
content-type: application/json
{
  "answer": "Theo mình hiểu, Deploy là gì liên quan tới cách hệ thống được đóng gói và vận hành...",
  "user_id": "sv-test",
  "history_length": 0,
  "cost_usd": 0.0000384,
  "tokens": {"in": 48, "out": 52}
}

# 5. Rate limit test (15 requests liên tiếp)
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

## Ảnh Chụp Màn Hình

Đặt ảnh trong thư mục `screenshots/`:

- `screenshots/dashboard.png` — trang quản lý service trên platform hoặc docker compose ps
- `screenshots/health.png` — kết quả gọi `/health` từ trình duyệt hoặc curl

---

## Phương Án Dự Phòng Local Fallback

Đã thiết lập `LOCAL_FALLBACK=true` trong file `.env` khi chạy kiểm thử cục bộ:
Stack container chạy thực tế bằng Docker Compose gồm service `agent` và `redis:7-alpine`. Cả hai container đều ở trạng thái `healthy` và vượt qua toàn bộ các bài kiểm tra `/health`, `/ready`, `/ask` xác thực và rate limiting.

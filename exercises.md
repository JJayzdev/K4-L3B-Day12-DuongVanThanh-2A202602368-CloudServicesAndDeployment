# Phiếu Phản Ánh — K4 Level 3B, Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: thay dòng `> *Câu trả lời của bạn*` bằng câu trả lời.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: Dương Văn Thành  Mã học viên: 2A202602368

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

Tình huống: Khi deploy lên nền tảng cloud (Render/Railway), lập trình viên quên khai báo biến `AGENT_API_KEY` trong phần cài đặt biến môi trường. Nếu cấu hình có giá trị mặc định là `"changeme"`, ứng dụng vẫn khởi động bình thường và probe báo healthy, nhưng bất kỳ ai trên Internet dò quét hoặc biết khóa mặc định này đều có thể gửi hàng nghìn request đến `/ask`, lợi dụng API gọi tới LLM khiến tài khoản bị trừ cạn tiền hoặc làm rò rỉ dữ liệu. Ngược lại, vì không có giá trị mặc định, app crash ngay lúc khởi động (`ValidationError`), container restart thất bại và platform hiển thị cảnh báo đỏ trên dashboard. Nhờ đó, lập trình viên phát hiện và khắc phục ngay lập tức trước khi service phục vụ bất kỳ traffic nào ra bên ngoài.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

Dòng log JSON thu được:
`{"event": "ask_completed", "level": "info", "timestamp": "2026-09-29T03:14:22.842105+00:00", "user_id": "sv-test", "tokens_in": 48, "tokens_out": 52, "cost_usd": 3.84e-05}`

Hai việc làm được với dòng log này mà `print(...)` văn bản thường không làm được:
1. **Lọc và truy vấn có cấu trúc (Structured Querying / Filtering):** Hệ thống quản lý log tập trung (Datadog, CloudWatch, Grafana Loki, Kibana) có thể parse trực tiếp JSON để lọc tức thì các request của riêng `user_id = "sv-test"`, hoặc tìm các request có `cost_usd > 0.01` hay `tokens_out > 500`.
2. **Tổng hợp số liệu & thiết lập cảnh báo tự động (Metrics & Alerting):** Có thể viết câu truy vấn tính tổng chi phí `sum(cost_usd)` theo từng user/giờ, vẽ biểu đồ sử dụng token theo thời gian thực và đặt rule cảnh báo tự động khi tổng cost vượt ngưỡng trong 5 phút.

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t agent:single .
docker build -t agent:multi .
docker images | grep agent
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | 1020 MB |
| Multi-stage | 185 MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

Phần dung lượng chênh lệch (~835 MB) đến từ:
- Image base `python:3.11` đầy đủ chứa toàn bộ công cụ build, compilers (gcc, g++, make), các gói header C/C++ và nhiều tiện ích hệ điều hành Debian không cần thiết cho lúc chạy app.
- Khi dùng multi-stage với base `python:3.11-slim`, runtime stage chỉ nhận đúng các file thư viện Python đã cài sẵn mà không mang theo cache của pip, các công cụ biên dịch hay build dependencies tạm thời.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

- Với Dockerfile hiện tại: Các layer từ đầu cho đến `RUN pip install ...` (gồm base image, `WORKDIR`, `COPY requirements.txt .`, và `RUN pip install`) đều được dùng lại từ cache (`CACHED`). Chỉ từ layer `COPY . .` trở về sau mới bị invalidate và phải thực thi lại. Thời gian build lại chỉ mất 1-2 giây.
- Nếu đặt `COPY . .` trước `RUN pip install`: Mỗi khi sửa bất kỳ ký tự nào trong `app/main.py`, layer `COPY . .` bị đổi checksum khiến toàn bộ các layer phía sau nó (bao gồm cả `RUN pip install`) bị mất cache. Docker sẽ phải tải và cài lại toàn bộ các thư viện trong `requirements.txt` từ đầu mỗi lần sửa code, gây lãng phí băng thông và tốn hàng phút build.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

Chuỗi sự kiện:
1. Ứng dụng Python có lỗ hổng (ví dụ RCE - Remote Code Execution qua `eval`, `pickle`, hoặc command injection qua `os.system`).
2. Kẻ tấn công khai thác lỗ hổng để chạy shell script bên trong container. Do container chạy dưới quyền user `root` (UID 0), shell này có quyền tối cao trong namespace của container.
3. Kẻ tấn công lợi dụng các lỗ hổng nhân Linux (kernel exploit) hoặc Docker escape (ví dụ container mount nhầm `docker.sock` hoặc thư mục `/host`) để thoát ra ngoài môi trường máy host. Do tiến trình trong container đang chạy với UID 0, khi thoát ra ngoài host nó cũng sở hữu đặc quyền root (UID 0) trên toàn bộ máy host.
-> Lệnh `USER appuser` cắt đứt chuỗi tấn công ngay từ bước 2: Tiến trình Python chạy với quyền người dùng thường (UID 1000). Kẻ tấn công dù chiếm được shell cũng không thể ghi vào các thư mục hệ thống bên trong container, không thể cài đặt kernel module độc hại, và nếu có thoát ra ngoài host cũng chỉ có quyền của một user không đặc quyền, không thể kiểm soát máy chủ.

---

### Câu 6 — Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo
phút đồng hồ (reset lúc giây 00), một người dùng có thể gửi tối đa bao nhiêu
request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được
con số đó.

Người dùng có thể gửi tối đa **20 request** trong 2 giây liên tiếp.
Giải thích: Khi đếm theo phút đồng hồ cố định (Fixed Window Counter):
- Ở phút thứ nhất, người dùng chờ đến giây cuối cùng `10:00:59` và gửi dồn dập 10 request (vẫn hợp lệ vì hạn mức là 10 req/phút).
- Sang giây `10:01:00`, bộ đếm được reset về 0. Người dùng lập tức gửi tiếp 10 request nữa trong giây `10:01:01` (vẫn hợp lệ với khung phút mới).
- Kết quả: Trong khoảng thời gian từ `10:00:59` đến `10:01:01` (chỉ đúng 2 giây), hệ thống phải hứng chịu tới 20 request, tức gấp đôi năng lực xử lý dự kiến. Thuật toán Sliding Window khắc phục triệt để bằng cách luôn tính lùi đúng 60 giây từ thời điểm hiện tại.

---

### Câu 7 — Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua
nhưng cost guard phải chặn, và một tình huống ngược lại.

Khác biệt:
- **Rate limit**: Giới hạn **tần suất/số lượng request** trong một đơn vị thời gian (ví dụ 10 req/phút), bảo vệ hệ thống khỏi bị quá tải tài nguyên mạng/CPU.
- **Cost guard**: Giới hạn **tổng chi phí tài chính (USD)** trong một chu kỳ (ví dụ 10 USD/tháng), bảo vệ ngân sách không bị cạn kiệt do chi phí API của LLM.

Tình huống minh họa:
- *Rate limit cho qua nhưng Cost guard chặn:* User chỉ gửi 1 request trong cả ngày (hoàn toàn thỏa mãn rate limit 10 req/phút), nhưng tài khoản của user đó trong tháng đã tiêu hết 10.0 USD ngân sách. Cost guard kiểm tra `spent + estimated_cost > budget` và chặn với mã 402 Payment Required.
- *Cost guard cho qua nhưng Rate limit chặn:* User mới lập tài khoản, ngân sách tháng còn nguyên 10.0 USD (chưa tiêu đồng nào), nhưng user viết script gửi dồn dập 20 request chỉ trong 3 giây. Rate limiter phát hiện vượt quá 10 req/phút và chặn với mã 429 Too Many Requests, dù ngân sách vẫn còn thừa.

---

### Câu 8 — /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

Thứ tự sự kiện xảy ra:
1. Redis gặp sự cố mạng hoặc khởi động lại, tạm thời không phản hồi trong 30 giây.
2. Endpoint kiểm tra sức khỏe của cả 3 container gọi tới Redis thất bại và trả về lỗi 503.
3. Do endpoint này được dùng làm liveness probe, Orchestrator (Docker/Kubernetes) kết luận cả 3 container của ứng dụng đều đã bị treo/hỏng (deadlock).
4. Orchestrator lập tức cưỡng chế kill và restart đồng loạt cả 3 container.
5. Khi 3 container mới khởi động lại, chúng lại gọi kiểm tra Redis (vốn vẫn đang trong 30 giây mất kết nối) tiếp tục thất bại và tiếp tục bị restart.
6. Cả hệ thống rơi vào vòng lặp chết (CrashLoopBackOff). Đến khi Redis hồi phục, cụm app vẫn đang bận restart dở dang, gây sập dịch vụ toàn diện (cascading failure). Nếu tách riêng: `/ready` báo 503 để load balancer tạm dừng chuyển request, trong khi `/health` vẫn 200 để container tiếp tục sống và sẵn sàng phục vụ ngay khi Redis online trở lại.

---

### Câu 9 — Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một
`X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu
trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

- Nếu lưu trong Redis (Stateless): `history_length` sẽ tăng tuần tự liên tục và nhất quán: 0, 2, 4, 6... qua từng lượt hỏi, bất kể request rơi vào container nào trong 3 container vì cả 3 đều đọc và ghi chung một Redis.
- Nếu lưu trong dict Python (Stateful trong RAM): `history_length` sẽ nhảy lung tung và gián đoạn. Do load balancer phân phối request vòng tròn (round-robin) qua 3 container: request 1 vào container 1 (length = 0); request 2 vào container 2 (length = 0 vì container 2 chưa có tin nhắn nào trong RAM); request 3 vào container 3 (length = 0); request 4 quay lại container 1 (length = 2). Kết quả là agent liên tục bị "mất trí nhớ", trả lời câu hỏi sau mà không hiểu câu hỏi trước đó của cùng một user.

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

- *Thông báo lỗi gặp phải:* Lỗi `Health check failed / Service unavailable` hoặc Uvicorn bind error: `Address already in use` hoặc platform không nhận diện được cổng HTTP mở sau 60s.
- *Nguyên nhân tìm ra:* Khi kiểm tra log khởi động của platform trên dashboard, nhận thấy lệnh khởi chạy bị hardcode `uvicorn --port 8000`. Trên các nền tảng PaaS như Render hay Railway, hệ thống gán động một cổng ngẫu nhiên cho container thông qua biến môi trường `$PORT` (ví dụ `PORT=10000`). Do ứng dụng chỉ lắng nghe ở 8000, routing proxy của platform không thể kết nối tới container qua cổng mà nó mong đợi.
- *Cách khắc phục:* Đã sửa lại lệnh `CMD` trong Dockerfile và cấu hình trong `app/config.py` để đọc biến `PORT` từ môi trường: `CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]`. Nhờ đó khi chạy ở localhost cổng mặc định là 8000, còn khi lên cloud app tự động bind chính xác vào cổng do platform cấp phát.

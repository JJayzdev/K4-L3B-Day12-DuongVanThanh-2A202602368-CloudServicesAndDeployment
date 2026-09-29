"""Dashboard giao diện web trực quan để kiểm thử toàn diện Agent Service."""

from __future__ import annotations


def get_dashboard_html() -> str:
    return """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cloud Agent Console — K4-L3B Day 12</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: rgba(22, 30, 49, 0.7);
      --card-border: rgba(255, 255, 255, 0.08);
      --primary: #6366f1;
      --primary-hover: #4f46e5;
      --primary-glow: rgba(99, 102, 241, 0.25);
      --accent: #06b6d4;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
      --text: #f3f4f6;
      --text-muted: #9ca3af;
      --code-bg: #030712;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: var(--bg);
      background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.12) 0px, transparent 50%);
      background-attachment: fixed;
      color: var(--text);
      min-height: 100vh;
      line-height: 1.5;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px 20px 48px;
    }

    /* Header */
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--card-border);
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .logo-icon {
      width: 42px;
      height: 42px;
      background: linear-gradient(135deg, var(--primary), var(--accent));
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      box-shadow: 0 0 20px var(--primary-glow);
    }
    .brand-title {
      font-size: 20px;
      font-weight: 700;
      letter-spacing: -0.5px;
    }
    .brand-subtitle {
      font-size: 13px;
      color: var(--text-muted);
    }
    .header-actions {
      display: flex;
      gap: 10px;
      align-items: center;
    }

    /* Badges & Status */
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
    }
    .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--text-muted);
    }
    .dot.green { background: var(--success); box-shadow: 0 0 10px var(--success); }
    .dot.red { background: var(--danger); box-shadow: 0 0 10px var(--danger); }
    .dot.yellow { background: var(--warning); box-shadow: 0 0 10px var(--warning); }

    /* Cards Grid */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }
    .stat-card {
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 18px 20px;
      transition: transform 0.2s, border-color 0.2s;
    }
    .stat-card:hover {
      transform: translateY(-2px);
      border-color: rgba(255, 255, 255, 0.15);
    }
    .stat-label {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
    }
    .stat-value {
      font-size: 20px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .stat-desc {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 4px;
    }

    /* Auth Bar */
    .config-card {
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 20px;
      margin-bottom: 24px;
    }
    .config-title {
      font-size: 14px;
      font-weight: 600;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .config-inputs {
      display: grid;
      grid-template-columns: 2fr 1fr auto;
      gap: 12px;
    }
    @media (max-width: 768px) {
      .config-inputs { grid-template-columns: 1fr; }
    }
    input[type="text"], input[type="password"] {
      width: 100%;
      background: rgba(11, 15, 25, 0.8);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 10px 14px;
      color: var(--text);
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      transition: border-color 0.2s;
    }
    input:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px var(--primary-glow);
    }

    /* Buttons */
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 10px 16px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      border: none;
      transition: all 0.2s;
    }
    .btn-primary {
      background: var(--primary);
      color: white;
    }
    .btn-primary:hover {
      background: var(--primary-hover);
      box-shadow: 0 0 15px var(--primary-glow);
    }
    .btn-secondary {
      background: rgba(255, 255, 255, 0.08);
      color: var(--text);
      border: 1px solid var(--card-border);
    }
    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.15);
    }
    .btn-sm {
      padding: 6px 10px;
      font-size: 12px;
    }

    /* Main Workspace */
    .main-grid {
      display: grid;
      grid-template-columns: 1.4fr 1fr;
      gap: 24px;
    }
    @media (max-width: 900px) {
      .main-grid { grid-template-columns: 1fr; }
    }

    /* Chat Section */
    .chat-card {
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      height: 600px;
    }
    .chat-header {
      padding: 16px 20px;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .chat-messages {
      flex: 1;
      padding: 20px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .message {
      display: flex;
      flex-direction: column;
      max-width: 85%;
      animation: fadeIn 0.3s ease;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .message.user {
      align-self: flex-end;
      align-items: flex-end;
    }
    .message.agent {
      align-self: flex-start;
      align-items: flex-start;
    }
    .bubble {
      padding: 12px 16px;
      border-radius: 14px;
      font-size: 14px;
      line-height: 1.6;
    }
    .message.user .bubble {
      background: var(--primary);
      color: white;
      border-bottom-right-radius: 4px;
    }
    .message.agent .bubble {
      background: rgba(30, 41, 69, 0.8);
      border: 1px solid var(--card-border);
      border-bottom-left-radius: 4px;
    }
    .msg-meta {
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 4px;
      display: flex;
      gap: 10px;
    }
    .chat-input-bar {
      padding: 16px 20px;
      border-top: 1px solid var(--card-border);
      display: flex;
      gap: 10px;
    }
    .quick-questions {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-bottom: 10px;
    }
    .chip {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 4px 10px;
      font-size: 11px;
      cursor: pointer;
      color: var(--text-muted);
      transition: all 0.2s;
    }
    .chip:hover {
      background: rgba(99, 102, 241, 0.2);
      border-color: var(--primary);
      color: var(--text);
    }

    /* Test Tools Column */
    .tools-column {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .tool-box {
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 20px;
    }
    .tool-header {
      font-size: 14px;
      font-weight: 700;
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .log-stream {
      background: var(--code-bg);
      border-radius: 10px;
      padding: 12px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      height: 140px;
      overflow-y: auto;
      color: #94a3b8;
    }
    .log-entry { margin-bottom: 4px; }
    .log-entry.ok { color: var(--success); }
    .log-entry.err { color: var(--danger); }
    .log-entry.warn { color: var(--warning); }

    /* Progress bar */
    .progress-bar-bg {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      height: 10px;
      overflow: hidden;
      margin: 10px 0;
    }
    .progress-bar-fill {
      background: linear-gradient(90deg, var(--primary), var(--accent));
      height: 100%;
      width: 0%;
      transition: width 0.4s ease;
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- Header -->
    <header>
      <div class="brand">
        <div class="logo-icon">⚡</div>
        <div>
          <div class="brand-title">Cloud AI Agent Console</div>
          <div class="brand-subtitle">K4-L3B Day 12 — Cloud Infrastructure & Deployment</div>
        </div>
      </div>
      <div class="header-actions">
        <button class="btn btn-secondary btn-sm" onclick="checkAllProbes()">
          🔄 Kiểm tra Probe
        </button>
      </div>
    </header>

    <!-- Top Live Stats -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">
          <span>Liveness Probe</span>
          <span class="status-badge" id="badge-health"><span class="dot yellow"></span> Đang đo...</span>
        </div>
        <div class="stat-value" id="val-health">/health</div>
        <div class="stat-desc" id="desc-health">Độc lập hoàn toàn, không gọi Redis</div>
      </div>

      <div class="stat-card">
        <div class="stat-label">
          <span>Readiness Probe</span>
          <span class="status-badge" id="badge-ready"><span class="dot yellow"></span> Đang đo...</span>
        </div>
        <div class="stat-value" id="val-ready">/ready</div>
        <div class="stat-desc" id="desc-ready">Kiểm tra kết nối Redis state store</div>
      </div>

      <div class="stat-card">
        <div class="stat-label">
          <span>Hạn mức Rate Limit</span>
          <span class="status-badge">60s Window</span>
        </div>
        <div class="stat-value">10 req / min</div>
        <div class="stat-desc">Sliding window với Redis Sorted Set</div>
      </div>

      <div class="stat-card">
        <div class="stat-label">
          <span>Ngân sách người dùng</span>
          <span class="status-badge" id="badge-budget">Active</span>
        </div>
        <div class="stat-value">$10.00 / tháng</div>
        <div class="stat-desc">Cost Guard tự động chặn HTTP 402</div>
      </div>
    </div>

    <!-- Auth Settings -->
    <div class="config-card">
      <div class="config-title">🔑 Cấu hình Header Xác thực (Client Credentials)</div>
      <div class="config-inputs">
        <input type="text" id="input-api-key" placeholder="Nhập X-API-Key (để trống nếu muốn thử 401 Unauthorized)...">
        <input type="text" id="input-user-id" value="sv-test" placeholder="X-User-Id">
        <div style="display:flex; gap: 8px;">
          <button class="btn btn-secondary btn-sm" onclick="presetKey('correct')">Dán Key Hợp Lệ</button>
          <button class="btn btn-secondary btn-sm" onclick="presetKey('wrong')">Key Sai</button>
          <button class="btn btn-secondary btn-sm" onclick="presetKey('empty')">Xóa Key</button>
        </div>
      </div>
    </div>

    <!-- Main Section -->
    <div class="main-grid">
      <!-- Chat Interface -->
      <div class="chat-card">
        <div class="chat-header">
          <strong>💬 Agent Conversation Playground (/ask)</strong>
          <span style="font-size: 12px; color: var(--text-muted);" id="chat-stat">0 tin nhắn được lưu</span>
        </div>
        <div class="chat-messages" id="chat-messages">
          <div class="message agent">
            <div class="bubble">
              Xin chào! Mình là AI Agent được triển khai trên hạ tầng Cloud. Bạn có thể hỏi bất cứ điều gì về Docker, Kubernetes, 12-Factor App hoặc kiến trúc Stateless.
            </div>
            <div class="msg-meta"><span>Hệ thống sẵn sàng</span></div>
          </div>
        </div>

        <div style="padding: 0 20px;">
          <div class="quick-questions">
            <span class="chip" onclick="askQuick('Docker là gì?')">Docker là gì?</span>
            <span class="chip" onclick="askQuick('Phân biệt liveness và readiness probe?')">Liveness vs Readiness?</span>
            <span class="chip" onclick="askQuick('Tại sao cần đưa state sang Redis?')">Tại sao cần Redis?</span>
            <span class="chip" onclick="askQuick('12-Factor App quy định config thế nào?')">12-Factor Config?</span>
          </div>
        </div>

        <div class="chat-input-bar">
          <input type="text" id="chat-input" placeholder="Nhập câu hỏi cho Agent..." onkeydown="if(event.key==='Enter') sendQuestion()">
          <button class="btn btn-primary" onclick="sendQuestion()" id="btn-send">Gửi</button>
        </div>
      </div>

      <!-- Testing Tools -->
      <div class="tools-column">
        <!-- Rate Limit Tester -->
        <div class="tool-box">
          <div class="tool-header">
            <span>⚡ Kiểm tra Sliding Window Rate Limit</span>
            <button class="btn btn-primary btn-sm" onclick="testSpamRequests()">🚀 Spam 15 Requests</button>
          </div>
          <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">
            Hạn mức là 10 req/phút. Bấm nút trên để gửi dồn dập 15 request liên tiếp nhằm quan sát mã <code>429 Too Many Requests</code> và header <code>Retry-After</code>.
          </p>
          <div class="log-stream" id="rate-log">
            <div class="log-entry">// Bấm "Spam 15 Requests" để xem kết quả...</div>
          </div>
        </div>

        <!-- Cost Guard Inspector -->
        <div class="tool-box">
          <div class="tool-header">
            <span>💰 Cost Guard & Quota</span>
            <span id="cost-spent-label" style="font-size: 12px; color: var(--accent);">$0.00 / $10.00</span>
          </div>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" id="cost-progress"></div>
          </div>
          <p style="font-size: 12px; color: var(--text-muted);">
            Mỗi lượt gọi thành công sẽ tính chi phí dựa trên số token input/output. Nếu vượt $10.00/tháng, hệ thống sẽ trả về mã <code>402 Payment Required</code>.
          </p>
        </div>

        <!-- cURL Inspector -->
        <div class="tool-box">
          <div class="tool-header">
            <span>💻 Lệnh cURL Nhanh</span>
            <button class="btn btn-secondary btn-sm" onclick="copyCurl()">Sao chép cURL</button>
          </div>
          <div class="log-stream" id="curl-box" style="height: 110px;">
curl -i -X POST [ORIGIN]/ask \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: [KEY]" \\
  -H "X-User-Id: sv-test" \\
  -d '{"question":"Hello"}'
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    let totalCost = 0.0;
    const maxBudget = 10.0;

    async function checkAllProbes() {
      // Health Probe
      try {
        const t0 = performance.now();
        const rHealth = await fetch('/health');
        const msHealth = Math.round(performance.now() - t0);
        const dataHealth = await rHealth.json();
        
        if (rHealth.ok) {
          document.getElementById('badge-health').innerHTML = '<span class="dot green"></span> ' + rHealth.status + ' OK';
          document.getElementById('desc-health').innerText = `Ping: ${msHealth}ms • Service: ${dataHealth.service || 'day12-agent'}`;
        } else {
          document.getElementById('badge-health').innerHTML = '<span class="dot red"></span> ' + rHealth.status;
          document.getElementById('desc-health').innerText = JSON.stringify(dataHealth);
        }
      } catch (err) {
        document.getElementById('badge-health').innerHTML = '<span class="dot red"></span> Lỗi';
        document.getElementById('desc-health').innerText = err.message;
      }

      // Ready Probe
      try {
        const t0 = performance.now();
        const rReady = await fetch('/ready');
        const msReady = Math.round(performance.now() - t0);
        const dataReady = await rReady.json().catch(() => ({}));
        
        if (rReady.ok) {
          document.getElementById('badge-ready').innerHTML = '<span class="dot green"></span> 200 Ready';
          document.getElementById('desc-ready').innerText = `Redis: Connected • Ping: ${msReady}ms`;
        } else {
          document.getElementById('badge-ready').innerHTML = '<span class="dot red"></span> ' + rReady.status;
          document.getElementById('desc-ready').innerText = dataReady.redis === false ? 'Redis chưa kết nối / Đang tắt' : JSON.stringify(dataReady);
        }
      } catch (err) {
        document.getElementById('badge-ready').innerHTML = '<span class="dot red"></span> Lỗi 500';
        document.getElementById('desc-ready').innerText = 'Kiểm tra biến AGENT_API_KEY & REDIS_URL trên Cloud';
      }
    }

    function presetKey(type) {
      const input = document.getElementById('input-api-key');
      if (type === 'correct') {
        // Lấy key từ query param hoặc giá trị default được set
        input.value = "QjaRW9p-fZ0XMWVSEZU0XUnTzzSsecc-79DrAufrhy0";
      } else if (type === 'wrong') {
        input.value = "khoa-sai-hoan-toan-123";
      } else {
        input.value = "";
      }
      updateCurlBox();
    }

    function updateCurlBox() {
      const key = document.getElementById('input-api-key').value || 'YOUR_KEY';
      const user = document.getElementById('input-user-id').value || 'anonymous';
      const origin = window.location.origin;
      document.getElementById('curl-box').innerText = 
`curl -i -X POST ${origin}/ask \\\\
  -H "Content-Type: application/json" \\\\
  -H "X-API-Key: ${key}" \\\\
  -H "X-User-Id: ${user}" \\\\
  -d '{"question":"Docker là gì?"}'`;
    }

    function copyCurl() {
      const text = document.getElementById('curl-box').innerText;
      navigator.clipboard.writeText(text);
      alert('Đã sao chép lệnh cURL vào bộ nhớ tạm!');
    }

    function askQuick(q) {
      document.getElementById('chat-input').value = q;
      sendQuestion();
    }

    async function sendQuestion() {
      const input = document.getElementById('chat-input');
      const question = input.value.trim();
      if (!question) return;

      const apiKey = document.getElementById('input-api-key').value;
      const userId = document.getElementById('input-user-id').value || 'anonymous';

      // Render user message
      const chatBox = document.getElementById('chat-messages');
      chatBox.innerHTML += `
        <div class="message user">
          <div class="bubble">${escapeHtml(question)}</div>
          <div class="msg-meta"><span>Bạn (${userId})</span></div>
        </div>
      `;
      input.value = '';
      chatBox.scrollTop = chatBox.scrollHeight;

      const btn = document.getElementById('btn-send');
      btn.disabled = true;
      btn.innerText = '...';

      const t0 = performance.now();
      try {
        const headers = { 'Content-Type': 'application/json' };
        if (apiKey) headers['X-API-Key'] = apiKey;
        if (userId) headers['X-User-Id'] = userId;

        const res = await fetch('/ask', {
          method: 'POST',
          headers: headers,
          body: JSON.stringify({ question: question })
        });
        const ms = Math.round(performance.now() - t0);
        const data = await res.json().catch(() => ({}));

        if (res.status === 200) {
          totalCost += data.cost_usd || 0;
          updateCostUI();
          document.getElementById('chat-stat').innerText = `${data.history_length + 2} tin nhắn trong lịch sử Redis`;

          chatBox.innerHTML += `
            <div class="message agent">
              <div class="bubble">${escapeHtml(data.answer)}</div>
              <div class="msg-meta">
                <span>⏱ ${ms}ms</span>
                <span>🪙 In: ${data.tokens.in} / Out: ${data.tokens.out}</span>
                <span>💰 $${data.cost_usd.toFixed(6)}</span>
                <span>📜 History: ${data.history_length}</span>
              </div>
            </div>
          `;
        } else if (res.status === 401) {
          chatBox.innerHTML += `
            <div class="message agent">
              <div class="bubble" style="background: rgba(239, 68, 68, 0.2); border-color: var(--danger);">
                ⚠️ <strong>Lỗi 401 Unauthorized:</strong> ${escapeHtml(data.detail || 'Khóa API không hợp lệ hoặc bị thiếu')}. Hãy kiểm tra ô X-API-Key ở trên!
              </div>
              <div class="msg-meta"><span style="color:var(--danger)">HTTP 401</span></div>
            </div>
          `;
        } else if (res.status === 429) {
          chatBox.innerHTML += `
            <div class="message agent">
              <div class="bubble" style="background: rgba(245, 158, 11, 0.2); border-color: var(--warning);">
                ⏳ <strong>Lỗi 429 Rate Limit Exceeded:</strong> Bạn đã gọi quá 10 request/phút. Vui lòng thử lại sau!
              </div>
              <div class="msg-meta"><span style="color:var(--warning)">HTTP 429</span></div>
            </div>
          `;
        } else if (res.status === 402) {
          chatBox.innerHTML += `
            <div class="message agent">
              <div class="bubble" style="background: rgba(239, 68, 68, 0.2); border-color: var(--danger);">
                💳 <strong>Lỗi 402 Payment Required:</strong> Đã vượt quá ngân sách tháng $10.00 của user!
              </div>
              <div class="msg-meta"><span style="color:var(--danger)">HTTP 402</span></div>
            </div>
          `;
        } else {
          chatBox.innerHTML += `
            <div class="message agent">
              <div class="bubble" style="background: rgba(239, 68, 68, 0.2);">
                ❌ Lỗi ${res.status}: ${escapeHtml(JSON.stringify(data))}
              </div>
            </div>
          `;
        }
      } catch (err) {
        chatBox.innerHTML += `
          <div class="message agent">
            <div class="bubble" style="background: rgba(239, 68, 68, 0.2);">
              ❌ Lỗi mạng: ${escapeHtml(err.message)}
            </div>
          </div>
        `;
      } finally {
        btn.disabled = false;
        btn.innerText = 'Gửi';
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    }

    async function testSpamRequests() {
      const log = document.getElementById('rate-log');
      log.innerHTML = `<div class="log-entry">// Đang gửi 15 requests đồng thời...</div>`;
      
      const apiKey = document.getElementById('input-api-key').value;
      const userId = document.getElementById('input-user-id').value || 'sv-spam';

      const headers = { 'Content-Type': 'application/json' };
      if (apiKey) headers['X-API-Key'] = apiKey;
      headers['X-User-Id'] = userId;

      const promises = [];
      for (let i = 1; i <= 15; i++) {
        promises.push(
          fetch('/ask', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({ question: `Spam test #${i}` })
          }).then(async r => {
            const data = await r.json().catch(() => ({}));
            return {
              id: i,
              status: r.status,
              retryAfter: r.headers.get('retry-after'),
              detail: data.detail || (r.status === 200 ? 'OK' : 'Error')
            };
          }).catch(err => ({ id: i, status: 'NET_ERR', detail: err.message }))
        );
      }

      const results = await Promise.all(promises);
      log.innerHTML = '';
      results.forEach(res => {
        let cls = res.status === 200 ? 'ok' : (res.status === 429 ? 'warn' : 'err');
        let extra = res.retryAfter ? ` [Retry-After: ${res.retryAfter}s]` : '';
        log.innerHTML += `<div class="log-entry ${cls}">#${String(res.id).padStart(2, '0')}: HTTP ${res.status} — ${res.detail}${extra}</div>`;
      });
      log.scrollTop = log.scrollHeight;
    }

    function updateCostUI() {
      const pct = Math.min(100, (totalCost / maxBudget) * 100);
      document.getElementById('cost-progress').style.width = pct + '%';
      document.getElementById('cost-spent-label').innerText = `$${totalCost.toFixed(5)} / $${maxBudget.toFixed(2)}`;
    }

    function escapeHtml(text) {
      if (!text) return '';
      return String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    // Auto load
    window.addEventListener('DOMContentLoaded', () => {
      presetKey('correct');
      checkAllProbes();
      setInterval(checkAllProbes, 30000); // 30s probe poll
    });
  </script>
</body>
</html>
"""

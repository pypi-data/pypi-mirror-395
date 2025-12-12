# n8n + n8nagent — Cài đặt nhanh và cấu hình (Docker, Nginx, Supervisor)

Hướng dẫn này mô tả các bước cài đặt và cấu hình n8n (chạy dưới Docker) và `n8nagent` (n8nControl) — agent Python để quản lý n8n trên VPS.

Tài liệu bao gồm chỉ dẫn cho Ubuntu/Debian và CentOS, cấu hình Nginx reverse-proxy, cách chạy n8n bằng Docker, cài đặt `n8nControl` (n8nagent) bằng pip, và cấu hình Supervisor để quản lý agent.

---

## Mục lục
- [Yêu cầu](#yêu-cầu)
- [Phần 1 — Cài đặt n8n (Docker)](#phần-1---cài-đặt-n8n-docker)
	- Cài Docker
	- Chạy container n8n
	- Cấu hình Nginx reverse-proxy
- [Phần 2 — Cài đặt n8nagent (n8nControl)](#phần-2---cài-đặt-n8nagent-n8ncontrol)
	- Cài Python / pip
	- Cài `n8nControl`
	- Tạo và cấu hình Supervisor
	- Cấu hình Nginx reverse-proxy cho n8nagent
- [Bảo mật & vận hành (tips)](#bảo-mật--vận-hành-tips)
- [Troubleshooting nhanh](#troubleshooting-nhanh)

---

## Yêu cầu
- Một máy chủ VPS (Ubuntu/Debian hoặc CentOS/Rocky/AlmaLinux)
- Quyền root hoặc sudo
- Docker (để chạy n8n container)
- Python 3.8+ và pip (để chạy n8nagent / n8nControl)

---

## Phần 1 — Cài đặt n8n (Docker) (CHUẨN 2025)

1) Cài Docker (recommended, 2025)

Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
	| sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
	"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
	https://download.docker.com/linux/ubuntu \
	$(lsb_release -cs) stable" \
	| sudo tee /etc/apt/sources.list.d/docker.list >/dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl enable --now docker
```

CentOS / Rocky / AlmaLinux

```bash
sudo dnf install -y yum-utils epel-release
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
```

2) Tạo thư mục lưu data n8n (quan trọng)

n8n trong container sử dụng user UID 1000 (thường là user `node`). Vì vậy thư mục trên host phải có ownership 1000:1000 để tránh vấn đề quyền khi container ghi file.

```bash
sudo mkdir -p /root/n8n
# đặt quyền owner là UID 1000 (user bên trong container)
sudo chown -R 1000:1000 /root/n8n
sudo chmod -R 775 /root/n8n
```

3) Chạy container n8n

Chạy n8n với volume đã chuẩn bị:

```bash
docker run -d \
	--name n8n \
	--restart=always \
	-p 5678:5678 \
	-v /root/n8n:/home/node/.n8n \
	n8nio/n8n
```

Kiểm tra:

```bash
docker ps        # kiểm tra container đang chạy
curl -I http://127.0.0.1:5678
```

4) Cấu hình Nginx (reverse-proxy)

Tạo file `/etc/nginx/conf.d/n8n.conf` với nội dung mẫu sau (thay `your-domain.example.com` bằng domain bạn sử dụng):

```nginx
server {
	listen 80;
	server_name _;
	return 444;
}

server {
	listen 80;
	server_name your-domain.example.com;

	location / {
		proxy_pass http://127.0.0.1:5678;
		proxy_http_version 1.1;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header Upgrade $http_upgrade;
		proxy_set_header Connection "upgrade";
	}
}
```

Kiểm tra và reload Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Gợi ý HTTPS (khuyến nghị):
- Dùng certbot / Let's Encrypt để bật TLS cho domain (`sudo apt install certbot python3-certbot-nginx` sau đó `sudo certbot --nginx -d your-domain.example.com`).
- Bật HTTPS là bắt buộc cho môi trường production (bảo mật cookie, authentication, webhook callbacks, WSS).

---

---

## Phần 2 — Cài đặt n8nagent (n8nControl)
Agent này giúp bạn quản lý n8n (import/export workflows, restart, update) — cài đặt bằng Python package `n8nControl`.

1) Cài Python & pip

Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

CentOS / Rocky / AlmaLinux

```bash
sudo dnf install -y python3 python3-pip
```

2) Cài `n8nControl` (n8nagent)

Bạn có thể cài global hoặc trong virtualenv. Ví dụ cài global via pip:

```bash
sudo pip install n8nControl
```

Kiểm tra lệnh:

```bash
n8nagent --help
```

3) Cài Supervisor để quản lý service (Ubuntu/Debian / CentOS)

Ubuntu / Debian

```bash
sudo apt install -y supervisor
sudo systemctl enable --now supervisor
```

CentOS / Rocky / AlmaLinux

```bash
sudo dnf install -y epel-release
sudo dnf install -y supervisor
sudo systemctl enable --now supervisord
```

4) Tạo cấu hình Supervisor cho n8nagent

Ubuntu / Debian — tạo `/etc/supervisor/conf.d/n8napp.conf`:

```
[program:n8napp]
command=n8nagent
autostart=true
autorestart=true
stderr_logfile=/var/log/n8n.err.log
stdout_logfile=/var/log/n8n.out.log


# nếu bạn chạy trong virtualenv, command nên là đường dẫn tới venv: /path/to/venv/bin/n8nagent
```

CentOS — tạo `/etc/supervisord.d/n8napp.ini` (tương tự nội dung trên)

Sau khi thêm file cấu hình, reload Supervisor:

```bash
# Ubuntu/Debian
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart n8napp

# CentOS (supervisord)
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart n8napp
```

Xem trạng thái:

```bash
sudo supervisorctl status n8napp
```

5) Cấu hình Nginx reverse proxy cho n8nagent (tùy chọn)

Nếu bạn muốn truy cập web UI của agent (ví dụ agent cung cấp UI tại port 9000), config Nginx tương tự như n8n:

```nginx
server {
	listen 80;
	server_name n8n-agent.example.com;

	location / {
		proxy_pass http://127.0.0.1:9000;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
		proxy_read_timeout 300;
		proxy_connect_timeout 300;
		proxy_send_timeout 300;
	}
}
```

Kiểm tra và reload Nginx như trên.

---



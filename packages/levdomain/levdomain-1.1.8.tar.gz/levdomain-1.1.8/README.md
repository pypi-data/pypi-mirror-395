# Levdomain — hướng dẫn triển khai (rõ ràng & ngắn gọn)

Hướng dẫn này mô tả các bước triển khai Bind9 (Master/Slave), cài đặt "domain agent" (gói `levdomain`), cấu hình `supervisor` và reverse proxy bằng Nginx. Nội dung được viết cho hệ điều hành Debian/Ubuntu.

Mục lục
- Giới thiệu
- Yêu cầu
- 1) Cài Bind9 (Master)
  - Cài đặt
  - Cấu hình chính
  - Tạo zone file
  - Kiểm tra và khởi động lại
- 2) Cấu hình Bind9 (Slave)
- 3) Cài và cấu hình Levdomain (domain agent)
- 4) Cấu hình Supervisor
- 5) Cấu hình Nginx (reverse proxy)
- Kiểm tra và khắc phục sự cố
- Liên hệ & License

---

## Giới thiệu

Levdomain (hay "domain agent") là một công cụ Python dùng kèm với Bind9 để quản lý zone / đồng bộ vùng DNS. README này chỉ tập trung vào các bước triển khai cơ bản và kiểm tra hoạt động.

## Yêu cầu
- Hệ điều hành: Debian/Ubuntu (hoặc tương đương)
- Quyền root / sudo
- Python 3 và pip
- bind9, supervisor, nginx (tuỳ theo môi trường)

## 1) Cài Bind9 (Master)

### 1.1 Cài đặt cơ bản

Chạy những lệnh sau:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install bind9 bind9utils bind9-doc -y

# Kiểm tra trạng thái service
systemctl status bind9
```

### 1.2 Cấu hình chính (named.conf.options)

Mở file cấu hình:

```bash
sudo nano /etc/bind/named.conf.options
```

Và thêm / chỉnh sửa phần `options` (ví dụ):

```conf
options {
    directory "/var/cache/bind";
    recursion no;                     # tắt recursion cho sản xuất
    allow-transfer { 192.168.1.11; }; # IP slave hoặc các máy cho phép AXFR
    notify yes;
    dnssec-validation auto;
    listen-on { any; };
    listen-on-v6 { any; };
};
```

### 1.3 Khai báo zone (named.conf.local)

Mở file:

```bash
sudo nano /etc/bind/named.conf.local
```

Thêm khai báo zone (master):

```conf
zone "example.com" {
    type master;
    file "/etc/bind/zones/db.example.com";
    allow-transfer { 107.167.82.3; }; # IP slave nếu cần
    notify yes;
};
```

### 1.4 Tạo zone file

Tạo thư mục và file zone:

```bash
sudo mkdir -p /etc/bind/zones
sudo nano /etc/bind/zones/db.example.com
```

Ví dụ nội dung file zone:

```dns
$TTL 86400

@   IN  SOA ns2.example.com. admin.example.com. (
        20250328 ; serial
        3600     ; refresh
        1800     ; retry
        604800   ; expire
        86400    ; minimum
)

@       IN  NS  ns1.example.com.
@       IN  NS  ns2.example.com.

ns1     IN  A   107.167.82.3
ns2     IN  A   148.163.73.102

@       IN  A   103.130.216.175
www     IN  A   103.130.216.175
```

### 1.5 Kiểm tra & khởi động lại Bind

```bash
sudo named-checkconf
sudo named-checkzone example.com /etc/bind/zones/db.example.com
sudo systemctl restart bind9
```

## 2) Cấu hình Bind9 (Slave)

Trên máy slave, chỉnh `named.conf.local` để khai báo zone dạng `slave`:

```conf
zone "example.com" {
    type slave;
    masters { 148.163.73.102; };
    file "/var/cache/bind/db.example.com";
};
```

Sau đó khởi động lại bind:

```bash
sudo systemctl restart bind9
ls -l /var/cache/bind/   # kiểm tra file zone nhận về
```

Nếu thấy file zone `db.example.com` trong `/var/cache/bind/` thì slave đã đồng bộ thành công.

## 3) Cài đặt Levdomain (domain agent)

Trên máy cần chạy `levdomain` (thường là ứng dụng hoặc agent xử lý các cập nhật):

```bash
sudo apt install python3 python3-pip -y
sudo apt install supervisor -y      # nếu dùng supervisor để quản lý service
pip install levdomain
```

Ghi chú: nếu `levdomain` được cài lên bằng phương pháp khác (venv, distro package), điều chỉnh lệnh đường dẫn tương ứng.

## 4) Cấu hình Supervisor (ví dụ)

Tạo file conf cho supervisor:

```bash
sudo nano /etc/supervisor/conf.d/levdomain.conf
```

Mẫu cấu hình:

```ini
[program:levdomain]
command=/usr/local/bin/levdomain
autostart=true
autorestart=true
stderr_logfile=/var/log/levdomain.err.log
stdout_logfile=/var/log/levdomain.out.log
```

Sau đó cập nhật supervisor và khởi động service:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start levdomain
```

## 5) Cấu hình Nginx (reverse proxy)

Ví dụ khối cấu hình Nginx để forward traffic tới ứng dụng chạy trên localhost:7000

```nginx
server {
    listen 80;
    server_name example.com;  # thay bằng IP hoặc hostname

    location / {
        proxy_pass http://127.0.0.1:7000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Kích hoạt và reload Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/levdomain /etc/nginx/sites-enabled/  # nếu chưa tồn tại
sudo systemctl restart nginx
```


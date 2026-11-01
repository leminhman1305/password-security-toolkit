# Password Security Toolkit

Ứng dụng desktop Python/Tkinter phục vụ học tập về kiểm tra
mật khẩu, password policy, sinh mật khẩu và password hashing.

## Chức năng

- Kiểm tra password policy từ file JSON.
- Đánh giá độ mạnh bằng các quy tắc minh họa.
- Phát hiện một số mật khẩu phổ biến, chuỗi và mẫu lặp.
- Sinh mật khẩu ngẫu nhiên bằng thư viện secrets.
- Hash và xác minh mật khẩu bằng Argon2id.
- Minh họa cùng mật khẩu tạo hai hash khác nhau nhờ salt.
- Kiểm thử tự động bằng pytest.

## Công nghệ

- Python 3.12
- Tkinter
- argon2-cffi
- pytest

## Cài đặt trên Windows

Mở PowerShell tại thư mục dự án:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Tkinter cần có trong bản cài Python.

## Chạy giao diện

```powershell
.\.venv\Scripts\python.exe gui.py
```

Giao diện gồm:

1. Kiểm tra policy và đánh giá độ mạnh.
2. Cửa sổ tạo mật khẩu ngẫu nhiên.
3. Cửa sổ thực hành hash và xác minh Argon2id.

## Chạy kiểm thử

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Kiểm thử bao gồm:

- Mật khẩu rỗng, quá ngắn và quá dài.
- Giới hạn 8 và 16 ký tự.
- Unicode và mật khẩu phổ biến.
- Phân biệt đạt policy với độ mạnh.
- Mật khẩu sinh ra đáp ứng policy.
- Hash khác nhau cho cùng mật khẩu.
- Xác minh mật khẩu đúng và sai.

## Password policy

Cấu hình trong policy.json.

Mặc định của dự án:

- Tối thiểu 8, tối đa 16 ký tự.
- Không bắt buộc mọi nhóm ký tự.
- Chặn danh sách mật khẩu phổ biến minh họa.

Giới hạn 16 ký tự là lựa chọn cho bài thực hành.
Ứng dụng thực tế nên hỗ trợ mật khẩu dài hơn và passphrase.

## Hashing

Sử dụng Argon2id với:

- memory_cost: 65536 KiB
- time_cost: 3
- parallelism: 4
- salt_len: 16 byte
- hash_len: 32 byte

Thư viện tự tạo salt ngẫu nhiên.
Chương trình xác minh bằng hash, không giải mã mật khẩu.
Tham số cần được đánh giá lại theo môi trường triển khai.

## Cấu trúc

- main.py: giao diện dòng lệnh.
- gui.py: giao diện desktop chính.
- password_policy.py: đọc và kiểm tra policy.
- strength_checker.py: đánh giá theo quy tắc.
- password_generator.py: sinh mật khẩu và cửa sổ tạo mật khẩu.
- hashing_tool.py: Argon2id và cửa sổ thực hành hashing.
- policy.json: cấu hình chính sách.
- test_toolkit.py: kiểm thử tự động.

## Hạn chế

- Điểm độ mạnh là đánh giá theo quy tắc, không phải phần trăm an toàn.
- Danh sách mật khẩu phổ biến chỉ là danh sách minh họa.
- Chưa kiểm tra mật khẩu rò rỉ, thông tin cá nhân hoặc việc dùng lại.
- Đạt policy không đồng nghĩa với mật khẩu mạnh.
- Hashing không khắc phục việc chọn mật khẩu dễ đoán.
- Chưa triển khai hệ thống tài khoản hoặc lưu trữ cơ sở dữ liệu.

Ứng dụng không chủ động ghi mật khẩu hay hash vào file và không
gửi chúng qua mạng. Dữ liệu vẫn tồn tại trong bộ nhớ khi sử dụng;
Python không bảo đảm xóa sạch dữ liệu nhạy cảm khỏi RAM.

Dùng mật khẩu giả để thực hành và chụp ảnh demo.
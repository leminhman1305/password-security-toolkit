import secrets
import string
import tkinter as tk
from tkinter import messagebox

from password_policy import check_policy, load_policy


def generate_password(length, policy):
    """Tao mat khau ngau nhien va bao dam dat policy."""
    if not policy["min_length"] <= length <= policy["max_length"]:
        raise ValueError(
            f"Do dai phai tu {policy['min_length']} "
            f"den {policy['max_length']}."
        )

    alphabet = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*()-_=+?"
    )

    # Thu lai neu mat khau chua dap ung policy
    for _ in range(1000):
        password = "".join(
            secrets.choice(alphabet) for _ in range(length)
        )

        if not check_policy(password, policy):
            return password

    raise ValueError(
        "Khong tao duoc mat khau dap ung policy. "
        "Hay kiem tra cau hinh."
    )


def open_generator(parent):
    try:
        policy = load_policy()
    except (OSError, ValueError, KeyError, TypeError) as error:
        messagebox.showerror(
            "Lỗi policy", str(error), parent=parent
        )
        return

    window = tk.Toplevel(parent)
    window.title("Tạo mật khẩu")
    window.geometry("580x380")
    window.resizable(False, False)
    window.configure(bg="#0f172a")
    window.transient(parent)

    content = tk.Frame(window, bg="#0f172a")
    content.pack(fill="both", expand=True, padx=28, pady=24)

    tk.Label(
        content,
        text="Tạo mật khẩu ngẫu nhiên",
        bg="#0f172a",
        fg="#f1f5f9",
        font=("Segoe UI", 20, "bold"),
    ).pack(anchor="w")

    tk.Label(
        content,
        text=(
            f"Chọn độ dài từ {policy['min_length']} "
            f"đến {policy['max_length']} ký tự"
        ),
        bg="#0f172a",
        fg="#94a3b8",
        font=("Segoe UI", 11),
    ).pack(anchor="w", pady=(8, 14))

    length_value = tk.StringVar(
        value=str(min(16, policy["max_length"]))
    )

    # Bao dam gia tri mac dinh nam trong policy
    length_value.set(
        str(max(policy["min_length"], int(length_value.get())))
    )

    tk.Spinbox(
        content,
        from_=policy["min_length"],
        to=policy["max_length"],
        textvariable=length_value,
        width=8,
        font=("Segoe UI", 13),
    ).pack(anchor="w")

    result_value = tk.StringVar()

    tk.Entry(
        content,
        textvariable=result_value,
        state="readonly",
        readonlybackground="#1e293b",
        fg="#4ade80",
        font=("Consolas", 16),
        relief="flat",
    ).pack(fill="x", pady=20, ipady=12)

    status = tk.Label(
        content,
        text="Kết quả sẽ hiển thị rõ trên màn hình, không lưu vào file.",
        bg="#0f172a",
        fg="#94a3b8",
        font=("Segoe UI", 10),
        wraplength=510,
        justify="left",
    )
    status.pack(anchor="w")

    def create():
        try:
            length = int(length_value.get())
            password = generate_password(length, policy)
        except (ValueError, KeyError, TypeError) as error:
            messagebox.showerror(
                "Không tạo được mật khẩu",
                str(error),
                parent=window,
            )
            return

        result_value.set(password)
        status.configure(
            text="Đã tạo bằng secrets và kiểm tra đạt policy."
        )

    tk.Button(
        content,
        text="Tạo mật khẩu mới",
        command=create,
        bg="#38bdf8",
        fg="#0f172a",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        padx=18,
        pady=10,
        cursor="hand2",
    ).pack(anchor="w", pady=(16, 0))
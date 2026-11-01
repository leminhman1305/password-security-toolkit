import tkinter as tk
from tkinter import messagebox

from argon2 import PasswordHasher, Type
from argon2.exceptions import (
    HashingError,
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)

from password_policy import check_policy, load_policy


# Tham so duoc ghi trong chuoi hash
HASHER = PasswordHasher(
    type=Type.ID,
    time_cost=3,
    memory_cost=65536,  # KiB = 64 MiB
    parallelism=4,
    hash_len=32,
    salt_len=16,
)


def hash_password(password):
    return HASHER.hash(password)


def verify_password(encoded_hash, password):
    try:
        HASHER.verify(encoded_hash, password)
        return True
    except VerifyMismatchError:
        return False


def open_hashing_tool(parent):
    window = tk.Toplevel(parent)
    window.title("Argon2id — Hash & xác minh")
    window.geometry("720x650")
    window.minsize(650, 600)
    window.configure(bg="#0f172a")
    window.transient(parent)

    # Chi giu hash trong phien cua so hien tai
    state = {"hash": None}

    content = tk.Frame(window, bg="#0f172a")
    content.pack(fill="both", expand=True, padx=24, pady=20)

    def label(text):
        widget = tk.Label(
            content,
            text=text,
            bg="#0f172a",
            fg="#f1f5f9",
            font=("Segoe UI", 11),
            anchor="w",
            justify="left",
            wraplength=650,
        )
        widget.pack(fill="x", pady=(10, 6))
        return widget

    def entry():
        widget = tk.Entry(
            content,
            show="*",
            bg="#1e293b",
            fg="#f1f5f9",
            insertbackground="white",
            font=("Segoe UI", 13),
            relief="flat",
        )
        widget.pack(fill="x", ipady=9)
        return widget

    def button(text, command):
        widget = tk.Button(
            content,
            text=text,
            command=command,
            bg="#38bdf8",
            fg="#0f172a",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=15,
            pady=9,
            cursor="hand2",
        )
        widget.pack(anchor="w", pady=(12, 6))
        return widget

    label("ARGON2ID • HASH & XÁC MINH")
    label(
        "Dùng mật khẩu giả để thực hành. "
        "Mật khẩu và hash không được ghi vào file."
    )

    label("1. Nhập mật khẩu đạt policy để tạo hash")
    password_entry = entry()

    output = tk.Text(
        content,
        height=7,
        bg="#1e293b",
        fg="#4ade80",
        font=("Consolas", 10),
        wrap="char",
        relief="flat",
        padx=10,
        pady=10,
        state="disabled",
    )

    def set_output(text):
        output.configure(state="normal")
        output.delete("1.0", "end")
        output.insert("1.0", text)
        output.configure(state="disabled")

    def create_hashes():
        password = password_entry.get()

        try:
            policy = load_policy()
            errors = check_policy(password, policy)

            if errors:
                messagebox.showwarning(
                    "Không đạt policy",
                    "\n".join(errors),
                    parent=window,
                )
                return

            first_hash = hash_password(password)
            second_hash = hash_password(password)

        except (
            OSError, ValueError, KeyError, TypeError, HashingError
        ) as error:
            messagebox.showerror(
                "Không tạo được hash", str(error), parent=window
            )
            return

        state["hash"] = first_hash

        set_output(
            f"Hash 1:\n{first_hash}\n\n"
            f"Hash 2:\n{second_hash}\n\n"
            f"Hai hash khác nhau: {first_hash != second_hash}"
        )

        password_entry.delete(0, "end")
        verify_entry.delete(0, "end")
        status.configure(
            text="Đã tạo hash. Nhập lại mật khẩu ở ô bên dưới.",
            fg="#94a3b8",
        )
        verify_entry.focus_set()

    button("Tạo 2 hash để quan sát salt", create_hashes)
    output.pack(fill="both", expand=True, pady=(6, 8))

    label("2. Nhập lại mật khẩu để xác minh với Hash 1")
    verify_entry = entry()

    def verify():
        if state["hash"] is None:
            messagebox.showinfo(
                "Chưa có hash",
                "Bạn cần tạo hash ở bước 1 trước.",
                parent=window,
            )
            return

        candidate = verify_entry.get()

        # Gioi han dau vao cho cua so thuc hanh
        if len(candidate) > 1024:
            status.configure(
                text="Nội dung xác minh quá dài.",
                fg="#fb7185",
            )
            return

        try:
            matched = verify_password(state["hash"], candidate)

            if matched:
                needs_rehash = HASHER.check_needs_rehash(
                    state["hash"]
                )
                status.configure(
                    text=(
                        "ĐÚNG MẬT KHẨU\n"
                        f"Cần cập nhật cấu hình hash: {needs_rehash}"
                    ),
                    fg="#4ade80",
                )
            else:
                status.configure(
                    text="SAI MẬT KHẨU",
                    fg="#fb7185",
                )
        except (InvalidHashError, VerificationError) as error:
            messagebox.showerror(
                "Lỗi xác minh", str(error), parent=window
            )
        finally:
            verify_entry.delete(0, "end")

    button("Xác minh mật khẩu", verify)

    status = label("Chưa tạo hash.")
    status.configure(fg="#94a3b8")

    label(
        "Hash không phải mã hóa để giải mã lại. "
        "Hashing cũng không làm mật khẩu yếu trở thành mạnh."
    )

    password_entry.focus_set()
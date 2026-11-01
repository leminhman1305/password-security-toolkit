import tkinter as tk
from password_generator import open_generator
from tkinter import messagebox, ttk

from password_policy import check_policy, load_policy
from strength_checker import check_strength
from hashing_tool import open_hashing_tool

BG = "#0f172a"
CARD = "#1e293b"
INPUT_BG = "#111827"
TEXT = "#f1f5f9"
MUTED = "#94a3b8"
ACCENT = "#38bdf8"
GREEN = "#4ade80"
RED = "#fb7185"


class PasswordApp:
    def __init__(self, root):
        self.root = root

        root.title("Password Security Toolkit")
        root.geometry("780x860")
        root.minsize(680, 800)
        root.configure(bg=BG)

        self.password = tk.StringVar()
        self.show_password = tk.BooleanVar(value=False)

        self.configure_styles()
        self.build_interface()

        # Xoa ket qua cu khi nguoi dung sua mat khau
        self.password.trace_add("write", self.reset_result)

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Strength.Horizontal.TProgressbar",
            troughcolor=INPUT_BG,
            background=MUTED,
            borderwidth=0,
            lightcolor=MUTED,
            darkcolor=MUTED,
        )

    def label(self, parent, text, size=11, color=TEXT, bold=False):
        return tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color,
            font=("Segoe UI", size, "bold" if bold else "normal"),
            anchor="w",
        )

    def button(self, parent, text, command, primary=False):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=ACCENT if primary else "#334155",
            fg=BG if primary else TEXT,
            activebackground="#7dd3fc" if primary else "#475569",
            activeforeground=BG if primary else TEXT,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            borderwidth=0,
            padx=20,
            pady=11,
            cursor="hand2",
        )

    def build_interface(self):
        container = tk.Frame(self.root, bg=BG)
        container.pack(fill="both", expand=True, padx=30, pady=24)

        self.label(
            container,
            "PASSWORD SECURITY TOOLKIT",
            size=10,
            color=ACCENT,
            bold=True,
        ).pack(fill="x")

        self.label(
            container,
            "Kiểm tra mật khẩu",
            size=25,
            bold=True,
        ).pack(fill="x", pady=(8, 4))

        self.label(
            container,
            "Kiểm tra policy, nhận diện mẫu yếu và xem gợi ý cải thiện.",
            color=MUTED,
        ).pack(fill="x")

        card = tk.Frame(container, bg=CARD)
        card.pack(fill="x", pady=(24, 16))

        content = tk.Frame(card, bg=CARD)
        content.pack(fill="x", padx=22, pady=20)

        self.label(content, "Mật khẩu cần kiểm tra", bold=True).pack(
            fill="x", pady=(0, 10)
        )

        self.entry = tk.Entry(
            content,
            textvariable=self.password,
            show="*",
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Segoe UI", 14),
        )
        self.entry.pack(fill="x", ipady=12)
        self.entry.bind("<Return>", lambda event: self.analyze())

        options = tk.Frame(content, bg=CARD)
        options.pack(fill="x", pady=(10, 16))

        tk.Checkbutton(
            options,
            text="Hiện mật khẩu",
            variable=self.show_password,
            command=self.toggle_password,
            bg=CARD,
            fg=MUTED,
            selectcolor=INPUT_BG,
            activebackground=CARD,
            activeforeground=TEXT,
            font=("Segoe UI", 10),
        ).pack(side="left")

        self.length_label = self.label(
            options, "0 ký tự", size=10, color=MUTED
        )
        self.length_label.pack(side="right")

        actions = tk.Frame(content, bg=CARD)
        actions.pack(fill="x")

        self.button(
            actions, "Kiểm tra mật khẩu", self.analyze, primary=True
        ).pack(side="left")

        self.button(actions, "Xóa", self.clear).pack(
            side="left", padx=(10, 0)
        )
        self.button(
            container,
            "Tạo mật khẩu ngẫu nhiên",
            lambda: open_generator(self.root),
        ).pack(anchor="w", pady=(0, 16))
        self.button(
            container,
            "Hash & xác minh Argon2id",
            lambda: open_hashing_tool(self.root),
        ).pack(anchor="w", pady=(0, 16))                

        result_card = tk.Frame(container, bg=CARD)
        result_card.pack(fill="both", expand=True)

        result = tk.Frame(result_card, bg=CARD)
        result.pack(fill="both", expand=True, padx=22, pady=20)

        header = tk.Frame(result, bg=CARD)
        header.pack(fill="x")

        self.level_label = self.label(
            header, "Chưa đánh giá", size=17, bold=True
        )
        self.level_label.pack(side="left")

        self.policy_label = self.label(
            header, "POLICY: —", size=10, color=MUTED, bold=True
        )
        self.policy_label.pack(side="right")

        self.progress = ttk.Progressbar(
            result,
            style="Strength.Horizontal.TProgressbar",
            maximum=100,
            value=0,
        )
        self.progress.pack(fill="x", pady=(15, 18), ipady=3)

        self.label(
            result, "CHI TIẾT & GỢI Ý", size=10, color=MUTED, bold=True
        ).pack(fill="x", pady=(0, 10))

        detail_frame = tk.Frame(result, bg=CARD)
        detail_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(detail_frame)
        scrollbar.pack(side="right", fill="y")

        self.details = tk.Text(
            detail_frame,
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 11),
            relief="flat",
            wrap="word",
            height=10,
            padx=0,
            pady=0,
            yscrollcommand=scrollbar.set,
        )
        self.details.pack(side="left", fill="both", expand=True)
        scrollbar.configure(command=self.details.yview)

        self.set_details(
            "Nhập mật khẩu thử, sau đó nhấn “Kiểm tra mật khẩu”.\n\n"
            "Đạt policy và độ mạnh là hai kết quả riêng biệt."
        )

        self.label(
            container,
            "Xử lý trên máy • Không ghi mật khẩu vào file • Dùng dữ liệu giả để demo",
            size=9,
            color=MUTED,
        ).pack(fill="x", pady=(14, 0))

        self.entry.focus_set()

    def set_details(self, text):
        self.details.configure(state="normal")
        self.details.delete("1.0", "end")
        self.details.insert("1.0", text)
        self.details.configure(state="disabled")

    def toggle_password(self):
        self.entry.configure(
            show="" if self.show_password.get() else "*"
        )

    def reset_result(self, *_):
        self.length_label.configure(
            text=f"{len(self.password.get())} ký tự"
        )
        self.level_label.configure(text="Chưa đánh giá", fg=TEXT)
        self.policy_label.configure(text="POLICY: —", fg=MUTED)
        self.progress["value"] = 0

        self.set_details(
            "Nhấn “Kiểm tra mật khẩu” để đánh giá nội dung hiện tại."
        )

    def analyze(self):
        password = self.password.get()

        if not password:
            messagebox.showinfo(
                "Chưa có mật khẩu",
                "Bạn hãy nhập mật khẩu thử trước.",
                parent=self.root,
            )
            self.entry.focus_set()
            return

        try:
            # Doc lai file moi lan kiem tra de nhan cau hinh moi
            policy = load_policy()
            errors = check_policy(password, policy)
            result = check_strength(password)
        except (OSError, ValueError, KeyError, TypeError) as error:
            messagebox.showerror(
                "Lỗi cấu hình",
                f"Không đọc được password policy:\n{error}",
                parent=self.root,
            )
            return

        levels = {
            "Rat yeu": ("Rất yếu", 15, RED),
            "Yeu": ("Yếu", 35, "#fb923c"),
            "Trung binh": ("Trung bình", 60, "#facc15"),
            "Kha theo quy tac": ("Khá theo quy tắc", 85, GREEN),
        }

        title, value, color = levels.get(
            result["level"], ("Chưa xác định", 0, MUTED)
        )

        self.level_label.configure(text=title, fg=color)
        self.progress["value"] = value

        ttk.Style().configure(
            "Strength.Horizontal.TProgressbar",
            background=color,
            lightcolor=color,
            darkcolor=color,
        )

        self.policy_label.configure(
            text="POLICY: KHÔNG ĐẠT" if errors else "POLICY: ĐẠT",
            fg=RED if errors else GREEN,
        )

        lines = [
            f"Policy hiện tại: {policy['min_length']}–"
            f"{policy['max_length']} ký tự.",
            "",
            "KIỂM TRA POLICY",
        ]

        if errors:
            lines.extend(f"• {error}" for error in errors)
        else:
            lines.append("• Đáp ứng các điều kiện đã cấu hình.")

        lines.extend(["", "MẪU YẾU PHÁT HIỆN"])

        if result["warnings"]:
            lines.extend(
                f"• {warning}" for warning in result["warnings"]
            )
        else:
            lines.append("• Chưa phát hiện mẫu yếu trong các quy tắc hiện có.")

        lines.extend(["", "GỢI Ý"])
        lines.extend(
            f"• {suggestion}" for suggestion in result["suggestions"]
        )

        lines.extend([
            "",
            "Thanh màu chỉ biểu diễn mức đánh giá theo quy tắc, "
            "không phải phần trăm an toàn.",
            "Công cụ chưa kiểm tra rò rỉ hoặc việc dùng lại mật khẩu.",
        ])

        self.set_details("\n".join(lines))

    def clear(self):
        self.password.set("")
        self.show_password.set(False)
        self.toggle_password()
        self.entry.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()
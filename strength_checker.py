import re
from collections import Counter

from password_policy import COMMON_PASSWORDS


SEQUENCES = (
    "0123456789",
    "abcdefghijklmnopqrstuvwxyz",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
)


def has_sequence(password):
    """Phat hien chuoi 4 ky tu theo thu tu hoac dao nguoc."""
    lowered = password.casefold()

    for sequence in SEQUENCES:
        for index in range(len(sequence) - 3):
            part = sequence[index:index + 4]

            if part in lowered or part[::-1] in lowered:
                return True

    return False


def check_strength(password):
    """Danh gia theo quy tac minh hoa, khong do thoi gian crack."""
    if not password:
        return {
            "level": "Rat yeu",
            "warnings": ["Mat khau rong."],
            "suggestions": ["Tao mot mat khau ngau nhien."],
        }

    length = len(password)
    warnings = []
    suggestions = []

    # Diem khoi dau dua tren do dai
    if length < 8:
        score = 0
    elif length < 12:
        score = 1
    elif length < 16:
        score = 2
    else:
        score = 3

    is_common = password.casefold() in COMMON_PASSWORDS

    if is_common:
        warnings.append("Trung danh sach mat khau pho bien minh hoa.")

    if has_sequence(password):
        warnings.append("Co chuoi de doan nhu 1234, abcd hoac qwerty.")
        score -= 1

    # Vi du: aaaa, 1111
    if re.search(r"(.)\1{3,}", password, flags=re.DOTALL):
        warnings.append("Co ky tu lap lien tiep tu 4 lan.")
        score -= 1

    # Vi du: abcabcabc, hellohello
    if re.fullmatch(r"(.+?)\1+", password, flags=re.DOTALL):
        warnings.append("Mat khau duoc tao bang cach lap lai mot cum.")
        score -= 2

    most_frequent = Counter(password).most_common(1)[0][1]

    if most_frequent / length >= 0.7:
        warnings.append("Mot ky tu chiem tu 70% mat khau.")
        score -= 1

    if length < 12:
        suggestions.append(
            "Nen tang do dai len 12-16 ky tu trong policy hien tai."
        )

    if warnings:
        suggestions.append(
            "Tao mat khau moi ngau nhien, tranh chuoi va cum lap."
        )

    # Mat khau pho bien hoac chi gom khoang trang luon rat yeu
    if is_common or password.isspace():
        score = 0

    score = max(0, min(score, 3))

    levels = {
        0: "Rat yeu",
        1: "Yeu",
        2: "Trung binh",
        3: "Kha theo quy tac",
    }

    suggestions.append("Dung mat khau rieng cho tung tai khoan.")

    return {
        "level": levels[score],
        "warnings": warnings,
        "suggestions": suggestions,
    }
import json
import string
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
POLICY_FILE = BASE_DIR / "policy.json"

# Danh sach minh hoa, chua phai danh sach ro ri day du
COMMON_PASSWORDS = {
    "123456",
    "12345678",
    "123456789",
    "password",
    "password123",
    "password123!",
    "admin123",
    "qwerty123",
    "letmein",
    "iloveyou",
    "passwordpassword",
}


def load_policy():
    """Doc cau hinh tu file JSON."""
    with POLICY_FILE.open("r", encoding="utf-8") as file:
        policy = json.load(file)

    min_length = policy["min_length"]
    max_length = policy["max_length"]

    if type(min_length) is not int or type(max_length) is not int:
        raise ValueError("Do dai trong policy phai la so nguyen.")

    if not 1 <= min_length <= max_length <= 1024:
        raise ValueError(
            "Policy can thoa: 1 <= min_length <= max_length <= 1024."
        )

    boolean_fields = (
        "require_uppercase",
        "require_lowercase",
        "require_digit",
        "require_symbol",
        "block_common_passwords",
    )

    for field in boolean_fields:
        if type(policy[field]) is not bool:
            raise ValueError(f"{field} phai la true hoac false.")

    return policy


def check_policy(password, policy):
    """Tra ve danh sach ly do khong dat; rong nghia la dat."""
    errors = []

    if len(password) < policy["min_length"]:
        errors.append(
            f"Can it nhat {policy['min_length']} ky tu."
        )

    if len(password) > policy["max_length"]:
        errors.append(
            f"Chi chap nhan toi da {policy['max_length']} ky tu."
        )

    if not password or password.isspace():
        errors.append("Mat khau khong duoc rong hoac chi co khoang trang.")

    if policy["require_uppercase"]:
        if not any(char.isupper() for char in password):
            errors.append("Can it nhat mot chu hoa.")

    if policy["require_lowercase"]:
        if not any(char.islower() for char in password):
            errors.append("Can it nhat mot chu thuong.")

    if policy["require_digit"]:
        if not any(char.isdigit() for char in password):
            errors.append("Can it nhat mot chu so.")

    if policy["require_symbol"]:
        if not any(char in string.punctuation for char in password):
            errors.append("Can it nhat mot ky hieu ASCII, vi du ! @ #.")

    if policy["block_common_passwords"]:
        if password.casefold() in COMMON_PASSWORDS:
            errors.append("Nam trong danh sach mat khau pho bien minh hoa.")

    return errors
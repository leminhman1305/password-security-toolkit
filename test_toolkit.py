import pytest

from password_policy import check_policy
from password_generator import generate_password
from strength_checker import check_strength
from hashing_tool import hash_password, verify_password


@pytest.fixture
def policy():
    return {
        "min_length": 8,
        "max_length": 16,
        "require_uppercase": False,
        "require_lowercase": False,
        "require_digit": False,
        "require_symbol": False,
        "block_common_passwords": True,
    }


@pytest.mark.parametrize(
    "password",
    ["", "       ", "a" * 7, "a" * 17, "password123!"],
)
def test_policy_rejects_invalid_passwords(policy, password):
    assert check_policy(password, policy)


@pytest.mark.parametrize("length", [8, 16])
def test_policy_accepts_length_boundaries(policy, length):
    assert check_policy("a" * length, policy) == []


def test_unicode_password(policy):
    assert check_policy("MậtKhẩuThử!2026", policy) == []


def test_policy_and_strength_are_separate(policy):
    password = "a" * 8

    assert check_policy(password, policy) == []
    assert check_strength(password)["level"] == "Rat yeu"


@pytest.mark.parametrize("length", [8, 12, 16])
def test_generator_meets_strict_policy(policy, length):
    policy.update({
        "require_uppercase": True,
        "require_lowercase": True,
        "require_digit": True,
        "require_symbol": True,
    })

    for _ in range(10):
        password = generate_password(length, policy)

        assert len(password) == length
        assert check_policy(password, policy) == []


@pytest.mark.parametrize("length", [7, 17])
def test_generator_rejects_invalid_length(policy, length):
    with pytest.raises(ValueError):
        generate_password(length, policy)


def test_argon2_hash_and_verification():
    password = "Demo-R7!k2@p9"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash.startswith("$argon2id$")
    assert first_hash != second_hash

    assert verify_password(first_hash, password) is True
    assert verify_password(second_hash, password) is True

    assert verify_password(first_hash, "Wrong-password!") is False
    assert verify_password(first_hash, password.lower()) is False
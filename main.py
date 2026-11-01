import getpass
import warnings

from password_policy import check_policy, load_policy
from strength_checker import check_strength


def main():
    try:
        policy = load_policy()
    except (OSError, ValueError, KeyError) as error:
        print(f"Khong doc duoc policy: {error}")
        return

    print("=== PASSWORD SECURITY TOOLKIT ===")
    print("Dung mat khau gia de thu. Chuong trinh khong luu mat khau.")
    print("Khi go, ky tu se khong hien tren man hinh.\n")

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", getpass.GetPassWarning)
            password = getpass.getpass("Nhap mat khau: ")
    except getpass.GetPassWarning:
        print("Hay chay trong Terminal ho tro nhap an.")
        return
    except (KeyboardInterrupt, EOFError):
        print("\nDa huy.")
        return

    errors = check_policy(password, policy)

    print("\n--- PASSWORD POLICY ---")
    if errors:
        print("KHONG DAT")
        for error in errors:
            print(f"- {error}")
    else:
        print("DAT")

    result = check_strength(password)

    print("\n--- DO MANH ---")
    print(result["level"])

    if result["warnings"]:
        for warning in result["warnings"]:
            print(f"- {warning}")
    else:
        print("- Khong tim thay mau yeu trong cac quy tac hien co.")

    print("\n--- GOI Y ---")
    for suggestion in result["suggestions"]:
        print(f"- {suggestion}")

    print("\nDat policy khong dong nghia voi mat khau manh.")
    print("Danh gia nay khong kiem tra mat khau bi ro ri hay dung lai.")


if __name__ == "__main__":
    main()
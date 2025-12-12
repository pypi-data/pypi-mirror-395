import argparse
from pathlib import Path
from .core import encrypt_file, decrypt_code

def main():
    parser = argparse.ArgumentParser(
        description="Convert any file (image, video, etc.) ↔ encrypted text code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  file2code encrypt photo.jpg -p MySecret123          → encrypted_code.txt
  file2code encrypt video.mp4                         → no password
  file2code decrypt encrypted_code.txt -p MySecret123 → restores video.mp4
        """
    )
    sub = parser.add_subparsers(dest="command", required=True)

    enc = sub.add_parser("encrypt", help="Encrypt file → text code")
    enc.add_argument("file", help="Path to file")
    enc.add_argument("-p", "--password", help="Protect with password (AES-256)")
    enc.add_argument("-o", "--output", default="encrypted_code.txt", help="Output text file")

    dec = sub.add_parser("decrypt", help="Decrypt text code → original file")
    dec.add_argument("code", help="Text code or path to .txt file containing code")
    dec.add_argument("-p", "--password", help="Password if encrypted")
    dec.add_argument("-o", "--output", help="Output filename (optional)")

    args = parser.parse_args()

    if args.command == "encrypt":
        code = encrypt_file(args.file, args.password)
        Path(args.output).write_text(code, encoding="utf-8")
        print(f"Encrypted code saved → {args.output}")
        print(f"Length: {len(code):,} characters")

    elif args.command == "decrypt":
        if Path(args.code).is_file():
            code = Path(args.code).read_text(encoding="utf-8").strip()
        else:
            code = args.code

        restored = decrypt_code(code, args.password, args.output)
        print(f"File restored → {restored}")

if __name__ == "__main__":
    main()
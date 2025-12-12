import argparse
import json
import sys
from .core import encrypt, decrypt

def main():
    parser = argparse.ArgumentParser(prog="dil-gcm-envelope")
    sub = parser.add_subparsers(dest="cmd")

    e = sub.add_parser("encrypt")
    e.add_argument("password")
    e.add_argument("--text", help="text to encrypt", required=True)
    e.add_argument("--pbkdf2", action="store_true")

    d = sub.add_parser("decrypt")
    d.add_argument("password")
    d.add_argument("--payload", required=True)
    d.add_argument("--iv", required=True)
    d.add_argument("--tag", required=True)
    d.add_argument("--salt", default=None)

    args = parser.parse_args()
    if args.cmd == "encrypt":
        out = encrypt(args.password, args.text, use_pbkdf2=args.pbkdf2)
        print(json.dumps(out))
    elif args.cmd == "decrypt":
        pt = decrypt(args.password, args.payload, args.iv, args.tag, salt_b64=args.salt)
        try:
            print(pt.decode("utf-8"))
        except Exception:
            print(pt)
    else:
        parser.print_help()
        sys.exit(2)

if __name__ == "__main__":
    main()

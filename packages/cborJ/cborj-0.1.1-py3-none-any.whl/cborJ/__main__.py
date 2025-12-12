import argparse
import json
import sys

from . import decode, encode


def main():
    parser = argparse.ArgumentParser(
        description="cborJ: Lightweight JSON ↔ CBOR encoder/decoder with optional compression",
        epilog="Examples:\n"
               "  cborJ encode input.json > out.cbor\n"
               "  cborJ decode out.cbor\n"
               "  cborJ encode --compress huge.json | gzip > out.cbor.gz",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # encode
    enc = subparsers.add_parser('encode', help="Encode JSON file/string to CBOR")
    enc.add_argument('input', nargs='?', default='-', help="Input JSON file (or '-' for stdin)")
    enc.add_argument('--compress', '-c', action='store_true', help="Compress with zlib")

    # decode
    dec = subparsers.add_parser('decode', help="Decode CBOR file/bytes to JSON string")
    dec.add_argument('input', nargs='?', default='-', help="Input CBOR file (or '-' for stdin)")
    dec.add_argument('--compress', '-c', action='store_true', help="Assume input was compressed")

    args = parser.parse_args()

    try:
        if args.command == 'encode':
            if args.input == '-':
                json_str = sys.stdin.read()
            else:
                with open(args.input, 'r', encoding='utf-8') as f:
                    json_str = f.read()
            # Optional: validate JSON
            try:
                json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Warning: Input may not be valid JSON: {e}", file=sys.stderr)
            result = encode(json_str, compress=args.compress)
            sys.stdout.buffer.write(result)

        elif args.command == 'decode':
            if args.input == '-':
                cbor_data = sys.stdin.buffer.read()
            else:
                with open(args.input, 'rb') as f:
                    cbor_data = f.read()
            json_str = decode(cbor_data, compress=args.compress)
            print(json_str, end='')

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

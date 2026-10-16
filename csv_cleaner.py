import argparse
import csv
import sys
from pathlib import Path


def normalize_header(name):
    return "_".join(name.strip().lower().split())


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(f, dialect=dialect)
        headers = [normalize_header(h) for h in (reader.fieldnames or [])]
        rows = []
        for raw in reader:
            rows.append({
                normalize_header(k): (v or "").strip()
                for k, v in raw.items() if k is not None
            })
    return headers, rows


def clean(files, keep_duplicates=False):
    all_headers, merged = [], []
    stats = {"files": 0, "read": 0, "empty": 0, "duplicates": 0}
    seen = set()

    for path in files:
        headers, rows = read_csv(path)
        stats["files"] += 1
        for h in headers:
            if h not in all_headers:
                all_headers.append(h)
        for row in rows:
            stats["read"] += 1
            if not any(row.values()):
                stats["empty"] += 1
                continue
            key = tuple(sorted(row.items()))
            if not keep_duplicates and key in seen:
                stats["duplicates"] += 1
                continue
            seen.add(key)
            merged.append(row)
    return all_headers, merged, stats


def main():
    parser = argparse.ArgumentParser(description="Merge and clean CSV files.")
    parser.add_argument("input", help="folder with CSV files or a single CSV file")
    parser.add_argument("-o", "--output", default="cleaned.csv", help="output file (default: cleaned.csv)")
    parser.add_argument("--keep-duplicates", action="store_true", help="do not remove duplicate rows")
    args = parser.parse_args()

    source = Path(args.input)
    files = sorted(source.glob("*.csv")) if source.is_dir() else [source]
    files = [f for f in files if f.resolve() != Path(args.output).resolve()]
    if not files:
        sys.exit("No CSV files found.")

    headers, rows, stats = clean(files, args.keep_duplicates)

    with open(args.output, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=headers, restval="")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Files processed:   {stats['files']}")
    print(f"Rows read:         {stats['read']}")
    print(f"Empty rows removed:{stats['empty']:>3}")
    print(f"Duplicates removed:{stats['duplicates']:>3}")
    print(f"Rows saved:        {len(rows)} -> {args.output}")


if __name__ == "__main__":
    main()

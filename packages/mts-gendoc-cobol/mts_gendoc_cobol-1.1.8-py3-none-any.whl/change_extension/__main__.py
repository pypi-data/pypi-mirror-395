import argparse as ap
import os

def main():
    parser = ap.ArgumentParser(description="Change file extensions in a directory.")
    parser.add_argument("-d", type=str, help="Path to the target directory.")
    parser.add_argument("-o", type=str, help="Old file extension (e.g., .txt).")
    parser.add_argument("-n", type=str, help="New file extension (e.g., .md)")

    args = parser.parse_args()

    for root, dirs, files in os.walk(args.d):
        print("walking through directory:", root)
        for file in files:
            print("    file:", file)
            if file.endswith(args.o):
                base = os.path.splitext(file)[0]
                old_file = os.path.join(root, file)
                new_file = os.path.join(root, base + args.n)
                os.rename(old_file, new_file)
                print(f"Renamed: {old_file} -> {new_file}")

if __name__ == "__main__":
    main()
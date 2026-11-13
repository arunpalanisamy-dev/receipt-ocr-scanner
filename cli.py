import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Receipt OCR Scanner"
    )

    parser.add_argument(
        "image",
        help="Path to the receipt image"
    )

    args = parser.parse_args()

    image_path = Path(args.image)

    if not image_path.exists():
        print(f"Image not found: {image_path}")
        return

    print(f"Processing receipt: {image_path}")

    # TODO: Connect your OCR processing function here.
    print("Receipt image loaded successfully!")

if __name__ == "__main__":
    main()

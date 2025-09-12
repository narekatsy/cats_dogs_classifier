from src.data_loader import split_dataset

RAW_DIR = "data/raw"
OUTPUT_DIR = "data/processed_padding"

if __name__ == "__main__":
    split_dataset(RAW_DIR, OUTPUT_DIR, resize_method="pad")
    print("✅ Data prepared with padding and stored in:", OUTPUT_DIR)

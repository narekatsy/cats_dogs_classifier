import os, random
from PIL import Image, ImageOps

def make_dirs(base_dir, classes):
    for split in ["train", "val", "test"]:
        for cls in classes:
            os.makedirs(os.path.join(base_dir, split, cls), exist_ok=True)

def resize_stretch(img, size):
    """Resize by stretching to target size (default)."""
    return img.resize(size)

def resize_pad(img, size):
    """Resize with padding (letterbox) to preserve aspect ratio."""
    return ImageOps.pad(img, size, method=Image.Resampling.BILINEAR, color=(0,0,0))

def split_dataset(
    raw_dir, 
    output_dir, 
    classes=["Cat","Dog"], 
    train_ratio=0.7, 
    val_ratio=0.15, 
    test_ratio=0.15, 
    image_size=(128,128),
    resize_method="stretch"
):
    """
    Splits raw dataset into train/val/test folders with resized images.
    resize_method: 'stretch' (default) or 'pad'
    """
    make_dirs(output_dir, classes)

    if resize_method == "pad":
        resize_func = lambda img: resize_pad(img, image_size)
    else:
        resize_func = lambda img: resize_stretch(img, image_size)

    for cls in classes:
        cls_dir = os.path.join(raw_dir, cls)
        files = os.listdir(cls_dir)
        random.shuffle(files)

        n_total = len(files)
        n_train = int(train_ratio * n_total)
        n_val = int(val_ratio * n_total)

        train_files = files[:n_train]
        val_files = files[n_train:n_train+n_val]
        test_files = files[n_train+n_val:]

        def process(files, split):
            for fname in files:
                src_path = os.path.join(cls_dir, fname)
                dst_path = os.path.join(output_dir, split, cls, fname)
                try:
                    img = Image.open(src_path).convert("RGB")
                    img = resize_func(img)
                    img.save(dst_path)
                except:
                    pass

        process(train_files, "train")
        process(val_files, "val")
        process(test_files, "test")

import shutil
from pathlib import Path

def copy_dicom(src_path: str, dest_dir: str) -> Path:
    """
    Copy a DICOM file to a destination directory, handling name collisions.
    """
    src = Path(src_path)
    dest_folder = Path(dest_dir)
    if not src.exists():
        raise FileNotFoundError(f"源文件不存在: {src}")
    dest_folder.mkdir(parents=True, exist_ok=True)

    dest = dest_folder / src.name
    if dest.exists():
        stem = src.stem
        suffix = src.suffix
        i = 1
        while True:
            candidate = dest_folder / f"{stem}_copy{i}{suffix}"
            if not candidate.exists():
                dest = candidate
                break
            i += 1

    shutil.copy2(src, dest)
    return dest

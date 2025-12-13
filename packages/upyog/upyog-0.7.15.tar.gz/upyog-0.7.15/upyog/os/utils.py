import PIL.features as PILFeatures

import warnings
import re
import shutil
import json
import os
import platform

from datetime import datetime
from pathlib import Path
from upyog.os.read_files import PathLike, get_files
from typing import List, Literal, Union, Optional
from tqdm import tqdm
from loguru import logger


__all__ = [
    "load_json", "read_json", "check_pil_simd_usage", "sanitise_filename", "get_file_size",
    "get_file_creation_date", "write_json", "write_text",
    "is_platform_macos", "is_platform_windows", "is_platform_linux",
    "convert_number_to_human_readable_format",
]


def load_json(path: PathLike):
    "Load a JSON file"
    return json.loads(Path(path).read_bytes())


def load_txt(path: PathLike) -> str:
    "Load a text file"
    return Path(path).read_text()


def read_json(path: PathLike):
    return load_json(path)


def write_json(json_data: dict, path: PathLike, indent=4):
    "Write `json_data` to `path`"
    with open(path, "w") as f:
        json.dump(json_data, f, indent=indent)


def write_text(text: str, save_path: PathLike):
    "Write text to a text file"
    with open(str(save_path), 'w') as f:
        f.write(text)


def check_pil_simd_usage():
    import PIL
    pil_version = PIL.__version__

    if not "post" in pil_version:
        msg = f"Pillow-SIMD not installed. Using PIL {pil_version} instead"
        warnings.warn(msg)

    else:
        if not PILFeatures.check_feature("libjpeg_turbo"):
            warnings.warn(
                f"Pillow-SIMD is installed, but Libjpeg Turbo is not being used. "
                f"Unlikely to see any speedups"
            )


def check_corrupted_images(filepaths: List[PathLike], verbose=True) -> List[PathLike]:
    from PIL import Image

    corrupted = []
    for f in tqdm(filepaths, "Scanning files for corruptions", disable=not verbose):
        try:    Image.open(f)
        except: corrupted.append(f)

    if verbose:
        logger.info(f"Found {len(corrupted)} corrupt files")

    return corrupted


# fmt: off
def sanitise_filename(
    f: str, lowercase=False, prefix=None, truncate: Optional[int] = 240
):
    # see https://stackoverflow.com/questions/49460802/regex-match-all-vular-fractions
    fractions = "\u00BC-\u00BE\u2150-\u215E"  # not-exhaustive..?
    supscripts = "\u00B1-\u00B9"

    fn = re.sub(f'[\W{supscripts}{fractions}]', '_', f) # captures (?) subscripts, fractions, other non-alphanumerics
    fn = re.sub(f'[^A-Za-z0-9_+]', '_', fn)             # captures alphabets in foreign languages
    fn = re.sub('^[\W_]*'     , '' , fn)                # replace leading spl characters or '_'

    assert re.match("^[A-Za-z0-9_]*$", fn), f'{fn} contains non-alphanumeric/underscore characters'
    assert re.match("^[A-Za-z0-9]",    fn), f'{fn} OR {f} starts with a non-alphanumeric character'

    if prefix: fn = f"{prefix}{fn}"
    if truncate: fn = fn[:truncate]
    if lowercase: fn = fn.lower()

    return fn


def get_file_size(path: PathLike, units: Literal["B", "KB", "MB", "GB"] = "MB"):
    path = Path(path)
    if path.is_dir():
        B = sum(os.path.getsize(f) for f in get_files(path, recurse=True))
    else:
        B = os.path.getsize(path)

    if   units == "B":  return B
    elif units == "KB": return B/1024
    elif units == "MB": return B/1024**2
    elif units == "GB": return B/1024**3


def get_file_creation_date(path_to_file) -> str:
    # Get the timestamp of the file's creation date
    timestamp = os.path.getctime(path_to_file)
    
    # Convert the timestamp to a datetime object
    date = datetime.fromtimestamp(timestamp)
    return date.strftime('%Y-%m-%d')


def convert_number_to_human_readable_format(number: Union[int, float], approx=True) -> str:
    """
    Formats a number to be human readable. Works best for larger numbers up to
    1 quintillion (1e18)
              100 -> 100
            10000 -> 10k
          100,000 -> 100k
      100,000,000 -> 100m
    1,000,000,000 -> 1b
    """
    magnitude = 0
    while abs(number) >= 1000:
        magnitude += 1
        number /= 1000.0

    if approx:
        return '%d%s' % (number, ['', 'k', 'm', 'b', 't', 'q'][magnitude])
    else:
        return '%.1f%s' % (number, ['', 'k', 'm', 'b', 't', 'q'][magnitude])


def is_platform_macos() -> bool:   return platform.system().lower() == "darwin"
def is_platform_windows() -> bool: return platform.system().lower() == "windows"
def is_platform_linux() -> bool:   return platform.system().lower() == "linux"


def restore_symlink(f: Path):
    f = Path(f)
    if not f.is_symlink():
        return f

    orig = f.resolve()

    if not orig.exists():
        logger.warning(f"Failed to find original file {orig}")
        return f

    # Create a temporary filename in the same directory
    temp_file = f.with_name(f.name + ".temp")

    try:
        # Copy the original file to the temporary location
        shutil.copy2(orig, temp_file)

        # Remove the symlink
        f.unlink()

        # Rename the temporary file to the original symlink name
        temp_file.rename(f)

    except Exception as e:
        logger.error(f"Failed to restore symlink {f}: {str(e)}")
        if temp_file.exists():
            temp_file.unlink()  # Clean up the temporary file if it exists

    return f

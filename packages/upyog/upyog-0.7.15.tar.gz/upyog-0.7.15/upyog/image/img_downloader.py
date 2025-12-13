import concurrent.futures
import os
import time

from dataclasses import asdict, dataclass
from io import BytesIO
from pathlib import Path
from typing import Union
from urllib.parse import urlparse


import pandas as pd
import requests

from PIL import Image
from tqdm import tqdm
from rich import print
from upyog.cli import P, call_parse


PathLike = Union[str, Path]


@dataclass
class DownloadResult:
    url_file: PathLike
    success: bool
    reason: Union[str, None]


def download_image(
    url_file: PathLike,
    output_path: PathLike,
    convert_rgb: bool = True,
    max_retries: int = 3,
) -> DownloadResult:
    """
    Download an image from a URL and save it to the output path.

    Args:
        url_file: Path to the file containing the image URL.
        output_path: Path to the output directory.
        convert_rgb: Whether to convert the image to RGB format (default: True).
        max_retries: Maximum number of retries in case of download failure (default: 3).

    Returns:
        A DownloadResult object containing the URL file path, success status, and error reason (if any).
    """
    url_file = Path(url_file)
    output_path = Path(output_path)
    
    # Determine the potential file name
    extension = "jpg" if convert_rgb else "png"  # Default to png if not converting to RGB
    file_name = output_path / f"{url_file.stem.replace('.url', '')}.{extension}"
    
    # Check if the file already exists
    if file_name.exists():
        return DownloadResult(url_file, True, "File already exists")

    retries = 0
    while retries < max_retries:
        try:
            with open(url_file, "r") as file:
                url = file.read().strip()

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            image_data = response.content
            try:
                image = Image.open(BytesIO(image_data))
            except:
                return DownloadResult(url_file, False, "Invalid image data")

            try:
                if convert_rgb:
                    image = image.convert("RGB")
                else:
                    extension = image.format.lower()
                    if extension in ["jpeg", ""]:
                        extension = "jpg"
                    file_name = output_path / f"{url_file.stem.replace('.url', '')}.{extension}"

                image.save(file_name)

            except Exception as e:
                return DownloadResult(url_file, False, str(e))

            return DownloadResult(url_file, True, None)

        except requests.exceptions.RequestException as e:
            retries += 1
            if retries == max_retries:
                return DownloadResult(url_file, False, str(e))

        except Exception as e:
            return DownloadResult(url_file, False, str(e))


@call_parse
def download_images(
    i: P("Input folder with url .txt files") = None,  # type: ignore
    o: P("Output folder") = None,  # type: ignore
    max_threads: P("Max. no. of threads", int) = os.cpu_count(), # type: ignore
    max_retries: P("No. of times to retry downloading an image if we fail", int) = 2, # type: ignore
):
    """
    Download images from URL files in a folder using multi-threading.

    Args:
        folder_path: Path to the input folder containing URL files.
        output_path: Path to the output folder for saving downloaded images.
        max_threads: Maximum number of threads to use for downloading.
    """
    assert i
    assert o

    folder_path = i
    output_path = o

    url_files = list(Path(folder_path).glob("*.url.txt"))
    total_files = len(url_files)

    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    results = []
    start_time = time.time()
    convert_rgb = True  # NOTE: Hard-coded for now.

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(download_image, url_file, output_path, convert_rgb, max_retries)
            for url_file in url_files
        ]

        with tqdm(
            total=total_files, unit="file", desc="Processing images"
        ) as progress:
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                progress.update(1)
                progress.set_postfix_str(
                    f"{progress.n}/{total_files} ({progress.n / total_files * 100:.2f}%)"
                )
                results.append(result)
    end_time = time.time()
    total_time = end_time - start_time

    df = pd.DataFrame([asdict(result) for result in results])
    success_count = df["success"].sum()
    already_exists_count = df[df["reason"] == "File already exists"].shape[0]
    new_downloads_count = success_count - already_exists_count
    success_rate = success_count / total_files * 100
    images_per_second = new_downloads_count / total_time
    print(
        f"\nProcessed {total_files} images:"
    )
    print(f"  - Successfully downloaded: {new_downloads_count}")
    print(f"  - Already existing: {already_exists_count}")
    print(f"  - Failed: {total_files - success_count}")
    print(f"Overall success rate: {success_rate:.2f}%")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"New images downloaded per second: {images_per_second:.2f}")

    output_file = output_path / "download_results.csv"
    df.to_csv(output_file, index=False)
    print(f"\nDownload results saved to: {output_file}")

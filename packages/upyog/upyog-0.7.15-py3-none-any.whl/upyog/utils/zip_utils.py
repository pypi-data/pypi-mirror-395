from upyog.imports import *

def zip_folder(path: PathLike):
    path = Path(path)
    assert path.is_dir()
    assert path.exists()

    return shutil.make_archive(path, "zip", path)

def compose_files_into_zip_archive(
    files: List[PathLike],
    out_dir: PathLike,
    zip_name: str = "Archive",
):
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    zip_name = zip_name + ".zip"

    for file in files:
        shutil.copy(file, str(out_dir / zip_name))

    zipfile = zip_folder(out_dir)
    shutil.rmtree(out_dir)

    return zipfile

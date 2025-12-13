from upyog.imports import *
from upyog.os.read_files import *


@fastcore.patch
def ls(self: Path, recurse: bool = False, extensions: Optional[List[str]] = None):
    return get_files(self, recurse=recurse, extensions=extensions)


@fastcore.patch
def list_dirs(self: Path):
    dirs = []
    for f in os.listdir(self):
        f = Path(os.path.join(self, f))
        if f.is_dir():
            dirs.append(f)
    return dirs

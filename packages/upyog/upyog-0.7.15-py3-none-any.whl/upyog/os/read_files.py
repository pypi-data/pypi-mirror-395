from upyog.imports import *
from upyog.utils.utils import flatten


"""
Taken from fastaiv1: https://github.com/fastai/fastai1/blob/a8327427ad5137c4899a1b4f74745193c9ea5be3/fastai/data_block.py#L22-L47
"""

__all__ = ["PathLike", "get_files", "get_image_files", "get_video_files", "collate_image_filenames"]


def get_files(
    path: PathLike,
    extensions: Collection[str] = None,
    recurse: bool = False,
    exclude: Optional[Collection[str]] = None,
    include: Optional[Collection[str]] = None,
    presort: bool = False,
    followlinks: bool = False,
) -> List[Path]:
    """
    Return list of files in `path` that have a suffix in `extensions`; optionally `recurse`.
    Use `include` and `exclude` for including/excluding folder names, `presort` to sort.
    """
    # fmt: off
    if recurse:
        res = []
        for i,(p,d,f) in enumerate(os.walk(path, followlinks=followlinks)):
            # skip hidden dirs
            if include is not None and i==0:   d[:] = [o for o in d if o in include]
            elif exclude is not None and i==0: d[:] = [o for o in d if o not in exclude]
            else:                              d[:] = [o for o in d if not o.startswith('.')]
            res += _get_files(path, p, f, extensions)
        if presort: res = sorted(res, key=lambda p: _path_to_same_str(p), reverse=False)
        return res
    else:
        f = [o.name for o in os.scandir(path) if o.is_file()]
        res = _get_files(path, path, f, extensions)
        if presort: res = sorted(res, key=lambda p: _path_to_same_str(p), reverse=False)
        return res
    # fmt: on


def _path_to_same_str(p_fn: PathLike) -> str:
    "path -> str, but same on nt+posix, for alpha-sort only"
    s_fn = str(p_fn)
    s_fn = s_fn.replace("\\", ".")
    s_fn = s_fn.replace("/", ".")
    return s_fn


def _get_files(parent, p, f, extensions) -> list:
    p = Path(p)  # .relative_to(parent)
    if isinstance(extensions, str):
        extensions = [extensions]
    low_extensions = [e.lower() for e in extensions] if extensions is not None else None
    res = [
        p / o
        for o in f
        if not o.startswith(".")
        and (extensions is None or f'.{o.split(".")[-1].lower()}' in low_extensions)
    ]
    return res


_IMAGE_EXTENSIONS = set(
    k for k, v in mimetypes.types_map.items() if v.startswith("image/")
)
_VIDEO_EXTENSIONS = set(
    [k for k, v in mimetypes.types_map.items() if v.startswith("video/")] + [".mkv"]
)


def get_image_files(
    path: Union[PathLike, List[PathLike]],
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
    recurse: bool = True,
) -> List[Path]:

    if not isinstance(path, list):
        path = [path]

    paths = path  # For backward compatibility
    all_files = []
    for path in paths:
        files = get_files(
            path=path,
            include=include,
            exclude=exclude,
            recurse=recurse,
            extensions=_IMAGE_EXTENSIONS,
        )
        all_files += files

    return flatten(files)


def get_video_files(
    path: PathLike,
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
    recurse: bool = True,
) -> List[Path]:
    return get_files(
        path=path,
        include=include,
        exclude=exclude,
        recurse=recurse,
        extensions=_VIDEO_EXTENSIONS,
    )


def collate_image_filenames(
    filenames: List[os.PathLike] = None,
    img_folders: Optional[List[os.PathLike]] = None,
    sort: bool = True,
    return_str: bool = False,
) -> List[PathLike]:
    """
    Take a list of `fnames` and `img_folders`, and return a flattened list of
    all image files in `img_folders` and `fnames` as a single list
    """
    all_files = []
    if filenames is not None:
        assert isinstance(filenames, list)
        filenames = [Path(f) for f in filenames]
        all_files.extend(filenames)

    if img_folders is not None:
        if isinstance(img_folders, (str, Path)):
            img_folders = [img_folders]
        for folder in img_folders:
            if not Path(folder).exists():
                raise FileNotFoundError(f"{folder} not found on disk.")
        for folder in img_folders:
            all_files.extend(get_image_files(folder))

    if sort:
        all_files = sorted(all_files)

    if return_str:
          return [str(f) for f in all_files]
    else: return all_files

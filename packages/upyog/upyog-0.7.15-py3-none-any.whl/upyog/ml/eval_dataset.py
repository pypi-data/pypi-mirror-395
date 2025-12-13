from upyog.ml.imports import *
from upyog.os import get_image_files, collate_image_filenames
from upyog.image import load_image


__all__ = ["ImageInferenceDataset", "image_filename_collate_fn"]


class ImageInferenceDataset(Dataset, ABC):
    """
    Base class that gathers files from a myriad number of folders / lists of
    filenames and stores them as `self.fnames`.

    Subclasses must implement the `__getitem__` method with the appropriate
    preprocessing for the model
    """

    def __init__(
        self,
        fnames: List[os.PathLike] = None,
        img_folders: Optional[List[os.PathLike]] = None,
        sort_fnames: bool = True,
    ):
        self.fnames = collate_image_filenames(fnames, img_folders)
        if sort_fnames:
            self.fnames.sort()

        num_unique_files = len(set(self.fnames))
        if not num_unique_files == len(self.fnames):
            before = len(self.fnames)
            logger.warning(f"Found {before} - {num_unique_files} duplicate filenames")

            self.fnames = sorted(set(self.fnames))
            after = len(self.fnames)

            logger.info(f"Removed duplicate filenames. Total no. filenames: {before} -> {after}")

    def post_init(self):
        pass

    def __len__(self):
        return len(self.fnames)

    @abstractmethod
    def __getitem__(self, i):
        pass

    def __repr__(self):
        info = [
            f"{self.__class__.__name__}(...)",
            f"Num Images: {len(self)}",
        ]
        return "\n".join(info)


def image_filename_collate_fn(items):
    fnames = L(items).itemgot(0)
    imgs = L(items).itemgot(1)

    return (list(fnames), torch.stack(list(imgs)))


def read_image(fn: Union[str, os.PathLike]) -> torch.Tensor:
    img = load_image(fn)
    return TF.to_tensor(img)

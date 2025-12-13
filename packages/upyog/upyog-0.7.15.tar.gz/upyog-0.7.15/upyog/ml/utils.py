from upyog.ml.imports import *
from upyog.os import *


__all__ = ["to_np", "to_torch", "save_tensor_to_json", "pick_device"]


# NOTE: PyTorch Lightning specific... do not use unless you know exactly what this
# function is meant for...
def get_num_gpus(gpus: Union[List[int], int]) -> Union[None, int]:
    if is_platform_macos():
        return None
    if gpus == -1:
        return torch.cuda.device_count()
    else:
        assert isinstance(gpus, list)
        return len(gpus)


def to_np(
    data: Union[Tensor, np.ndarray, Collection[Any]],
    dtype=np.float32
):
    "Convert a Tensor / array / collection of numbers to a NP array and optionally change its dtype"
    if   isinstance(data, np.ndarray): pass
    elif isinstance(data, Tensor):     data = data.detach().cpu().numpy()
    else:                              data = np.array(data)

    if dtype is not None: return data.astype(dtype)
    else:                 return data


def to_torch(x) -> Tensor:
    assert isinstance(x, (np.ndarray, torch.Tensor))
    return x.detach() if isinstance(x, torch.Tensor) else torch.from_numpy(x)


def save_tensor_to_json(data: Union[Tensor, np.ndarray], path: PathLike):
    "Save tensor to disk as a JSON file"
    data = to_np(data) if isinstance(data, Tensor) else data
    if not isinstance(data, (Tensor, np.ndarray)):
        raise ValueError(f"Invalid `data` type. Expected tensor/array, got {type(data)}")
    data = data.tolist()

    path = Path(path).with_suffix(".json")
    # path = Path(path)
    # filename = f"{path.stem}.json"  # Ensure extension is .json
    # path = path.parent / filename
    write_json(data, path, indent=None)


def pick_device(device=None) -> torch.device:
    if device is None:
        if torch.cuda.is_available():
            return torch.device("cuda:0")
        else:
            # MacOS
            if platform.system() == "Darwin":
                try: return torch.device("mps")
                except: return torch.device("cpu")
            else:
                return torch.device("cpu")

    if isinstance(device, int):
        return torch.device(f"cuda:{device}")

    if device == "cpu":
        return torch.device("cpu")

    if device == "mps":
        return torch.device("mps")

    if isinstance(device, torch.device):
        return device

    raise ValueError(f"Invalid device value: {device}")

from upyog.ml.imports import *


__all__ = ["compare_state_dicts", "set_bn_eval", "load_weights_from_checkpoint"]


ModuleOrWeights = Union[nn.Module, OrderedDict]


def compare_state_dicts(
    m1: ModuleOrWeights, m2: ModuleOrWeights, verbose=True, name: str = "models"
) -> bool:
    mismatch_keys = []
    m1 = m1.state_dict() if isinstance(m1, nn.Module) else m1
    m2 = m2.state_dict() if isinstance(m2, nn.Module) else m2

    for (k1, m1v), (k2, m2v) in zip(m1.items(), m2.items()):
        assert k1 == k2, f"Key mismatch, looks like you're comparing different models"
        if not torch.equal(m1v.cpu(), m2v.cpu()):
            logger.error(
                f"Mismatch in <fg #0F77A9>{name}</> in layer <fg #0F77A9>{k1}</>"
            )
            mismatch_keys.append(k1)

    if not mismatch_keys == []:
        err_msg = f"Weights didn't match exactly in {len(mismatch_keys)} layers: {mismatch_keys}"
        raise RuntimeError(err_msg if verbose else "")
    logger.success(f"`state_dict`s of both <fg #0F77A9>{name} </> match!")
    return True


BN_LAYER_TYPES = (nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d)
def set_bn_eval(m: nn.Module) -> None:
    "Set bn layers in eval mode for all recursive children of `m`."
    for l in m.children():
        if isinstance(l, BN_LAYER_TYPES) and not next(l.parameters()).requires_grad:
            l.eval()
        set_bn_eval(l)


def load_weights_from_checkpoint(
    path_checkpoint: os.PathLike,
    model: nn.Module,
    replace_pattern: str = "",
    replace_with: str = "",
    re_count: int = 0,
    strict: bool = True,
    verbose: bool = True,
    device: Union[None, torch.device, str] = None,
):
    """
    Loads the state_dict from `path_checkpoint`, which can be a path on disk or a URL

    * If the checkpoint is an elaborate one, then it checks for weights inside the
      'state_dict' or 'model' key.
    * You can use `replace_pattern` and `replace_with` to regex-replace keys in the
      checkpoint
    * If `strict`, it's ensured that none of the keys in the `model`'s state dict
      are missing from the checkpoint
    * Use `re_count` to limit the number of replacements. Defaults to 0 i.e. replace all
      Use if you want to sub "model.model.0" to "model.0" (re_count=1) instead of "0" (re_count=0)
    """
    device = device or "cpu"
    is_url_ckpt = "http" in path_checkpoint and "://" in path_checkpoint

    if is_url_ckpt:
        pt_wts = torch.hub.load_state_dict_from_url(path_checkpoint, map_location=device)
    else:
        pt_wts = torch.load(path_checkpoint, map_location=device)

    if not isinstance(pt_wts, OrderedDict):
        if not isinstance(pt_wts, dict):
            raise TypeError(f"Expected to load a `dict` checkpoint, got {type(pt_wts)}")

        if   "state_dict" in pt_wts.keys(): wts_key = "state_dict"
        elif "model"      in pt_wts.keys(): wts_key = "model"

        else:
            raise ValueError(f"No appropriate key found for loading model weights")

        pt_wts = pt_wts[wts_key]
        assert isinstance(pt_wts, OrderedDict)

    pt_wts = {
        re.sub(replace_pattern, replace_with, layer_name, count=re_count): weights
        for layer_name, weights in pt_wts.items()
    }

    result = model.load_state_dict(pt_wts, strict=False)
    missing, unexpected = result.missing_keys, result.unexpected_keys

    if verbose:
        print(f"Loaded weights from {path_checkpoint}")
        print(f"Missing Keys In Checkpoint\n: {missing}")
        print()
        print(f"Extra Keys From Checkpoint That Weren't Loaded\n: {unexpected}")
    if strict:
        assert missing == [], f"Missing Keys: {missing}"

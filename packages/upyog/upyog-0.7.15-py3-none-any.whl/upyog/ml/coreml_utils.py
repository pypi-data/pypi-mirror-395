from upyog.ml.imports import *
import coremltools as ct


__all__ = ["get_coreml_input", "add_top_level_metadata"]

MLModelSpec = ct.proto.Model_pb2.Model


# TODO: Get from upyog
def get_coreml_input(
    H: int,
    W: int,
    norm_mean: Optional[Tuple[float, float, float]] = (0.485, 0.456, 0.406),
    norm_stdev: Optional[Tuple[float, float, float]] = (0.229, 0.224, 0.225),
    input_name: str = "Image",
    input_format: Literal["RGB", "BGR"] = "RGB",
) -> List[ct.ImageType]:
    """
    Get CoreML input image type to feed into a model. If using `norm_mean` and
    `norm_stdev`, it does preprocessing as described (ImageNet example) here:
    https://github.com/apple/coremltools/issues/1160

    If `norm_mean` or `norm_stdev` is None, inputs are are not normalised
    and are in the range of 0-255 (as is the case for YOLOX)

    Returns a list so you can call the function inside the converter alone
        `ct.convert(model, inputs = get_coreml_input(...))`
    """
    if norm_mean and norm_stdev:
        assert len(norm_mean) == 3 and len(norm_stdev) == 3
        scale_div = sum(norm_stdev) / len(norm_stdev)
        scale = 1.0 / (255.0 * scale_div)
        bias = list(map(lambda x: -x / scale_div, norm_mean))
    else:
        scale = 1.0
        bias = None

    input_type = ct.ImageType(
        input_name,
        shape=torch.rand(1, 3, H, W).shape,
        scale=scale,
        bias=bias,
        color_layout=input_format,
    )
    return [input_type]


def add_top_level_metadata(
    mlmod: Union[ct.models.MLModel, MLModelSpec],
    version: str,
    author: str,
    license: str,
    description: str,
) -> ct.models.MLModel:
    ""

    """
    NOTE: We always use the model spec to add the metadata because editing an .mlpackage
    file directly is unreliable -- the metadata shows up in the model in an interactive
    python session but gets erased when you save the model file. Wtf??
    """

    if isinstance(mlmod, MLModelSpec):
        pass

    elif isinstance(mlmod, ct.models.MLModel):
        spec = mlmod.get_spec()

    spec.description.metadata.author = author
    spec.description.metadata.license = license
    spec.description.metadata.shortDescription = description

    check_version_string(version)
    spec.description.metadata.versionString = version

    try:
        return ct.models.MLModel(spec)
    except:
        return ct.models.MLModel(spec, weights_dir=mlmod.weights_dir)


def check_version_string(version: str):
    if not len(version.split(".")) == 3:
        raise ValueError(
            f"Version string seems to be in the wrong format. Expected something like "
            f"'X.Y.Z' or 'X.Y.Z-rc3' ( <MAJOR.MINOR.PATCH-EXTRA> ), got {version} instead. "
            f"See https://semver.org/ for more info"
        )

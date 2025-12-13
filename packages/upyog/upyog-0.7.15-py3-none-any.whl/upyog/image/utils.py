from upyog.imports import *

# Inspired by https://github.com/gordicaleksa/stable_diffusion_playground/blob/a4508d0650c6940f64b858aa818291cfa0bdad9c/generate_images.py#L84-L97
def save_image_with_metadata(
    img: Image.Image, metadata: dict, filepath: PathLike
):
    """
    Embed `metadata` inside an image as the Exif UserComment when saving it to disk
    """

    import exif
    import cv2

    filepath = Path(filepath)
    ext = filepath.suffix

    # If no extension given, add .jpg extension
    if ext == "":
        filepath = filepath.parent / f"{filepath.name}.jpg"

    elif ext != "jpg":
        raise ValueError(f"Only '.jpg' extensions are acceptable, you provided {ext}")

    assert json.dumps(metadata), f"JSON Data not serialisable!"
    assert ".jpg" in filepath, f"Expected full filepath with '.jpg' extension in filename"

    # See https://exif.readthedocs.io/en/latest/usage.html
    exif_img = exif.Image(
        cv2.imencode(".jpg", np.asarray(img)[..., ::-1])[1].tobytes()
    )
    exif_img.user_comment = json.dumps(metadata)

    with open(filepath, "wb") as f:
        f.write(exif_img.get_file())


def fig_to_pil(fig, pad_inches: float = 0.25):
    """
    Convert a Matplotlib figure to a PIL Image and return it
    """
    # Save figure to buf in png format
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=pad_inches)
    buf.seek(0)

    # Convert to PIL Image
    img = Image.open(buf).convert("RGB")
    buf.close()
    return img

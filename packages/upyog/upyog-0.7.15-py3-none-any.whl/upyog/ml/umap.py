from upyog.imports import *
from upyog.image.io import *
import umap
import altair as alt


def umap_plot(
    sentences: List[str],
    embeddings: np.ndarray,
    width: int = 700,
    height: int = 400,
) -> alt.Chart:

    # UMAP reduces the dimensions from 1024 to 2 dimensions that we can plot
    reducer = umap.UMAP(n_neighbors=2)
    umap_embeds = reducer.fit_transform(embeddings)

    # Setup DataFrame
    df_explore = pd.DataFrame({
        "text" : sentences,
        "x" : umap_embeds[:,0],
        "y" : umap_embeds[:,1],
    })

    # Plot
    chart = alt.Chart(df_explore).mark_circle(size=60).encode(
        x = alt.X('x', scale=alt.Scale(zero=False)),
        y = alt.Y('y', scale=alt.Scale(zero=False)),
        tooltip = ['text']
    ).properties(width=width, height=height)
    return chart


def img_filepath_or_url_to_base64(
    img_filepath_or_url: PathLike,
    image_WH: Optional[Tuple[int, int]] = None,
) -> str:
    "Convert a PIL image to a base64 encoded string"
    if img_filepath_or_url.startswith("http"):
        return img_filepath_or_url  # URL, can be used directly
    else:
        img = Image.open(img_filepath_or_url)
        if image_WH:
            img = resize_with_padding(img, image_WH)
        return pil_image_to_base64(img)


# TODO: Test
def umap_image_plot(
    image_paths: List[str],
    embeddings: np.ndarray,
    image_WH: Tuple[int, int] = (640, 384),
    width: int = 700,
    height: int = 400,
) -> alt.Chart:

    # UMAP dimensionality reduction
    reducer = umap.UMAP(n_neighbors=2)
    umap_embeds = reducer.fit_transform(embeddings)

    # Convert images to base64 or keep as URL
    image_paths_converted = [
        img_filepath_or_url_to_base64(path, image_WH) for path in image_paths
    ]

    # Setup DataFrame
    df_explore = pd.DataFrame({
        "image_path": image_paths_converted,
        "x": umap_embeds[:, 0],
        "y": umap_embeds[:, 1],
    })

    # Create a custom HTML tooltip
    image_tooltip = alt.Tooltip(
        field="image_path",
        type="nominal",
        title="Image",
        format=("<img src='{0}' width='100'>")
    )

    # Plot
    chart = alt.Chart(df_explore).mark_circle(size=60).encode(
        x=alt.X('x', scale=alt.Scale(zero=False)),
        y=alt.Y('y', scale=alt.Scale(zero=False)),
        tooltip=[image_tooltip]
    ).properties(width=width, height=height)
    
    return chart

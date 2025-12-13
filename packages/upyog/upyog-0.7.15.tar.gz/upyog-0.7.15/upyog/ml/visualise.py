from upyog.ml.imports import *
from upyog.ml.utils import to_np, to_torch
from upyog.image import fig_to_pil


__all__ = ["visualise_conf_matrix"]


class MetricsVisualiser:
    def __init__(
        self,
        ground_truths: Union[Collection[float], Collection[str]],
        predictions: Union[Collection[float], Collection[str]],
    ):
        self.ground_truths = to_np(ground_truths, dtype=None)
        self.predictions = to_np(predictions, dtype=None)

    @classmethod
    def from_df(
        cls,
        df: pd.DataFrame, ground_truths_colname: str, predictions_colname: str, 
    ):
        return cls(
            ground_truths = df[ground_truths_colname].values.tolist(),
            predictions = df[predictions_colname].values.tolist(),
        )

    def visualise_confusion_matrix():
        ...

    def visualise_metrics():
        ...

    def get_classification_report():
        ...


def get_confusion_matrix(
    ground_truths: Union[List[float], List[str]],
    predictions: Union[List[float], List[str]],
):
    from sklearn.metrics import confusion_matrix

    if not len(ground_truths) == len(predictions):
        raise RuntimeError(f"Mismatch between `len(ground_truths)` and `len(predictions)`")
    return confusion_matrix(ground_truths, predictions)

def visualise_conf_matrix(
    conf_matrix: np.ndarray,
    labels: List[str],
    title: Optional[str] = None,
    normalize: bool = True,
    cmap: Union[None, str, mpl.colors.Colormap] = None,
    width: int = 6,
    dpi: int = 200,
    return_pil: bool = True,
):
    # Convert to DataFrame
    cm = conf_matrix
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        cm = pd.DataFrame(cm * 100)
    else:
        cm = pd.DataFrame(cm)
    cm.index = labels
    cm.columns = labels

    # Setup plot canvas
    fig, ax = plt.subplots(figsize=(width, width), dpi=dpi)

    # Colormap
    if not cmap:
        cmap = 'Blues'
        # cmap = sns.cubehelix_palette(as_cmap=True)

    # Draw heatmap, axes and title
    sns.heatmap(cm, annot=True, fmt=".1f", cbar=False, ax=ax, cmap=cmap)
    _= ax.set_yticklabels(labels, rotation=0)
    _= ax.set_xticklabels(labels, rotation=90)

    if title:
        ax.set_title(title)

    if return_pil: return fig_to_pil(fig)
    else:          return fig

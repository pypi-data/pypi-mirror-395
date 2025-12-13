from upyog.ml.imports import *


__all__ = ["SoftmaxProcessor", "SigmoidProcessor"]


@dataclass
class Prediction:
    label: List[str]
    confidence: List[float]

    def __post_init__(self):
        if isinstance(self.label,      np.ndarray): self.label = self.label.tolist()
        if isinstance(self.confidence, np.ndarray): self.confidence = self.confidence.tolist()


class ActivationsProcessor(ABC):
    "Post processors for predictions coming out of Softmax / Sigmoid layers"

    @property
    @abstractmethod
    def labels(self) -> np.ndarray:
        ...

    @abstractmethod
    def _forward(self):
        ...

    def _type_check(self, preds: np.ndarray):
        if not isinstance(preds, np.ndarray):
            raise TypeError(f"Expected `preds` to be an array, got {type(preds)}")

    def __call__(self, preds: np.ndarray) -> Union[Prediction, List[Prediction]]:
        self._type_check(preds)

        if self._is_singular_pred(preds): return          self._forward(preds)
        else:                             return list(map(self._forward, preds))

    @staticmethod
    def _is_singular_pred(preds: np.ndarray):
        # assert preds.ndim in [1, 2]
        return preds.ndim == 1

    # @abstractmethod
    # def activate(self, preds: np.ndarray):
    #     ...


class SoftmaxProcessor(ActivationsProcessor):
    def __init__(self, labels: List[str], top_k: int = 1):
        self.top_k = top_k
        self._labels = np.array(labels)

    @property
    def labels(self): return self._labels

    def _forward(self, preds) -> Prediction:
        index = np.argsort(preds)[-self.top_k:]  # argsort gives idxs in ascending order
        confidence = preds[index]
        label = self.labels[index]

        return Prediction(label, confidence)


class SigmoidProcessor(ActivationsProcessor):
    def __init__(self, labels: List[str], thresh: float = 0.8):
        self.thresh = thresh
        self._labels = np.array(labels)

    @property
    def labels(self): return self._labels

    def _forward(self, preds) -> Prediction:
        index = np.where(preds > self.thresh)
        confidence = preds[index]
        label = self.labels[index]

        return Prediction(label, confidence)

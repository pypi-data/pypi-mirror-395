from upyog.imports import *
from upyog.image.composition import make_img_grid


__all__ = ["CosineSimilarityQueryRunner"]


class CosineSimilarityQueryRunner:
    def __init__(
        self,
        indices: List[Any],
        embeddings: np.ndarray,
        normalize=True,
        verbose=True,
    ):
        self.indices = np.array(indices)
        self.verbose = verbose
        
        if not embeddings.ndim==2:
            raise ValueError(f"Expected `embeddings` to be a 2-dim array")

        if not len(embeddings) == len(indices):
            raise ValueError(f"Expected number of `embeddings` to be the same as `indices`")
        
        if normalize:
            self.log(f"Normalizing input embeddings")
            if not embeddings.ndim==2:
                raise ValueError(f"Expected 2-dim embeddings, got {embeddings.ndim}")
            embeddings_norm = np.linalg.norm(embeddings, axis=1)
            embeddings /= embeddings_norm[:, np.newaxis]

        self.embeddings = embeddings
        self.log("Init successful!")

    @classmethod
    def from_df(cls, df: pd.DataFrame, index_col: str, embed_col: str, verbose=True):
        df = df.sort_values(index_col)
        if verbose: logger.info("Initialising from DataFrame")
        return cls(
            indices = df.loc[:, index_col].values.tolist(),
            embeddings = np.stack(df.loc[:, embed_col]),
            verbose = verbose,
        )

    def log(self, msg: str) -> None:
        if self.verbose:
            logger.info(msg)

    def get_top_matches_with_embeds(
        self,
        query_embedding: np.ndarray,
        embeddings: np.ndarray,
        normalize=True
    ):
        if query_embedding.ndim != 1 or embeddings.ndim != 2:
            raise ValueError("Incorrect dimensions for query_embedding or embeddings")

        # Normalize the embeddings if required
        if normalize:
            self.log("Normalizing query embedding")
            query_norm = np.sqrt(np.dot(query_embedding, query_embedding))
            query_embedding /= query_norm

        # Compute similarities and get sorted indices
        self.log("Doing cosine similarity")
        similarities = query_embedding @ embeddings.T
        sorted_indices = np.argsort(similarities)[::-1]

        return [(similarities[i], i) for i in sorted_indices]

    
    def query(self, i: int, normalize=True):
        sim = self.get_top_matches_with_embeds(
            query_embedding = self.embeddings[i],
            embeddings = self.embeddings,
            normalize = normalize,
        )
        return sim

    def query_top_N(self, i:int, N=9, debug=False, normalize=True) -> List[Any]:
        self.log(f"Querying for Top {N} matches")
        sim = self.query(i, normalize=normalize)
        scores, indices = zip(*sim)
        
        result_indices = indices[:N if debug else N+1]
        result_indices = self.indices[list(result_indices)]
        
        return result_indices
    
    def view_top_N(self, i: int, N=9, debug=False, normalize=True) -> Image.Image:
        self.log("Visualising results")
        result_indices = self.query_top_N(i,N,debug,normalize)
        return make_img_grid(
            imgs=[Image.open(f).convert("RGB") for f in result_indices],
            ncol=2,
        )

    def __del__(self):
        del self.indices
        del self.embeddings

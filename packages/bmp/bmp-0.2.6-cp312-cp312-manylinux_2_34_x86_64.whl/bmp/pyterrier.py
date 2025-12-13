import numpy as np
import pandas as pd
from pathlib import Path
import pyterrier as pt
import pyterrier_alpha as pta
from bmp import Indexer, Searcher

class BmpIndex(pta.Artifact, pt.Indexer):
    """ Represents a Block-Max Pruning Index stored on disk.

    .. cite.dblp:: conf/sigir/MalliaST24
    """
    ARTIFACT_TYPE = 'sparse_index'
    ARTIFACT_FORMAT = 'bmp'

    def __init__(self, path: str):
        """
        Args:
            path (str): Path to the index directory.
        """
        super().__init__(path)
        self._searcher = None

    def built(self) -> bool:
        """ Checks whether the index has been built.

        Returns:
            bool: True if the index exists on disk, False otherwise.
        """
        return Path(self.path).exists()

    def indexer(
        self,
        *,
        bsize: int = 32,
        compress_range: bool = False,
        scale_float: float = 100.,
    ) -> pt.Indexer:
        """ Creates a :class:`bmp.pyterrier.BmpIndexer` for indexing documents.

        Args:
            bsize (int): Block size for block-max pruning.
            compress_range (bool): Whether to compress the index.
            scale_float (float): Scaling factor for float token values into integers.

        Returns:
            BmpIndexer: The indexer instance.
        """
        return BmpIndexer(self, bsize=bsize, compress_range=compress_range, scale_float=scale_float)

    def index(self, inp: pt.model.IterDict) -> pt.Artifact:
        """ Index the documents with default settings.

        Args:
            inp: An iterable of documents (dicts containing ``docno`` and ``toks`` keys) to index.
        """
        return self.indexer().index(inp)

    def retriever(
        self,
        *,
        num_results: int = 1000,
        alpha: float = 1.0,
        beta: float = 1.0,
    ) -> pt.Transformer:
        """ Creates a :class:`bmp.pyterrier.BmpRetriever` for this index.

        Args:
            num_results: the number of results per query to retrieve.
            alpha: block termination threshold (terminate retrievel when the maximum block score is less than ``alpha`` of the threshold. Decreasing this value increases the chance documents are missed, but speeds up retrieval by pruning more blocks. For exact retrieval, use ``alpha=1.0`` (default).
            beta: query term pruning factor (keeps the top ``beta`` weight of query terms). Decreasing this value introduces score approximation error, but reduces computational cost. For exact scoring, use ``beta=1.0`` (default).

        Returns:
            The retriever instance.
        """
        return BmpRetriever(self, num_results=num_results, alpha=alpha, beta=beta)

    def transform(self, inp: pd.DataFrame) -> pd.DataFrame:
        """ Retrieve documents from the index for the given queries using default settings (exact retrieval),

        Args:
            inp: A DataFrame containing queries with a ``query_toks`` column.

        Returns:
            DataFrame containing retrieved documents with ``docno``, ``score``, and ``rank`` columns.
        """
        return self.retriever()(inp)

    def load_into_memory(self):
        """ Loads the index into memory and returns a Searcher instance.

        If the searcher is already loaded, it returns the existing instance.

        Returns:
            Searcher: The in-memory searcher instance.
        """
        if self._searcher is None:
            self._searcher = Searcher(str(self.path/'index.bmp'))
        return self._searcher

    def close(self):
        """ Closes the in-memory searcher if it exists. """
        self._searcher = None

    def __enter__(self):
        self.load_into_memory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class BmpIndexer(pt.Indexer):
    """ An indexer for a BMP index. """
    def __init__(
        self,
        bmp_index: BmpIndex,
        bsize: int = 32,
        compress_range: bool = False,
        scale_float: float = 100.
    ):
        """
        Args:
            bmp_index: BMP index object to create.
            bsize: Block size for block-max pruning.
            compress_range: Whether to compress the index.
            scale_float: Scaling factor for float token values into integers.

        Returns:
            BmpIndexer: The indexer instance.
        """
        self.bmp_index = bmp_index
        self.bsize = bsize
        self.compress_range = compress_range
        self.scale_float = scale_float

    def index(self, inp: pt.model.IterDict) -> pt.Artifact:
        """ Index the documents with default settings.

        Args:
            inp: An iterable of documents (dicts containing ``docno`` and ``toks`` keys) to index.
        """
        assert not self.bmp_index.built()
        with pta.ArtifactBuilder(self.bmp_index) as builder:
            indexer = Indexer(str(self.bmp_index.path/'index.bmp'), bsize=self.bsize, compress_range=self.compress_range)
            count = 0
            for doc in inp:
                vector = doc['toks']
                if len(vector) > 0 and isinstance(next(iter(vector.values())), float):
                    vector = {k: int(v * self.scale_float) for k, v in vector.items()}
                indexer.add_document(doc['docno'], vector)
                count += 1
            indexer.finish()
            builder.metadata['bsize'] = self.bsize
            builder.metadata['compress_range'] = self.compress_range
            builder.metadata['scale_float'] = self.scale_float
            builder.metadata['num_docs'] = count
        return self.bmp_index


class BmpRetriever(pt.Transformer):
    """ A transformer that retrieves over a BMP index. """
    def __init__(
        self,
        bmp_index: BmpIndex,
        *,
        num_results: int = 1000,
        alpha: float = 1.0,
        beta: float = 1.0
    ):
        """
        Args:
            bmp_index: BMP index object to retrieve over.
            num_results: the number of results per query to retrieve.
            alpha: block termination threshold (terminate retrievel when the maximum block score is less than ``alpha`` of the threshold. Decreasing this value increases the chance documents are missed, but speeds up retrieval by pruning more blocks. For exact retrieval, use ``alpha=1.0`` (default).
            beta: query term pruning factor (keeps the top ``beta`` weight of query terms). Decreasing this value introduces score approximation error, but reduces computational cost. For exact scoring, use ``beta=1.0`` (default).
        """
        self.bmp_index = bmp_index
        self.num_results = num_results
        self.alpha = alpha
        self.beta = beta

    def transform(self, inp: pd.DataFrame) -> pd.DataFrame:
        """ Retrieve documents from the index for the given queries.

        Args:
            inp: A DataFrame containing queries with a ``query_toks`` column.

        Returns:
            DataFrame containing retrieved documents with ``docno``, ``score``, and ``rank`` columns.
        """
        pta.validate.query_frame(inp, extra_columns=['query_toks'])
        searcher = self.bmp_index.load_into_memory()
        res = pta.DataFrameBuilder(['docno', 'score', 'rank'])
        for toks in inp['query_toks']:
            docnos, scores = searcher.search(toks, k=self.num_results, alpha=self.alpha, beta=self.beta)
            res.extend({
                'docno': docnos,
                'score': scores,
                'rank': np.arange(len(scores))
            })
        return res.to_df(inp)

    def fuse_rank_cutoff(self, k):
        if self.num_results > k:
            return BmpRetriever(self.bmp_index, num_results=k, alpha=self.alpha, beta=self.beta)

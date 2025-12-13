BMP + PyTerrier
===========================================

BMP (Block-Max Pruning) is a retrieval approach and software package that provides fast exact and approximate sparse search
functionality. It was introduced in the following article:

.. cite.dblp:: conf/sigir/MalliaST24

Overview
-----------------------------------------

.. related:: bmp.pyterrier.BmpIndex
.. related:: bmp.pyterrier.BmpIndexer
.. related:: bmp.pyterrier.BmpRetriever

BMP provides a PyTerrier-compatible interface, which is covered in this documentation. You an install it with pip:

.. code-block:: bash

    pip install bmp[pyterrier]

:class:`bmp.pyterrier.BmpIndex` is an artifact that provides indexing and retrieval functionality. Most of the time,
you will likely use :class:`~bmp.pyterrier.BmpIndex` in conjunction with a LSR model, such as SPLADE.

.. code-block:: python
    :caption: Indexing with BMP and Splade

    from bmp.pyterrier import BmpIndex
    from pyt_splade import SPLADE
    index = BmpIndex('my_index.bmp') # :footnote: Specify the path that you want to index to. The ``.bmp`` extension is optional.
    model = Splade() # :footnote: Load a learned sparse retrieval model. Here we use SPLADE, but you can use any LSR model that you wish.
    indexing_pipeline = model >> index.indexer() # :footnote: The indexing pipeline first encodes documents with SPLADE, then adds them to the BMP index.
    indexing_pipeline.index([
        {'docno': '1', 'text': 'My document'},
        {'docno': '1', 'text': 'Another document'},
    ])

.. code-block:: python
    :caption: Retrieval with BMP and Splade

    from bmp.pyterrier import BmpIndex
    from pyt_splade import Splade
    index = BmpIndex('my_index.bmp') # :footnote: Specify the path to a BMP index that you built.
    model = Splade() # :footnote: Load the learned sparse model that you used to build your index
    retrieval_pipeline = model >> index.retriever() # :footnote: The retrieval pipeline first encodes queries with SPLDE, then retrieves over the BMP index.
    retrieval_pipeline.search('my query')


Additional Materials
-----------------------------------------

.. toctree::
   :maxdepth: 1

   API Reference <api>

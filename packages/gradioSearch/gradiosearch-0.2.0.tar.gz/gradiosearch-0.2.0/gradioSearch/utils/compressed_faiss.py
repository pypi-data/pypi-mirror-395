"""
Inherit from FAISS vectorstore from langchain but using binary embeddings from faiss.


Source:
https://python.langchain.com/api_reference/_modules/langchain_community/vectorstores/faiss.html#FAISS
https://github.com/facebookresearch/faiss/wiki/Binary-indexes
"""

from __future__ import annotations
from pathlib import Path

import logging
import pickle
import zlib
from beartype.typing import (
    Any,
)
from langchain_core.embeddings import Embeddings

from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.faiss import (
    dependable_faiss_import,
)

logger = logging.getLogger(__name__)


class CompressedFAISS(FAISS):
    """FAISS vector store with compressed storage.

    This subclass adds zlib compression to the save_local and load_local methods
    to reduce storage size of the docstore and index mappings.
    """

    def save_local(self, folder_path: str, index_name: str = "index") -> None:
        """Save FAISS index, docstore, and index_to_docstore_id to disk with compression.

        Args:
            folder_path: folder path to save index, docstore,
                and index_to_docstore_id to.
            index_name: for saving with a specific index file name
        """
        path = Path(folder_path)
        path.mkdir(exist_ok=True, parents=True)

        # save index separately since it is not picklable
        faiss = dependable_faiss_import()
        p = str(path / f"{index_name}.faiss")
        if "IndexBinaryFlat" in str(self.index):
            faiss.write_index_binary(self.index, p)
        else:
            faiss.write_index(self.index, p)

        # save docstore and index_to_docstore_id with zlib compression
        pickle_data = pickle.dumps((self.docstore, self.index_to_docstore_id))
        compressed_data = zlib.compress(pickle_data)
        with open(path / f"{index_name}.pkl", "wb") as f:
            f.write(compressed_data)

    @classmethod
    def load_local(
        cls,
        folder_path: str,
        embeddings: Embeddings,
        index_name: str = "index",
        *,
        allow_dangerous_deserialization: bool = False,
        **kwargs: Any,
    ) -> "CompressedFAISS":
        """Load FAISS index, docstore, and index_to_docstore_id from disk with decompression.

        Args:
            folder_path: folder path to load index, docstore,
                and index_to_docstore_id from.
            embeddings: Embeddings to use when generating queries
            index_name: for saving with a specific index file name
            allow_dangerous_deserialization: whether to allow deserialization
                of the data which involves loading a pickle file.
                Pickle files can be modified by malicious actors to deliver a
                malicious payload that results in execution of
                arbitrary code on your machine.
        """
        if not allow_dangerous_deserialization:
            raise ValueError(
                "The de-serialization relies loading a pickle file. "
                "Pickle files can be modified to deliver a malicious payload that "
                "results in execution of arbitrary code on your machine."
                "You will need to set `allow_dangerous_deserialization` to `True` to "
                "enable deserialization. If you do this, make sure that you "
                "trust the source of the data. For example, if you are loading a "
                "file that you created, and know that no one else has modified the "
                "file, then this is safe to do. Do not set this to `True` if you are "
                "loading a file from an untrusted source (e.g., some random site on "
                "the internet.)."
            )
        path = Path(folder_path)
        # load index separately since it is not picklable
        faiss = dependable_faiss_import()
        p = str(path / f"{index_name}.faiss")
        try:
            index = faiss.read_index(p)
        except RuntimeError as e:
            if (
                "index type" not in str(e).lower()
                and " not recognized" in str(e).lower()
            ):
                raise
            index = faiss.read_index_binary(p)

        # load docstore and index_to_docstore_id with zlib decompression
        # fallback to uncompressed loading if decompression fails
        with open(path / f"{index_name}.pkl", "rb") as f:
            file_data = f.read()

        try:
            # Try loading with zlib decompression first
            pickle_data = zlib.decompress(file_data)
            (
                docstore,
                index_to_docstore_id,
            ) = pickle.loads(pickle_data)  # ignore[pickle]: explicit-opt-in
        except (zlib.error, pickle.UnpicklingError) as e:
            # Fallback: try loading without decompression (backwards compatibility)
            logger.info(
                f"Failed to load compressed data ({e}), trying uncompressed format"
            )
            (
                docstore,
                index_to_docstore_id,
            ) = pickle.loads(file_data)  # ignore[pickle]: explicit-opt-in

        return cls(embeddings, index, docstore, index_to_docstore_id, **kwargs)

"""
Main module for gradioSearch CLI tool
"""

import argparse
import sys
from pathlib import Path
from tqdm import tqdm
import json
import pickle

# from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from .utils.gui import launch_gui
from .utils.compressed_faiss import CompressedFAISS as FAISS


class SentenceTransformerEmbeddings(Embeddings):
    """Wrapper for SentenceTransformer to make it compatible with LangChain Embeddings interface.

    This is needed because FAISS expects an Embeddings object with embed_query() and
    embed_documents() methods, while SentenceTransformer uses a different API.
    """

    def __init__(self, model_name: str, **encode_kwargs):
        """
        Initialize with model name and optional encoding kwargs.

        Parameters
        ----------
        model_name : str
            Name of the sentence-transformers model to load
        **encode_kwargs : dict
            Additional keyword arguments to pass to model.encode()
            e.g., batch_size, show_progress_bar, normalize_embeddings, etc.
        """
        self.model = SentenceTransformer(model_name)
        self.encode_kwargs = encode_kwargs

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.

        Parameters
        ----------
        texts : List[str]
            List of documents to embed

        Returns
        -------
        List[List[float]]
            List of embeddings, one per document
        """
        return self.model.encode(
            texts, convert_to_tensor=False, **self.encode_kwargs
        ).tolist()

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query.

        Parameters
        ----------
        text : str
            Query text to embed

        Returns
        -------
        List[float]
            Query embedding
        """
        return self.model.encode([text], convert_to_tensor=False, **self.encode_kwargs)[
            0
        ].tolist()


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="CLI tool for searching FAISS vector databases with Gradio GUI"
    )

    parser.add_argument(
        "--db_path",
        type=str,
        required=True,
        help="Path to the Langchain FAISS database",
    )

    parser.add_argument(
        "--embedding_model",
        type=str,
        required=True,
        help="Embedding model name for sentence-transformers",
    )

    parser.add_argument(
        "--metadata_keys",
        type=str,
        default="*",
        help="Comma-separated list of metadata columns to display, or '*' to use all available keys (default: '*')",
    )

    parser.add_argument(
        "--topk",
        type=int,
        default=50,
        help="Number of top results to retrieve (default: 50)",
    )

    parser.add_argument(
        "--convert-embeddings",
        action="store_true",
        help="Convert embeddings: re-compute all embeddings using the specified model and save to output path",
    )

    parser.add_argument(
        "--output-db-path",
        type=str,
        default=None,
        help="Output path for converted FAISS database (required when --convert-embeddings is used)",
    )

    parser.add_argument(
        "--embedding-kwargs",
        type=str,
        default="{}",
        help='JSON string of kwargs to pass to the embedder, e.g. \'{"batch_size": 32, "normalize_embeddings": true}\'',
    )

    return parser.parse_args()


def convert_embeddings(
    vectorstore: FAISS,
    embedding_model: SentenceTransformerEmbeddings,
    output_path: str,
    batch_size: int = 32,
) -> None:
    """
    Extract all documents from vectorstore and re-compute embeddings.

    Parameters
    ----------
    vectorstore : FAISS
        Source FAISS vectorstore to extract documents from
    embedding_model : SentenceTransformerEmbeddings
        Embedding model to use for re-computation
    output_path : str
        Path to save the new FAISS database
    batch_size : int
        Batch size for embedding computation (default: 32)
    """
    print("\n=== Starting Embedding Conversion ===")

    # Extract all documents from the vectorstore's docstore
    print("Extracting documents from vectorstore...")
    documents = []
    if hasattr(vectorstore, "docstore") and hasattr(vectorstore.docstore, "_dict"):
        documents = list(vectorstore.docstore._dict.values())
    else:
        raise ValueError("Cannot access docstore to extract documents")

    print(f"Found {len(documents)} documents to re-embed")

    if not documents:
        print("No documents found. Aborting conversion.")
        return

    # Extract texts for embedding
    texts = [doc.page_content for doc in documents]

    # Re-compute embeddings in batches with progress bar
    print(f"Re-computing embeddings in batches of {batch_size}...")
    all_embeddings = []

    for i in tqdm(range(0, len(texts), batch_size), desc="Embedding batches"):
        batch_texts = texts[i : i + batch_size]
        batch_embeddings = embedding_model.embed_documents(batch_texts)
        all_embeddings.extend(batch_embeddings)

    print(f"Generated {len(all_embeddings)} embeddings")

    # Create new FAISS vectorstore from documents and embeddings
    print("Creating new FAISS vectorstore...")
    new_vectorstore = FAISS.from_embeddings(
        text_embeddings=list(zip(texts, all_embeddings)),
        embedding=embedding_model,
        metadatas=[doc.metadata for doc in documents],
    )

    # Save the new vectorstore
    print(f"Saving converted vectorstore to: {output_path}")
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    new_vectorstore.save_local(output_path)

    print(f"✓ Conversion complete! New database saved to: {output_path}")


def main():
    """Main entry point"""
    try:
        args = parse_args()
    except SystemExit:
        return 1

    # Validate db_path exists (can be either directory for FAISS or file for pickle)
    db_path = Path(args.db_path)
    if not db_path.exists():
        print(f"Error: Database path '{args.db_path}' does not exist")
        return 1

    # Validate topk is positive
    if args.topk <= 0:
        print(f"Error: topk must be positive, got {args.topk}")
        return 1

    # Parse metadata_keys argument
    metadata_keys_input = args.metadata_keys.strip()
    if metadata_keys_input == "*":
        metadata_keys = ["*"]
    else:
        try:
            metadata_keys = [
                key.strip() for key in metadata_keys_input.split(",") if key.strip()
            ]
            if not metadata_keys:
                print("Error: metadata_keys cannot be empty")
                return 1
        except Exception as e:
            print(f"Error parsing metadata_keys: {e}")
            return 1

    print(f"Database path: {args.db_path}")
    print(f"Embedding model: {args.embedding_model}")
    print(f"Metadata keys: {metadata_keys}")
    print(f"Top-k results: {args.topk}")

    # Validate conversion mode arguments
    if args.convert_embeddings:
        if not args.output_db_path:
            print("Error: --output-db-path is required when using --convert-embeddings")
            return 1

        output_path = Path(args.output_db_path)
        if output_path.exists():
            print(
                f"Warning: Output path '{args.output_db_path}' already exists and will be overwritten"
            )

    try:
        # Parse embedding kwargs
        try:
            embedding_kwargs = json.loads(args.embedding_kwargs)
            if not isinstance(embedding_kwargs, dict):
                print("Error: --embedding-kwargs must be a JSON object/dict")
                return 1
            print(f"Embedding kwargs: {embedding_kwargs}")
        except json.JSONDecodeError as e:
            print(f"Error parsing --embedding-kwargs JSON: {e}")
            return 1

        # Load embedding model
        print(f"Loading embedding model: {args.embedding_model}")
        try:
            embedding_model = SentenceTransformerEmbeddings(
                args.embedding_model, **embedding_kwargs
            )
        except Exception as e:
            print(f"Error loading embedding model '{args.embedding_model}': {e}")
            print("Please check that the model name is correct and available")
            return 1

        # Load FAISS database
        print(f"Loading FAISS database from: {args.db_path}")
        try:
            vectorstore = FAISS.load_local(
                args.db_path, embedding_model, allow_dangerous_deserialization=True
            )
        except Exception as e:
            print(f"Error loading FAISS database from '{args.db_path}': {e}")
            print("Attempting to load as pickled documents list...")

            # Fallback: try to load as a pickle file containing a list of Documents
            # This allows converting a pickled list of documents into a FAISS database
            try:
                db_path = Path(args.db_path)
                with open(db_path, "rb") as f:
                    unpickled_data = pickle.load(f)

                # Validate that it's a list of Documents
                if not isinstance(unpickled_data, list):
                    print("Error: Pickled data is not a list")
                    return 1

                if not unpickled_data:
                    print("Error: Pickled list is empty")
                    return 1

                # Check if items are Documents by checking for required attributes
                # We check the first item as a sample
                first_item = unpickled_data[0]
                if not (
                    hasattr(first_item, "page_content")
                    and hasattr(first_item, "metadata")
                ):
                    print(
                        "Error: Pickled data doesn't contain valid Langchain Documents"
                    )
                    print(
                        "Expected objects with 'page_content' and 'metadata' attributes"
                    )
                    return 1

                print(f"Found {len(unpickled_data)} documents in pickle file")
                print(
                    "Creating FAISS database from documents using provided embedding model..."
                )

                # Create FAISS database from the documents
                # This will embed all documents using the provided embedding model
                vectorstore = FAISS.from_documents(
                    documents=unpickled_data, embedding=embedding_model
                )

                print("Successfully created FAISS database from pickled documents")

            except pickle.UnpicklingError as pickle_error:
                print(f"Error unpickling file: {pickle_error}")
                print("File is not a valid pickle file")
                return 1
            except Exception as fallback_error:
                print(f"Error loading as pickled documents: {fallback_error}")
                print("Please check that the path contains either:")
                print("  - A valid Langchain FAISS database directory, or")
                print("  - A pickle file containing a list of Langchain Documents")
                return 1

        # Handle conversion mode
        if args.convert_embeddings:
            try:
                # Extract batch_size from embedding_kwargs if provided, otherwise use default
                batch_size = embedding_kwargs.get("batch_size", 32)
                convert_embeddings(
                    vectorstore=vectorstore,
                    embedding_model=embedding_model,
                    output_path=args.output_db_path,
                    batch_size=batch_size,
                )
                print("\n=== Conversion completed successfully ===")
                return 0
            except Exception as e:
                import traceback

                print(f"Error during conversion: {e}")
                print(f"Traceback:\n{traceback.format_exc()}")
                return 1

        # Create search function with error handling
        def search_function(query: str, topk: int = args.topk) -> List[Dict[str, Any]]:
            try:
                # For empty queries, use a space to get initial documents
                search_query = query.strip() if query and query.strip() else " "

                # Perform similarity search
                print(f"DEBUG: Performing search for: '{search_query}' with k={topk}")
                docs_with_scores = vectorstore.similarity_search_with_score(
                    search_query, k=topk
                )
                print(f"DEBUG: Got {len(docs_with_scores)} results")

                results = []
                for i, (doc, score) in enumerate(docs_with_scores):
                    print(
                        f"DEBUG: Processing result {i}, score={score}, doc type={type(doc)}"
                    )
                    print(f"DEBUG: doc.page_content type={type(doc.page_content)}")
                    print(
                        f"DEBUG: doc.metadata type={type(doc.metadata)}, value={doc.metadata}"
                    )

                    # FAISS returns distance scores (lower = more similar)
                    # Convert to similarity score (higher = more similar)
                    similarity_score = 1.0 - float(score)

                    result = {
                        "similarity_score": similarity_score,
                        "content": str(doc.page_content) if doc.page_content else "",
                        "metadata": dict(doc.metadata)
                        if isinstance(doc.metadata, dict)
                        else {},
                    }
                    results.append(result)

                print(f"DEBUG: Returning {len(results)} formatted results")
                return results
            except Exception as e:
                import traceback

                print(f"Error during search: {e}")
                print(f"Traceback:\n{traceback.format_exc()}")
                return []

        # Launch GUI
        print("Starting Gradio interface...")
        try:
            launch_gui(search_function, metadata_keys, args.topk)
        except Exception as e:
            print(f"Error launching GUI: {e}")
            return 1

    except KeyboardInterrupt:
        print("\nShutting down...")
        return 0
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

    return 0

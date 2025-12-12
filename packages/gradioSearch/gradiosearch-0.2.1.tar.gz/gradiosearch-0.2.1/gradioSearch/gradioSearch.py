"""
Main module for gradioSearch CLI tool
"""

import argparse
import sys
from pathlib import Path
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from .utils.gui import launch_gui


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
        required=True,
        help="Comma-separated list of metadata columns to display, or '*' to use all available keys",
    )

    parser.add_argument(
        "--topk",
        type=int,
        default=50,
        help="Number of top results to retrieve (default: 50)",
    )

    return parser.parse_args()


def main():
    """Main entry point"""
    try:
        args = parse_args()
    except SystemExit:
        return 1

    # Validate db_path exists
    db_path = Path(args.db_path)
    if not db_path.exists():
        print(f"Error: Database path '{args.db_path}' does not exist")
        return 1

    # Validate db_path is a directory
    if not db_path.is_dir():
        print(f"Error: Database path '{args.db_path}' is not a directory")
        return 1

    # Validate topk is positive
    if args.topk <= 0:
        print(f"Error: topk must be positive, got {args.topk}")
        return 1

    # Parse and validate metadata keys
    metadata_keys_input = args.metadata_keys.strip()
    if metadata_keys_input == "*":
        # Will be determined after loading the database
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

    try:
        # Load embedding model
        print(f"Loading embedding model: {args.embedding_model}")
        try:
            embedding_model = SentenceTransformer(args.embedding_model)
        except Exception as e:
            print(f"Error loading embedding model '{args.embedding_model}': {e}")
            print("Please check that the model name is correct and available")
            return 1

        # Load FAISS database
        print(f"Loading FAISS database from: {args.db_path}")
        try:
            vectorstore = FAISS.load_local(args.db_path, embedding_model)
        except Exception as e:
            print(f"Error loading FAISS database from '{args.db_path}': {e}")
            print(
                "Please check that the path contains a valid Langchain FAISS database"
            )
            return 1

        # If metadata_keys is '*', extract all unique keys from the database
        if metadata_keys == ["*"]:
            print("Extracting all metadata keys from database...")
            try:
                all_keys = set()

                # Try to access docstore directly for efficient sampling
                if hasattr(vectorstore, "docstore") and hasattr(
                    vectorstore.docstore, "_dict"
                ):
                    # Sample documents from docstore
                    count = 0
                    for doc_id, doc in vectorstore.docstore._dict.items():
                        if count >= 100:  # Sample up to 100 documents
                            break
                        if hasattr(doc, "metadata") and doc.metadata:
                            all_keys.update(doc.metadata.keys())
                        count += 1
                else:
                    # Fallback: do a dummy search to get sample documents
                    try:
                        sample_docs = vectorstore.similarity_search("sample", k=50)
                        for doc in sample_docs:
                            if doc.metadata:
                                all_keys.update(doc.metadata.keys())
                    except:
                        pass

                if not all_keys:
                    print(
                        "Warning: No metadata keys found in database. Using empty list."
                    )
                    metadata_keys = []
                else:
                    metadata_keys = sorted(list(all_keys))
                    print(f"Found metadata keys: {metadata_keys}")
            except Exception as e:
                print(f"Error extracting metadata keys: {e}")
                return 1

        # Create search function with error handling
        def search_function(query: str, topk: int = args.topk) -> List[Dict[str, Any]]:
            if not query or not query.strip():
                return []

            try:
                # Perform similarity search
                docs_with_scores = vectorstore.similarity_search_with_score(
                    query, k=topk
                )

                results = []
                for doc, score in docs_with_scores:
                    result = {
                        "similarity_score": round(score, 2),
                        "content": doc.page_content or "",
                        **doc.metadata,  # Flatten metadata into the result dict
                    }
                    results.append(result)

                return results
            except Exception as e:
                print(f"Error during search: {e}")
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

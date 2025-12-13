"""
Gradio GUI components for gradioSearch
"""

import gradio as gr
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
import json


def create_search_interface(
    search_function, metadata_keys: List[str], topk: int = 50
) -> gr.Blocks:
    """
    Create Gradio interface for FAISS database search

    Args:
        search_function: Function that takes query string and topk, returns search results
        metadata_keys: List of metadata keys to display and their order
        topk: Number of top results to retrieve

    Returns:
        Gradio Blocks interface
    """

    def format_search_results(
        results: List[Dict[str, Any]],
        metadata_keys: List[str],
    ) -> pd.DataFrame:
        """
        Format search results into dataframe with dynamic columns.
        Filters and orders columns based on metadata_keys specification.

        Args:
            results: List of search result dictionaries with 'content', 'metadata', 'similarity_score'
            metadata_keys: List of metadata keys to display. '*' means all remaining keys.
                          e.g., ['A', 'B', '*'] shows A, B first, then all other keys

        Returns:
            DataFrame with columns ordered according to metadata_keys
        """
        if not results:
            # Return empty dataframe with basic columns
            return pd.DataFrame(columns=["Similarity", "Content"])

        # Scan all results to find metadata keys with non-empty values
        all_metadata_keys_with_values = set()
        for result in results:
            metadata = result.get("metadata", {})
            for key, value in metadata.items():
                # Include key if value is non-empty (not None, not empty string, not empty list, etc.)
                if value is not None and value != "" and value != [] and value != {}:
                    all_metadata_keys_with_values.add(key)

        # Process metadata_keys specification to determine column order
        if metadata_keys == ["*"]:
            # Show all metadata columns, sorted alphabetically
            active_metadata_keys = sorted(list(all_metadata_keys_with_values))
        else:
            # Build ordered list based on metadata_keys specification
            active_metadata_keys = []
            explicit_keys = []
            wildcard_index = -1

            # First pass: identify explicit keys and wildcard position
            for i, key in enumerate(metadata_keys):
                if key == "*":
                    wildcard_index = i
                else:
                    explicit_keys.append(key)

            # Second pass: build the ordered list
            if wildcard_index >= 0:
                # Keys before wildcard
                active_metadata_keys.extend(metadata_keys[:wildcard_index])

                # Remaining keys (all keys minus explicit ones), sorted
                remaining_keys = sorted(
                    list(all_metadata_keys_with_values - set(explicit_keys))
                )
                active_metadata_keys.extend(remaining_keys)

                # Keys after wildcard
                active_metadata_keys.extend(metadata_keys[wildcard_index + 1 :])
            else:
                # No wildcard: only use explicitly specified keys that exist in results
                active_metadata_keys = [
                    k for k in metadata_keys if k in all_metadata_keys_with_values
                ]

        # Prepare dataframe data
        df_data = []
        for result in results:
            row = {}

            # Add similarity score as first column
            row["Similarity"] = round(result.get("similarity_score", 0.0), 2)

            # Add cropped content
            content = result.get("content", "")
            row["Content"] = content[:100] + "..." if len(content) > 100 else content

            # Add only the active metadata columns
            metadata = result.get("metadata", {})
            for key in active_metadata_keys:
                row[key] = metadata.get(key, "")

            df_data.append(row)

        df = pd.DataFrame(df_data)
        return df

    def on_row_select(evt: gr.SelectData, results_state) -> Tuple[str, str]:
        """
        Handle row selection in dataframe to show document details

        Args:
            evt: Gradio SelectData event
            results_state: Current search results

        Returns:
            Tuple of (content_text, metadata_text)
        """
        if not results_state or evt.index[0] >= len(results_state):
            return "", ""

        selected_result = results_state[evt.index[0]]
        content = selected_result.get("content", "")
        metadata = selected_result.get("metadata", {})

        # Format the content
        content_text = f"**Document Content:**\n\n{content}"

        # Format metadata as bullet points with bold keys
        if metadata:
            metadata_lines = []
            for key, value in metadata.items():
                metadata_lines.append(f"- **{key}:** {value}")
            metadata_text = "\n".join(metadata_lines)
        else:
            metadata_text = "*No metadata available*"

        return content_text, metadata_text

    def perform_search(
        query: str, topk_value: int, results_state
    ) -> Tuple[pd.DataFrame, str, str, List[Dict]]:
        """
        Perform search and update interface

        Args:
            query: Search query string
            topk_value: Number of results to retrieve
            results_state: Current results state

        Returns:
            Tuple of (updated_dataframe, empty_content, empty_metadata, new_results_state)
        """
        # Perform the search with topk parameter (empty queries return initial documents)
        results = search_function(query, topk_value)

        # Format results for display with filtered/ordered columns
        df = format_search_results(results, metadata_keys)

        return df, "", "", results

    # Get initial results to populate the dataframe on load
    initial_results = search_function("", topk)
    initial_df = format_search_results(initial_results, metadata_keys)

    # Create the Gradio interface
    with gr.Blocks(
        title="gradioSearch - FAISS Database Search", fill_height=True, fill_width=True
    ) as interface:
        gr.Markdown("# gradioSearch - FAISS Database Search")

        # State to store current search results
        results_state = gr.State(initial_results)

        # Search input at the top
        search_input = gr.Textbox(
            label="Search Query",
            placeholder="Enter your search query and press Enter...",
            lines=1,
        )

        # Top-k slider
        topk_slider = gr.Slider(
            minimum=1,
            maximum=200,
            value=topk,
            step=1,
            label="Number of Results (Top-K)",
            interactive=True,
        )

        # Layout with dataframe on left, details on right
        with gr.Row():
            with gr.Column(scale=2):
                results_df = gr.Dataframe(
                    label="Search Results",
                    interactive=False,
                    wrap=True,
                    row_count=(10, "dynamic"),
                    value=initial_df,
                    max_height=1200,
                    show_search="filter",
                    pinned_columns=2,  # Pin only the Similarity and Content column
                    show_row_numbers=True,
                    line_breaks=True,
                    column_widths=[
                        "5%",
                        "25%",
                    ],  # Set widths for Similarity and Content columns
                )

            with gr.Column(scale=1):
                document_content = gr.Markdown(
                    label="Document Content",
                    value="Select a row from the search results to view document details.",
                )

                with gr.Accordion(label="Metadata", open=False):
                    document_metadata = gr.Markdown(value="*No metadata available*")

        # Event handlers
        search_input.submit(
            fn=perform_search,
            inputs=[search_input, topk_slider, results_state],
            outputs=[results_df, document_content, document_metadata, results_state],
        )

        topk_slider.change(
            fn=perform_search,
            inputs=[search_input, topk_slider, results_state],
            outputs=[results_df, document_content, document_metadata, results_state],
        )

        results_df.select(
            fn=on_row_select,
            inputs=[results_state],
            outputs=[document_content, document_metadata],
        )

    return interface


def launch_gui(
    search_function,
    metadata_keys: List[str],
    topk: int = 50,
    share: bool = False,
    server_port: Optional[int] = None,
) -> None:
    """
    Launch the Gradio interface

    Args:
        search_function: Function that performs the search
        metadata_keys: List of metadata keys to display and their order
        topk: Number of top results to retrieve
        share: Whether to create a public link
        server_port: Port to run the server on
    """
    interface = create_search_interface(search_function, metadata_keys, topk)
    interface.launch(share=share, server_port=server_port, server_name="0.0.0.0")

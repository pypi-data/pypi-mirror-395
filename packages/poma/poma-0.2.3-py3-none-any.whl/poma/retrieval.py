# retrieval.py
from collections import defaultdict
from itertools import chain
from typing import Any
import warnings


def deprecated(replacement: str):
    def decorator(func):
        msg = (
            f"{func.__name__}() is deprecated and will be removed in a future version. "
            f"Use {replacement} instead."
        )

        def wrapper(*args, **kwargs):
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = (func.__doc__ or "") + f"\n\nDEPRECATED: {msg}\n"
        return wrapper

    return decorator


def generate_cheatsheets(
    relevant_chunksets: list[dict[str, Any]],
    all_chunks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    # get chunks grouped by document file_id
    doc_chunks = defaultdict(list)
    for chunk in all_chunks:
        file_id = chunk.get("file_id") or chunk.get("tag") or "single_doc"
        chunk["file_id"] = file_id  # update
        doc_chunks[file_id].append(chunk)

    # Check for duplicate chunk_index values
    # (necessary when file_id was not set in chunks)
    for file_id, chunks in doc_chunks.items():
        chunk_indices = [c["chunk_index"] for c in chunks]
        if len(chunk_indices) != len(set(chunk_indices)):
            raise ValueError(f"Duplicate chunk_index found for file_id: {file_id}")

    # get relevant chunksets grouped by document file_id
    relevant_chunksets_per_doc = defaultdict(list)
    for chunkset in relevant_chunksets:
        file_id = chunkset.get("file_id") or chunkset.get("tag") or "single_doc"
        chunkset["file_id"] = file_id  # update
        if "chunks" not in chunkset:
            raise ValueError(
                "Chunkset not valid; must contain a 'chunks' key with a list of chunk IDs."
            )
        relevant_chunksets_per_doc[file_id].append(chunkset)

    # Ensure that chunksets and chunks correspond to the same file_ids
    for file_id in relevant_chunksets_per_doc.keys():
        if file_id not in doc_chunks:
            raise ValueError(
                f"Chunksets contain file_id '{file_id}' which is not present in the chunks."
            )

    # retrieve relevant chunks with content per document
    relevant_content_chunks: list[RetrievalChunk] = []
    for file_id, chunksets_per_doc in relevant_chunksets_per_doc.items():
        chunk_ids = list(  # flattened list
            chain.from_iterable(chunkset["chunks"] for chunkset in chunksets_per_doc)
        )
        relevant_chunks_dict = _get_relevant_chunks_for_ids(
            chunk_ids, doc_chunks[file_id]
        )
        relevant_chunks: list[RetrievalChunk] = chunks_from_dicts(relevant_chunks_dict)
        relevant_content_chunks.extend(relevant_chunks)

    return _cheatsheets_from_chunks(relevant_content_chunks)


@deprecated("generate_cheatsheets(relevant_chunksets, all_chunks)")
def generate_single_cheatsheet(
    relevant_chunksets: list[dict[str, Any]],
    all_chunks: list[dict[str, Any]],
) -> str:
    cheatsheets = generate_cheatsheets(
        relevant_chunksets=relevant_chunksets,
        all_chunks=all_chunks,
    )
    return cheatsheets[0].get("content", "") if cheatsheets else ""


########################
# RetrievalChunk Class #
########################


class RetrievalChunk:
    """
    Represents a chunk of text with associated metadata.
    Attributes:
        index (int): The index of the chunk within a sequence.
        file_id (str): The id associating the chunk with a document.
        content (str): The textual content of the chunk.
        depth_rebased (int, optional): The hierarchical depth of the chunk content.
            In cheatsheets, this affects indentation for certain text parts.
            Currently only used for code blocks.
    """

    def __init__(
        self,
        index: int,
        file_id: str,
        content: str,
        depth_rebased: int | None,
    ):
        self.index = index
        self.file_id = file_id
        self.content = content
        self.depth_rebased = depth_rebased

    @classmethod
    def from_chunk_dict(
        cls,
        chunk_dict: dict,
        block_min_depth: int | None,
    ):
        if block_min_depth is not None:
            depth = int(chunk_dict["depth"])
            depth_rebased = cls._rebase_depth(depth, block_min_depth)
        else:
            depth_rebased = None
        return cls(
            index=int(chunk_dict["chunk_index"]),
            file_id=str(
                chunk_dict.get("file_id") or chunk_dict.get("tag") or "single_doc"
            ),
            content=str(chunk_dict["content"]),
            depth_rebased=depth_rebased,
        )

    @staticmethod
    def _rebase_depth(depth: int, min_depth: int, base_unit: int = 0) -> int | None:
        rebased = depth - min_depth + base_unit
        return max(0, rebased)

    def __repr__(self):
        return f"RetrievalChunk(index={self.index}, file_id={self.file_id}, content={self.content}), depth_rebased={self.depth_rebased}"


def chunks_from_dicts(chunk_dicts: list[dict]) -> list[RetrievalChunk]:
    """
    Converts a list of chunk dictionaries into a list of Chunk objects.
    File_ids are needed to identify chunks from different documents;
    if is_single_doc is True, all chunks are assumed to come from a single document
    and file_id is optional.
    Args:
        chunk_dicts (list[dict]): A list of dictionaries, each representing a chunk with required keys:
            - "chunk_index": The index of the chunk within the document.
            - "file_id": The identifier of the document.
            - "content": The textual content of the chunk.
            - "depth": The depth or level of the chunk.
    Returns:
        list[Chunk]: A list of Chunk objects with the textual content needed for the cheatsheets.
    """

    # Determine the minimum depth per code block
    min_depth_per_code_block: dict[str, int] = {}
    for chunk_dict in chunk_dicts:
        block_id = chunk_dict.get("code")
        if block_id is None:
            continue
        depth = int(chunk_dict["depth"])
        current = min_depth_per_code_block.get(block_id)
        min_depth_per_code_block[block_id] = (
            depth if current is None else min(current, depth)
        )

    # Create Chunk objects
    all_chunks: list[RetrievalChunk] = []
    for chunk_dict in chunk_dicts:
        code_id = chunk_dict.get("code")
        if bool(code_id):
            block_min_depth = min_depth_per_code_block.get(str(code_id))
        else:
            block_min_depth = None
        chunk = RetrievalChunk.from_chunk_dict(chunk_dict, block_min_depth)
        all_chunks.append(chunk)

    # Sanity check: Make sure there are no duplicate chunk_index values
    check_dict = defaultdict(set)
    has_duplicates = any(
        chunk.index in check_dict[chunk.file_id]
        or check_dict[chunk.file_id].add(chunk.index)
        for chunk in all_chunks
    )
    if has_duplicates:
        raise ValueError(
            "Duplicate chunk indices found in single document mode. "
            "Each chunk must have a unique index."
        )

    return all_chunks


###################
# Private Methods #
###################


def _get_relevant_chunks_for_ids(
    chunk_ids: list[int],
    chunks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    chunk_indices_of_retrieved_chunksets = chunk_ids
    all_chunks_of_doc = chunks

    # Build helpers
    sorted_chunks = sorted(all_chunks_of_doc, key=lambda c: c["chunk_index"])
    index_to_chunk = {c["chunk_index"]: c for c in sorted_chunks}
    index_to_depth = {c["chunk_index"]: c["depth"] for c in sorted_chunks}

    # Find relatively deepest indices in the retrieval
    candidate_indices = set(chunk_indices_of_retrieved_chunksets)

    def is_ancestor(idx1, idx2):
        """True if idx1 is an ancestor of idx2."""
        # idx1 must be before idx2 and have smaller depth
        if idx1 >= idx2:
            return False
        if idx1 not in index_to_depth or idx2 not in index_to_depth:
            return False
        depth1 = index_to_depth[idx1]
        depth2 = index_to_depth[idx2]
        if depth1 >= depth2:
            return False
        # scan from idx1+1 up to idx2, making sure all are deeper than depth1 until idx2
        # Use sorted_chunks to iterate in order, but check chunk_index values
        for chunk in sorted_chunks:
            chunk_idx = chunk["chunk_index"]
            if chunk_idx <= idx1:
                continue
            if chunk_idx > idx2:
                break
            if chunk_idx == idx2:
                continue  # skip idx2 itself, we'll check it after
            depth = index_to_depth[chunk_idx]
            if depth <= depth1:
                return False
        return True

    # Exclude any index that is an ancestor of another in the set
    relatively_deepest = set(candidate_indices)
    for idx1 in candidate_indices:
        for idx2 in candidate_indices:
            if idx1 != idx2 and is_ancestor(idx1, idx2):
                relatively_deepest.discard(idx1)
                break

    # Standard subtree/parent finding routines
    def get_child_indices(chunk_index: int) -> list[int]:
        if chunk_index not in index_to_depth:
            return []
        base_depth = index_to_depth[chunk_index]
        children = []
        # Find the position of chunk_index in sorted_chunks
        start_pos = None
        for pos, chunk in enumerate(sorted_chunks):
            if chunk["chunk_index"] == chunk_index:
                start_pos = pos
                break
        if start_pos is None:
            return []
        # Iterate forward from the next position
        for i in range(start_pos + 1, len(sorted_chunks)):
            idx = sorted_chunks[i]["chunk_index"]
            depth = sorted_chunks[i]["depth"]
            if depth <= base_depth:
                break
            children.append(idx)
        return children

    def get_parent_indices(chunk_index: int) -> list[int]:
        if chunk_index not in index_to_depth:
            return []
        parents = []
        current_depth = index_to_depth[chunk_index]
        # Find the position of chunk_index in sorted_chunks
        start_pos = None
        for pos, chunk in enumerate(sorted_chunks):
            if chunk["chunk_index"] == chunk_index:
                start_pos = pos
                break
        if start_pos is None:
            return []
        # Iterate backward from the previous position
        for i in range(start_pos - 1, -1, -1):
            idx = sorted_chunks[i]["chunk_index"]
            depth = sorted_chunks[i]["depth"]
            if depth < current_depth:
                parents.append(idx)
                current_depth = depth
        return parents[::-1]  # root -> leaf order

    # Collect all relevant indices
    all_indices = set(
        chunk_indices_of_retrieved_chunksets
    )  # always include all search hits
    for idx in relatively_deepest:
        all_indices.update(get_child_indices(idx))

    # Parents for all found nodes
    for idx in list(all_indices):
        all_indices.update(get_parent_indices(idx))

    # Return in doc order
    return [index_to_chunk[i] for i in sorted(all_indices)]


def _cheatsheets_from_chunks(
    content_chunks: list[RetrievalChunk],
) -> list[dict[str, Any]]:
    if not content_chunks:
        return []

    if isinstance(content_chunks[0], dict):
        raise ValueError(
            "Input to _cheatsheets_from_chunks must be a list of RetrievalChunk objects, not dicts."
            "Use chunks_from_dicts() to convert dicts to RetrievalChunk objects first."
        )

    def _format_chunk_content(chunk: "RetrievalChunk") -> str:
        if not getattr(chunk, "depth_rebased", False):
            return chunk.content
        else:
            indent = " " * 4 * (chunk.depth_rebased or 0)
            return f"{indent}{chunk.content}"

    cheatsheets: list[dict] = []

    compressed_data = {}
    content_chunks = sorted(content_chunks, key=lambda c: (c.file_id, c.index))
    for chunk in content_chunks:
        if chunk.file_id not in compressed_data:
            # If there is data stored for a previous file_id, save it to the cheatsheets list
            if compressed_data:
                for key, value in compressed_data.items():
                    cheatsheets.append(
                        {"file_id": key, "tag": key, "content": value["content"]}
                    )
            # Clear the compressed_data for the current file_id
            compressed_data.clear()
            # Start a new entry for the current file_id
            compressed_data[chunk.file_id] = {
                "content": _format_chunk_content(chunk),
                "last_chunk": chunk.index,
            }
        else:
            chunk_content = _format_chunk_content(chunk)
            # Check if chunks are consecutive
            if chunk.index == int(compressed_data[chunk.file_id]["last_chunk"]) + 1:
                compressed_data[chunk.file_id]["content"] += "\n" + chunk_content
            else:
                compressed_data[chunk.file_id]["content"] += "\n[…]\n" + chunk_content
            # Update the last chunk index
            compressed_data[chunk.file_id]["last_chunk"] = chunk.index

    # Save the last processed entry to the cheatsheets list
    if compressed_data:
        for key, value in compressed_data.items():
            cheatsheets.append(
                {"file_id": key, "tag": key, "content": value["content"]}
            )

    return cheatsheets

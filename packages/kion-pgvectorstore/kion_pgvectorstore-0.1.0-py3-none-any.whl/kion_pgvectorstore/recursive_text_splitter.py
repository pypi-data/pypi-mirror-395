import datetime
import os
import re
from typing import Iterable, List
from kion_pgvectorstore.document import Document
import tiktoken

class RecursiveCharacterTextSplitter:
    """
    A simple, native text splitter that:
    - Produces chunks up to chunk_size tokens (not characters)
    - Uses a token-based overlap of chunk_overlap
    - Tries to split at natural boundaries (\n\n, then \n, then space) before falling back to a hard cut
    - Returns a list of Document objects when splitting documents

    NOTE: Both `chunk_size` and `chunk_overlap` are measured in TOKENS, not characters.
    """

    def __init__(self, chunk_size: int, chunk_overlap: int, length_function=len, is_separator_regex: bool = False):
        """
        Args:
            chunk_size (int): Max number of TOKENS per chunk.
            chunk_overlap (int): Number of overlapping TOKENS between chunks.
        """
        if chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")
        if chunk_overlap < 0:
            raise ValueError("chunk_overlap must be >= 0")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        self.chunk_size = int(chunk_size)
        self.chunk_overlap = int(chunk_overlap)
        # Length function should use token count, but retained for backward compatibility
        self.length_function = length_function
        self.is_separator_regex = is_separator_regex  # accepted for API parity; not used here
        # Use cl100k_base encoding for tokenization
        self._encoding = tiktoken.get_encoding("cl100k_base")
        # Debug: optional path to write chunks; set via env var or attribute
        self.debug_chunks_file = os.path.join(os.getcwd(), f"test output/chunks_{self.chunk_size}_{self.chunk_overlap}.txt")
        self._suppress_split_text_debug = False  # used by split_documents to avoid duplicate writes
        self.token_too_short : bool = False
        self.prev_content : str = ""

    def _encode(self, text: str) -> List[int]:
        # Encode to tokens
        return self._encoding.encode(text, disallowed_special=())

    def _decode_slice(self, tokens: List[int], start: int, end: int) -> str:
        # Decode a token slice [start:end)
        return self._encoding.decode(tokens[start:end])

    def _snap_start_to_boundary(self, tokens: List[int], start_tok: int, upper_bound_tok: int) -> int:
        """
        Move the start token forward to the next 'safe' boundary so we don't start in the middle of a word.
        A safe boundary is defined as the first non-whitespace character that follows any whitespace in the
        overlap window. If none is found, we keep the original start token.

        Args:
            tokens: Full token list of the text being split.
            start_tok: Proposed next start token (typically split_at_tok - chunk_overlap).
            upper_bound_tok: An upper bound token index to limit forward scan (typically split_at_tok).

        Returns:
            An adjusted start token index that starts at a word boundary when possible.
        """
        try:
            if start_tok <= 0:
                return 0

            # Define small token windows for backward and forward scans
            back_window = max(self.chunk_overlap, 64)
            fwd_window = max(self.chunk_overlap, 64)

            left_tok = max(0, start_tok - back_window)
            right_tok = max(start_tok, min(upper_bound_tok, start_tok + fwd_window))

            left_text = self._decode_slice(tokens, left_tok, start_tok)
            right_text = self._decode_slice(tokens, start_tok, right_tok)

            # If we're already at a boundary (left endswith whitespace or right startswith whitespace),
            # keep the current start
            if (left_text and left_text[-1].isspace()) or (right_text and right_text[0].isspace()) or (not left_text):
                return start_tok

            # Try to snap backward to the beginning of the current word.
            # Find last whitespace in left_text. The boundary is the first char after it.
            back_idx = None
            for i in range(len(left_text) - 1, -1, -1):
                if left_text[i].isspace():
                    back_idx = i + 1
                    break

            if back_idx is not None and back_idx >= 0 and back_idx <= len(left_text):
                # Convert the character offset to tokens relative to left_tok
                delta_tokens = len(self._encode(left_text[:back_idx]))
                adjusted = left_tok + delta_tokens
                if adjusted < start_tok and adjusted < upper_bound_tok:
                    return adjusted

            # If no backward boundary, try forward snapping within the right window.
            if right_text:
                # Look for first occurrence of (<whitespace><non-whitespace>) and snap to the non-space
                m = re.search(r"\s\S", right_text)
                if m:
                    idx = m.start() + 1
                    if 0 < idx < len(right_text):
                        delta_tokens = len(self._encode(right_text[:idx]))
                        adjusted = start_tok + delta_tokens
                        if start_tok < adjusted < upper_bound_tok:
                            return adjusted

            # Fallback: keep original start token
            return start_tok
        except Exception:
            # On any failure, keep the original to avoid data loss
            return start_tok

    def _write_debug_chunks(self, header: str, chunks: List[str]) -> None:
        try:
            path = getattr(self, "debug_chunks_file", None)
            if not path:
                print(f"[splitter-debug] No debug_chunks_file set; skipping debug write.")
                return
            os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
            with open(path, "a", encoding="utf-8") as f:
                f.write("\n" + "="*80 + "\n")
                f.write(f"[{datetime.datetime.now().isoformat(sep=' ', timespec='seconds')}] {header}\n")
                for i, ch in enumerate(chunks, 1):
                    tok_len = len(self._encode(ch))
                    f.write(f"--- Chunk {i} (tokens={tok_len}, chars={len(ch)}) ---\n")
                    f.write(ch.rstrip("\n") + "\n\n")
                f.write("="*80 + "\n")
        except Exception as e:
            print(f"[splitter-debug] Failed to write chunks to file: {e}")

    def split_text(self, prev_text :str, text: str) -> List[str]:
        """
        Splits text into chunks, each up to `self.chunk_size` tokens,
        with `self.chunk_overlap` token overlap.
        """
        text = prev_text + text
        # Clear any previous carry so we don't duplicate it across pages unless we explicitly set it below
        self.prev_content = ""
        all_tokens = self._encode(text)
        n = len(all_tokens)
        print(f"Splitting text of token length {n} with chunk_size {self.chunk_size} and chunk_overlap {self.chunk_overlap}")
        if n <= self.chunk_size:
            self.token_too_short = True
            print(f"Text is shorter than or equal to chunk_size; returning single chunk.")
            return [text] if text.strip() else []
        else:
            self.token_too_short = False
        chunks: List[str] = []
        start_tok = 0

        while start_tok < n:
            print(f"Splitting text from token index {start_tok}")
            print(f"Token length of text = {n}")
            end_tok = min(start_tok + self.chunk_size, n)

            split_at_tok = -1
            window_text = self._decode_slice(all_tokens, start_tok, end_tok)

            for sep in ("\n\n", "\n", " "):
                idx = window_text.rfind(sep)
                print(f"  Trying to split at '{sep}' within decoded window: found at {idx}")
                if idx != -1 and idx > 0:
                    prefix_text = window_text[: idx + len(sep)]
                    prefix_tokens = self._encode(prefix_text)
                    split_at_tok = start_tok + len(prefix_tokens)
                    break

            if split_at_tok == -1:
                split_at_tok = end_tok  # hard cut

            chunk_text = self._decode_slice(all_tokens, start_tok, split_at_tok)
            if chunk_text:
                chunks.append(chunk_text)
                print(f"  Created chunk of token length {len(self._encode(chunk_text))} from token {start_tok} to {split_at_tok}")

            remaining_token_length = n - split_at_tok
            if 0 < remaining_token_length and remaining_token_length < self.chunk_size:
                carry_start = max(0, int(split_at_tok - self.chunk_overlap))
                # Adjust carry start forward to the next word boundary to avoid mid-word starts
                safe_carry_start = self._snap_start_to_boundary(all_tokens, carry_start, split_at_tok)
                self.prev_content = self._decode_slice(all_tokens, safe_carry_start, n)
                print(f"  Too few tokens left; Carry over text.")
                print(f"  Carry text:\n {self.prev_content}\n\n")
                return chunks

            print(f"  Finalizing chunk from token {start_tok} to {split_at_tok} (token length {split_at_tok - start_tok})")
            # Step forward by chunk_size minus overlap, always making forward progress
            next_start_tok = max(int(split_at_tok - self.chunk_overlap), int(start_tok))
            # Snap the next start forward to a "safe" boundary so the next chunk does not begin mid-word
            next_start_tok = self._snap_start_to_boundary(all_tokens, int(next_start_tok), int(split_at_tok))
            # Always advance at least 1 token to prevent infinite loops
            if next_start_tok <= start_tok:
                next_start_tok = start_tok + 1
            start_tok = int(next_start_tok)

        chunks = [c.strip() for c in chunks if c and c.strip()]
        if getattr(self, "debug_chunks_file", None) and not getattr(self, "_suppress_split_text_debug", False):
            try:
                self._write_debug_chunks(header="split_text: chunks", chunks=chunks)
            except Exception as _e:
                print(f"[splitter-debug] {str(_e)}")
        return chunks

    def split_documents(self, docs: Iterable[Document]) -> List[Document]:
        out: List[Document] = []
        all_debug_chunks: List[str] = []
        prev_flag = self._suppress_split_text_debug
        self._suppress_split_text_debug = True
        try:
            self.prev_content = ""
            last_meta = None
            for idx, doc in enumerate(docs, 1):
                content = getattr(doc, "page_content", "") or ""
                base_meta = dict(getattr(doc, "metadata", {}) or {})
                last_meta = base_meta
                pieces = self.split_text(self.prev_content, content)
                if self.token_too_short:
                    # If the combined text (prev + current) is still <= chunk_size, accumulate it
                    if pieces:
                        self.prev_content = (self.prev_content + pieces[0])
                    # else: empty page; nothing to add
                else:
                    # We produced at least one full chunk; emit them
                    for piece in pieces:
                        out.append(Document(page_content=piece, metadata=dict(base_meta)))
                        if getattr(self, "debug_chunks_file", None):
                            all_debug_chunks.append(piece)
                    # 'self.prev_content' may contain a remainder to carry to next page (set inside split_text)
                    # If no remainder was set in split_text, it remains empty due to clearing at the start of split_text

            # After processing all docs, flush any remaining carry so nothing is lost
            if self.prev_content and self.prev_content.strip():
                leftover = self.prev_content.strip()
                out.append(Document(page_content=leftover, metadata=dict(last_meta or {})))
                if getattr(self, "debug_chunks_file", None):
                    all_debug_chunks.append(leftover)

            if getattr(self, "debug_chunks_file", None) and all_debug_chunks:
                self._write_debug_chunks(header=f"split_documents: total_chunks={len(all_debug_chunks)}", chunks=all_debug_chunks)
        finally:
            self._suppress_split_text_debug = prev_flag
        return out
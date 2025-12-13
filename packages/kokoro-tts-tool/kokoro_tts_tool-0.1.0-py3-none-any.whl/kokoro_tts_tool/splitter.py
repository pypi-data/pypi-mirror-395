"""
Text splitter for intelligent markdown chunking.

Uses LangChain's RecursiveCharacterTextSplitter to split text while
respecting document structure (headers, paragraphs, sentences) and
maintaining semantic coherence.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import re
from dataclasses import dataclass

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from kokoro_tts_tool.logging_config import get_logger

logger = get_logger(__name__)

# Default chunking configuration
# Note: Kokoro has a 510 phoneme limit, so we use smaller chunks
# 200 words is safer for technical text with complex terminology
DEFAULT_CHUNK_SIZE_WORDS = 200  # ~1 minute listen at normal speed
DEFAULT_CHUNK_OVERLAP_WORDS = 20


@dataclass
class TextChunk:
    """A chunk of text with optional metadata about its source."""

    content: str
    chapter: str | None = None
    section: str | None = None
    topic: str | None = None
    index: int = 0


def clean_text_for_tts(text: str) -> str:
    """Remove markdown formatting that sounds bad in TTS.

    Converts markdown symbols to clean text:
    - **Bold** -> Bold
    - ## Header -> Header.
    - [link text](url) -> link text
    - - list item -> list item

    Args:
        text: Raw markdown text

    Returns:
        Cleaned text suitable for TTS
    """
    # Remove bold/italic markers (* or **)
    text = re.sub(r"\*+(.*?)\*+", r"\1", text)

    # Remove header hashes but keep text, add period for pause
    text = re.sub(r"^#+\s+(.*)", r"\1.", text, flags=re.MULTILINE)

    # Remove links [text](url) -> keep only text
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)

    # Remove list dashes at start of line
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.MULTILINE)

    # Remove code blocks (backticks)
    text = re.sub(r"`{1,3}[^`]*`{1,3}", "", text)

    # Collapse multiple whitespace/newlines into single space
    text = re.sub(r"\s+", " ", text).strip()

    return text


def split_text(
    text: str,
    chunk_size_words: int = DEFAULT_CHUNK_SIZE_WORDS,
    chunk_overlap_words: int = DEFAULT_CHUNK_OVERLAP_WORDS,
    use_markdown_headers: bool = True,
) -> list[TextChunk]:
    """Split text into chunks respecting structure and length.

    For markdown text, splits by headers first, then by paragraphs.
    For plain text, splits by paragraphs and sentences.

    Args:
        text: Input text (markdown or plain)
        chunk_size_words: Target words per chunk (~350 = 2 min)
        chunk_overlap_words: Words of context overlap between chunks
        use_markdown_headers: Whether to split by markdown headers first

    Returns:
        List of TextChunk objects
    """
    logger.debug(f"Splitting text: {len(text)} chars, chunk_size={chunk_size_words}")

    chunks: list[TextChunk] = []

    if use_markdown_headers and _has_markdown_headers(text):
        logger.debug("Detected markdown headers, using two-stage split")
        chunks = _split_markdown(text, chunk_size_words, chunk_overlap_words)
    else:
        logger.debug("Using simple paragraph split")
        chunks = _split_plain(text, chunk_size_words, chunk_overlap_words)

    # Clean all chunks for TTS
    cleaned_chunks = []
    for i, chunk in enumerate(chunks):
        cleaned_content = clean_text_for_tts(chunk.content)
        if cleaned_content.strip():
            cleaned_chunks.append(
                TextChunk(
                    content=cleaned_content,
                    chapter=chunk.chapter,
                    section=chunk.section,
                    topic=chunk.topic,
                    index=i,
                )
            )

    logger.info(f"Split into {len(cleaned_chunks)} chunks")
    return cleaned_chunks


def _has_markdown_headers(text: str) -> bool:
    """Check if text contains markdown headers."""
    return bool(re.search(r"^#{1,6}\s+", text, re.MULTILINE))


def _split_markdown(
    text: str,
    chunk_size_words: int,
    chunk_overlap_words: int,
) -> list[TextChunk]:
    """Split markdown text by headers, then by length."""
    # Define headers to split on
    headers_to_split_on = [
        ("#", "Chapter"),
        ("##", "Section"),
        ("###", "Topic"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False,  # Keep headers in content for context
    )

    header_splits = markdown_splitter.split_text(text)
    logger.debug(f"Split into {len(header_splits)} header sections")

    # Now split each section by word count
    word_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size_words,
        chunk_overlap=chunk_overlap_words,
        length_function=lambda x: len(x.split()),
        separators=["\n\n", "\n", ". ", " "],
    )

    final_splits = word_splitter.split_documents(header_splits)

    chunks = []
    for i, doc in enumerate(final_splits):
        chunks.append(
            TextChunk(
                content=doc.page_content,
                chapter=doc.metadata.get("Chapter"),
                section=doc.metadata.get("Section"),
                topic=doc.metadata.get("Topic"),
                index=i,
            )
        )

    return chunks


def _split_plain(
    text: str,
    chunk_size_words: int,
    chunk_overlap_words: int,
) -> list[TextChunk]:
    """Split plain text by paragraphs and sentences."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size_words,
        chunk_overlap=chunk_overlap_words,
        length_function=lambda x: len(x.split()),
        separators=["\n\n", "\n", ". ", " "],
    )

    splits = splitter.split_text(text)

    return [TextChunk(content=s, index=i) for i, s in enumerate(splits)]

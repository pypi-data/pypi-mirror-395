"""
Tests for the text splitter module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from kokoro_tts_tool.splitter import (
    TextChunk,
    clean_text_for_tts,
    split_text,
)


class TestCleanTextForTts:
    """Tests for clean_text_for_tts function."""

    def test_removes_bold_markers(self) -> None:
        """Bold text markers should be removed."""
        assert clean_text_for_tts("This is **bold** text") == "This is bold text"
        assert clean_text_for_tts("This is *italic* text") == "This is italic text"

    def test_removes_header_hashes(self) -> None:
        """Header hashes should be removed and period added."""
        assert clean_text_for_tts("# Chapter One") == "Chapter One."
        assert clean_text_for_tts("## Section Title") == "Section Title."
        assert clean_text_for_tts("### Subsection") == "Subsection."

    def test_removes_links(self) -> None:
        """Links should be replaced with just the link text."""
        result = clean_text_for_tts("Check [this link](https://example.com) out")
        assert result == "Check this link out"

    def test_removes_list_dashes(self) -> None:
        """List dashes should be removed."""
        text = "- Item one\n- Item two"
        result = clean_text_for_tts(text)
        assert "-" not in result
        assert "Item one" in result
        assert "Item two" in result

    def test_removes_code_blocks(self) -> None:
        """Code blocks should be removed."""
        assert clean_text_for_tts("Run `command` here") == "Run here"
        assert clean_text_for_tts("Code: ```python\nprint()```") == "Code:"

    def test_collapses_whitespace(self) -> None:
        """Multiple whitespace should be collapsed."""
        assert clean_text_for_tts("Too   many    spaces") == "Too many spaces"
        assert clean_text_for_tts("Line\n\nbreaks") == "Line breaks"

    def test_empty_string(self) -> None:
        """Empty string should return empty."""
        assert clean_text_for_tts("") == ""

    def test_plain_text_unchanged(self) -> None:
        """Plain text without markdown should be minimally changed."""
        text = "This is plain text."
        assert clean_text_for_tts(text) == text


class TestSplitText:
    """Tests for split_text function."""

    def test_returns_text_chunks(self) -> None:
        """Should return list of TextChunk objects."""
        text = "This is a test paragraph."
        chunks = split_text(text, chunk_size_words=100)
        assert len(chunks) > 0
        assert all(isinstance(c, TextChunk) for c in chunks)

    def test_respects_chunk_size(self) -> None:
        """Chunks should respect approximate word limit."""
        # Create long text
        text = " ".join(["word"] * 500)
        chunks = split_text(text, chunk_size_words=100)

        # Each chunk should be around the limit (with some flexibility)
        for chunk in chunks:
            word_count = len(chunk.content.split())
            assert word_count <= 150  # Allow some overflow due to splitting logic

    def test_splits_by_markdown_headers(self) -> None:
        """Should split at markdown headers when present."""
        text = """# Chapter 1

This is chapter one content.

# Chapter 2

This is chapter two content."""

        chunks = split_text(text, chunk_size_words=500, use_markdown_headers=True)
        # Should create at least 2 chunks (one per chapter)
        assert len(chunks) >= 2

    def test_plain_text_mode(self) -> None:
        """Should handle plain text without markdown."""
        text = "First paragraph.\n\nSecond paragraph."
        chunks = split_text(text, chunk_size_words=100, use_markdown_headers=False)
        assert len(chunks) >= 1

    def test_cleans_markdown_in_output(self) -> None:
        """Output chunks should have markdown cleaned."""
        text = "# Title\n\nThis is **bold** text."
        chunks = split_text(text)

        for chunk in chunks:
            assert "**" not in chunk.content
            assert "#" not in chunk.content

    def test_empty_input(self) -> None:
        """Empty input should return empty list."""
        chunks = split_text("")
        assert chunks == []

    def test_whitespace_only(self) -> None:
        """Whitespace-only input should return empty list."""
        chunks = split_text("   \n\n   ")
        assert chunks == []

    def test_chunk_index_increments(self) -> None:
        """Chunk indices should increment correctly."""
        text = "First. " * 100 + "\n\n" + "Second. " * 100
        chunks = split_text(text, chunk_size_words=50)

        for i, chunk in enumerate(chunks):
            assert chunk.index == i


class TestTextChunk:
    """Tests for TextChunk dataclass."""

    def test_default_values(self) -> None:
        """Default values should be set correctly."""
        chunk = TextChunk(content="test")
        assert chunk.content == "test"
        assert chunk.chapter is None
        assert chunk.section is None
        assert chunk.topic is None
        assert chunk.index == 0

    def test_with_metadata(self) -> None:
        """Should store metadata correctly."""
        chunk = TextChunk(
            content="test",
            chapter="Chapter 1",
            section="Introduction",
            topic="Overview",
            index=5,
        )
        assert chunk.chapter == "Chapter 1"
        assert chunk.section == "Introduction"
        assert chunk.topic == "Overview"
        assert chunk.index == 5

"""Tests for the markdown parser."""

import tempfile
import unittest
from pathlib import Path

from markdeck.parser import Slide, SlideParser


class TestSlide(unittest.TestCase):
    """Test the Slide class."""

    def test_slide_creation(self):
        """Test basic slide creation."""
        content = "# Test Slide\n\nThis is content."
        slide = Slide(content, 0)

        self.assertEqual(slide.content, content)
        self.assertEqual(slide.index, 0)
        self.assertEqual(slide.notes, "")

    def test_slide_with_notes(self):
        """Test slide with speaker notes."""
        content = """# Test Slide

Content here

<!--NOTES:
These are notes
-->"""
        slide = Slide(content, 0)

        self.assertNotIn("NOTES", slide.content)
        self.assertEqual(slide.notes, "These are notes")

    def test_slide_to_dict(self):
        """Test converting slide to dictionary."""
        slide = Slide("# Test", 0)
        result = slide.to_dict()

        self.assertEqual(result["id"], 0)
        self.assertEqual(result["content"], "# Test")
        self.assertIn("notes", result)

    def test_empty_slide(self):
        """Test handling of empty slide."""
        slide = Slide("   \n\n   ", 0)
        self.assertEqual(slide.content, "")


class TestSlideParser(unittest.TestCase):
    """Test the SlideParser class."""

    def test_parse_content_single_slide(self):
        """Test parsing content with a single slide."""
        content = "# Single Slide\n\nContent here."
        slides = SlideParser.parse_content(content)

        self.assertEqual(len(slides), 1)
        self.assertEqual(slides[0].content, content)

    def test_parse_content_multiple_slides(self):
        """Test parsing content with multiple slides."""
        content = """# Slide 1

Content 1

---

# Slide 2

Content 2

---

# Slide 3

Content 3"""
        slides = SlideParser.parse_content(content)

        self.assertEqual(len(slides), 3)
        self.assertIn("# Slide 1", slides[0].content)
        self.assertIn("# Slide 2", slides[1].content)
        self.assertIn("# Slide 3", slides[2].content)

    def test_parse_content_with_empty_slides(self):
        """Test parsing content with empty slides filtered out."""
        content = """# Slide 1

---

---

# Slide 2"""
        slides = SlideParser.parse_content(content)

        # Empty slides should be filtered out
        self.assertTrue(all(slide.content for slide in slides))

    def test_parse_content_edge_cases(self):
        """Test edge cases in parsing."""
        # Delimiter at start
        content = "---\n# Slide 1"
        slides = SlideParser.parse_content(content)
        self.assertGreaterEqual(len(slides), 1)

        # Delimiter at end
        content = "# Slide 1\n---"
        slides = SlideParser.parse_content(content)
        self.assertGreaterEqual(len(slides), 1)

    def test_get_title_from_h1(self):
        """Test extracting title from first H1."""
        content = "# My Presentation\n\nContent\n---\n# Slide 2"
        slides = SlideParser.parse_content(content)
        parser = SlideParser.__new__(SlideParser)
        parser.file_path = Path("test.md")

        # Mock parse method
        def mock_parse():
            return slides
        parser.parse = mock_parse

        title = parser.get_title()
        self.assertEqual(title, "My Presentation")

    def test_to_json(self):
        """Test converting parser output to JSON format."""
        content = "# Slide 1\n---\n# Slide 2"
        parser = SlideParser.__new__(SlideParser)
        parser.file_path = Path("test.md")

        slides = SlideParser.parse_content(content)

        def mock_parse():
            return slides
        parser.parse = mock_parse

        result = parser.to_json()

        self.assertIn("slides", result)
        self.assertIn("total", result)
        self.assertIn("title", result)
        self.assertEqual(result["total"], 2)
        self.assertEqual(len(result["slides"]), 2)


class TestSlideParserWithFiles(unittest.TestCase):
    """Test SlideParser with actual files."""

    def test_file_not_found(self):
        """Test handling of missing file."""
        with self.assertRaises(FileNotFoundError):
            SlideParser("nonexistent.md")

    def test_parse_real_file(self):
        """Test parsing a real markdown file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "test.md"
            content = """# Test Presentation

Intro slide

---

# Second Slide

Content here

<!--NOTES:
Speaker notes for testing
-->

---

# Final Slide

Conclusion"""
            test_file.write_text(content, encoding="utf-8")

            parser = SlideParser(test_file)
            slides = parser.parse()

            self.assertEqual(len(slides), 3)
            self.assertEqual(slides[0].index, 0)
            self.assertEqual(slides[1].notes, "Speaker notes for testing")
            self.assertEqual(slides[2].index, 2)

    def test_get_title_fallback_to_filename(self):
        """Test title fallback to filename when no H1 present."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "my-presentation.md"
            test_file.write_text("Content without H1", encoding="utf-8")

            parser = SlideParser(test_file)
            title = parser.get_title()

            self.assertEqual(title, "my-presentation")


if __name__ == "__main__":
    unittest.main()

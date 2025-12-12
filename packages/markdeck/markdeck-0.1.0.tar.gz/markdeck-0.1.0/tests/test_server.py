"""Tests for the FastAPI server."""

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from markdeck.server import app, set_presentation_file


class TestHealthEndpoint(unittest.TestCase):
    """Test the health check endpoint."""

    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)

    def test_health_check(self):
        """Test health endpoint returns OK."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


class TestSlidesEndpoint(unittest.TestCase):
    """Test the slides API endpoint."""

    def setUp(self):
        """Set up test client and sample file."""
        self.client = TestClient(app)
        self.temp_dir = tempfile.TemporaryDirectory()
        self.sample_file = Path(self.temp_dir.name) / "test.md"
        content = """# Test Presentation

First slide

---

# Second Slide

Second slide content

<!--NOTES:
Test notes
-->

---

# Third Slide

Final slide"""
        self.sample_file.write_text(content, encoding="utf-8")

    def tearDown(self):
        """Clean up temporary files."""
        self.temp_dir.cleanup()

    def test_get_slides_no_file(self):
        """Test getting slides without setting a file."""
        set_presentation_file(None)
        response = self.client.get("/api/slides")
        self.assertEqual(response.status_code, 400)

    def test_get_slides_with_current_file(self):
        """Test getting slides with current file set."""
        set_presentation_file(self.sample_file)
        response = self.client.get("/api/slides")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn("slides", data)
        self.assertIn("total", data)
        self.assertIn("title", data)
        self.assertEqual(data["total"], 3)
        self.assertEqual(len(data["slides"]), 3)

    def test_get_slides_with_query_param(self):
        """Test getting slides with file query parameter."""
        response = self.client.get(f"/api/slides?file={self.sample_file}")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total"], 3)

    def test_get_slides_file_not_found(self):
        """Test getting slides with non-existent file."""
        response = self.client.get("/api/slides?file=/nonexistent/file.md")
        self.assertEqual(response.status_code, 404)

    def test_slide_structure(self):
        """Test the structure of returned slides."""
        set_presentation_file(self.sample_file)
        response = self.client.get("/api/slides")
        data = response.json()

        slide = data["slides"][0]
        self.assertIn("id", slide)
        self.assertIn("content", slide)
        self.assertIn("notes", slide)
        self.assertEqual(slide["id"], 0)

    def test_speaker_notes_extraction(self):
        """Test that speaker notes are properly extracted."""
        set_presentation_file(self.sample_file)
        response = self.client.get("/api/slides")
        data = response.json()

        # Second slide has notes
        slide_with_notes = data["slides"][1]
        self.assertEqual(slide_with_notes["notes"], "Test notes")
        self.assertNotIn("NOTES", slide_with_notes["content"])


class TestRootEndpoint(unittest.TestCase):
    """Test the root HTML endpoint."""

    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)

    def test_root_returns_html(self):
        """Test that root endpoint returns HTML."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        self.assertIn("MarkDeck", response.text)


class TestStaticFiles(unittest.TestCase):
    """Test static file serving."""

    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)

    def test_css_file_served(self):
        """Test that CSS file is served."""
        response = self.client.get("/static/style.css")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/css", response.headers["content-type"])

    def test_js_file_served(self):
        """Test that JavaScript file is served."""
        response = self.client.get("/static/slides.js")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()

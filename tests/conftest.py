"""Shared pytest fixtures and configuration."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_markdown_content():
    """Sample markdown content for testing."""
    return """# Recognition: Detection

## Main Conference

| Title | Links | Paper | Video |
|-------|-------|-------|-------|
| [Sample Paper Title](https://example.com/paper) | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/user/repo) | [![thecvf](https://img.shields.io/badge/pdf-thecvf-green)](https://example.com/paper.pdf) | [![YouTube](https://img.shields.io/badge/YouTube-Video-red)](https://youtube.com/watch?v=123) |
"""


@pytest.fixture
def sample_json_data():
    """Sample JSON data structure for testing."""
    return [
        {
            "title": "Sample Paper Title",
            "base_url": "https://example.com",
            "title_page": "/paper",
            "ieee_id": None,
            "github": "user/repo",
            "web_page": None,
            "github_page": None,
            "colab": None,
            "modelscope": None,
            "gitee": None,
            "gitlab": None,
            "zenodo": None,
            "kaggle": None,
            "demo_page": None,
            "paper_thecvf": "/paper.pdf",
            "paper_arxiv_id": None,
            "paper_pdf": None,
            "paper_hal_science": None,
            "paper_researchgate": None,
            "paper_amazon": None,
            "youtube_id": "123",
            "drive_google": None,
            "dropbox": None,
            "onedrive": None,
            "loom": None,
            "section": "Recognition: Detection"
        }
    ]


@pytest.fixture
def mock_config(monkeypatch):
    """Mock configuration values for testing."""
    monkeypatch.setenv("GITHUB_REPOSITORY", "test-owner/test-repo")
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    monkeypatch.setenv("GITHUB_WORKSPACE", "/test/workspace")
    
    class MockConfig:
        GITHUB_TOKEN = "test-token"
        GITHUB_WORKSPACE = "/test/workspace"
        MARKDOWN_DIRECTORY = "sections"
        OUTPUT_DIRECTORY = "json_data"
        MARKDOWN_DIRECTORY_LOCAL = Path("./sections").resolve()
        OUTPUT_DIRECTORY_LOCAL = Path("./local_json_data").resolve()
        REPO_OWNER = "test-owner"
        REPO_NAME = "test-repo"
        COMMIT_MESSAGE = "Update files"
    
    return MockConfig


@pytest.fixture
def mock_github_repo():
    """Mock GitHub repository for testing."""
    mock_repo = Mock()
    mock_repo.default_branch = "main"
    mock_repo.get_branch.return_value.commit.sha = "abc123"
    mock_repo.get_git_commit.return_value.tree.sha = "tree123"
    mock_repo.create_git_tree.return_value.sha = "newtree123"
    mock_repo.create_git_commit.return_value.sha = "newcommit123"
    return mock_repo


@pytest.fixture
def sample_html_content():
    """Sample HTML content for testing BeautifulSoup parsing."""
    return """
    <h2>Recognition: Detection</h2>
    <table>
        <tr>
            <th>Title</th>
            <th>Links</th>
            <th>Paper</th>
            <th>Video</th>
        </tr>
        <tr>
            <td><a href="/paper">Sample Paper Title</a></td>
            <td>
                <a href="https://github.com/user/repo">
                    <img alt="GitHub" src="github.png">
                </a>
            </td>
            <td>
                <a href="/paper.pdf">
                    <img alt="thecvf" src="pdf.png">
                </a>
            </td>
            <td>
                <a href="https://youtube.com/watch?v=123">
                    <img alt="Video" src="video.png">
                </a>
            </td>
        </tr>
    </table>
    """


@pytest.fixture
def create_test_file(temp_dir):
    """Factory fixture to create test files."""
    def _create_file(filename, content):
        file_path = temp_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return file_path
    return _create_file


@pytest.fixture
def mock_beautiful_soup(monkeypatch):
    """Mock BeautifulSoup for testing without actual HTML parsing."""
    def mock_init(self, *args, **kwargs):
        pass
    
    monkeypatch.setattr("bs4.BeautifulSoup.__init__", mock_init)


@pytest.fixture
def capture_logs(caplog):
    """Capture log messages during tests."""
    with caplog.at_level("INFO"):
        yield caplog
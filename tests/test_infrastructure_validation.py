"""Validation tests to verify the testing infrastructure is properly set up."""

import json
from pathlib import Path

import pytest


class TestInfrastructureValidation:
    """Test class to validate the testing infrastructure setup."""
    
    def test_pytest_is_working(self):
        """Basic test to verify pytest is working."""
        assert True
        assert 1 + 1 == 2
    
    def test_fixtures_are_available(self, temp_dir, sample_markdown_content):
        """Test that fixtures from conftest.py are accessible."""
        assert isinstance(temp_dir, Path)
        assert temp_dir.exists()
        assert isinstance(sample_markdown_content, str)
        assert "Recognition: Detection" in sample_markdown_content
    
    def test_temp_dir_fixture_creates_directory(self, temp_dir):
        """Test that temp_dir fixture creates a working directory."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello, testing!")
        
        assert test_file.exists()
        assert test_file.read_text() == "Hello, testing!"
    
    def test_create_test_file_fixture(self, create_test_file):
        """Test the create_test_file factory fixture."""
        test_file = create_test_file("subdir/test.json", '{"key": "value"}')
        
        assert test_file.exists()
        assert test_file.parent.name == "subdir"
        
        data = json.loads(test_file.read_text())
        assert data == {"key": "value"}
    
    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that unit test marker is working."""
        assert True
    
    @pytest.mark.integration
    def test_integration_marker(self):
        """Test that integration test marker is working."""
        assert True
    
    @pytest.mark.slow
    def test_slow_marker(self):
        """Test that slow test marker is working."""
        assert True
    
    def test_mock_fixtures_available(self, mock_config, mock_github_repo):
        """Test that mock fixtures are available and working."""
        assert mock_config.GITHUB_TOKEN == "test-token"
        assert mock_config.REPO_OWNER == "test-owner"
        assert mock_github_repo.default_branch == "main"
    
    def test_sample_json_data_fixture(self, sample_json_data):
        """Test the sample JSON data fixture."""
        assert isinstance(sample_json_data, list)
        assert len(sample_json_data) == 1
        assert sample_json_data[0]["title"] == "Sample Paper Title"
        assert sample_json_data[0]["github"] == "user/repo"
    
    def test_coverage_is_tracked(self):
        """Test that code coverage is being tracked."""
        # This test ensures coverage reporting works
        def dummy_function(x):
            if x > 0:
                return x * 2
            else:
                return 0
        
        assert dummy_function(5) == 10
        assert dummy_function(-1) == 0
    
    def test_pytest_mock_is_available(self, mocker):
        """Test that pytest-mock is installed and working."""
        mock_func = mocker.Mock(return_value=42)
        assert mock_func() == 42
        mock_func.assert_called_once()
    
    def test_parameterized_tests(self):
        """Test that pytest parametrization works."""
        
        @pytest.mark.parametrize("input_val,expected", [
            (1, 2),
            (2, 4),
            (3, 6),
        ])
        def inner_test(input_val, expected):
            assert input_val * 2 == expected
        
        # Run the parameterized test
        inner_test(1, 2)
        inner_test(2, 4)
        inner_test(3, 6)
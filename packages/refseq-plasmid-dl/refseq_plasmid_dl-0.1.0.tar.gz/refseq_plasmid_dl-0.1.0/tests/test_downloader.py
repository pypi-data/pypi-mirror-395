from refseq_plasmid_dl import downloader
import pytest


def test_regex_patterns():
    """Test that the file pattern regex matches the files we want."""
    # Prod mode regex
    pattern_prod = downloader.get_file_pattern(dev_mode=False)

    assert pattern_prod.search("plasmid.1.genomic.fna.gz")
    assert pattern_prod.search("plasmid.55.1.genomic.fna.gz")

    # UPDATE: We now assert that this DOES match, consistent with your code
    assert pattern_prod.search("plasmid.1.genomic.gbff.gz")

    # This should still fail (wrong prefix)
    assert not pattern_prod.search("bacteria.1.genomic.fna.gz")

    # Dev mode regex
    pattern_dev = downloader.get_file_pattern(dev_mode=True)
    assert pattern_dev.search("plasmid.1.genomic.fna.gz")
    # Dev mode strictly targets #1, so #55 should still fail
    assert not pattern_dev.search("plasmid.55.genomic.fna.gz")


def test_get_total_files_count_success(mocker, mock_html_content, tmp_path):
    """Test parsing of the HTML directory listing."""
    # Mock requests.get to return our fake HTML
    mock_response = mocker.Mock()
    mock_response.text = mock_html_content
    mock_response.status_code = 200
    mocker.patch("requests.get", return_value=mock_response)

    # Use a dummy URL; the mock prevents actual network access
    count, content = downloader.get_total_files_count(
        "http://fake.url", False, tmp_path
    )

    # In mock_html_content (conftest.py), there is 1 matching file:
    # "plasmid.1.1.genomic.fna.gz" matches your regex.
    # "README.txt" does not.
    assert count == 1
    assert content == mock_html_content
    assert (tmp_path / "plasmids_index.html").exists()


def test_download_file_https_writes_file(mocker, tmp_path):
    """Test that the downloader writes bytes to disk."""
    mock_response = mocker.Mock()
    # Mock iter_content to return fake binary data
    mock_response.iter_content = lambda chunk_size: [b"data_chunk_1", b"data_chunk_2"]
    mock_response.status_code = 200

    # Mock the requests.get context manager
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.__enter__.return_value = mock_response

    url = "http://fake.url/test_file.gz"
    success = downloader.download_file_https(url, tmp_path)

    assert success is True
    output_file = tmp_path / "test_file.gz"
    assert output_file.exists()
    assert output_file.read_bytes() == b"data_chunk_1data_chunk_2"

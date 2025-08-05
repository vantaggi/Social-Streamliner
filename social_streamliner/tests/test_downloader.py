import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import requests

# Aggiungi la directory principale al percorso di sistema
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from downloader import download_video

class TestDownloader(unittest.TestCase):

    @patch('downloader.os.makedirs')
    @patch('downloader.requests.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_video_success(self, mock_file_open, mock_requests_get, mock_makedirs):
        """Testa il download di un video con successo."""
        # Configura il mock per requests.get
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b'chunk1', b'chunk2']
        mock_requests_get.return_value = mock_response

        video_url = "http://example.com/video.mp4"
        destination = "test_videos"

        # Esegui la funzione
        result_path = download_video(video_url, destination_folder=destination)

        # Asserzioni
        mock_makedirs.assert_called_once_with(destination, exist_ok=True)
        mock_requests_get.assert_called_once_with(video_url, stream=True, timeout=60)

        # Verifica che il file sia stato aperto in modalità scrittura binaria ('wb')
        # e che il percorso del file sia corretto
        self.assertTrue(result_path.startswith(os.path.join(destination, '')))
        self.assertTrue(result_path.endswith('.mp4'))
        mock_file_open.assert_called_once_with(result_path, 'wb')

        # Verifica che i chunk siano stati scritti sul file
        handle = mock_file_open()
        handle.write.assert_any_call(b'chunk1')
        handle.write.assert_any_call(b'chunk2')

    @patch('downloader.requests.get')
    def test_download_video_request_error(self, mock_requests_get):
        """Testa il fallimento del download a causa di un errore di rete."""
        # Configura il mock per sollevare un'eccezione
        from requests.exceptions import RequestException
        mock_requests_get.side_effect = RequestException("Network Error")

        video_url = "http://example.com/nonexistent.mp4"

        # Esegui la funzione e verifica che restituisca None
        result_path = download_video(video_url)

        self.assertIsNone(result_path)

    @patch('downloader.os.makedirs')
    @patch('downloader.requests.get')
    def test_download_video_http_error(self, mock_requests_get, mock_makedirs):
        """Testa il fallimento del download a causa di un errore HTTP (es. 404)."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_requests_get.return_value = mock_response

        video_url = "http://example.com/404video.mp4"

        result_path = download_video(video_url)

        self.assertIsNone(result_path)


if __name__ == '__main__':
    # Aggiungiamo 'requests' al namespace del test per l'errore HTTP
    import requests
    unittest.main()

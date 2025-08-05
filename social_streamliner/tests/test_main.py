import unittest
from unittest.mock import patch, MagicMock
import json
import os

# Aggiungi la directory principale al percorso di sistema
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa l'app Flask da testare
from main import app

class TestMainApp(unittest.TestCase):

    def setUp(self):
        """Configura il client di test per ogni test."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    # --- Test per l'endpoint /webhook ---

    @patch('main.send_to_telegram', new_callable=unittest.mock.AsyncMock)
    @patch('main.save_to_id_store')
    def test_webhook_success(self, mock_save, mock_send):
        """Testa il successo dell'endpoint /webhook."""
        # Configura i mock per restituire successo
        mock_save.return_value = True
        mock_send.return_value = True

        response = self.client.post('/webhook',
                                    data=json.dumps({'videoUrl': 'http://test.com/vid.mp4'}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        mock_save.assert_called_once()
        mock_send.assert_called_once()

    def test_webhook_bad_request_no_json(self):
        """Testa un errore 400 se il corpo non è JSON."""
        response = self.client.post('/webhook', data='not json')
        self.assertEqual(response.status_code, 400)

    def test_webhook_bad_request_missing_url(self):
        """Testa un errore 400 se manca 'videoUrl'."""
        response = self.client.post('/webhook',
                                    data=json.dumps({'otherKey': 'value'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    @patch('main.save_to_id_store', return_value=False)
    def test_webhook_sheets_failure(self, mock_save):
        """Testa un errore 500 se il salvataggio su Sheets fallisce."""
        response = self.client.post('/webhook',
                                    data=json.dumps({'videoUrl': 'http://test.com/vid.mp4'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)

    # --- Test per l'endpoint /telegram_callback ---

    @patch('main.send_confirmation_message', new_callable=unittest.mock.AsyncMock)
    @patch('main.add_to_content_calendar')
    @patch('main.generate_content')
    @patch('main.get_video_url_by_clip_id')
    def test_callback_approve_success(self, mock_get_url, mock_gen, mock_add, mock_send_confirm):
        """Testa il flusso di approvazione con successo."""
        mock_get_url.return_value = "http://retrieved.url"
        mock_gen.return_value = {"title": "AI Title", "description": "AI Desc", "hashtags": ["#ai"]}
        mock_add.return_value = True
        mock_send_confirm.return_value = True

        callback_data = {
            "callback_query": {
                "data": "approve:clip123",
                "message": {"chat": {"id": "chat456"}}
            }
        }
        response = self.client.post('/telegram_callback',
                                    data=json.dumps(callback_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        mock_get_url.assert_called_once_with("clip123")
        mock_gen.assert_called_once()
        mock_add.assert_called_once()
        mock_send_confirm.assert_called_once_with("chat456", "✅ Clip approvata e aggiunta al calendario!")

    @patch('main.send_confirmation_message', new_callable=unittest.mock.AsyncMock)
    def test_callback_reject(self, mock_send_confirm):
        """Testa il flusso di rifiuto."""
        callback_data = {
            "callback_query": {
                "data": "reject:clip123",
                "message": {"chat": {"id": "chat456"}}
            }
        }
        response = self.client.post('/telegram_callback',
                                    data=json.dumps(callback_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        mock_send_confirm.assert_called_once_with("chat456", "❌ Clip clip123 rifiutata. Non verrà pubblicata.")

    @patch('main.send_confirmation_message', new_callable=unittest.mock.AsyncMock)
    @patch('main.get_video_url_by_clip_id', return_value=None)
    def test_callback_approve_url_not_found(self, mock_get_url, mock_send_confirm):
        """Testa il fallimento se l'URL non viene trovato."""
        callback_data = {
            "callback_query": {
                "data": "approve:clip123",
                "message": {"chat": {"id": "chat456"}}
            }
        }
        response = self.client.post('/telegram_callback',
                                    data=json.dumps(callback_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 404)
        mock_send_confirm.assert_called_once()


if __name__ == '__main__':
    unittest.main()

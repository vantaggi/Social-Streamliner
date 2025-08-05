import unittest
from unittest.mock import patch, MagicMock
import os

# Aggiungi la directory principale al percorso di sistema per permettere l'importazione dei moduli
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sheets_handler import (
    save_to_id_store,
    get_video_url_by_clip_id,
    add_to_content_calendar,
    get_next_scheduled_post,
    update_post_status
)

class TestSheetsHandler(unittest.TestCase):

    @patch('sheets_handler.get_spreadsheet')
    def test_save_to_id_store_success(self, mock_get_spreadsheet):
        """Testa il salvataggio su ID_Store con successo."""
        mock_worksheet = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_spreadsheet.worksheet.return_value = mock_worksheet
        mock_get_spreadsheet.return_value = mock_spreadsheet

        # Ora passiamo tutti i parametri richiesti
        result = save_to_id_store("test_id", "http://video.url", "TestGame", "Some details")

        self.assertTrue(result)
        mock_spreadsheet.worksheet.assert_called_once_with("ID_Store")
        mock_worksheet.append_row.assert_called_once()
        # Verifica che i dati corretti siano stati passati
        appended_row = mock_worksheet.append_row.call_args[0][0]
        self.assertEqual(appended_row[0], "test_id")
        self.assertEqual(appended_row[1], "http://video.url")
        self.assertEqual(appended_row[3], "TestGame")
        self.assertEqual(appended_row[4], "Some details")

    @patch('sheets_handler.get_spreadsheet')
    def test_get_video_url_by_clip_id_found(self, mock_get_spreadsheet):
        """Testa il recupero dei dati di una clip quando il clip_id viene trovato."""
        mock_cell = MagicMock()
        mock_cell.row = 1

        # Simula i dati restituiti per l'intera riga
        mock_row_values = ["found_id", "http://found.url", "2025-01-01", "FoundGame", "FoundDetails"]
        mock_worksheet = MagicMock()
        mock_worksheet.find.return_value = mock_cell
        mock_worksheet.row_values.return_value = mock_row_values

        mock_spreadsheet = MagicMock()
        mock_spreadsheet.worksheet.return_value = mock_worksheet
        mock_get_spreadsheet.return_value = mock_spreadsheet

        # La funzione ora restituisce un dizionario
        clip_data = get_video_url_by_clip_id("found_id")

        # Verifica che il dizionario restituito sia corretto
        expected_data = {
            "video_url": "http://found.url",
            "game_name": "FoundGame",
            "clip_details": "FoundDetails"
        }
        self.assertEqual(clip_data, expected_data)
        mock_worksheet.find.assert_called_once_with("found_id")
        mock_worksheet.row_values.assert_called_once_with(1)

    @patch('sheets_handler.get_spreadsheet')
    def test_get_video_url_by_clip_id_not_found(self, mock_get_spreadsheet):
        """Testa il recupero di un URL quando il clip_id non viene trovato."""
        mock_worksheet = MagicMock()
        mock_worksheet.find.return_value = None

        mock_spreadsheet = MagicMock()
        mock_spreadsheet.worksheet.return_value = mock_worksheet
        mock_get_spreadsheet.return_value = mock_spreadsheet

        url = get_video_url_by_clip_id("not_found_id")

        self.assertIsNone(url)

    @patch('sheets_handler.get_spreadsheet')
    def test_add_to_content_calendar_success(self, mock_get_spreadsheet):
        """Testa l'aggiunta al Content_Calendar con successo."""
        mock_worksheet = MagicMock()
        mock_worksheet.get_all_records.return_value = [] # Simula un foglio vuoto

        mock_spreadsheet = MagicMock()
        mock_spreadsheet.worksheet.return_value = mock_worksheet
        mock_get_spreadsheet.return_value = mock_spreadsheet

        result = add_to_content_calendar("http://video.url", "title", "desc", ["#tag"])

        self.assertTrue(result)
        mock_worksheet.append_row.assert_called_once()
        appended_row = mock_worksheet.append_row.call_args[0][0]
        self.assertEqual(appended_row[0], 1) # post_id
        self.assertEqual(appended_row[4], "#tag") # hashtags
        self.assertEqual(appended_row[5], "scheduled") # status

    @patch('sheets_handler.get_spreadsheet')
    def test_get_next_scheduled_post_found(self, mock_get_spreadsheet):
        """Testa la ricerca di un post schedulato quando esiste."""
        mock_posts = [
            {'post_id': 1, 'status': 'posted'},
            {'post_id': 2, 'status': 'scheduled', 'video_url': 'http://test.url'},
            {'post_id': 3, 'status': 'scheduled'},
        ]
        mock_worksheet = MagicMock()
        mock_worksheet.get_all_records.return_value = mock_posts

        mock_spreadsheet = MagicMock()
        mock_spreadsheet.worksheet.return_value = mock_worksheet
        mock_get_spreadsheet.return_value = mock_spreadsheet

        post = get_next_scheduled_post()

        self.assertIsNotNone(post)
        self.assertEqual(post['post_id'], 2)

    @patch('sheets_handler.get_spreadsheet')
    def test_get_next_scheduled_post_not_found(self, mock_get_spreadsheet):
        """Testa la ricerca quando non ci sono post schedulati."""
        mock_posts = [
            {'post_id': 1, 'status': 'posted'},
            {'post_id': 2, 'status': 'failed'},
        ]
        mock_worksheet = MagicMock()
        mock_worksheet.get_all_records.return_value = mock_posts

        mock_spreadsheet = MagicMock()
        mock_spreadsheet.worksheet.return_value = mock_worksheet
        mock_get_spreadsheet.return_value = mock_spreadsheet

        post = get_next_scheduled_post()

        self.assertIsNone(post)

    @patch('sheets_handler.get_spreadsheet')
    @patch('sheets_handler.datetime')
    def test_update_post_status(self, mock_datetime, mock_get_spreadsheet):
        """Testa l'aggiornamento dello stato di un post."""
        mock_now = MagicMock()
        mock_now.isoformat.return_value = "2025-01-01T12:00:00"
        mock_datetime.now.return_value = mock_now

        mock_cell = MagicMock()
        mock_cell.row = 2
        mock_worksheet = MagicMock()
        mock_worksheet.find.return_value = mock_cell

        mock_spreadsheet = MagicMock()
        mock_spreadsheet.worksheet.return_value = mock_worksheet
        mock_get_spreadsheet.return_value = mock_spreadsheet

        result = update_post_status(1, 'posted')

        self.assertTrue(result)
        # Verifica che lo stato sia aggiornato (colonna 6)
        mock_worksheet.update_cell.assert_any_call(2, 6, 'posted')
        # Verifica che la data di pubblicazione sia aggiornata (colonna 8)
        mock_worksheet.update_cell.assert_any_call(2, 8, "2025-01-01T12:00:00")


if __name__ == '__main__':
    unittest.main()

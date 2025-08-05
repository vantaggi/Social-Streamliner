import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // TODO: Move this URL to an environment configuration file.
  static const String _backendUrl = "http://127.0.0.1:5000/webhook";

  /// Invia i dati della clip (URL, nome del gioco, dettagli) al backend.
  ///
  /// Restituisce `true` se la richiesta ha successo, altrimenti `false`.
  Future<bool> sendClipData(String videoUrl, String gameName, String clipDetails) async {
    try {
      final response = await http.post(
        Uri.parse(_backendUrl),
        headers: {
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'videoUrl': videoUrl,
          'gameName': gameName,
          'clipDetails': clipDetails,
        }),
      );

      if (response.statusCode == 200) {
        print('Dati della clip inviati con successo al backend.');
        return true;
      } else {
        print('Errore dal backend: ${response.statusCode}');
        print('Corpo della risposta: ${response.body}');
        return false;
      }
    } catch (e) {
      print('Errore durante la chiamata al backend: $e');
      return false;
    }
  }
}

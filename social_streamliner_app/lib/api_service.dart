import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // TODO: Move this URL to an environment configuration file.
  static const String _backendUrl = "http://127.0.0.1:5000/webhook";

  /// Invia l'URL del video al backend.
  ///
  /// Restituisce `true` se la richiesta ha successo, altrimenti `false`.
  Future<bool> sendVideoUrl(String videoUrl) async {
    try {
      final response = await http.post(
        Uri.parse(_backendUrl),
        headers: {
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'videoUrl': videoUrl,
        }),
      );

      if (response.statusCode == 200) {
        print('URL inviato con successo al backend.');
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

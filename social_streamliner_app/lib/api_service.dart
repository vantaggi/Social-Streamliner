import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String _backendUrlKey = 'backend_url';

  Future<String?> _getBackendUrl() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_backendUrlKey);
  }

  Future<bool> sendClipData(String videoUrl, String gameName, String clipDetails) async {
    final baseUrl = await _getBackendUrl();
    if (baseUrl == null || baseUrl.isEmpty) {
      print('URL del backend non configurato!');
      return false;
    }

    final fullUrl = '$baseUrl/webhook';

    try {
      final response = await http.post(
        Uri.parse(fullUrl),
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

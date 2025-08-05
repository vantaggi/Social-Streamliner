import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  Future<bool> sendClipData({
    required String backendUrl,
    required String videoUrl,
    required String gameName,
    required String clipDetails,
  }) async {
    if (backendUrl.isEmpty) {
      print('URL del backend non configurato!');
      return false;
    }

    final fullUrl = '$backendUrl/webhook';

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

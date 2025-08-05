import 'package:flutter/material.dart';
import 'api_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _urlController = TextEditingController();
  final _apiService = ApiService();
  bool _isLoading = false;

  Future<void> _submitUrl() async {
    if (_urlController.text.isEmpty) {
      // Opzionale: mostra un messaggio se l'URL è vuoto
      return;
    }

    setState(() {
      _isLoading = true;
    });

    final success = await _apiService.sendVideoUrl(_urlController.text);

    setState(() {
      _isLoading = false;
    });

    if (mounted) { // Assicura che il widget sia ancora nell'albero
      final snackBar = SnackBar(
        content: Text(
          success ? 'URL inviato con successo!' : 'Errore durante l\'invio dell\'URL.',
        ),
        backgroundColor: success ? Colors.green : Colors.red,
      );
      ScaffoldMessenger.of(context).showSnackBar(snackBar);
    }

    if (success) {
      _urlController.clear();
    }
  }

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Social Streamliner'),
        backgroundColor: Colors.deepPurple,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            const Text(
              'Incolla l\'URL della clip qui sotto:',
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _urlController,
              enabled: !_isLoading,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'URL del video',
                hintText: 'https://clips.eklipse.gg/...',
              ),
            ),
            const SizedBox(height: 24),
            // Mostra il pulsante o l'indicatore di caricamento
            _isLoading
                ? const Center(child: CircularProgressIndicator())
                : ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.deepPurple,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      textStyle: const TextStyle(fontSize: 18),
                    ),
                    onPressed: _submitUrl,
                    child: const Text('Invia per Approvazione'),
                  ),
          ],
        ),
      ),
    );
  }
}

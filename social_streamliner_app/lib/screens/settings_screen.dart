import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:social_streamliner_app/providers/app_provider.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({Key? key}) : super(key: key);

  @override
  _SettingsScreenState createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late TextEditingController _backendUrlController;

  @override
  void initState() {
    super.initState();
    _backendUrlController = TextEditingController();
    // Carica l'URL iniziale dal provider
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final provider = Provider.of<AppProvider>(context, listen: false);
      _backendUrlController.text = provider.backendUrl;
    });
  }

  Future<void> _saveBackendUrl() async {
    final provider = Provider.of<AppProvider>(context, listen: false);
    await provider.saveBackendUrl(_backendUrlController.text);
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('URL del backend salvato!')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Impostazioni'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _backendUrlController,
              decoration: const InputDecoration(
                labelText: 'URL del Backend',
                hintText: 'https://tua-app.trycloudflare.com',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _saveBackendUrl,
              child: const Text('Salva'),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _backendUrlController.dispose();
    super.dispose();
  }
}

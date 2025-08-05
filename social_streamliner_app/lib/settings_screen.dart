import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({Key? key}) : super(key: key);

  @override
  _SettingsScreenState createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final _backendUrlController = TextEditingController();
  static const String _backendUrlKey = 'backend_url';

  @override
  void initState() {
    super.initState();
    _loadBackendUrl();
  }

  Future<void> _loadBackendUrl() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _backendUrlController.text = prefs.getString(_backendUrlKey) ?? '';
    });
  }

  Future<void> _saveBackendUrl() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_backendUrlKey, _backendUrlController.text);
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('URL del backend salvato!')),
    );
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

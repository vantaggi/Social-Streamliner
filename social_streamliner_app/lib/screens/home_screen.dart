import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:social_streamliner_app/providers/app_provider.dart';
import 'package:social_streamliner_app/services/api_service.dart';
import 'package:social_streamliner_app/screens/settings_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _urlController = TextEditingController();
  final _gameNameController = TextEditingController();
  final _clipDetailsController = TextEditingController();
  final _apiService = ApiService();

  @override
  void initState() {
    super.initState();
    // Carica le preferenze all'avvio e imposta il nome del gioco se disponibile
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final provider = Provider.of<AppProvider>(context, listen: false);
      provider.loadPreferences().then((_) {
        if (provider.lastUsedGame.isNotEmpty) {
          _gameNameController.text = provider.lastUsedGame;
        }
      });
    });
  }

  Future<void> _submitClip() async {
    final provider = Provider.of<AppProvider>(context, listen: false);

    if (_urlController.text.isEmpty || _gameNameController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('URL del video e Nome Gioco sono obbligatori.'),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    provider.setLoading(true);

    final success = await _apiService.sendClipData(
      backendUrl: provider.backendUrl,
      videoUrl: _urlController.text,
      gameName: _gameNameController.text,
      clipDetails: _clipDetailsController.text,
    );

    if (success) {
      await provider.saveGamePreferences(_gameNameController.text);
    }

    provider.setLoading(false);

    if (mounted) {
      final snackBar = SnackBar(
        content: Text(
          success ? 'Clip inviata con successo!' : 'Errore durante l\'invio della clip.',
        ),
        backgroundColor: success ? Colors.green : Colors.red,
      );
      ScaffoldMessenger.of(context).showSnackBar(snackBar);
    }

    if (success) {
      _urlController.clear();
      _clipDetailsController.clear();
    }
  }

  @override
  void dispose() {
    _urlController.dispose();
    _gameNameController.dispose();
    _clipDetailsController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<AppProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Social Streamliner'),
        backgroundColor: Colors.deepPurple,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const SettingsScreen()),
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              const Text("Dati della Clip", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              TextField(
                controller: _urlController,
                enabled: !provider.isLoading,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'URL del video (obbligatorio)',
                  hintText: 'https://clips.eklipse.gg/...',
                ),
              ),
              const SizedBox(height: 16),
              Autocomplete<String>(
                optionsBuilder: (TextEditingValue textEditingValue) {
                  if (textEditingValue.text.isEmpty) {
                    return const Iterable<String>.empty();
                  }
                  return provider.gameHistory.where((String option) {
                    return option.toLowerCase().contains(textEditingValue.text.toLowerCase());
                  });
                },
                onSelected: (String selection) {
                  _gameNameController.text = selection;
                },
                fieldViewBuilder: (context, fieldController, fieldFocusNode, onFieldSubmitted) {
                  fieldController.text = _gameNameController.text;
                  fieldController.addListener(() {
                    _gameNameController.text = fieldController.text;
                  });
                  return TextField(
                    controller: fieldController,
                    focusNode: fieldFocusNode,
                    enabled: !provider.isLoading,
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                      labelText: 'Nome Gioco (obbligatorio)',
                      hintText: 'Es. Call of Duty',
                    ),
                  );
                },
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _clipDetailsController,
                enabled: !provider.isLoading,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'Dettagli Clip (opzionale)',
                  hintText: 'Es. 1v3 clutch, sorpasso al primo giro...',
                ),
              ),
              const SizedBox(height: 24),
              provider.isLoading
                  ? const Center(child: CircularProgressIndicator())
                  : ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.deepPurple,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        textStyle: const TextStyle(fontSize: 18),
                      ),
                      onPressed: _submitClip,
                      child: const Text('Invia per Approvazione'),
                    ),
            ],
          ),
        ),
      ),
    );
  }
}

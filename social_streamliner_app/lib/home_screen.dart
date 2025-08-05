import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'api_service.dart';
import 'settings_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  // Controllers per i campi di testo
  final _urlController = TextEditingController();
  final _gameNameController = TextEditingController();
  final _clipDetailsController = TextEditingController();

  final _apiService = ApiService();
  bool _isLoading = false;

  // Stato per la gestione dei suggerimenti
  List<String> _gameSuggestions = [];
  static const String _gameHistoryKey = 'game_history';
  static const String _lastUsedGameKey = 'last_used_game';

  @override
  void initState() {
    super.initState();
    _loadPreferences();
  }

  /// Carica la cronologia dei giochi e l'ultimo gioco usato da SharedPreferences.
  Future<void> _loadPreferences() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _gameSuggestions = prefs.getStringList(_gameHistoryKey) ?? [];
      final lastUsedGame = prefs.getString(_lastUsedGameKey);
      if (lastUsedGame != null) {
        _gameNameController.text = lastUsedGame;
      }
    });
  }

  /// Salva il nome del gioco nella cronologia e come ultimo gioco usato.
  Future<void> _saveGamePreferences(String gameName) async {
    final prefs = await SharedPreferences.getInstance();

    // Aggiungi alla cronologia solo se non è già presente
    if (!_gameSuggestions.contains(gameName)) {
      _gameSuggestions.add(gameName);
      await prefs.setStringList(_gameHistoryKey, _gameSuggestions);
    }

    // Salva come ultimo gioco usato
    await prefs.setString(_lastUsedGameKey, gameName);
  }

  /// Invia i dati della clip al backend.
  Future<void> _submitClip() async {
    if (_urlController.text.isEmpty || _gameNameController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('URL del video e Nome Gioco sono obbligatori.'),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    setState(() {
      _isLoading = true;
    });

    final success = await _apiService.sendClipData(
      _urlController.text,
      _gameNameController.text,
      _clipDetailsController.text,
    );

    if (success) {
      // Salva il gioco usato solo se l'invio ha successo
      await _saveGamePreferences(_gameNameController.text);
    }

    setState(() {
      _isLoading = false;
    });

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
      // Non pulire il nome del gioco per facilitare invii multipli
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
              // --- CAMPO URL ---
              const Text("Dati della Clip", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              TextField(
                controller: _urlController,
                enabled: !_isLoading,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'URL del video (obbligatorio)',
                  hintText: 'https://clips.eklipse.gg/...',
                ),
              ),
              const SizedBox(height: 16),

              // --- CAMPO NOME GIOCO (AUTOCOMPLETE) ---
              Autocomplete<String>(
                optionsBuilder: (TextEditingValue textEditingValue) {
                  if (textEditingValue.text == '') {
                    return const Iterable<String>.empty();
                  }
                  return _gameSuggestions.where((String option) {
                    return option.toLowerCase().contains(textEditingValue.text.toLowerCase());
                  });
                },
                onSelected: (String selection) {
                  _gameNameController.text = selection;
                },
                fieldViewBuilder: (BuildContext context, TextEditingController fieldController, FocusNode fieldFocusNode, VoidCallback onFieldSubmitted) {
                  // Sincronizza il controller esterno con quello interno del builder
                  fieldController.text = _gameNameController.text;
                  fieldController.addListener(() {
                    _gameNameController.text = fieldController.text;
                   });

                  return TextField(
                    controller: fieldController,
                    focusNode: fieldFocusNode,
                    enabled: !_isLoading,
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                      labelText: 'Nome Gioco (obbligatorio)',
                      hintText: 'Es. Call of Duty',
                    ),
                  );
                },
              ),
              const SizedBox(height: 16),

              // --- CAMPO DETTAGLI CLIP ---
              TextField(
                controller: _clipDetailsController,
                enabled: !_isLoading,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'Dettagli Clip (opzionale)',
                  hintText: 'Es. 1v3 clutch, sorpasso al primo giro...',
                ),
              ),
              const SizedBox(height: 24),

              // --- PULSANTE DI INVIO ---
              _isLoading
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

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AppProvider with ChangeNotifier {
  bool _isLoading = false;
  String _backendUrl = '';
  List<String> _gameHistory = [];
  String _lastUsedGame = '';

  static const String _backendUrlKey = 'backend_url';
  static const String _gameHistoryKey = 'game_history';
  static const String _lastUsedGameKey = 'last_used_game';

  bool get isLoading => _isLoading;
  String get backendUrl => _backendUrl;
  List<String> get gameHistory => _gameHistory;
  String get lastUsedGame => _lastUsedGame;

  void setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }

  Future<void> loadPreferences() async {
    final prefs = await SharedPreferences.getInstance();
    _backendUrl = prefs.getString(_backendUrlKey) ?? '';
    _gameHistory = prefs.getStringList(_gameHistoryKey) ?? [];
    _lastUsedGame = prefs.getString(_lastUsedGameKey) ?? '';
    notifyListeners();
  }

  Future<void> saveGamePreferences(String gameName) async {
    final prefs = await SharedPreferences.getInstance();
    if (!_gameHistory.contains(gameName)) {
      _gameHistory.add(gameName);
      await prefs.setStringList(_gameHistoryKey, _gameHistory);
    }
    _lastUsedGame = gameName;
    await prefs.setString(_lastUsedGameKey, gameName);
    notifyListeners();
  }

  Future<void> saveBackendUrl(String url) async {
    final prefs = await SharedPreferences.getInstance();
    _backendUrl = url;
    await prefs.setString(_backendUrlKey, url);
    notifyListeners();
  }
}

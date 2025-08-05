import 'package:flutter/material.dart';
import 'home_screen.dart'; // Importa la nuova home screen

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    const primaryColor = Color(0xFFFF4500);

    final lightTheme = ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primaryColor,
        brightness: Brightness.light,
      ),
      // Ulteriori personalizzazioni per il tema chiaro in stile Expressive
      textTheme: const TextTheme(
        displayLarge: TextStyle(fontFamily: 'Roboto', fontSize: 57, fontWeight: FontWeight.bold),
        // Aggiungi altri stili di testo se necessario
      ),
    );

    final darkTheme = ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primaryColor,
        brightness: Brightness.dark,
      ),
      // Ulteriori personalizzazioni per il tema scuro in stile Expressive
      textTheme: const TextTheme(
        displayLarge: TextStyle(fontFamily: 'Roboto', fontSize: 57, fontWeight: FontWeight.bold),
        // Aggiungi altri stili di testo se necessario
      ),
    );

    return MaterialApp(
      title: 'Social Streamliner',
      theme: lightTheme,
      darkTheme: darkTheme,
      themeMode: ThemeMode.system, // Segue le impostazioni di sistema
      debugShowCheckedModeBanner: false, // Rimuove il banner di debug
      home: const HomeScreen(), // Imposta la HomeScreen come pagina iniziale
    );
  }
}

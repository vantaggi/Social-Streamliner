import 'package:flutter/material.dart';
import 'home_screen.dart'; // Importa la nuova home screen

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Social Streamliner',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      debugShowCheckedModeBanner: false, // Rimuove il banner di debug
      home: const HomeScreen(), // Imposta la HomeScreen come pagina iniziale
    );
  }
}

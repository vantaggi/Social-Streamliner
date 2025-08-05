import 'package:flutter/material.dart';

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

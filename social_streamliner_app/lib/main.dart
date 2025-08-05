import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:social_streamliner_app/providers/app_provider.dart';
import 'package:social_streamliner_app/screens/home_screen.dart';
import 'package:social_streamliner_app/theme.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => AppProvider(),
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
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

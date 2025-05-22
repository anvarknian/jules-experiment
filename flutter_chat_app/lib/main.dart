import 'package:flutter/material.dart';
import 'package:flutter_chat_app/src/providers/chat_provider.dart';
import 'package:flutter_chat_app/src/screens/chat_screen.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => ChatProvider(),
      child: MaterialApp(
        title: 'Flutter Chat App',
        themeMode: ThemeMode.system, // Or ThemeMode.light, ThemeMode.dark
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal, brightness: Brightness.light),
          useMaterial3: true,
        ),
        darkTheme: ThemeData( // Optional: Define a dark theme
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal, brightness: Brightness.dark),
          useMaterial3: true,
        ),
        home: const ChatScreen(),
      ),
    );
  }
}

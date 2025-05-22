import 'package:flutter/foundation.dart';
import '../models/chat_message.dart';
import '../services/api_service.dart'; // Import ApiService
import 'dart:math';

class ChatProvider with ChangeNotifier {
  final List<ChatMessage> _messages = [
    ChatMessage(id: '0', text: 'Connected to FastAPI backend! Send a message.', isUserMessage: false, timestamp: DateTime.now()),
  ];
  final ApiService _apiService = ApiService(); // Instantiate ApiService
  
  bool _isLoading = false; // New loading state
  bool get isLoading => _isLoading;

  List<ChatMessage> get messages => List.unmodifiable(_messages.reversed);

  String _generateId() {
    return DateTime.now().millisecondsSinceEpoch.toString() + Random().nextInt(99999).toString();
  }

  Future<void> addUserMessage(String text) async {
    final userMessage = ChatMessage(
      id: _generateId(),
      text: text,
      isUserMessage: true,
      timestamp: DateTime.now(),
    );
    _messages.add(userMessage);
    
    _isLoading = true;
    notifyListeners(); // Notify for user message and loading state

    try {
      final String botReplyText = await _apiService.sendMessage(text);
      _addBotMessage(botReplyText, isError: false);
    } catch (e) {
      _addBotMessage(e.toString(), isError: true);
    } finally {
      _isLoading = false;
      notifyListeners(); // Notify for bot message and loading state finished
    }
  }

  void _addBotMessage(String text, {bool isError = false}) {
    final botMessage = ChatMessage(
      id: _generateId(),
      text: isError ? "Error: $text" : text, 
      isUserMessage: false,
      timestamp: DateTime.now(),
    );
    _messages.add(botMessage);
    // isLoading is handled in addUserMessage's finally block
    // notifyListeners(); // This will be called by finally in addUserMessage
  }
}

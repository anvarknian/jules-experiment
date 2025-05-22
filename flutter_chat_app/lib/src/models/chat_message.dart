// lib/src/models/chat_message.dart
class ChatMessage {
  final String id; // Unique ID for each message
  final String text;
  final bool isUserMessage;
  final DateTime timestamp;

  ChatMessage({
    required this.id,
    required this.text,
    required this.isUserMessage,
    required this.timestamp,
  });
}

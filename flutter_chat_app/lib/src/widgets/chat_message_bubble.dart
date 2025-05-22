import 'package:flutter/material.dart';

class ChatMessageBubble extends StatelessWidget {
  final String message;
  final bool isUserMessage;

  const ChatMessageBubble({
    super.key,
    required this.message,
    required this.isUserMessage,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Align(
      alignment: isUserMessage ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 5.0, horizontal: 8.0),
        padding: const EdgeInsets.symmetric(vertical: 10.0, horizontal: 14.0), // Adjusted padding
        decoration: BoxDecoration(
          color: isUserMessage ? colorScheme.primary : colorScheme.secondaryContainer, // M3 colors
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16.0),
            topRight: const Radius.circular(16.0),
            bottomLeft: Radius.circular(isUserMessage ? 16.0 : 4.0), // Different style for user
            bottomRight: Radius.circular(isUserMessage ? 4.0 : 16.0), // Different style for assistant
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.05),
              blurRadius: 2.0,
              offset: const Offset(0, 1),
            ),
          ],
        ),
        child: Text(
          message,
          style: TextStyle(
            color: isUserMessage ? colorScheme.onPrimary : colorScheme.onSecondaryContainer, // M3 text colors
          ),
        ),
      ),
    );
  }
}

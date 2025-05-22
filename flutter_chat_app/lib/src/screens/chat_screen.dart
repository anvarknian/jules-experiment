import 'package:flutter/material.dart';
import 'package:flutter_chat_app/src/models/chat_message.dart';
import 'package:flutter_chat_app/src/providers/chat_provider.dart';
import 'package:flutter_chat_app/src/widgets/chat_message_bubble.dart';
import 'package:provider/provider.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    // Scroll to bottom when messages change and widget is built
    // Also, listen to provider changes to scroll when new messages are added.
    final chatProvider = Provider.of<ChatProvider>(context);
    chatProvider.addListener(_scrollToBottomIfNecessary);

    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) {
        _scrollToBottom();
      }
    });
  }

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    // Important to remove the listener to avoid memory leaks
    Provider.of<ChatProvider>(context, listen: false).removeListener(_scrollToBottomIfNecessary);
    super.dispose();
  }
  
  void _scrollToBottomIfNecessary() {
    // This function is called by the provider listener.
    // We use addPostFrameCallback to ensure scrolling happens after the build.
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted && _scrollController.hasClients) {
        _scrollController.animateTo(
          0.0, 
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _scrollToBottom() {
    if (_scrollController.hasClients) {
      _scrollController.animateTo(
        0.0, 
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    }
  }

  void _handleSendPressed() {
    if (_textController.text.isNotEmpty) {
      Provider.of<ChatProvider>(context, listen: false).addUserMessage(_textController.text);
      _textController.clear();
      // Scrolling is handled by the listener now, but this can ensure an immediate scroll if needed
      // WidgetsBinding.instance.addPostFrameCallback((_) => _scrollToBottom());
    }
  }

  @override
  Widget build(BuildContext context) {
    // Access the provider
    final chatProvider = Provider.of<ChatProvider>(context); 
    final messages = chatProvider.messages; // Messages are already reversed in provider

    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter Chat'), // Simplified title
        backgroundColor: Theme.of(context).colorScheme.surfaceVariant, // M3 style appbar
        elevation: 1.0,
      ),
      body: Column(
        children: <Widget>[
          Expanded(
            child: Scrollbar( // Added Scrollbar
              thumbVisibility: true, // Make scrollbar always visible
              controller: _scrollController,
              child: ListView.builder(
                controller: _scrollController,
                padding: const EdgeInsets.all(8.0),
                reverse: true,
                itemCount: messages.length,
                itemBuilder: (_, int index) {
                  final message = messages[index]; 
                  return ChatMessageBubble(
                    message: message.text,
                    isUserMessage: message.isUserMessage,
                  );
                },
              ),
            ),
          ),
          const Divider(height: 1.0),
          _buildTextComposer(),
        ],
      ),
    );
  }

  Widget _buildTextComposer() {
    final chatProvider = Provider.of<ChatProvider>(context, listen: true);
    final theme = Theme.of(context);

    return Container( // Decorated the input area
      padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 8.0),
      decoration: BoxDecoration(
        color: theme.cardColor, // Or theme.colorScheme.surface for M3
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 4.0,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: SafeArea( // Ensure input field is not obscured by system UI
        child: Row(
          children: <Widget>[
            Flexible(
              child: TextField(
                controller: _textController,
                onSubmitted: chatProvider.isLoading ? null : (text) => _handleSendPressed(),
                decoration: InputDecoration( // Added some decoration to TextField
                  hintText: 'Send a message...',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(20.0),
                    borderSide: BorderSide.none,
                  ),
                  filled: true,
                  fillColor: theme.colorScheme.surfaceVariant.withOpacity(0.5), // Subtle fill
                  contentPadding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 10.0),
                ),
                enabled: !chatProvider.isLoading,
              ),
            ),
            const SizedBox(width: 8.0), // Spacing
            Container(
              margin: const EdgeInsets.symmetric(horizontal: 0.0), // Adjusted margin
              child: chatProvider.isLoading
                  ? Container( // Ensure loading indicator is centered and sized
                      width: 48.0, // Standard IconButton touch target size
                      height: 48.0,
                      padding: const EdgeInsets.all(12.0), // Center CircularProgressIndicator
                      child: const CircularProgressIndicator(strokeWidth: 2.5),
                    )
                  : IconButton(
                      icon: const Icon(Icons.send),
                      onPressed: _handleSendPressed,
                      style: IconButton.styleFrom( // M3 style IconButton
                        backgroundColor: theme.colorScheme.primary,
                        foregroundColor: theme.colorScheme.onPrimary,
                        padding: const EdgeInsets.all(12.0),
                      ),
                    ),
            ),
          ],
        ),
      ),
    );
  }
}

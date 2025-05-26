// lib/src/services/api_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/chat_message.dart'; // For potential use if API returns full message objects, though not strictly needed for this post.

class ApiService {
  // Ensure your FastAPI backend is running and accessible at this URL.
  // For Android emulator, 10.0.2.2 typically maps to your host machine's localhost.
  // For iOS simulator, localhost or 127.0.0.1 should work.
  // If running on a physical device, use your machine's network IP.
  // Use String.fromEnvironment to get the backend URL.
  // The 'BACKEND_URL' will be passed during the Docker build.
  static const String _baseUrl = String.fromEnvironment(
    'BACKEND_URL',
    defaultValue: 'http://localhost:8000', // Fallback for local development
  );

  Future<String> sendMessage(String userMessage) async {
    // The API endpoint is now /api/v1/chat as per backend main.py
    final Uri chatUri = Uri.parse('$_baseUrl/api/v1/chat');
    
    try {
      final response = await http.post(
        chatUri,
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, dynamic>{ // Changed to dynamic for user_id and chat_id
          'message': userMessage,
          // TODO: Implement actual user_id and chat_id management
          'user_id': 1, // Placeholder user_id
          'chat_id': null, // Placeholder chat_id (optional, backend creates new if null)
        }),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> responseData = jsonDecode(response.body);
        if (responseData.containsKey('reply') && responseData['reply'] != null) {
          // Optionally, you might want to use chat_id or message_ids from response
          // String chatId = responseData['chat_id']?.toString() ?? '';
          return responseData['reply'] as String;
        } else if (responseData.containsKey('error') && responseData['error'] != null) {
          return Future.error('Error from server: ${responseData['error']}');
        } else {
          return Future.error('Invalid response format from server.');
        }
      } else {
        // Try to parse error from backend if available
        String serverError = response.body;
        try {
            final Map<String, dynamic> errorData = jsonDecode(response.body);
            if (errorData.containsKey('detail')) {
                serverError = errorData['detail'].toString();
            }
        } catch (_) {
            // Ignore if response body is not json or doesn't have detail
        }
        return Future.error('Failed to send message. Status: ${response.statusCode}. Error: $serverError');
      }
    } catch (e) {
      // This catches network errors, parsing errors etc.
      return Future.error('Failed to connect to the chat service: $e');
    }
  }
}

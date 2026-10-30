# CMND.ai Extension

You can start editing the `tools.py` file to create your own extension.

## Context

Besides its arguments, CMND sends every tool call some context about the conversation. Add a `context` parameter to a tool's `runCmd` to receive it as a dict:

| Key | Value |
| --- | --- |
| `organizationId` | The organization the conversation belongs to |
| `chatbotId` | The chatbot the user is talking to |
| `chatbotConversationId`, `chatbotConversationRef` | The chatbot conversation |
| `conversationId` | The conversation, outside of chatbots |
| `senderPhoneNumber` | WhatsApp only: the user's phone number, or `None` when it is unknown |

WhatsApp hides the phone number of users with a username. Turn on "require phone number" on the chatbot so it asks those users to share it, and `senderPhoneNumber` is always set. See `get_phone_number` in `tools.py`.

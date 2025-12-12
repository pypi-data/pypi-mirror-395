from typing import TypedDict

# Data Structure for Chat Message
class ChatHistory(TypedDict):
    role: str
    content: str
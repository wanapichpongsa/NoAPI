import ollama
import os

def create_conversation_file():
  data_dir = "../database/conversations"
  no_conversations = len(os.listdir(data_dir))
  file_path = f"{data_dir}/conversation_{no_conversations + 1}.txt"
  with open(file_path, "w") as f:
    f.write()
  return file_path

class ConversationalAgent:
  def __init__(self, model: str = "llama3.2:latest"):
    self.client = ollama.Client()
    self.model = model # Try deepseekr-1 later.
    self.messages = []
    self.file_path = create_conversation_file()

  # to give ST memory within a conversation, we have input previous messages.
  def system_prompt(self, system_prompt: str):
    self.messages.append({"role": "system", "content": system_prompt})

  def conversation(self, user_query: str, attachment: str = None):
    if attachment:
      user_query += f"\nAttachment: {attachment}"
    self.messages.append({"role": "user", "content": user_query})
    
    # ChatGPT and Claude are never the same instances by the way. They basically operate as RAGs.
    response = self.client.chat(model=self.model, messages=self.messages)
    self.messages.append({"role": "assistant", "content": response.message.content})
    # TODO: Save to DB
    with open(self.file_path, "a") as f:
      f.write(f"You: {user_query}\nAgent: {response.message.content}\n")

    print(f"Agent: {response.message.content}\n")

  # When GUI, can do this for any message in conversation.
  def get_latest_response(self):
    return self.messages[-1]["content"]
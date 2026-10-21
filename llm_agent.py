from groq import Groq
from dotenv import load_dotenv
import os

TEXT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = "qwen/qwen3.8-27b"


class ConversationAgent:

    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])
        self.conversation_history = [
            {
                "role": "system",
                "content": self.read_file(file_path="./context.txt")
            }
        ]

    @staticmethod
    def read_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def get_conversation_history(self):
        return self.conversation_history[1:]

    def update_conversation_history(self, role, content):
        self.conversation_history.append(
            {
                "role": role,
                "content": content,
            }
        )

    def history_has_image(self):
        for message in self.conversation_history:
            if isinstance(message["content"], list):
                for block in message["content"]:
                    if block["type"] == "image_url":
                        return True
        return False

    def remove_old_images(self):
        # on ne garde que la dernière image : les anciennes deviennent du texte
        for message in self.conversation_history:
            if isinstance(message["content"], list):
                texts = [b["text"] for b in message["content"] if b["type"] == "text"]
                message["content"] = " ".join(texts) + " [image envoyée précédemment]"

    def ask_llm(self, text_interaction, image_data_url=None):
        if image_data_url:
            self.remove_old_images()
            content = [
                {"type": "text", "text": text_interaction or "Décris cette image."},
                {"type": "image_url", "image_url": {"url": image_data_url}},
            ]
        else:
            content = text_interaction

        self.update_conversation_history(role="user", content=content)

        # modèle vision si une image est dans l'historique, sinon modèle texte
        model = VISION_MODEL if self.history_has_image() else TEXT_MODEL

        parameters = {"messages": self.conversation_history, "model": model}
        if model == TEXT_MODEL:
            parameters["include_reasoning"] = False   # option propre à gpt-oss

        response = self.groq_client.chat.completions.create(
            **parameters
        ).choices[0].message.content

        self.update_conversation_history(role="assistant", content=response)
        return response


if __name__ == "__main__":
    agent = ConversationAgent()
    question = input("Pose ta question :\n")
    print("\n")
    print(agent.ask_llm(question))
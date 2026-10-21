import base64
import streamlit as st
from llm_agent import ConversationAgent
from stt import SpeechToText
from image_utils import image_to_data_url


class UserInterface:

    def __init__(self):
        st.set_page_config(page_title="Jarvis")
        st.title("Barbe-Quasar")
        self.conversation_agent_object = self.get_persistant_conversation_agent()
        self.speech_to_text = SpeechToText()

    def get_persistant_conversation_agent(self):
        if "conversation_agent_object" not in st.session_state:
            st.session_state.conversation_agent_object = ConversationAgent()
        return st.session_state.conversation_agent_object

    def show_discussion_history(self):
        for message in self.conversation_agent_object.get_conversation_history():
            with st.chat_message(message["role"]):
                content = message["content"]
                if isinstance(content, str):
                    st.markdown(content)
                else:
                    for block in content:
                        if block["type"] == "text":
                            st.markdown(block["text"])
                        elif block["type"] == "image_url":
                            encoded = block["image_url"]["url"].split(",", 1)[1]
                            st.image(base64.b64decode(encoded))

    def run(self):
        user_input = st.chat_input(
            "Écris, parle ou joins une image, moussaillon...",
            accept_file=True,
            file_type=["png", "jpg", "jpeg"],
            accept_audio=True,
        )

        if user_input:
            text_interaction = user_input.text
            image_data_url = None

            if user_input.audio:
                with st.spinner("Transcription..."):
                    text_interaction = self.speech_to_text.transcribe(user_input.audio)

            if user_input.files:
                image_data_url = image_to_data_url(user_input.files[0])

            if text_interaction or image_data_url:
                with st.spinner("Le capitaine réfléchit..."):
                    self.conversation_agent_object.ask_llm(
                        text_interaction, image_data_url=image_data_url
                    )

        self.show_discussion_history()


if __name__ == "__main__":
    user_interface_object = UserInterface()
    user_interface_object.run()
import streamlit as st
from llm_agent import ConversationAgent
from stt import SpeechToText


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
                st.markdown(message["content"])

    def run(self):
        user_input = st.chat_input(
            "Écris ou parle, moussaillon...",
            accept_audio=True,
        )

        if user_input:
            text_interaction = user_input.text

            if user_input.audio:
                with st.spinner("Transcription..."):
                    text_interaction = self.speech_to_text.transcribe(user_input.audio)

            if text_interaction:
                with st.spinner("Le capitaine réfléchit..."):
                    self.conversation_agent_object.ask_llm(text_interaction)

        self.show_discussion_history()


if __name__ == "__main__":
    user_interface_object = UserInterface()
    user_interface_object.run()
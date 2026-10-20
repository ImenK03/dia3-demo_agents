
import streamlit as st

st.set_page_config(
    page_title="Assistant conversationnel",
    page_icon="💬",
)

st.title("💬 Mon assistant conversationnel")

# Initialiser l'historique une seule fois
if "messages" not in st.session_state:
    st.session_state.messages = []

# Bouton pour démarrer une nouvelle conversation
if st.sidebar.button("Nouvelle conversation"):
    st.session_state.messages = []
    st.rerun()

# Afficher tous les anciens messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Champ de saisie en bas de la page
prompt = st.chat_input("Écris ton message...")

if prompt:
    # Enregistrer le message de l'utilisateur
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse temporaire pour tester l'historique
    answer = (
        f"Réponse de démonstration à ton message : {prompt}"
    )

    # Enregistrer la réponse de l'assistant
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
    })

    with st.chat_message("assistant"):
        st.markdown(answer)

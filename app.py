import streamlit as st # type: ignore
from datetime import datetime
import openai
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Définir la clé API d'OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

class Chatbot:
    def __init__(self):
        self.chat_history = []

    def generate_response(self, user_input):
        messages = [{'role': 'user', 'content': user_input}]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Erreur lors de l'appel à l'API : {str(e)}"

def main():
    st.set_page_config(page_title="Chatbot SQL", page_icon=":speech_balloon:", layout="wide")

    st.title('Chatbot')
  
    # Affichage de la date actuelle en haut de l'historique des questions
    current_date = datetime.now().strftime("%Y-%m-%d")
    st.sidebar.write(f"Date : {current_date}")

    # Initialiser l'historique des questions et des réponses
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Historique des questions dans la barre latérale gauche
    st.sidebar.title("Historique des questions")
    selected_question = None
    for i, chat in enumerate(st.session_state.chat_history):
        if st.sidebar.button(f"Q{i+1}: {chat['question']}", key=f"question_{i}"):
            selected_question = chat

    # Bloc d'introduction stylisé avec des couleurs améliorées
    st.markdown("""
    <div style='background-color: #4CAF50; color: white; padding: 15px; border-radius: 10px;'>
        <h2 style='color: white;'>Bienvenue sur l'assistant SQL</h2>
        <p>Cette application vous permet d'apprendre les bases de SQL de manière interactive.</p>
    </div>
    """, unsafe_allow_html=True)

    # Zone de texte pour la saisie de l'utilisateur et bouton pour envoyer la question
    with st.form(key='user_input_form'):
        user_input = st.text_input("Posez votre question ici...", placeholder="Exemple : Qu'est-ce qu'une jointure en SQL ?")
        submit_button = st.form_submit_button('Envoyer', help="Cliquez pour envoyer votre question")

    # Traitement de la question lorsqu'on appuie sur le bouton Envoyer
    if submit_button and user_input:
        chatbot = Chatbot()
        response = chatbot.generate_response(user_input)
        st.session_state.chat_history.append({'question': user_input, 'response': response})

    # Afficher uniquement la dernière réponse ou la réponse sélectionnée dans l'historique
    st.markdown("<hr>", unsafe_allow_html=True)
    if selected_question:
        st.markdown(f"<div style='background-color: #F0F0F0; padding: 10px; border-radius: 5px;'>"
                    f"<strong>Réponse à la question :</strong> {selected_question['response']}</div>", unsafe_allow_html=True)
    elif st.session_state.chat_history:
        # Afficher la dernière réponse si aucune question n'a été sélectionnée
        last_response = st.session_state.chat_history[-1]['response']
        st.markdown(f"<div style='background-color: #F0F0F0; padding: 10px; border-radius: 5px;'>"
                    f"<strong>Réponse :</strong> {last_response}</div>", unsafe_allow_html=True)

    # Bouton pour effacer l'historique
    st.sidebar.write("---")
    if st.sidebar.button('Effacer l\'historique'):
        st.session_state.chat_history = []

    # Affichage du nom en bas à droite avec CSS, couleur modifiée pour correspondre au style général
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            bottom: 0;
            right: 0;
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            font-size: 14px;
            border-radius: 10px;
        }
        </style>
        <div class="footer">
            TUNGAMWESE Carlène
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == '__main__':
    main()

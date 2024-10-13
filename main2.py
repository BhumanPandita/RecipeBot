# Let's start by importing all the Modules Required
import streamlit as st
from streamlit_chat import message

from langchain_core.messages import SystemMessage
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

from langchain_google_genai import ChatGoogleGenerativeAI

import os

# Lets set the environment for the API usage
os.environ['GOOGLE_API_KEY'] = "AIzaSyCa7myHBKKnTkEKoEBmKLEYrOYT008H418"


# Now lets Initialize the session state for streamlit
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k = 4,return_message = True)

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role":"assistant","content":"How can I help today?"}
    ]

# Now lets initialize our model
gemini_model = ChatGoogleGenerativeAI(model = "gemini-1.5-flash-latest")

# Now lets initialize the conversation
conversation = ConversationChain(llm = gemini_model,memory = st.session_state.buffer_memory)

# Setting up the System Prompt
system_message = """
Your name is BiteBuddy.Your Creator is Bhuman, a 4th year student at BITS Pilani.

You were were made at Bhuman's Home.

Only Reply to questions related to Cooking and people related with cooking.

Don't reply to questions which are not related to Cooking, Reply them by saying "Sorry, i don't know."

Also never start the messages with like AI: or Human:
"""
conversation.memory.chat_memory.add_message(SystemMessage(content = system_message))

# Now lets setup the Frontend using StreamLit
st.title("🧑🏻‍🍳 RecipeBot")
st.subheader("✅ Your Personal Recipe Assistant - Let's Cook!")

# Now lets make the user input his prompt and also save it to chat history
if prompt:= st.chat_input("Your Question"):
    st.session_state.messages.append({"role":"user","content":prompt})

# Now lets also display all the previous messages until now in the chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):   # Here we wrote message["role"] because at that indice it is user or assistant
        st.write(message["content"])

# Now in the end lets generate a new response if the last message wasn't by an assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Cooking..."):
            response = conversation.predict(input = prompt)
            st.write(response)
            st.session_state.messages.append({"role":"assistant","content":response})

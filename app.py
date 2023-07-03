import streamlit as st
import openai


def handle_userinput(user_input):

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🦜"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🧑‍🔧"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        

def displayHistoryMsgs():
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar="🦜"):
                st.markdown(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant", avatar="🧑‍🔧"):
                st.markdown(message["content"])

            
def init():


    # Set OpenAI API key from Streamlit secrets
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    st.set_page_config(
        page_title="Your own ChatGPT",
        page_icon="🤖"
    )
    st.header("Your own ChatGPT 🤖")

def main():

    init()

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo-0613"

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": """You are a professional AI assistant whose name is J.A.R.V.I.S."""}
        ]
    
    displayHistoryMsgs()

    user_question = st.chat_input("Type your question")
    if user_question:
        handle_userinput(user_question)



if __name__ == '__main__':
    main()

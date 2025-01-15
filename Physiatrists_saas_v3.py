import streamlit as st
#from openai import OpenAI
import openai
import base64

#pip install streamlit openai
#make sure you have python 3.11 or later
#to run the program: streamlit run .\Physiatrists_saas_v3.py
#make sure you have stored the file 'logo.png' in the base directory


# -- 1. Provide your API key (NOT RECOMMENDED to do it this way in production!)
openai.api_key = "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"

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

#this can be called to set a backround image
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


#To clear the text in the user_input field after they hit continue.
def clear_text():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""


def chat_with_model(text):
    """
    Calls the custom 'gpt-4o' model to generate a response
    with emotional support and open question at the end.
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an emotionally supportive AI assistant. "
                    "You will give advice about how people can deal with problems. "
                    "When appropriate, you will end your response with an open question to the person you chat with."
                ),
            },
            {"role": "user", "content": text},
        ],
    )
    advice = response.choices[0].message.content
    return advice

def main():
    #set_background('./logo.png')

    st.title("Chatbot with Emotional Intelligence")
    st.sidebar.image('./logo.png')
    # 2. Initialize or retrieve the conversation history in session_state
    if "conversation" not in st.session_state:
        st.session_state["conversation"] = []

        st.sidebar.write("I am here to listen and give advice. I can talk about anything you like, but am especially adapted to be emotionally intelligent.")
        user_input = st.sidebar.text_input("What do you want to talk about? ", key='widget', on_change=clear_text)

    # 3. Text input for the user
    else:
        st.sidebar.write("I am here to listen and give advice.")
        user_input = st.sidebar.text_input("User input: ", key='widget', on_change=clear_text)

    user_input = st.session_state.get('my_text', '')
    if user_input.strip():
        # Add user's message to the conversation
        st.session_state["conversation"].append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            # Get model's response
            advice = chat_with_model(user_input)
            st.session_state["conversation"].append({"role": "assistant", "content": advice})
    else:
        st.sidebar.warning("Please enter a valid message.")

    # 4. Display the conversation in Streamlit
    st.write("## Conversation")
    for msg in st.session_state["conversation"]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Assistant:** {msg['content']}")

if __name__ == "__main__":
    main()

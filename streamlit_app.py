import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat
from hugchat.login import Login
from transformers import pipeline

st.set_page_config(page_title="HugChat - An LLM-powered Streamlit app")

# Sidebar contents
# with st.sidebar:
#     st.title('🤗💬 HugChat App Demo Takeo2')
    # #authentification
    # EMAIL = ""
    # PASSWD = ""
    # EMAIL = st.text_input("Enter your email")
    # PASSWD = st.text_input("Enter your password", type="password")
    # cookie_path_dir = "./cookies/" # NOTE: trailing slash (/) is required to avoid errors
    # sign = Login(EMAIL, PASSWD)
    # cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

# Generate empty lists for generated and past.
## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm HugChat, How may I help you?"]
## past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

# chatbot
# chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
chatbot = pipeline('text-generation', model='gpt2')


# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()



# User input
## Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text
## Applying the user input box
with input_container:
    user_input = get_text()

# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
    # chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    # response = chatbot.chat(prompt)
    # ans = response.text
    ans = generator(prompt, max_length=30, num_return_sequences=5)
    return ans

## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        st.write(st.session_state)
        for i in range(len(st.session_state['generated'])):
            # st.write(st.session_state['past'][i])
            # st.write(st.session_state["generated"][i])
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

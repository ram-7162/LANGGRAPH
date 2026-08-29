import streamlit as st
import random

## Streamlit reruns your entire Python script
## from top to bottom whenever the user interacts with the page i.e. whenever user press enter.

# if st.button("Click"):
#     st.write("Button pressed")


#### basic message show
# user_input = input("Enter your name : ")
# st.write(user_input)



###This is the widget you'll use most for a chatbot
###It gives a ChatGPT-like input box at the bottom.
# prompt = st.chat_input("Ask something")

# with st.chat_message("user"):
#     st.write("Hello")

# with st.chat_message("assistant"):
#     st.write("Hi!")

# with st.chat_message("user"):
#     st.write(prompt)




# user_input = st.chat_input("Ask Something")

# iteration = 0
# if user_input:
#     with st.chat_message("user"):
#         st.write(user_input)

#     with st.chat_message("assistant"):
#         iteration += 1
#         st.write(f"""dalle dekhna iteration 1 hii ayega kyoki streamlit enter 
#                  press karta hii pura program ko re run karta hai:
#                  ya dekh iteration : {iteration}""")






# # Initialize history
# message_history = []

# # Add initial messages
# message_history.append({'role': 'user', 'content': f"Hello {random.randint(1, 100)}"})
# message_history.append({'role': 'assistant', 'content': "Hello how can I assist you."})

# # Display older conversation
# for message in message_history:
#     with st.chat_message(message['role']):
#         st.text(message['content'])

# # User input
# user_input = st.chat_input("Type Here")

# if user_input:
#     # Add user message
#     message_history.append({'role': 'user', 'content': user_input})
#     with st.chat_message('user'):
#         st.text(user_input)

#     # Add assistant response
#     with st.chat_message('assistant'):
#         st.text("abhi mai ai nahi hoon")

#     message_history.append({'role': 'assistant', 'content': 'ai_response'})




# Initialize history
# st.session_state --> dictionary
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

#### dekh st.session_state ek dict haa aur usma ekk key message_history joo kii ek list hai;
#### uss list mai dict hai bohot sari ex: {'role': 'assistant', 'content': "Hello how can I assist you."}

# Add initial messages
st.session_state['message_history'].append({'role': 'user', 'content': f"Hello {random.randint(1, 100)}"})
st.session_state['message_history'].append({'role': 'assistant', 'content': "Hello how can I assist you."})

# Display older conversation
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# User input
user_input = st.chat_input("Type Here")

if user_input:
    # Add user message
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # Add assistant response
    with st.chat_message('assistant'):
        st.text("abhi mai ai nahi hoon")

    st.session_state['message_history'].append({'role': 'assistant', 'content': 'ai_response'})

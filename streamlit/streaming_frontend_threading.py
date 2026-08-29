import streamlit as st
import random
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph_backend import chatbot
import uuid  #### for generating dynamic thread id for many conversation


### ### ui with single thread_id 
# ## --------------------------------------** utility function **------------------------
# def generate_threadid():
#     thread_id = uuid.uuid4()
#     return thread_id



# if 'message_history' not in st.session_state:
#     st.session_state['message_history'] = []


# if 'thread_id' not in st.session_state:
#     st.session_state['thread_id'] = generate_threadid()



# st.sidebar.title("Langgraph Chatbot")
# st.sidebar.button("New Button")
# st.sidebar.header("My Conversation")
# st.sidebar.text(st.session_state['thread_id'])




# # Display older conversation
# for message in st.session_state['message_history']:
#     with st.chat_message(message['role']):
#         st.text(message['content'])

# # User input
# user_input = st.chat_input("Type Here")

# if user_input:
#     # Add user message
#     st.session_state['message_history'].append({'role': 'user', 'content': user_input})
#     with st.chat_message('user'):
#         st.text(user_input)


#     config1 = {'configurable' : {'thread_id' : st.session_state['thread_id']}}

#     with st.chat_message('assistant'):
#         ai_message = st.write_stream(
#             message_chunk.content for message_chunk , meta_data in chatbot.stream(
#             {'messages' : [HumanMessage(content = user_input)]},
#             config = config1,
#             stream_mode="messages")
#         )
    
#     st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})







### for generating new chat on each turn
# ## --------------------------------------** utility function **------------------------
# def generate_threadid():
#     thread_id = uuid.uuid4()
#     return thread_id


# def reset_chat():
#     thread = generate_threadid()
#     st.session_state['thread_id'] = thread
#     st.session_state['message_history'] = [] 


# st.sidebar.title("Langgraph Chatbot")

# if st.sidebar.button("New Button"):
#     reset_chat()

# st.sidebar.header("My Conversation")

# st.sidebar.text(st.session_state['thread_id'])



# if 'message_history' not in st.session_state:
#     st.session_state['message_history'] = []


# if 'thread_id' not in st.session_state:
#     st.session_state['thread_id'] = generate_threadid()


# # Display older conversation
# for message in st.session_state['message_history']:
#     with st.chat_message(message['role']):
#         st.text(message['content'])

# # User input
# user_input = st.chat_input("Type Here")

# if user_input:
#     # Add user message
#     st.session_state['message_history'].append({'role': 'user', 'content': user_input})
#     with st.chat_message('user'):
#         st.text(user_input)


#     config1 = {'configurable' : {'thread_id' : st.session_state['thread_id']}}

#     with st.chat_message('assistant'):
#         ai_message = st.write_stream(
#             message_chunk.content for message_chunk , meta_data in chatbot.stream(
#             {'messages' : [HumanMessage(content = user_input)]},
#             config = config1,
#             stream_mode="messages")
#         )
    
#     st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})





### creating thread_list
# ## --------------------------------------** utility function **------------------------
# def generate_threadid():
#     thread_id = uuid.uuid4()
#     return thread_id


# def reset_chat():
#     thread = generate_threadid()
#     st.session_state['thread_id'] = thread
#     add_threads(st.session_state['thread_id'])
#     st.session_state['message_history'] = [] 


# def add_threads(thread_id):
#     if thread_id not in st.session_state['thread_list']:
#         st.session_state['thread_list'].append(thread_id)

# ## ----------------------------------------------------------------------------------------------

# if 'message_history' not in st.session_state:
#     st.session_state['message_history'] = []

# if 'thread_id' not in st.session_state:
#     st.session_state['thread_id'] = generate_threadid()

# if 'thread_list' not in st.session_state:
#     st.session_state['thread_list'] = []


# add_threads(st.session_state['thread_id'])

# ## --------------------------------------------------- sidebar ui ------------------------
# st.sidebar.title("Langgraph Chatbot")

# if st.sidebar.button("New Button"):
#     reset_chat()

# st.sidebar.header("My Conversation")

# for thread_id in st.session_state['thread_list']:
#     st.sidebar.button(str(thread_id))


# # Display older conversation
# for message in st.session_state['message_history']:
#     with st.chat_message(message['role']):
#         st.text(message['content'])

# # User input
# user_input = st.chat_input("Type Here")

# if user_input:
#     # Add user message
#     st.session_state['message_history'].append({'role': 'user', 'content': user_input})
#     with st.chat_message('user'):
#         st.text(user_input)

#     config1 = {'configurable' : {'thread_id' : st.session_state['thread_id']}}

#     with st.chat_message('assistant'):
#         ai_message = st.write_stream(
#             message_chunk.content for message_chunk , meta_data in chatbot.stream(
#             {'messages' : [HumanMessage(content = user_input)]},
#             config = config1,
#             stream_mode="messages")
#         )
    
#     st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})




## --------------------------------------** utility function **------------------------
def generate_threadid():
    thread_id = uuid.uuid4()
    return thread_id

# def generate_threadid():
#     st.session_state['thread_counter'] += 1
#     return f"conversation{st.session_state['thread_counter']}"


def reset_chat():
    thread = generate_threadid()
    st.session_state['thread_id'] = thread
    add_threads(st.session_state['thread_id'])
    st.session_state['message_history'] = [] 


def add_threads(thread_id):
    if thread_id not in st.session_state['thread_list']:
        st.session_state['thread_list'].append(thread_id)


def load_conversation(thread_id):
    hist = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return hist.values.get('messages', [])

## ----------------------------------------------------------------------------------------------

# It means:

# "If this is the first time this Streamlit session needs message_history, create it."

# It does not mean:

# "Every time I switch conversations, create a new message history."

# There is a huge difference.

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_threadid()


if 'thread_list' not in st.session_state:
    st.session_state['thread_list'] = []
    

if 'thread_counter' not in st.session_state:
    st.session_state['thread_counter'] = 0


add_threads(st.session_state['thread_id'])

## --------------------------------------------------- sidebar ui ------------------------
st.sidebar.title("Langgraph Chatbot")



if st.sidebar.button("New Button"):
    reset_chat()   ### this reset do one of thing is :: message_history = []

st.sidebar.header("My Conversation")

for thread_id in st.session_state['thread_list']:

    if st.sidebar.button(str(thread_id)):

        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:

            if isinstance(msg, HumanMessage):
                role = "user"
            else:
                role = "assistant"

            temp_messages.append({
                "role": role,
                "content": msg.content
            })

        st.session_state['message_history'] = temp_messages

        # VERY IMPORTANT
        # Make the clicked conversation the active conversation
        st.session_state['thread_id'] = thread_id



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

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']},
              "metadata" : {'thread_id': st.session_state['thread_id']},
              'run_name' : "chat_run"}

    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk , meta_data in chatbot.stream(
            {'messages' : [HumanMessage(content = user_input)]},
            config=CONFIG,
            stream_mode="messages")
        )
    
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})






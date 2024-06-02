import chainlit as cl
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
import chainlit as cl
import os
from functions import *

load_dotenv()
client = AsyncAzureOpenAI(azure_endpoint=os.getenv('openai_endpoint'),api_key=os.getenv('openai_key'),api_version=os.getenv('api_version'))
cl.instrument_openai()


settings = {
    "model":os.getenv('chat_model') ,
    "temperature": 0,
    "max_tokens": 500
}

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None
    

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set(
        "message_history",
        [],
    )
    await cl.Avatar(
        name="GL Bajaj Bot",
        url="/public/mortarboard.png",
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()
    obj=RAG()
    context=obj.answer(message.content)
    message_history = cl.user_session.get("message_history")
    message_history.append({"role":"system","content":message.content})
    prompt=[{"role": "system", "content":f"""You are an experienced college assistant at the G.L.Bajaj group of institutions. Use the following context to answer the question at the end.
            Additionally, please engage in basic conversational etiquette as a college assistant. Also answer the greeting gently like hi good bye, how are you and other generic answers.
            <context>
            {context}
            </context>
            Question
            {message.content}"""}]
    if message.content:
        stream = await client.chat.completions.create(
            messages=prompt, stream=True, **settings
        )
        async for part in stream:
            if part.choices[0].delta.content is not None:
                token = part.choices[0].delta.content
                await msg.stream_token(token)



        


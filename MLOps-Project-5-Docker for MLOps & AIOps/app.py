# Import necessary libraries
from fastapi import FastAPI                     # Web framework to build the API
from openai import OpenAI                       # OpenAI SDK to interact with GPT Assistants
from dotenv import load_dotenv                  # To load environment variables from a .env file
import os                                       # To access environment variables
from pydantic import BaseModel                  # For request body validation
import uvicorn                                  # ASGI server to run the FastAPI app

# Load environment variables from .env file
load_dotenv()

# Fetch the OpenAI Assistant ID and API Key from environment variables
assistant_id = os.getenv("ASSISTANT_ID")
api_key = os.getenv("OPEN_AI_API_KEY")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

# Create a FastAPI app instance
app = FastAPI()

# Define the structure of the expected POST request body
class ChatRequest(BaseModel):
    message: str

# Define a simple health check or welcome endpoint
@app.get("/")
def root():
    return {"message": "Hello Welcome to the Chatbot Assistant"}

# Define a POST endpoint to handle chat messages
@app.post("/chat")
def chat(body: ChatRequest):
    prompt = body.message  # Extract the user's message from the request

    # Step 1: Create a new thread (a conversation container)
    thread = client.beta.threads.create()

    # Step 2: Add the user's message to the thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    # Debug print (can be removed in production)
    print(assistant_id)
    print(type(assistant_id))

    # Step 3: Start a "run" — this prompts the assistant to process the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Step 4: Poll the run status until it completes
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run.status == "completed":
            # Step 5: Once completed, fetch and return the assistant's reply
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            message_content = messages.data[0].content[0].text.value
            break;

    return message_content  # Return the assistant's response to the user

# Entry point to run the FastAPI app using Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI                    # FastAPI for creating APIs
from openai import OpenAI                      # OpenAI client for calling the API
from pydantic import BaseModel                 # For request body validation
import uvicorn                                 # To run the FastAPI server
import config                                  # To load hardcoded API key + assistant ID
import time                                    # For adding delay inside the polling loop

# Load assistant ID and API key from config file
assistant_id = config.assistant_id
api_key = config.api_key

# Create the OpenAI client using the provided API key
client = OpenAI(api_key=api_key)

# Create an instance of the FastAPI app
app = FastAPI()

# Define a Pydantic model to validate incoming JSON body
class Body(BaseModel):
    text: str   # Incoming JSON must have a "text" field (user's prompt)


# Basic test route to make sure the server is running
@app.get("/")         
async def root():     
    return {"message": "Welcome to ChatGPT AI Application"}


# Another simple test route
@app.get("/demo")      
def welcome():
    return {"message": "Welcome Home!"}


# Dummy POST route to test incoming body data (for testing)
@app.post("/dummy")     
def demo_function(data: Body):
    return {"message": data.text}


# Main endpoint that connects to OpenAI Assistant
@app.post("/response")
def generate(body: Body):
    # Step 1: Extract user prompt from request body
    prompt = body.text

    # Step 2: Create a new thread (each thread holds a conversation)
    thread = client.beta.threads.create()

    # Step 3: Add the user prompt into the thread as a message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",               # Role must be "user"
        content=prompt             # The user's message
    )

    # Step 4: Start a run — this tells the assistant to respond to the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Step 5: Polling loop — check every second until the assistant is done
    # This part re-fetches the current status of the assistant "run" every loop iteration 
    # — kind of like saying: "Hey OpenAI, has the assistant finished processing this request yet?"
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        # This checks whether the assistant's job is done. 
        # When status == "completed", we know the assistant finished generating a response.
        if run.status == "completed":
            # Step 6: Once complete, fetch the response messages
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            latest_message = messages.data[0]   # Get the latest response
            text = latest_message.content[0].text.value  # Extract the response text
            break;

        # Optional: Sleep to avoid hammering the API too fast
        time.sleep(1)

    # Step 7: Return the assistant's reply as the API response
    return {"response": text}


# Entry point — run the server on port 80
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)

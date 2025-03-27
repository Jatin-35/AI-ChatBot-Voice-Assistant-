import cohere   # import the cohere library for AI service
from rich import print # import thr rich library to enhance terminal output
from dotenv import dotenv_values # Import dotenv to load environment variables from a .env file

# load the environment variable from the .env file
env_vars = dotenv_values(".env")

# retrieve API Key

CohereAPIKey = env_vars.get("CohereAPIKey")

# Create a cohere client using the following API Kay

co = cohere.Client(api_key=CohereAPIKey)

# Define a list of recognized keyword functions for task categorization.
funcs = [
    "exit" , "general" , "realtime" , "open" , "close", "play",
    "generate image"  , "system" , "content" , "google search",
    "youtube search" , "reminder" 
]

# Initialize the empty list to store user messages 
messages = []

# Define a preamble that guides the Ai model on how to categorize queries
preamble = """"""

# Define a Chat History with predefined user - ChatBot interactions for content.
ChatHistory = [
    {"role" : "User" , "message" : "how are you?"},
    {"role" : "ChatBot" , "message" : "general how are you?"},
    {"role" : "User" , "message" : "Do you like pizza?"},
    {"role" : "ChatBot" , "message" : "general Do you like pizza"},
    {"role" : "User" , "message" : "open chrome and tell me about Mahatama Gandhi."},
    {"role" : "ChatBot" , "message" : "open open, general tell me about Mahatama Gandhi."},
    {"role" : "User" , "message" : "open chrome and firefox."},
    {"role" : "ChatBot" , "message" : "open chrome, open firefox."},
    {"role" : "User" , "message" : "what is today's date and by the way remind me that i have a dance performance on 5th aug at 11pm."},
    {"role" : "ChatBot" , "message" : "general what is today's date , reminder 11:00pm 5th aug dancing performance."},
    {"role" : "User" , "message" : "chat with me."},
    {"role" : "ChatBot" , "message" : "general chat with me."},
]

# Define main function for decision-making on queries
def FirstLayerDMM(prompt : str = "test") :
    # add the user's query to the message list.
    messages.append({"role" : "User" , "content" : f"{prompt}"})
    
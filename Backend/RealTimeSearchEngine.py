# from serpapi import Googlesearch as search
import requests
from groq import Groq  # Importing the Groq library to use its API.
from json import load , dump # Importing function to read and write JSON file.
import datetime # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values # Importing dotenv_values to read environment variables from a .env file.

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve Specific environment variables for the ChatBot configuration.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
SerpAPIKey = env_vars.get("SerpAPIKey")

# initialize the Groq client with the provided API Key.
client = Groq(api_key=GroqAPIKey)

# Define the system instruction for the Chatbot.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Try to load the chat log from a JSON file , or create an empty one if it doesn't exist.
try :
    with open(r"Data\ChatLog.json" , "r") as f :
        messages = load(f)
except :
    with open(r"Data\ChatLog.json" , "w") as f :
        dump([] , f)
        
# # function to perfrom a Google Search and format the results.
# def GoogleSearch(query) :
#     results = list(search(query , advanced= True , num_results= 5))
#     Answer = f"The Search result for '{query}' are:\n[start]\n"
    
#     for i in results :
#         Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
        
#     Answer += "[end]"
#     return Answer

# Function to perform a Google Search using SerpAPI
def GoogleSearch(query):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SerpAPIKey,
        "num": 5,
        "engine": "google"
    }

    response = requests.get(url, params=params)
    
    try:
        data = response.json()
        Answer = f"The Search result for '{query}' are:\n[start]\n"

        for result in data.get("organic_results", []):
            title = result.get("title", "No Title")
            snippet = result.get("snippet", "No Description")
            Answer += f"Title: {title}\nDescription: {snippet}\n\n"
        Answer += "[end]"
        return Answer

    except Exception as e:
        return f"An error occurred while processing search results: {str(e)}"

# Function to clean up the answer by removing empty lines.
def AnswerModifier(Answer) :
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    # non_empty_lines = []
    # for line in lines:
    #     if line.strip():
    #         non_empty_lines.append(line)
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Predefined chatbot conversation system message and an initial user message.
SystemChatBot = [
    {"role" : "system" , "content" : System},
    {"role" : "user" , "content" : "Hi"},
    {"role" : "assistant" , "content" : "Hello, how can I help you?"}
]

# Function to get real-time information like the current date and time.
def Information() :
    data = ""
    current_date_time = datetime.datetime.now()  # Get the current date and time.
    # Output for current_date_time is 2025-03-28 22:41:58.194932,
    day = current_date_time.strftime("%A")  # Day of the week.
    date = current_date_time.strftime("%d")  # Day of the month.
    month = current_date_time.strftime("%B") # Full Month name.
    year = current_date_time.strftime("%Y") # Year.
    hour = current_date_time.strftime("%H") # Hour in 24 hr format.
    minute = current_date_time.strftime("%M") # Minute.
    second = current_date_time.strftime("%S") # Second.
    data += f"Use This Real-time Information if needed\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours ,{minute} minutes , {second} seconds.\n"
    return data

# Function to handle Real-time search and response generation.
def RealtimeSearchEngine(prompt) :
    global SystemChatBot , messages
    
    # Load the chat log from the JSON file.
    with open(r"Data\ChatLog.json" , "r") as f :
        messages = load(f)
    messages.append({"role" : "user" , "content" : f"{prompt}"})
    
    # Add Google search results to the system chatbot messages.
    SystemChatBot.append({"role" : "system" , "content" : GoogleSearch(prompt)})
    
    # Generate a response using the Groq Client.
    completion = client.chat.completions.create(
        model= "llama3-70b-8192",
        messages= SystemChatBot + [{"role" : "system" , "content" : Information()}] + messages,
        temperature= 0.7,
        max_tokens= 2048,
        top_p=1,
        stream=True,
        stop=None
    )
    
    Answer = ""
    
    # Concatenate response chunks from the streaming output.
    for chunk in completion:
        if chunk.choices[0].delta.content :
            Answer += chunk.choices[0].delta.content
            
    # Clean Up the response.
    Answer = Answer.strip().replace("<\s>" , "")
    messages.append({"role" : "assistant" , "content" : Answer})
    
    # Save the updated chat log back to the JSON file.
    with open(r"Data\ChatLog.json" , "w") as f :
        dump(messages , f , indent = 4)
        
    # Remove the most recent system message from the chatbot conversation.
    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

# Main entry point of the program for interactive querying.
if __name__ == "__main__" :
    while True :
        prompt = input("Enter your Query: ")
        print(RealtimeSearchEngine(prompt))
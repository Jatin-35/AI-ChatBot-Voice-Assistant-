from groq import Groq # Import the Groq library to use its API
from json import load , dump  # importing functions to read and write JSON file.
import datetime # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values # Importing dotenv_values to read environment variables from .env file.

# Load environment variables  from the .env file.
env_vars = dotenv_values(".env")

# Retrieve Specific environment variables for username , assistant name and API Key.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq Client using the provided API Key
client = Groq(api_key = GroqAPIKey)

# Initialize an empty list to store chat messages.
messages = []

# Define a system message that provide context to the AI ChatBot about its role and behavior.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# A list of system instructions for the chatbot.
SystemChatBot = [
    {"role" : "system" , "content" : System}
]

# Attempt to load the chat log from a JSON file.
try : 
    with open(r"Data\ChatLog.json", "r") as f :
        messages = load(f) # Load existing message from the chat log.
except FileNotFoundError :
    # If the file doesn't exist, create an empty JSON file to store chat logs.
    with open(r"Data\ChatLog.json", "w") as f :
        dump([], f)
        
# Function to get real-time date and time information.
def RealtimeInformation() :
    current_date_time = datetime.datetime.now()  # Get the current date and time.
    # Output for current_date_time is 2025-03-28 22:41:58.194932,
    day = current_date_time.strftime("%A")  # Day of the week.
    date = current_date_time.strftime("%d")  # Day of the month.
    month = current_date_time.strftime("%B") # Full Month name.
    year = current_date_time.strftime("%Y") # Year.
    hour = current_date_time.strftime("%H") # Hour in 24 hr format.
    minute = current_date_time.strftime("%M") # Minute.
    second = current_date_time.strftime("%S") # Second.
    
    
    # Format the information into a string.
    data = f"Please use this real-time information if needed,\n"
    data += f"Day : {day}\nDate: {date}\nMonth : {month}\nYear : {year}\n"
    date += f"Time : {hour} hours : {minute} minutes :{second} seconds.\n"
    return data
        
# Function to modify chatbot's response for better formatting
def AnswerModifier(Answer) :
    lines = Answer.split('\n')  # Split the responses into lines 
    non_empty_lines = [line for line in lines if line.strip()] # Remove empty lines
    modified_answer = '\n' .join(non_empty_lines)  # Join the cleaned lines back together
    return modified_answer

# Main ChatBot function to handle user Queries
def ChatBot(Query, has_retried=False):
    """This function sends the user's query to the chatbot and returns AI's response."""

    try:
        # Load the existing chat log from the JSON file
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)

        # Append the user's query
        messages.append({"role": "user", "content": f"{Query}"})

        # Make a request to the Groq API
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""  # Initialize empty answer

        # Stream the response
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")  # Clean up

        # Save the assistant's response
        messages.append({"role": "assistant", "content": Answer})

        # Update chat log
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer=Answer)

    except Exception as e:
        print(f"Error: {e}")
        if not has_retried:
            # Reset the chat log and retry once
            with open(r"Data\ChatLog.json", "w") as f:
                dump([], f, indent=4)
            return ChatBot(Query, has_retried=True)
        else:
            return "Sorry, an internal error occurred. Please try again later."

    
# Main program entry point.
if __name__ == "__main__" :
    while True :
        user_input = input("Enter Your Question : ") # Prompt the user for a question.
        print(ChatBot(user_input)) # Call the chatbot function and print its response.
        
        
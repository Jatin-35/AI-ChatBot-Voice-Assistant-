# Import required Library.
from AppOpener import close , open as appopen # IMport functions to open and clos app.
from webbrowser import open as webopen # Import webbrowser functionality.
from pywhatkit import search , playonyt # IMport functions to google search and toutube playback.
from dotenv import dotenv_values # Import dotenv to manage environment variables.
from bs4 import BeautifulSoup # Import beautiful soup for parsing HTMl content.
from rich import print # Import rich for styled console output.
from groq import Groq # Import Groq for Ai chat functionality.
import webbrowser # import webbrowsers for opening URls.
import subprocess # IMport subprocess for interacting with system.
import requests # Import requests for making HTTP requests.
import keyboard # Import keyboard for keyboard related action.
import asyncio # Import asyncio for asynchronous programming.
import os # Import os for operating system functionality.

# Load the environment variable from the .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey") # Retrieve the Groq API Key

# Define CSS classes for parsing specific elements in HTML content.
classes = ["zCubwf" , "hgKElc" , "LTKOO sY7ric" , "Z0LcW" , "gsrt vk_bk FzvWSb YwPhnf" , "pclqee","tw-Data-text tw-text-small tw-ta",
           "IZ6rdc" , "O5uR6d LTKOO" , "vlzY6d" , "webanswers-webanswers_table__webanswers-table" ,"dDoNo ikb4Bb  gsrt" , "sXLaOe" ,
           "LWkfKe" , "VQF4g" , "qv3Wpe" , "kno-rdesc" , "SPZz6b"]

# Define a user-agent for making web requests.
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'

# Initialize the Groq client with the API Key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority ; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional question or support you may need-don't hesitate to ask."
]

# list to store ChatBot message,
messages = []

# system message to provide context to the chatbot.
SystemChatBot = [{"role" : "system" , "content" : f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letter" }]

# Function to perform a google search.
def GoogleSearch(Topic) :
    search(Topic) # Use pywhatkit's search function to perform a Google Search.
    return True # Indicate Success.

# Function to generate content using AI and save it to a file.
def Content(Topic) :
    
    # Nested function to open a file in notepad.
    def OpenNotepad(File) :
        default_text_editor = 'notepad.exe' # Default text editor.
        subprocess.Popen([default_text_editor , File]) # Open the file in Notepad.
        
    # Nested function to generate content using the Ai ChatBot.
    def ContentWriterAI(prompt) :
        messages.append({"role" : "user" , "content" : f"{prompt}"}) # Add the user prompt to the message.
        
        completion = client.chat.completions.create(
            model = "llama-3.3-70b-versatile", # Specify the AI Model
            messages= SystemChatBot + messages , # Include systems Interactions and chat history.
            max_tokens= 2048 , # Limit the maximum tokens in the responses.
            temperature= 0.7, # Adjust response randomness.
            top_p = 1 , # Use necleus sampling for response diversity.
            stream = True , # Enable streaming response
            stop = None # Allow the model.
        )
        
        Answer = "" # Initialize the empty string for responses.
        
        # Process streamed responses chunks.
        for chunk in completion :
            if chunk.choices[0].delta.content : # Check for the conmtent in the current chunk.
                Answer += chunk.choices[0].delta.content # Add the content to the answer.
            
        Answer = Answer.replace("</s>" , "") # Remove unwanted token from the response.
        messages.append({"role" : "assistant" , "content" : Answer}) # Add the AI response to the message.
        return Answer
    
    Topic : str = Topic.replace("Content " , "" ) # Remove "Content " from the topic.
    ContentByAI = ContentWriterAI(Topic) # Generate content using AI.
    
    # Save the generated content to a text file.
    with open(rf"Data\{Topic.lower().replace(' ' , '')}.txt" , "w" , encoding="utf-8") as file :
        file.write(ContentByAI) # Write the generated content to the file.
        file.close()
        
    OpenNotepad(rf"Data\{Topic.lower().replace(' ' ,'')}.txt") # open the file in Notepad.
    return True # Indicate Success.


def YoutubeSearch(Topic) :
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}" # Construct the Youtube search URl
    webbrowser.open(Url4Search) # Open the search URL in the default browser.
    return True # Indicate Success.

# Function to play a video on Youtube.
def PlayYoutube(Topic) :
    playonyt(Topic) # Use pywhatkit's playonyt function to play the video.
    return True # Indicate Success.

# Function to open a app or a relevent webpage.
def OpenApp(app, sess=requests.session()):
    """
    Opens an application or navigates to its relevant website.
    
    Args:
        app (str): Name of the application to open
        sess (requests.Session, optional): Session for HTTP requests
        
    Returns:
        bool: True if successful, False otherwise
    """
    # First attempt: Try to open locally installed app
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        print(f"Successfully opened {app} locally")
        return True
    except Exception as e:
        print(f"Could not open {app} locally: {str(e)}")
        print(f"Attempting to find {app} online...")
    
    # Second attempt: Try to search for the app's official website
    try:
        # Extract domain and search
        search_query = f"{app} official website download"
        url = f"https://www.google.com/search?q={search_query}"
        
        # Set headers for the request
        headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1"
        }
        
        # Get search results
        response = sess.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to retrieve search results. Status code: {response.status_code}")
            raise Exception("Search failed")
            
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        
        # Find links in search results (prioritize potential official domains)
        app_keywords = [kw.lower() for kw in app.split()]
        
        # Method 1: Look for links in search results
        for a in soup.find_all('a', href=True):
            href = a.get('href')
            # Skip search engine domains
            if href.startswith('http') and not any(domain in href.lower() for domain in ['google.com', 'youtube.com']):
                # Check if URL might be related to the app (contains app name parts)
                if any(keyword in href.lower() for keyword in app_keywords):
                    links.append(href)
        
        # Method 2: Look for specific search result containers
        for div in soup.find_all(['div', 'a'], class_=['g', 'yuRUbf', 'DKV0Md']):
            link = div.find('a')
            if link and link.get('href'):
                href = link.get('href')
                if href.startswith('http') and not any(domain in href.lower() for domain in ['google.com', 'youtube.com']):
                    links.append(href)
        
        # Method 3: Look for links in specific data attributes
        for element in soup.find_all(['div', 'a'], attrs={'data-hveid': True}):
            link = element.find('a')
            if link and link.get('href'):
                href = link.get('href')
                if href.startswith('http') and not any(domain in href.lower() for domain in ['google.com', 'youtube.com']):
                    links.append(href)
        
        # Remove duplicates
        links = list(set(links))
        
        # If links were found, open the first one
        if links:
            # Safety check: Ensure the link is a well-formed URL
            link = links[0]
            if not link.startswith('http'):
                link = 'https://' + link
                
            print(f"Opening website for {app}: {link}")
            webopen(link)
            return True
    
    except Exception as e:
        print(f"Error during web search: {str(e)}")
    
    # Final attempt: Generate a URL based on the app name
    try:
        # Create a domain name from the app name
        clean_name = ''.join(c.lower() for c in app if c.isalnum())
        direct_url = f"https://www.{clean_name}.com"
        print(f"No search results found. Trying generated URL: {direct_url}")
        webopen(direct_url)
        return True
    except Exception as e:
        print(f"Failed to open {app}: {str(e)}")
        return False

# OpenApp("twitteer")  
# Function to close an Application.
def CloseApp(app) :
    
    if "chrome" in app :
        pass # Skip if the app is chrome.
    else : 
        try : 
            close(app , match_closest= True , output= True , throw_error= True) # Attempt ot close the app.
            return True # Indicate Success.
        except :
            return False # Indicate Failure.
        
# Function to execute system-level commands.
def System(command) :
    
    # Nested function to mute the system volume.
    def mute() :
        keyboard.press_and_release("volume mute")  # Simulate the mute key press.
        
    # Nested function to unmute the system volume.
    def unmute() :
        keyboard.press_and_release("volume unmute")  # Simulate the ynmute key press.
        
    # Nested function to increase the system volume.
    def volume_up() :
        keyboard.press_and_release("volume up")  # Simulate the volume up key press.
        
    # Nested function to decrease the system volume.
    def volume_down() :
        keyboard.press_and_release("volume down")  # Simulate the volume down key press.
         
    # Execute the appropriate command.
    if command == "mute" :
        mute() # Mute the system volume.
    elif command == "unmute" :
        unmute() # Unmute the system volume.
    elif command == "volume up" :
        volume_up() # Increase the system volume.
    else :
        volume_down() 
    
    return True # Inidicate Success.

# Asynchrouns function to transalte and execute user command.
async def TranslateAndExecute(commands : list[str]) :
    
    funcs = [] # List to store asynchronous tasks.
    
    for command in commands :
        
        if command.startswith("open ") : # Handle "open" commands.
            
            if "open it" in command : # Ignore "open it " commands.
                pass
            
            if "open file" == command : # Ignore "open file" commands.
                pass
            
            else :
                fun = asyncio.to_thread(OpenApp , command.removeprefix("open ")) # Scheduling app opening.
                funcs.append(fun)
                
        elif command.startswith("general ") : # Placeholder for general commands.
            pass
        
        elif command.startswith("realtime ") : # Placeholder for realtime commands.
            pass
    
        elif command.startswith("close ") : # Handle "close " command.
            fun = asyncio.to_thread(CloseApp , command.removeprefix("close ")) # Scheduling app closing.
            funcs.append(fun)
                
        elif command.startswith("play ") : # Handle "close " command.
            fun = asyncio.to_thread(PlayYoutube , command.removeprefix("play ")) # Scheduling Youtube playback.
            funcs.append(fun) 
            
        elif command.startswith("content ") : # Handle "close " command.
            fun = asyncio.to_thread(Content , command.removeprefix("content  ")) # Scheduling Content Creation.
            funcs.append(fun) 
            
        elif command.startswith("google search ") : # Handle "google search " command.
            fun = asyncio.to_thread(GoogleSearch , command.removeprefix("google search ")) # Scheduling google search.
            funcs.append(fun) 
         
        elif command.startswith("youtube search ") : # Handle "youtube search " command.
            fun = asyncio.to_thread(YoutubeSearch , command.removeprefix("youtube search ")) # Scheduling youtube search.
            funcs.append(fun)    
     
        elif command.startswith("system ") : # Handle "system "" command.
            fun = asyncio.to_thread(System , command.removeprefix("system ")) # Scheduling system command.
            funcs.append(fun)
            
        else :
            print(f"No Function Found. For {command}") # Print an error for unrecognized command.
            
    results = await asyncio.gather(*funcs) # execute all commands concurrenty.
    
    for result in results : # Process the results.
        if isinstance(result , str) :
            yield result
        else :
            yield result
            
# Asynchronous function to auto mate command execution.
async def Automation(commands : list[str]) :
    
    async for result in TranslateAndExecute(commands) : # Translate and execute commands.
        pass
    
    return True # Indicate Success.

if __name__ == "__main__" :
    asyncio.run(Automation(["open instagram"]))
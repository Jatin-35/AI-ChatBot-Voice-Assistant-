from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# Load environment variables from the .env file. 
env_vars = dotenv_values(".env")
# Get the input language setting from the environment variable.
InputLanguage = env_vars.get("InputLanguage")

# #define the Html code for the sppech recognition interface.
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace the language setting in the HTML code with the input language from the environment variables.
HtmlCode = str(HtmlCode).replace("recognition.lang = '';" , f"recognition.lang = '{InputLanguage}';")

# Write the modified HTML code to a file.
with open(r"Data\Voice.html","w") as f :
    f.write(HtmlCode)
    
# Get the current working directory.
current_dir = os.getcwd()
# Generate the file path from the HTML file.
Link = f"{current_dir}/Data/Voice.html"

# Set the chrome options for your WebDriver.
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")
# Initialize the Chrome Webdriver using the ChromeDriverManager.
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service= service , options= chrome_options)

# Define the path for temperary files
TempDirPath = rf"{current_dir}/Frontend/Files"

# Function to the assistant's status by writing it to a file.
def SetAssisatntStatus(status) :
    with open(rf"{TempDirPath}/Status.data" , "w" , encoding = 'utf-8') as file :
        file.write(status)
        
# Function to modify a quert to ensure proper punctuation and formatting.
def QueryModifier(Query) :
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how" , "what" , "who" , "where" , "when" , "why" ,"whose" , "whom" , "can you" , "what's" , "where's" , "how's" , "can you"]
    
    # Check if a question is  a query and add question mark if necessary.
    if any(word + " " in new_query for word in question_words) :
        if query_words[-1][-1] in ['.' , '?' ,'!'] :
            new_query = new_query[:-1] + "?"
        else :
            new_query += "?"
    else :
        # Add a period if the query is not a question.
        if query_words[-1][-1] not in ['.' , '?' ,'!'] :
            new_query = new_query[:-1] + "."
        else :
            new_query += "."
            
    return new_query.capitalize()

# Function to translate text into English using the mtranslate library.
def UniversalTranslate(Text) :
    english_translation = mt.translate(Text , "en", "auto")
    return english_translation

# Function to perform speech recognition using the WebDriver.
def SpeechRecognition() :
    # Open the HTML file in the browser.
    driver.get("file:///" + Link)
    # Start speech rocognition by clicking the start button.
    driver.find_element(by = By.ID , value = "start" ).click()
    
    while True :
        try :
            # Get the recognized text from the HTMl output file.
            Text = driver.find_element(by = By.ID , value= "output").text
            
            if Text :
                # Stop recognizing by clicking the stop button.
                driver.find_element(by = By.ID , value= "end").click()
                 
                # If the input language is English , return the Modified Query.
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower() :
                    return QueryModifier(Text)
                else :
                    #  If the input language is not English , translate the text and return it.
                    SetAssisatntStatus("Translating...")
                    return QueryModifier(UniversalTranslate(Text))
                
        except Exception as e :
            pass
        
# Main execution Block
if __name__ == "__main__" :
    while True :
        # Continuously perfrom DSpeech Recognition and print the recognized text.
        Text = SpeechRecognition()
        print(Text)
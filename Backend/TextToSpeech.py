import pygame # Import pygame library to handle audio playback.
import random #  Import random for generating random choices.
import asyncio # Import asyncio for asynchronous operations.
import edge_tts # Import edge_tts for Text to Speech functionality.
import os # Import os for file path handling
from dotenv import dotenv_values # Import dotenv for reading environment variables from a .env file.

# Load environment variables for a .env file.
env_vars = dotenv_values('.env')
AssistantVoice = env_vars.get("AssistantVoice")

# Asynchronous function to convert text to an audio file.
async def TextToAudioFIle(text) -> None :
    file_path = r"Data\speech.mp3" # Define the path where the speech file will be saved.
    
    if os.path.exists(file_path) : # Check if the file already exists.
        os.remove(file_path) # If the file exists, delete it to avoid overwritting errors.
    
    # Create the communication object to create speech.
    communicate = edge_tts.Communicate(text , AssistantVoice , pitch= '+5Hz' , rate= '+13%')
    await communicate.save(r'Data\speech.mp3') # Save the generated speech as an MP3 file.
    
# Function to manage Text-to-Speech (TTS) functionality.
def TTS(Text , func = lambda r= None :True) :
    while True :
        try : 
            # Convert text to an audio file asynchronously.
            asyncio.run(TextToAudioFIle(Text))   
            
            # Initialise pygame mixer for audio playback.
            pygame.mixer.init() 
            
            # Load the generated speech file into the pygame.
            pygame.mixer.music.load(r'Data\speech.mp3')
            pygame.mixer.music.play() # Play the audio.
            
            # loop until the audio is done playing or the function stops.
            while pygame.mixer.music.get_busy():
                if func() == False : # Check if the external function return false.
                    break
                pygame.time.Clock().tick(10) # Limit the loop to 10 ticks per second.
                
            return True # Return True if the audio played sucessfully.
        
        except Exception as e : # Haandling any exception during during the process.
            print(f"Error in TTS: {e}") # Print the error message.
            
        finally :
            try :
                # Call the provided function with False to signal the end of TTS.
                func(False)
                pygame.mixer.music.stop() # Stop the audio playback.
                pygame.mixer.quit() # Quit the pygame mixer.
                
            except Exception as e :
                print(f"Error in finally Block: {e}" )   
    
# Function to manage Text-to-Speech with additional response for long text.
def TextToSpeech(Text , func = lambda r = None : True) :
    Data = str(Text).split(".") # Split the text by periods into a list of sentences.
    
    # List of predefined responses for cases where the text is too long.
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]
    
    # If the text is very long (more than 4 sentences and 250 characters ) , add a response message.
    if len(Data) > 4 and len(Text) >= 250 :
        TTS(" ".join(Text.split(".")[0:2]) + ". " + random.choice(responses) , func)
        
        # Otherwise just play the whole text.
    else :
        TTS(Text , func)
        
# Main execution loop.
if __name__ == "__main__" :
    while True :
        # Prompt user for input and paste it to TexttoSpeech function.
        TextToSpeech(input("Enter the text: "))
import speech_recognition as sr
import pyttsx3
from functions import speak, save_to_file, dalleUrl, chatgpt, basicFormat,formatImage,formatQuestion,append_to_images,append_to_last_line,basicFormatAdded,hex_to_html,save_image_as_rgba,list_files_in_directory,append_to_image_url,list_files_in_txt_file,formated_files_into_img_elements_from_txt_file

# Initialize recognizer object
r = sr.Recognizer()

# Function to convert speech to text
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Sorry, I did not understand that.")
        query = ""
    print(query)
    return query

# asks chat gpt a question
def ask_chat():
    speak("what would you like to ask")
    reminder = recognize_speech()
    answer = chatgpt(reminder)
    speak(answer)
    minutes = recognize_speech()
# Function to respond to the user's commands


# Function to set a reminder
def set_reminder():
    import time

    def word_to_number(word):
        numbers = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
            "eleven": 11,
            "twelve": 12,
            "thirteen": 13,
            "fourteen": 14,
            "fifteen": 15,
            "sixteen": 16,
            "seventeen": 17,
            "eighteen": 18,
            "nineteen": 19,
            "twenty": 20,
            "thirty": 30,
            "forty": 40,
            "fifty": 50,
            "sixty": 60,
            "seventy": 70,
            "eighty": 80,
            "ninety": 90,
            "hundred": 100,
            "thousand": 1000,
            "million": 1000000,
            "billion": 1000000000
        }
        
        # Convert word number to integer
        if word in numbers:
            return numbers[word]
        elif "-" in word:
            # Handle numbers with hyphens, like "twenty-one"
            parts = word.split("-")
            if len(parts) == 2 and parts[0] in numbers and parts[1] in numbers:
                return numbers[parts[0]] + numbers[parts[1]]
        elif "and" in word:
            # Handle numbers with "and", like "one hundred and twenty"
            parts = word.split("and")
            if len(parts) == 2 and parts[0] in numbers and parts[1] in numbers:
                return numbers[parts[0]] + numbers[parts[1]]
        else:
            # Handle larger numbers
            parts = word.split()
            total = 0
            current = 0
            for part in parts:
                if part in numbers:
                    current += numbers[part]
                elif part == "hundred":
                    current *= 100
                elif part == "thousand":
                    current *= 1000
                    total += current
                    current = 0
                elif part in ["million", "billion"]:
                    current *= numbers[part]
                    total += current
                    current = 0
            total += current
            return total

        return None

    def convert_word_to_int(string):
        # Split the string into words
        words = string.lower().split()
        
        # Convert any word numbers to integers
        for i in range(len(words)):
            num = word_to_number(words[i])
            if num is not None:
                words[i] = str(num)
        
        # Join the words back together with spaces
        return ' '.join(words)


    speak("What would you like me to remind you about?")
    reminder = recognize_speech()
    
    # Keep asking for the reminder time until a valid integer is provided
    while True:
        speak("In how many minutes?")
        try:
            minutes = int(convert_word_to_int(recognize_speech()))
            break
        except ValueError:
            speak("Sorry, I didn't understand. Please try again.")
            continue
    
    seconds = minutes * 60
    speak(f"I will remind you about {reminder} in {minutes} minutes.")
    time.sleep(seconds)
    speak(f"Reminder: {reminder}")

    
# Function to create a to-do list
def create_todo_list():
    speak("What tasks would you like to add?")
    task = recognize_speech()
    # Use a text file to store the to-do list
    
# Function to search the web
def search_web():
    import webbrowser
    speak("What would you like me to search for?")
    query = recognize_speech()
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(url)
    speak("Here is what I found for " + query)


def run():
    print("Ran")

def photoFunk():
    speak("what photo would you like?")
    query = recognize_speech()
    speak("here is your photo")
    print(query)
    dalleUrl(query)


if __name__ == "__main__":
    run()
    speak("Hi, how can I help you today?")
    while True:
        command = recognize_speech().lower()
        if "set reminder" in command:
            set_reminder()
        elif "create to-do list" in command:
            create_todo_list()
        elif "ask chat" in command:
            ask_chat()
        elif "search web" in command:
            search_web()
        elif "make photo" in command:
            photoFunk()
        elif "exit" in command:
            speak("Goodbye!")
            break
# https://www.w3schools.com/python/ used for general code 
# Basic Chatbot code from https://www.youtube.com/watch?v=5MvYe44zen4
# Chat GTP used for trouble shooting errors
# Text to scpeech from https://pypi.org/project/gTTS/ text to speech


import openai
import random
import serial
import time
import threading
from gtts import gTTS
from pynput.mouse import Listener

# Chat GTP Model 
openai.api_key = "private-key"
model_engine = "text-davinci-003"

# Open Arduino the serial port connection
ser = serial.Serial('COM3', 9600)  

# Define mouse click variables
click_count = 0 
stop_listening = False  # Flag to stop listening for mouse clicks

# Define Arduino variables
arduino_listener = None  # Variable to hold the Arduino listener thread
received_ones = 0 # Counter for received '1' from Arduio
received_twos = 0
received_threes = 0

mario_side_quest = None

#--------------------------------- Set Up --------------------------------------------

# Here is a list of placeholder variables of data which can be collected from
# the Super Mario Lego experience set via the bluetooth module in Mario.


#Start and End timer and Interactive Bricks:
level_timer = 0 #Time placeholder for game length
warp_pipe = 1 #Trigger to start level and timer
goal_pole = 0 #Trigger to end level and timer


#Side Quest Interactive Brick
question_block = 1 #Triggers Mario Side Quest

#Barcode Actions - Mario's interaction with interactive bricks
jumped_on_bowserjr = 0
jump_on_goomba = 1
balance_on_bridge = 1
fly_on_cloud = 1

# Mario Colour Scanner Data
blue_water_swimming = 0
red_lava_fall = 1
green_grass_run = 0

#Accelerometer Data from Mario that could be interpreted as:
fell_over = 0
flying = 0
front_flip = 0
back_flip = 0
cartwheel = 1

#Mario Coin Counter
coin_counter = 25



#-------------------------------- Start of Game -----------------------------------
# To trigger the generation of a Side Quest, Mario needs to jump on the
# question block where there is a 1 in 5 chance a quest will be generated.
# Otherwise the block will behave normally giving coins and powerups.  



# Check if 'question_block' is pressed
if question_block >= 1:
        # Introduce a 1 in 5 chance of responding with the current theme
   # if random.randint(1, 5) == 1:
        
        theme_actions = {

    "The sky has turned to pink custard!": {
        "actions": [
            "Jump on the Cloud and surf the custard collecting coins in the sky!",
            "Make a tower as high as you can to reach above the custard and stay safe!",
            "Annoy Goomba by jumping on him to stay afloat!"
           
        ],
        "time_limit": "As fast as you as you can!",
    },
    
      "The world has turned into Jelly!": {
        "actions": [
            "Mario falls off everything he jumps on!",
            "Jump the highest to collect the most coins!",
            "Don't let Mario get sucked into the Jelly!"
           
        ],
        "time_limit": "Be careful!",
    },
    
    
    "Bowser Jr has returned for revenge!": {
        "actions": [
            "Balance on the brigdge to avoid Bowser Jr",
            "Attack Bowser Jr and defeat him 3 times",
            "Ambush Bowser Jr! Hide then push him in the lava!",
            "Jump, cartwheel and flip to avoid Bowser Jr's attack!"	
           
        ],
        "time_limit": "Untill Bowser Jr surrenders and runs away",
    },
    }
        
        
        # Select a random theme from the list
        selected_theme = random.choice(list(theme_actions.keys()))
        
        # quest
        quest_theme = selected_theme 

        # Select a random action from the chosen theme
        selected_action = random.choice(theme_actions[selected_theme]["actions"])

        # Select a random time limit from the chosen theme
        selected_time_limit = theme_actions[selected_theme]["time_limit"]

        # Construct the initial_prompt with the selected theme, action, and time limit
        initial_prompt = f"{selected_theme}: discribe as Mario {selected_action} {selected_time_limit} instruct mario less than 30 words"
        
#     else:
#         
#         theme_actions = {
#              "Go Mario!": {
#        "actions": [
#            "Jump High!",
#            "Keep collecting coins!",
#         ],
#        },
# }
#                             
#         # selected_theme
#         selected_theme= "Go Mario!"
#         selected_action = random.choice(theme_actions[selected_theme]["actions"])
#         initial_prompt = f"{selected_action} encourage mario to win coins in less than 30 words"
#    

    
 
# Generate a statement about Super Mario using the chatbot
initial_response = openai.Completion.create(
    engine=model_engine,
    prompt=initial_prompt,
    max_tokens=50,  # Adjust the max_tokens as needed for the statement length
    n=1,
    stop=None,
    temperature=0.6,
)

# Extract and print the theme statemenet and AI-generated statement
initial_statement = initial_response.choices[0].text.strip()
print(f"Mario: {selected_theme}, {initial_statement}")


# ------------------ Text to Speech of Side Quest ------------------------------
# After the Side Quest has been generated it will be converted to speech and saved
# as an mp3 to be sent through bluetooth to Mario and played through his speaker.


# Rename statement for text to speech
mario_side_quest = initial_statement

# Convert the text story to speech using gTTS
tts = gTTS(text=mario_side_quest, lang='en')

# Save the speech to an audio file
tts.save("mario_side_quest.mp3")

# Play the audio file using Windows Media Player
#subprocess.Popen(["wmplayer.exe", "mario_side_quest.mp3"])


# ----------------------------Mario (Arduino) Communication -------------------------


# For demonstration purposes the mouse clicks here are used to print comments explaining
# how the application would work.

# After the above Side Quest has been annouced Mario will need to jump on the Warp Pipe
# to accept the Quest and additional time will be added to Mario's time display.

# During the Quest, data from Mario will be sent to the program relating to the above
# place holder variables. Such as how many times Mario jumped on Goomba, fell over,
# swam through water and collected coins.

# An Arduino with a Button has been connected to the program to replicate the data recived
# from LEGO Mario jumping on Bowser Jr.

# The Quest ends when Mario jumps on the Goal Pole or when the additional time runs out.

# Theses data points will then be used to generate a personalised story of Marios Quest. 
# This can then be sent to the LEGO Super Mario App. 


# Mouse click trigger sequence for creating personalised Quest Story
def on_click(x, y, button, pressed):
    global click_count, jumped_on_bowserjr, stop_listening, arduino_listener

    if pressed:
        click_count += 1
        
        # When mouse is clicked once print count down message and allow for arduino communication
        if click_count == 1: 
            print("App: 3..2..1 COMPLETE YOUR QUEST MARIO!!")
            
        # Once sufficient Arduino data has been recieved click mouse for second time to turn
        # off arduino listener and print message.
        elif click_count == 2:
            # Stop listening to Arduino data
            stop_listening = True
            if arduino_listener:
                arduino_listener.join()
            print("App: Story Incoming!")
  
        # When mouse is clicked for a third time generate story using data recived from arduino
        # (and placeholder variables).
        elif click_count == 3:
            prompt = f"Using {quest_theme} for context, generate in less than 50 words, a Super Mario Lego adventure story where Mario:"
            # Conditionally include warp_pipe
            if warp_pipe >= 1:
                prompt += f"\n- starts with jumping down the warp pipe"

        # Conditionally include jump_on_goomba
            if jump_on_goomba >= 1:
                prompt += f"\n- Annoy Goomba by jumping on him and defeating him ({jump_on_goomba} times)"

        # Conditionally include mario_fell_over
            if fell_over >= 1:
                prompt += f"\n- Mario accidently falls over ({fell_over} times)"
                
        # Conditionally include fly_on_cloud
            if fly_on_cloud >= 1:
                prompt += f"\n- Jumps on a cloud and surfs through the sky {fly_on_cloud}"
        
        # Conditionally include balance_on_bridge
            if balance_on_bridge >= 1:
                prompt += f"\n- Struggled to balanced on the bridge and tried not to fall off {balance_on_bridge}"

        # Conditionally include jump_on_bowserjr
            if jumped_on_bowserjr >= 1:
                prompt += f"\n- Jumped on the powerfull angry Bowser Jr and defeated him ({jumped_on_bowserjr} times)"
       
        # Conditionally include red_lava_fall
            if red_lava_fall >= 1:
                prompt += f"\n- Fell in the burning lava ({red_lava_fall} times)"
                
        # Conditionally include cartwheel
            if cartwheel >= 1:
                prompt += f"\n- Fell in the burning lava ({cartwheel} times)"

        # Conditionally include goal_pole
            if goal_pole >= 1:
                prompt += f"\n- ends with jumping on the a goal pole {goal_pole}"

        # Conditionally include coin_counter
            if coin_counter >= 1:
                prompt += f"\n- has earned {coin_counter} coins"

        # Conditionally include level_timer
            if level_timer >= 1:
                prompt += f"\n- it took {level_timer} seconds to complete the adventure"

        # End the prompt
                prompt += "\nTell the story of Mario's adventure."

        # Generate a story from the prompt
            response = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=200,  # Adjust the max_tokens to control the length of the story
                n=1,
                stop=None,
                temperature=0.8,  # Adjust the temperature for creativity
        )
  
          # Extract and print the AI-generated story
            story = response.choices[0].text.strip()
            print(story)
 


# Mouse click and arduino data listener threads to allow processes to
# run at the same time

def mouse_listener_thread():
    global stop_listening

    # Start listening for mouse clicks
    with Listener(on_click=on_click) as listener:
        listener.join()

    # When the listener thread exits, set stop_listening to True
    stop_listening = True


def arduino_listener_thread():
    global jumped_on_bowserjr, fell_over, goal_pole, stop_listening, received_ones, received_twos, received_threes

    while not stop_listening:
        # Read data from Arduino
        arduino_data = ser.read().decode('utf-8')

        # Check if the received data is '1'
        if arduino_data == '1':
            # Increment jump_on_bowserjr
            jumped_on_bowserjr += 1
            received_ones += 1  # Increment the count of received '1's
            # Print the current value of jump_on_bowserjr
            print(f"Mario: jumped_on_bowserjr: {jumped_on_bowserjr}")

        
        if arduino_data == '2':
            # Increment jump_on_bowserjr
            fell_over += 1
            received_twos += 1  # Increment the count of received '1's
            # Print the current value of mario_fell_over
            print(f"Mario: fell_over: {fell_over}")
  
          
        if arduino_data == '3':
            # Increment jump_on_bowserjr
            goal_pole += 1
            received_threes += 1  # Increment the count of received '1's
            # Print the current value of mario_fell_over
            print(f"Mario: jumped on the goal_pole: {goal_pole}")
            print("App: Mario scores received!")
            stop_listening = True
            break  # Exit the loop 

     
#         print("AI: Mario scores received!")
#         stop_listening = True
#         break  # Exit the loop
#          # Add a delay to avoid reading data too quickly
#         time.sleep(0.9)
      
                 
#       # Check if 3 has been to terminate arduino listener
#         if received_threes >= 1:
#             print("AI: Mario scores received!")
#             stop_listening = True
#             break  # Exit the loop 

        # Add a delay to avoid reading data too quickly
        time.sleep(0.9)
        

# Create a thread for the mouse listener
mouse_listener = threading.Thread(target=mouse_listener_thread)

# Create a thread for the Arduino data listener
arduino_listener = threading.Thread(target=arduino_listener_thread)

# Start both threads
mouse_listener.start()
arduino_listener.start()

# Wait for both threads to finish
mouse_listener.join()
arduino_listener.join()


       

 
  



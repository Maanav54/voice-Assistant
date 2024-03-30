import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import speech_recognition as sr
import pyttsx3
import datetime
import requests

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Placeholder variables for API keys and credentials
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "your_email@gmail.com"
smtp_password = "your_password"
openweathermap_api_key = "your_openweathermap_api_key"

# Placeholder list to store reminders
reminders = []

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for user input
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Can you please repeat?")
            return listen()
        except sr.RequestError:
            speak("Sorry, I'm having trouble processing your request. Please try again later.")
            return ""

# Function to send an email
def send_email(sender_email, receiver_email, subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Function to set a reminder
def set_reminder(date_time, description):
    reminder = {
        "date_time": date_time,
        "description": description
    }
    reminders.append(reminder)

# Function to fetch weather data
def fetch_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweathermap_api_key}"
    response = requests.get(url)
    data = response.json()
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    return f"The weather in {city} is currently {weather_description} with a temperature of {temperature} Kelvin and humidity of {humidity}%."

# Function to control smart home devices
def control_smart_home(device, action):
    return f"Controlling {device} {action}."

# Function to answer general knowledge questions
def answer_general_knowledge_question(question):
    return "Placeholder answer to the general knowledge question."

# Function to handle the user's input
def process_input():
    query = user_input.get("1.0", tk.END)
    response = "Processing your request..."
    assistant_response.config(state=tk.NORMAL)
    assistant_response.delete("1.0", tk.END)
    assistant_response.insert(tk.END, response)
    assistant_response.config(state=tk.DISABLED)
    if query.strip() == "":
        return
    elif "send email" in query:
        send_email(smtp_username, "recipient_email@gmail.com", "Test Email", "This is a test email.")
        response = "Email sent successfully."
    elif "set reminder" in query:
        set_reminder(datetime.datetime.now() + datetime.timedelta(hours=1), "Meeting at 2 PM")
        response = "Reminder set successfully."
    elif "weather update" in query:
        response = fetch_weather_data("New York")
    elif "control smart home" in query:
        response = control_smart_home("lights", "on")
    elif "general knowledge question" in query:
        response = answer_general_knowledge_question("Who is the president of the United States?")
    else:
        response = "Sorry, I don't understand. Please try again."
    assistant_response.config(state=tk.NORMAL)
    assistant_response.delete("1.0", tk.END)
    assistant_response.insert(tk.END, response)
    assistant_response.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Jarvis")

# Create a label for the assistant name
assistant_name_label = tk.Label(root, text="Jarvis", font=("Helvetica", 24))
assistant_name_label.pack(pady=10)

# Create a text area for user input
user_input = scrolledtext.ScrolledText(root, width=50, height=10, wrap=tk.WORD)
user_input.pack(pady=10)

# Create a button to speak the input
speak_button = tk.Button(root, text="Speak", command=process_input)
speak_button.pack(pady=5)

# Create a text area for assistant response
assistant_response = scrolledtext.ScrolledText(root, width=50, height=10, wrap=tk.WORD, state=tk.DISABLED)
assistant_response.pack(pady=10)

# Start the main event loop
root.mainloop()

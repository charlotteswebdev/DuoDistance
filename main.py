# Imports
import constants
#py file that sotres my api service key. Good professional practice to keep it separate from the public code.
#key obtained by creating an account on openweathermap.org
from datetime import datetime
#for formatting dates.
import random
#to perform random actions, I use it to get a random item from list love_letter_prompts.

#The modules below had to be installed before I could import them. This was achieved by using the terminal and pip.
#pip install requests, pip install pytz, pip install geopy, pip install timezonefinder
import requests
#for making API requests
import pytz
#to obtain the local time of selected location.
from geopy.geocoders import Nominatim
#used to find latitude and longitude coordinates location
from timezonefinder import TimezoneFinder
#find the timezone of location based on latitude and longitude coordinates


# Constants
service_key = constants.api_weather_key

# ASCII Art, to enhance UX
logo = """
 ,,-,-.,-. ,-. ,,-. ,-,-. ,-.-. ,-.. ,-. ,-.,-.-..
(( (  (   (   '(   ' (   '   ) '   )'   )   )  ) ))
 \\ \  \   \    \    ,\     /.    /    /   /  / //
   \\ \ /\ / \ /  \ /   \ /   \ /  \ / \ /\ / //
    '' '  '   '    '     '     '    '   '  ' ''
"""
hourglass = """
.____.
|(__)|
| )( | 
|(::)|
"""
letter_logo = """
    _________
   |\       /|
   | \     / |
   |  `...'  |
   |__/___\__|
"""

love_letter_prompts = [
    "Our funniest memory together...",
    "You've taught me...",
    "I knew our relationship was special when...",
    "I treasure the time we...",
    "My favorite qualities in you are...",
    "I'm looking forward to...",
    "The thing I miss about you the most is...",
    "My bucket list with you ...",
    "I'm proud of you for...",
    "The top 5 reasons I'm most grateful for you are..."
]

print("Welcome to DuoDistance!")
print(logo)
print("The app that helps long distance couples stay connected!\n")

location = input("Type in your partner's city 🗺️: ").title()

# Geopy to obtain latitude and longitude of city name
geolocator = Nominatim(user_agent="duodistance_app")
location_data = geolocator.geocode(location)

#input validation, capitalising the city name.
while not location_data:
    print("City not found: {}, please enter a valid city name.".format(location))
    location = input("Type in your partner's city 🗺️: ").title()
    location_data = geolocator.geocode(location)

city_latitude = location_data.latitude
city_longitude = location_data.longitude

# Timezonefinder to get the timezone based of latitude and longitude
tf = TimezoneFinder()
timezone_str = tf.timezone_at(lng=city_longitude, lat=city_latitude)
city_timezone = pytz.timezone(timezone_str)

#API request URL using the API key.
# The service_key in the URL acts as a query parameter,
# This is how I authenticate the request with the OpenWeatherMap API.
complete_api_link = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(city_latitude, city_longitude, service_key)
#making api requests using requests library, data stored in .json format
api_link = requests.get(complete_api_link)
api_data = api_link.json()

#converting the temperature from kelvins into degrees celcius
#only extracting the data I need for the weather information that I wish to show
temp_city = ((api_data["main"]["temp"]) - 273.15)
description_city = (api_data["weather"][0]["description"])

local_time = datetime.now(city_timezone).strftime("%H:%M") #hours and minutes
local_date = datetime.now(city_timezone).strftime("%d %B") #date and month name which is capitalised

#readable information obtained from the API:
print("\nThe current temperature in {} is {:.1f}°C and the weather is {}.".format(location, temp_city, description_city))
print("{} local time is: {}, {}.\n".format(location, local_time, local_date))


def is_valid_date(date_str):
    """
    Checks if a date string is in the correct format.
    Returns a boolean value. True if the date is valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def write_love_letter():
    """
        Asks the user if they want to write a love letter, provides a random prompt,
        then saves the completed letter to a text file, included in title is first initial of partner's name.
        """
    print(letter_logo)
    response = input("Do you want to write a love letter to your partner? 💌 (y/n): ").lower()

    if response == 'y' or response == 'yes':
        prompt = random.choice(love_letter_prompts)

        print("Prompt: " + prompt)
        print("Start writing your love letter below. Enter 'done' on a new line to finish.")

        love_letter_lines = []
        while True:
            line = input()
            if line.lower() == 'done':
                break
            love_letter_lines.append(line)

        # Create a new text file for the love letter
        partner_name = input("Enter your partner's name: ")
        initial = partner_name[0:1]
        file_name = f"love_letter_for_{initial}.txt"

        with open(file_name, 'w') as file:
            file.write(f"Love Letter to {partner_name}\n")
            file.write(prompt + "\n")
            file.write("\n".join(love_letter_lines))

        print(f"\nYour love letter to {partner_name} has been saved to {file_name}. You can send and attach this file via email.")

        with open(file_name, 'r') as file:
            letter_content = file.read()
            print(f"Here is your full love letter:\n\n{letter_content}\n\nThank you for using DuoDistance.👋💞")

    else:
        print("No love letter will be written.\n\nThank you for using DuoDistance.👋💞")
        return


def calculate_time_remaining(target_date):
    """
       Calculates the time remaining until a target date. By subtracting current date from target date.
       Returns a tuple containing days, hours, minutes, and seconds remaining.
       """
    current_date = datetime.now()
    time_remaining = target_date - current_date
    # Calculate days, hours, minutes, and seconds
    days, seconds = divmod(int(time_remaining.total_seconds()), 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return days, hours, minutes, seconds


def trip_letter():
    """
    Asks user if they have an upcoming trip, prompts for the trip date, calculates
    the time remaining, and gives option to write a love letter.
    """
    global date_prompt  # Declare date_prompt as a global variable
    trip_prompt = input("Do you have an upcoming trip to {}? 🧳 Type 'y' for yes, or 'n' for no: ".format(location)).lower()

    if trip_prompt == "n" or trip_prompt == "no":
        print("""
        If you would like to plan a trip, we recommend the following global travel websites: \n
        For transport: \n
            www.skyscanner.net\n
            www.rome2rio.com\n
            www.google.com/flights\n\n
        For accommodation: \n
            www.booking.com\n
            www.expedia.com\n
            www.airbnb.com
            """)
        write_love_letter()

    else:
        while True:
            date_str = input("Type the date of departure for your trip to {} (dd/mm/yyyy): ".format(location))
            if is_valid_date(date_str):
                date_prompt = datetime.strptime(date_str, "%d/%m/%Y")  # Convert input to datetime
                break
            else:
                print("Invalid date format. Please enter a date in the 'dd/mm/yyyy' format.")
        print("You entered the date:", date_prompt.strftime("%d/%m/%Y"))  # Display the formatted date

        days, hours, minutes, seconds = calculate_time_remaining(date_prompt)
        countdown_str = "{:02d} days {:02d} hours {:02d} minutes {:02d} seconds".format(days, hours, minutes, seconds)
        print(hourglass)
        print("Time remaining until your trip to {}: {}".format(location, countdown_str))
        write_love_letter()  # Prompt for a love letter after calculating time remaining

trip_letter()


# Saves all the API results to a text file
with open("duodistance_results.txt", "w") as result_file:
    result_file.write("DuoDistance Results\n")
    result_file.write("Location: {}\n".format(location))
    result_file.write("The current temperature in {} is {:.1f}°C and the weather is {}.\n".format(location, temp_city, description_city))
    result_file.write("{} local time is: {}, {}.\n".format(location, local_time, local_date))
    result_file.write("\n")

print("N.B. API data from our program has been saved to 'duodistance_results.txt'.")


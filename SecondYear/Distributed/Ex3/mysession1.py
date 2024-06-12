#!/usr/bin/python3
# *** INSTRUCTIONS TO RUN *****
# python3 mysession1.py
# No other arguments are needed
import reservationapi
import configparser
import random

#Colours for better user experience
class colours:
    HEADER = '\033[95m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


# Load the configuration file containing the URLs and keys
config = configparser.ConfigParser()
config.read("api.ini")

# Create an API object to communicate with the hotel API
hotel = reservationapi.ReservationApi(config['hotel']['url'],
                                       config['hotel']['key'],
                                       int(config['global']['retries']),
                                       float(config['global']['delay']))

# Your code goes here

# Check if we hold 2 reservations on the system (3.4)
print(f"{colours.HEADER}Getting slot held... {colours.ENDC}")
slot_held = [int(i['id']) for i in hotel.get_slots_held()]
print(f"{colours.YELLOW}The slot held is: {colours.ENDC}", slot_held)

# Release slot if there is more than 2 slots (3.2)
if len(slot_held) >= 2:
    slot_release = random.choice(slot_held)
    print(f"{colours.FAIL}Releasing slot {colours.ENDC} %d " % slot_release)
    x = hotel.release_slot(slot_release)
    print(x['message'])
    slot_held.remove(slot_release)

# Get the available slot (3.3)
print(f"{colours.HEADER}Getting available slots... {colours.ENDC}")
slot_available = [int(i['id']) for i in hotel.get_slots_available()]
print(f"{colours.YELLOW}The slots available are: {colours.ENDC}", slot_available)

# Book a random slot (3.1)
slot_book = random.choice(slot_available)
print(f"{colours.HEADER}Booking slot: {colours.ENDC} %d" % slot_book)
x = hotel.reserve_slot(slot_book)
slot_held.append(int(x['id']))
print(f"{colours.YELLOW}Booked slot: {colours.ENDC} %d" % int(x['id']))

# Release a random slot (3.2)
slot_release = random.choice(slot_held)
print(f"{colours.FAIL}Releasing slot: {colours.ENDC} %d" % slot_release)
x = hotel.release_slot(slot_release)
print(f"{colours.FAIL}",x['message'])








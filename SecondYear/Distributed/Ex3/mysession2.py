#!/usr/bin/python3
# *** INSTRUCTIONS TO RUN *****
# python3 mysession2.py
# No other arguments are needed
import reservationapi
import configparser
import random

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

# Create an API object to communicate with the band API
band = reservationapi.ReservationApi(config['band']['url'],
                                       config['band']['key'],
                                       int(config['global']['retries']),
                                       float(config['global']['delay']))

correct = 0
while correct < 5:

    if correct > 0:
        print(f"{colours.HEADER}Rechecking...{colours.ENDC}")
    # Initialise 2 list to store the available slot of hotel and band
    slot_free_hotel = []
    slot_free_band = []

    # Request available free slots from hotel and band
    print(f"{colours.HEADER}Getting free slots available for Hotel and Band...{colours.ENDC}")
    x, y = hotel.get_slots_available(), band.get_slots_available()

    # Turn the free slots into a list
    slot_free_hotel = [int(i['id']) for i in x]
    slot_free_band = [int(j['id']) for j in y]
    # print(slot_free_band)
    # print(slot_free_hotel)
    print("Successfully got free slots available for Hotel and Band")

    # Loop again if no slot is available
    if not slot_free_band or not slot_free_hotel:
        continue

    #Common slots for hotel and band
    common_slots = sorted(list(set(slot_free_hotel).intersection(slot_free_band)))

    if len(common_slots) <= 20:
        print(f"{colours.HEADER}Common slots not held (available):{colours.ENDC}", common_slots)
    else:
        print(f"{colours.HEADER}Common slots not held: (available){colours.ENDC}", common_slots[:20])

    # Find the earliest common slot
    earliest_slot = min(set(slot_free_hotel).intersection(slot_free_band), default=-1)


    # Get the slot held by hotel and band
    print(f"{colours.HEADER}Getting slots held by hotel and band...{colours.ENDC}")

    x, y = hotel.get_slots_held(), band.get_slots_held()
    slot_held_hotel = [int(i['id']) for i in x]
    slot_held_band = [int(j['id']) for j in y]

    print("The slot held by Hotel is: ", slot_held_hotel)
    print("The slot held by Band is: ", slot_held_band)

    # Get the real earliest slot
    if slot_held_hotel and slot_held_band:
        # hotel has booked the earliest slot and it is a free slot in band
        if len(slot_held_hotel) > 0 and slot_held_hotel[0] < earliest_slot and slot_held_hotel[0] in slot_free_band:
            earliest_slot = slot_held_hotel[0]
        # band has booked the earliest slot and it is a free slot in hotel
        elif len(slot_held_band) > 0 and slot_held_band[0] < earliest_slot and slot_held_band[0] in slot_free_hotel:
            earliest_slot = slot_held_band[0]
        # both hotel and band has booked the earliest slot
        elif len(slot_held_band) > 0 and len(slot_held_hotel) > 0:
            if slot_held_band[0] < earliest_slot and slot_held_band[0] in slot_held_hotel:
                earliest_slot = slot_held_band[0]
            elif slot_held_hotel[0] < earliest_slot and slot_held_hotel[0] in slot_held_band:
                earliest_slot = slot_held_hotel[0]

    # Loop again if no common slot
    if earliest_slot == -1:
        continue

    print(f"{colours.YELLOW}The earliest slot is: {colours.ENDC}", earliest_slot)

    # Book the earliest slot for hotel and band
    print(f"{colours.HEADER}Booking slots... {colours.ENDC}")

    # try:
    #     if earliest_slot not in slot_held_hotel:
    #         x = hotel.reserve_slot(earliest_slot)
    #     else:
    #         x = {'id': earliest_slot}
    #     if earliest_slot not in slot_held_band:
    #         y = band.reserve_slot(earliest_slot)
    #     else:
    #         y = {'id': earliest_slot}
    # except:
    #     # Check if there both hotel and band already hold the same slot
    #     for i in slot_held_hotel:
    #         if i in slot_held_band:
    #             band.cancel_reservation(i)
    #             hotel.cancel_reservation(i)
    #             break
    #     continue

    correct1 = 0
    correct2 = 0

    if earliest_slot not in slot_held_hotel:
        try:
            x = hotel.reserve_slot(earliest_slot)
            print("Hotel slot booked: %d" % earliest_slot)
            correct1 = 1
        except:
            earliest_slot = -1
            print(f"{colours.FAIL}Cannot book Hotel slot {colours.ENDC} %d" % earliest_slot)
    else:
        x = {'id': earliest_slot}
        print("Hotel slot booked %d" % earliest_slot)
        correct1 = 1

    if earliest_slot not in slot_held_band:
        try:
            y = band.reserve_slot(earliest_slot)
            print("Band slot booked: %d" % earliest_slot)
            correct2 = 1
        except:
            earliest_slot = -1
            print(f"{colours.FAIL}Cannot book Band slot{colours.ENDC}  %d" % earliest_slot)
    else:
        y = {'id': earliest_slot}
        print("Band slot booked: %d" % earliest_slot)
        correct2 = 1

    if correct1 == 1 and correct2 == 1:
        correct += 1

    else:
        # Check if both hotel and band already hold the same slot
        for i in slot_held_hotel:
            if i in slot_held_band:
                earliest_slot = i

    # Remove extra slots
    for i in slot_held_hotel:
        if i != earliest_slot:
            print(f"{colours.FAIL}Releasing slot: {colours.ENDC} %d" % i)
            x = hotel.release_slot(i)
            print(x['message'])

    for j in slot_held_band:
        if j != earliest_slot:
            print(f"{colours.FAIL}Releasing slot: {colours.ENDC} %d" % j)
            y = band.release_slot(j)
            print(y['message'])



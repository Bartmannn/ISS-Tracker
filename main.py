"""
    Title: ISS Tracker
    Author: Bartosz Bohdziewicz
    Date: 24-07-2022
"""

from tkinter import *
from consts import MULTIPLIER, COOLDOWN, COPY_BUTTON_TEXT

def set_ISS_coords(longitude, latitude):
    x = START_POINT[0] + (float(longitude) * MULTIPLIER)
    y = START_POINT[1] - (float(latitude) * MULTIPLIER)
    canvas.coords(ISS_station, int(x), int(y))

def get_coords():
    from requests import get
    response = get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])
    x = START_POINT[0] + (longitude * MULTIPLIER)
    y = START_POINT[1] - (latitude * MULTIPLIER)
    return (int(x), int(y), latitude, longitude)

def update_coords():
    from datetime import datetime
    current_time = datetime.now()
    # print(current_time.hour, current_time.minute)
    x, y, lat, long = get_coords()
    information = f"Lat: {lat} | Long: {long} | Time: {current_time.date()} {current_time.hour}:{current_time.minute}"
    info_to_save = f"{lat}#{long}#{current_time.date()}#{to_two_letter_time(current_time.hour)}:{to_two_letter_time(current_time.minute)}"
    coords.insert(0, info_to_save.split("#"))
    if time_slider.get() == 0:
        canvas.coords(ISS_station, x, y)
        coords_time_label.configure(text=information)
        copy_coords_button.configure(text=COPY_BUTTON_TEXT)
    time_slider.configure(to=len(coords)-1)
    save(info_to_save)
    window.after(COOLDOWN, update_coords)

def save(info_to_save):
    try:
        with open(file="./saves/coords.txt", mode="a") as data:
            data.write(f"{info_to_save}\n")
    except FileNotFoundError:
        with open(file="./saves/coords.txt", mode="w") as data:
            data.write(f"{info_to_save}\n")

def upload_data():
    from datetime import datetime
    global coords
    try:
        with open(file="./saves/coords.txt", mode="r") as data:
            # One Line: latitude longitude date time, Separation: #
            coords = [coord.replace("\n", "").split("#") for coord in data.readlines()]
            coords = coords[::-1]  # The newest data on lower index, last saved data on index 0
    except FileNotFoundError:
        x, y, lat, long = get_coords()
        current_time = datetime.now()
        coords = [f"{lat}#{long}#{current_time.date()}#{current_time.hour}:{current_time.minute}".split("#")]

def change_position(arg):
    lat, long, date, time = coords[time_slider.get()]
    coords_time_label.configure(text=f"Lat: {lat} | Long: {long} | Time: {date} {time}")
    set_ISS_coords(longitude=long, latitude=lat)
    copy_coords_button.configure(text=COPY_BUTTON_TEXT)

def copy():
    from pyperclip import copy
    copy(f"{coords[time_slider.get()][0]}, {coords[time_slider.get()][1]}")
    copy_coords_button.configure(text="Copied!")

def to_two_letter_time(time):
    if len(str(time)) < 2:
        return f"0{time}"
    return str(time)


SCREEN_SIZE = (360 * MULTIPLIER, 180 * MULTIPLIER)
START_POINT = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
coords = []

#Window setup
window = Tk()
window.title("ISS Tracker")
window.configure(width=SCREEN_SIZE[0], height=SCREEN_SIZE[1])

#Canvas create with world image
canvas = Canvas(width=SCREEN_SIZE[0], height=SCREEN_SIZE[1], highlightthickness=0)
world_map_image_src = f"./images/world_map_{SCREEN_SIZE[0]}x{SCREEN_SIZE[1]}.png"
world_map_image = PhotoImage(file=world_map_image_src)
canvas.create_image(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2, image=world_map_image)

#ISS station create
iss_station_image_src = "./images/ISS_station.gif"
iss_station_image = PhotoImage(file=iss_station_image_src)
ISS_station = canvas.create_image(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2, image=iss_station_image)

#Label for time line
coords_time_label = Label(text="", width=int(27.5 * MULTIPLIER))
time_slider = Scale(window, from_=0, to=len(coords)-1, orient=HORIZONTAL, showvalue=0, length=SCREEN_SIZE[0], command=change_position)

#Button to copy selected coords
copy_coords_button = Button(text=COPY_BUTTON_TEXT, command=copy, width=5 * MULTIPLIER, highlightthickness=0)

#Upload older datas
upload_data()

#Move ISS station
update_coords()

#Setup UI
canvas.grid(row=0, column=0, columnspan=2)
coords_time_label.grid(row=1, column=0)
copy_coords_button.grid(row=1, column=1)
time_slider.grid(row=2, column=0, columnspan=2)

window.mainloop()

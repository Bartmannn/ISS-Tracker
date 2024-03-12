from turtle import Turtle, Screen
import math
from consts import MULTIPLIER, SECOND


class ISS_station(Turtle):

    def __init__(self, shape_dir):
        super().__init__()
        self.penup()
        self.goto(START_POINT)
        self.shape(shape_dir)

    def get_coords(self):
        from requests import get
        from math import radians, cos
        response = get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
        data = response.json()
        longitude = float(data["iss_position"]["longitude"])
        latitude = float(data["iss_position"]["latitude"])
        x = longitude * MULTIPLIER
        y = latitude * MULTIPLIER
        print(f"Lat: {latitude} | Long: {longitude}")
        return (int(x), int(y))

    def update_coords(self):
        self.goto(self.get_coords())
        Screen().ontimer(self.update_coords, SECOND * 3)



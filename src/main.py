from Plant import Plant
import helpers.logger_config
from helpers.open_meteo import fetch_weather_data
from configuration import *
from loguru import logger



if __name__ == "__main__":

    df = fetch_weather_data(latitude=37.24, longitude=6)
    print(df)
    # plant = create_plant_from_input()

    # if plant:
    #     print("\nPlant created successfully!")
    #     print(plant)
2
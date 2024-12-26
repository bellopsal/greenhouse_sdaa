from Plant import Plant
import helpers.logger_config
from configuration import *
from loguru import logger



if __name__ == "__main__":
    logger.info("HEY")
    plant = create_plant_from_input()

    if plant:
        print("\nPlant created successfully!")
        print(plant)
2
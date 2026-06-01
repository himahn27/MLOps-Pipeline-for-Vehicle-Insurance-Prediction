import sys

from vehicle_insurance.logger.logger import logger
from vehicle_insurance.exception.exception import VehicleInsuranceException


def divide_numbers():
    try:
        logger.info("Starting division")
        a = 10
        b = 0
        result = a / b
        logger.info(f"Result: {result}")
    except Exception as e:
        logger.error("An error occurred during division")
        raise VehicleInsuranceException(e, sys)


if __name__ == "__main__":
    divide_numbers()
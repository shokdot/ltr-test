import logging
from datetime import datetime
import os
from time import sleep

import board
import busio
from adafruit_ltr390 import LTR390, Gain, Resolution

# Setup file paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(SCRIPT_DIR, "research/messurments.txt")
log_path = os.path.join(SCRIPT_DIR, "research/ltr390_internal.log")

# Configure logging
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Setup sensor
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = LTR390(i2c)
    sensor.resolution = Resolution.RESOLUTION_20BIT
    sensor.gain = Gain.GAIN_6X
except Exception as e:
    logging.exception("Failed to initialize sensor")
    sensor = None

def messure():
    data = {"uv": None, "lux": None}
    if sensor is None:
        logging.error("Sensor not initialized.")
        return None
    try:
        data["uv"] = sensor.uvi
        data["lux"] = sensor.lux
    except Exception:
        logging.exception("Error reading sensor data")
        return None
    return data

def main():
    logging.info("Starting measurement loop")
    while True:
        try:
            now = datetime.now()
            if now.minute > 37:
                logging.info("Exiting loop due to time condition")
                break

            data = messure()
            with open(data_path, "a") as file:
                if data:
                    log_line = f"{now.isoformat()} {data['uv']} {data['lux']}"
                    file.write(log_line + "\n")
                    logging.info("Data written: " + log_line)
                else:
                    file.write(f"{now.isoformat()} Error during measurement\n")
                    logging.warning("Measurement failed")
            sleep(1)
        except Exception:
            logging.exception("Unexpected error in main loop")

if __name__ == "__main__":
    main()

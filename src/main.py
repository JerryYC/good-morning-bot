import time
import yaml
import logging
import sys
import random
from insta_api import InstaDriver

if __name__ == "__main__":
    # load config
    config_path = sys.argv[1]
    with open(config_path, 'r') as stream:
        try:
            config = yaml.load(stream)
        except Exception as e:
            logging.error("Failed to read config", e)
    
    # randomdelay 
    delay_min = int(random.random() * config["message"]["time_range"] * 60)
    time.sleep(delay_min)

    # send message
    driver = InstaDriver(config["env"]["driver_path"])
    driver.login(config["credential"]["account_username"], config["credential"]["account_password"])
    driver.open_chat(config["credential"]["chat_id"])

    messages = config["message"]["messages"]
    message = messages[int(random.random() * len(messages))]
    driver.send_message(message)

    driver.shutdown()
    logging.info("Job finished")


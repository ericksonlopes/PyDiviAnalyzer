import configparser
import os

config = configparser.RawConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

API_KEY_OPENAI = config.get("Openai", "KEY")

# this file is to store the user data as telegram doesnt store it for you

import json
import os

STATE_FILE = "state.json"
# This function is to load the state from the json file
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


# This function is to save state to file
def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

# Global in-memory state
user_state = load_state()
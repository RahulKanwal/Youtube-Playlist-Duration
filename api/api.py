from flask import Flask
import time

app = Flask(__name__)

@app.route('/duration')
def get_current_time():
    return {"time": time.time()}
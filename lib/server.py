import os
import time
from flask import Flask
from bike.bike import order_bike
from car.car import order_car
from scooter.scooter import order_scooter

import time
import tracemalloc as tm
import threading as th

app = Flask(__name__)

@app.route("/bike")
def bike():
    order_bike(0.2)
    return "<p>Bike ordered</p>"


@app.route("/scooter")
def scooter():
    order_scooter(0.3)
    return "<p>Scooter ordered</p>"


@app.route("/car")
def car():
    order_car(0.4)
    return "<p>Car ordered</p>"


@app.route("/")
def environment():
    result = "<h1>environment vars:</h1>"
    for key, value in os.environ.items():
        result +=f"<p>{key}={value}</p>"
    return result

def run_app():
    app.run(threaded=False, processes=1, host='0.0.0.0', port=4040, debug=False)

if __name__ == '__main__':
    tm.start(10)
    
    t = th.Thread(target=run_app)
    t.start()

    time.sleep(1)
    print("Snapshot:")
    snap = tm.take_snapshot()
    snap = snap.filter_traces([tm.Filter(True, filename_pattern="/workdir/*", all_frames=True)])
    for i, alloc in enumerate(snap.statistics("traceback")):
        for k, tr in enumerate(alloc.traceback):
            print(tr)
        print("Size %s B count %d" % (alloc.size, alloc.count))

    t.join()
    print("Done!")


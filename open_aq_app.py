from flask import Flask, jsonify, request

import open_aq_database_mysql

# Haetaan open_aq_database
import open_aq_database

app = Flask(__name__)

# Yhden päivän mittaukset
@app.route('/measurements/<int:location_id>', methods=['GET'])
def get_daily_measurements(location_id):
    # Päivän haku
    date = request.args.get('date')
    result = open_aq_database_mysql.get_location_daily_measurements(location_id, date)
    return jsonify(result)


# Valitun mittauspaikan kaikkien mittausten lukumäärä
@app.route('/measurements/<int:loc_id>/count', methods=['GET'])
def get_total_measurement(loc_id):
    # Funktio joka tekee count kyselyn
    result = open_aq_database_mysql.get_total_place_measurement(loc_id)
    return jsonify(result)


# Valitun mittauspaikan ja sensorin päivittäinen mittauskeskiarvo
@app.route('/measurements/<int:loc_id>/average', methods=['GET'])
def get_daily_average(loc_id):
    # Sensorin ID ja päivä
    # sensor_id -> int
    sensor_id = request.args.get('sensor_id', type=int)
    date = request.args.get('date')
    result = open_aq_database_mysql.get_daily_avg_for_sensor(loc_id, sensor_id, date)
    return jsonify(result)

@app.route('/stations', methods=['GET'])
def get_stations():
    # Palautetaan kiinteä lista asemien ID-numeroista
    test_stations = [
        {"id": 2975, "name": "FI00781-2975", "city": "Helsinki", "latitude": 60.22393, "longitude": 25.10244},
        {"id": 2998, "name": "FI00841-2998", "city": "Helsinki", "latitude": 60.22024, "longitude": 24.81133},
        {"id": 4529, "name": "FI00370-4529", "city": "Helsinki", "latitude": 60.28995, "longitude": 25.03953},
        {"id": 4588, "name": "FI00564-4588", "city": "Helsinki", "latitude": 60.16964, "longitude": 24.93924},
        {"id": 4593, "name": "FI00425-4593", "city": "Helsinki", "latitude": 60.18739, "longitude": 24.95060},
        {"id": 9287, "name": "FI00902-9287", "city": "Helsinki", "latitude": 60.19644, "longitude": 24.95198}
    ]

    return jsonify(test_stations)

if __name__ == '__main__':
    app.run(debug=True)
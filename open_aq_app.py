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

if __name__ == '__main__':
    app.run(debug=True)
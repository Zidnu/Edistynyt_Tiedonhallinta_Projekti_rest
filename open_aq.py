import os

import psycopg2
from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor

# Flask
app = Flask(__name__)

def get_avg_total_by_daily(loc_id, year):
    # Käytetään psycopg2 yhteyttä
    with psycopg2.connect(database=os.getenv('PG_DB'), user=os.getenv('PG_USER'), password=os.getenv('PG_PWD')) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            # Kysely
            _query = ("SELECT ROUND(AVG(value)::numeric,2)::float AS avg_total,"
                      " EXTRACT (MONTH FROM datetime) AS month"
                      " FROM measurements"
                      " JOIN sensors ON measurements.sensor_id = sensors.id"
                      " WHERE sensors.location_id = %s"
                      " AND EXTRACT(YEAR FROM datetime) = %s"
                      " GROUP BY month"
                      " ORDER BY month")

            cur.execute(_query, (loc_id, year))

        # Palauttaa kaikki
        return cur.fetchall()


# Kaikkien mittausten lukumäärä
def get_total_place_measurement(loc_id):
    # Käytetään psycopg2-yhteyttä
    with psycopg2.connect(database=os.getenv('PG_DB'), user=os.getenv('PG_USER'), password=os.getenv('PG_PWD')) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            # Kysely
            # m = measurement
            # s = sensors
            _query = (" SELECT COUNT(m.id) AS total_count"
                      " FROM measurements m"
                      " JOIN sensors s ON m.sensor_id = s.id"
                      " WHERE s.location_id = %s")

            cur.execute(_query, (loc_id,))
            # Palauttaa yhden rivin
            return cur.fetchone()

# Mittauksen keskiarvo
def get_daily_avg_for_sensor(loc_id, date_str):
    # Käytetään psycopg2 yhteyttä
    with psycopg2.connect(database=os.getenv('PG_DB'), user=os.getenv('PG_USER'), password=os.getenv('PG_PWD')) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            # Lasketaan keskiarvo - value
            # m = measurement
            # s = sensors
            _query = (" SELECT m.datetime, m.value, s.parameter, s.unit"
                      " FROM measurements m"
                      " JOIN sensors s ON m.sensor_id = s.id"
                      " WHERE s.location_id = %s"
                      " AND m.datetime::date = %s" # 
                      " ORDER BY m.datetime")

            # MUISTA
            # cur.execute-metodi
            # -> muuttujat samassa järjestyksessä kuin %s merkit
            cur.execute(_query, (loc_id, date_str))

            # Palauttaa yhden keskiarvon
            return cur.fetchone()


# Suoritin
if __name__ == '__main__':
        app.run(debug=True)
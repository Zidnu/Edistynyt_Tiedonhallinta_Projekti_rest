import os

import mysql.connector

from dotenv import load_dotenv



load_dotenv()

def get_location_daily_measurements(loc_id, date_str):
    # Käytetään mysql yhteyttä
    with mysql.connector.connect(database=os.getenv('PG_DB'),
                                user=os.getenv('PG_USER'),
                                password=os.getenv('PG_PWD')) as conn:

        with conn.cursor(dictionary=True) as cur:

            # Kysely
            # m = measurement
            # s = sensor
            # l = location
            # Haetaan yhden paikan mittaukset
            _query = (" SELECT m.id, m.value, m.datetime, l.name as location_name"
                      " FROM measurements m"
                      " JOIN sensors s ON m.sensor_id = s.id"
                      " JOIN locations l ON s.location_id = l.id"
                      # l.name/l.id = kummallakin voi hakea
                      " WHERE (l.name = %s OR l.id = %s)" 
                      " AND DATE(m.datetime) = %s"
                      )

            cur.execute(_query, (loc_id, loc_id, date_str))

            # Palauttaa kaikki
            return cur.fetchall()


# Kaikkien mittausten lukumäärä
def get_total_place_measurement(loc_id):
    # Käytetään mysql-yhteyttä
    with mysql.connector.connect(database=os.getenv('PG_DB'),
                          user=os.getenv('PG_USER'),
                          password=os.getenv('PG_PWD')) as conn:

        with conn.cursor(dictionary=True) as cur:

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
def get_daily_avg_for_sensor(loc_id, sensor_id, date_str):
    # Käytetään mysql yhteyttä
    with mysql.connector.connect(database=os.getenv('PG_DB'),
                          user=os.getenv('PG_USER'),
                          password=os.getenv('PG_PWD')) as conn:

        with conn.cursor(dictionary=True) as cur:

            # Lasketaan keskiarvo - value
            # m = measurement
            # s = sensors
            _query = (" SELECT ROUND(AVG(m.value), 2) AS daily_avg"
                      " FROM measurements m"
                      " JOIN sensors s ON m.sensor_id = s.id"
                      " WHERE s.location_id = %s"
                      " AND s.id = %s"
                      " AND DATE(m.datetime) = %s"
                      )

            # MUISTA
            # cur.execute-metodi
            # -> muuttujat samassa järjestyksessä kuin %s merkit
            cur.execute(_query, (loc_id, sensor_id, date_str))

            # Palauttaa yhden keskiarvon
            return cur.fetchone()


import os

import psycopg2
from psycopg2.extras import RealDictCursor

from dotenv import load_dotenv

load_dotenv()


def get_location_daily_measurements(loc_id, date_str):
    # Käytetään psycopg2 yhteyttä
    with psycopg2.connect(database=os.getenv('PG_DB'),
                          user=os.getenv('PG_USER'),
                          password=os.getenv('PG_PWD')) as conn:

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            # Kysely
            # m = measurement
            # s = sensor
            _query = (" SELECT m.datetime, m.value, s.parameter, s.unit"
                      " FROM measurements m"
                      " JOIN sensors s ON m.sensor_id = s.id"
                      " WHERE s.location_id = %s"
                      " AND m.datetime::date = %s"
                      " ORDER BY m.datetime")

            cur.execute(_query, (loc_id, date_str))

            # Palauttaa kaikki
            return cur.fetchall()


# Kaikkien mittausten lukumäärä
def get_total_place_measurement(loc_id):
    # Käytetään psycopg2-yhteyttä
    with psycopg2.connect(database=os.getenv('PG_DB'),
                          user=os.getenv('PG_USER'),
                          password=os.getenv('PG_PWD')) as conn:

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
def get_daily_avg_for_sensor(loc_id, sensor_id, date_str):
    # Käytetään psycopg2 yhteyttä
    with psycopg2.connect(database=os.getenv('PG_DB'),
                          user=os.getenv('PG_USER'),
                          password=os.getenv('PG_PWD')) as conn:

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            # Lasketaan keskiarvo - value
            # m = measurement
            # s = sensors
            _query = (" SELECT ROUND(AVG(m.value)::numeric, 2)::float AS daily_avg"
                      " FROM measurements m"
                      " JOIN sensors s ON m.sensor_id = s.id"
                      " WHERE s.location_id = %s"
                      " AND s.id = %s"
                      " AND m.datetime::date = %s")

            # MUISTA
            # cur.execute-metodi
            # -> muuttujat samassa järjestyksessä kuin %s merkit
            cur.execute(_query, (loc_id, sensor_id, date_str))

            # Palauttaa yhden keskiarvon
            return cur.fetchone()

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
            _query = (" SELECT * "
                      " FROM measurements m"
                      )

            cur.execute(_query )

            # Palauttaa kaikki
            return cur.fetchall()


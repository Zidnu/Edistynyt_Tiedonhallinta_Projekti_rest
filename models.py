from typing import List

from sqlalchemy import Column, DECIMAL, DateTime, Double, ForeignKeyConstraint, Index, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped


Base = declarative_base()


class Countries(Base):
    __tablename__ = 'countries'

    id = mapped_column(INTEGER(11), primary_key=True)
    name = mapped_column(String(100), nullable=False)

    locations: Mapped[List['Locations']] = relationship('Locations', uselist=True, back_populates='country')


class Locations(Base):
    __tablename__ = 'locations'
    __table_args__ = (
        ForeignKeyConstraint(['country_id'], ['countries.id'], name='fk_locations_countries1'),
        Index('fk_locations_countries1_idx', 'country_id')
    )

    id = mapped_column(INTEGER(11), primary_key=True)
    name = mapped_column(String(100), nullable=False)
    city = mapped_column(String(45), nullable=False)
    latitude = mapped_column(DECIMAL(9, 6), nullable=False)
    longitude = mapped_column(DECIMAL(9, 6), nullable=False)
    country_id = mapped_column(INTEGER(11), nullable=False)

    country: Mapped['Countries'] = relationship('Countries', back_populates='locations')
    sensors: Mapped[List['Sensors']] = relationship('Sensors', uselist=True, back_populates='location')


class Sensors(Base):
    __tablename__ = 'sensors'
    __table_args__ = (
        ForeignKeyConstraint(['location_id'], ['locations.id'], name='fk_sensors_locations'),
        Index('fk_sensors_locations_idx', 'location_id')
    )

    id = mapped_column(INTEGER(11), primary_key=True)
    parameter = mapped_column(String(45), nullable=False)
    unit = mapped_column(String(45), nullable=False)
    location_id = mapped_column(INTEGER(11), nullable=False)


    location: Mapped['Locations'] = relationship('Locations', back_populates='sensors')
    measurements: Mapped[List['Measurements']] = relationship('Measurements', uselist=True, back_populates='sensor')


class Measurements(Base):
    __tablename__ = 'measurements'
    __table_args__ = (
        ForeignKeyConstraint(['sensor_id'], ['sensors.id'], name='fk_measurements_sensors1'),
        Index('fk_measurements_sensors1_idx', 'sensor_id')
    )

    id = mapped_column(INTEGER(11), primary_key=True)
    value = mapped_column(Double(asdecimal=True), nullable=False)
    datetime = mapped_column(DateTime, nullable=False)
    sensor_id = mapped_column(INTEGER(11), nullable=False)

    sensor: Mapped['Sensors'] = relationship('Sensors', back_populates='measurements')

from sqlalchemy import Column, DateTime, Float, Integer, String

from db.session import Base


class SeismicEvent(Base):
    __tablename__ = 'seismic_events'

    date = Column(DateTime, primary_key=True)
    lat = Column(Float, primary_key=True)
    lon = Column(Float, primary_key=True)
    magnitude = Column(Float)
    magnitude_type = Column(String)
    depth = Column(Integer)
    degree = Column(String)
    local = Column(String)
    obs_region = Column(String)
    source = Column(String)
    updated_at = Column(DateTime)

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    status = Column(String)
    status_text = Column(String)
    preforclosure = Column(Boolean)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, ForeignKey('properties.id'), primary_key=True)
    address = Column(String, primary_key=True)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    property = relationship("Property")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, ForeignKey('properties.id'), primary_key=True)
    price = Column(Float)
    zestimate = Column(Integer)
    rent_zestimate = Column(Integer)
    tax_value = Column(Integer)
    property = relationship("Property")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class SingleFamily(Base):
    __tablename__ = 'single_family'
    id = Column(Integer, ForeignKey('properties.id'), primary_key=True)
    beds = Column(Integer)
    baths = Column(Integer)
    area = Column(Integer)
    lot_area = Column(Integer)
    property = relationship("Property")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class MultiFamily(Base):
    __tablename__ = 'multi_family'
    id = Column(Integer, ForeignKey('properties.id'), primary_key=True)
    beds = Column(Integer)
    baths = Column(Integer)
    area = Column(Integer)
    lot_area = Column(Integer)
    property = relationship("Property")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Townhome(Base):
    __tablename__ = 'townhomes'
    id = Column(Integer, ForeignKey('properties.id'), primary_key=True)
    beds = Column(Integer)
    baths = Column(Integer)
    area = Column(Integer)
    lot_area = Column(Integer)
    property = relationship("Property")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Condo(Base):
    __tablename__ = 'condos'
    id = Column(Integer, ForeignKey('properties.id'), primary_key=True)
    beds = Column(Integer)
    baths = Column(Integer)
    area = Column(Integer)
    lot_area = Column(Integer)
    property = relationship("Property")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Apartment(Base):
    __tablename__ = 'apartments'
    id = Column(Integer, ForeignKey('properties.id'), primary_key=True)
    beds = Column(Integer)
    baths = Column(Integer)
    area = Column(Integer)
    lot_area = Column(Integer)
    property = relationship("Property")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def schema_exists(engine, schema_name='public'):
    query = text(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name='{schema_name}';")
    return bool(engine.execute(query).scalar())

engine = create_engine("postgresql://postgres: @localhost/capstone")

if not schema_exists(engine, 'public'):
    Base.metadata.create_all(engine, checkfirst=True)
else:
    print("The public schema already exists.")
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Property(Base):
    __tablename__ = 'properties'
    __table_args__ = {'schema': 'capstone'}
    id = Column(Integer, primary_key=True)
    status = Column(String)
    status_text = Column(String)
    preforclosure = Column(Boolean)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Address(Base):
    __tablename__ = 'addresses'
    __table_args__ = {'schema': 'capstone'}
    id = Column(Integer, ForeignKey('capstone.properties.id'), primary_key=True)
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
    __table_args__ = {'schema': 'capstone'}
    id = Column(Integer, ForeignKey('capstone.properties.id'), primary_key=True)
    price = Column(Float)
    zestimate = Column(Integer)
    rent_zestimate = Column(Integer)
    tax_value = Column(Integer)
    property = relationship("Property")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class SingleFamily(Base):
    __tablename__ = 'single_family'
    __table_args__ = {'schema': 'capstone'}
    id = Column(Integer, ForeignKey('capstone.properties.id'), primary_key=True)
    beds = Column(Integer)
    baths = Column(Integer)
    area = Column(Integer)
    lot_area = Column(Integer)
    property = relationship("Property")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class MultiFamily(Base):
    __tablename__ = 'multi_family'
    __table_args__ = {'schema': 'capstone'}
    id = Column(Integer, ForeignKey('capstone.properties.id'), primary_key=True)
    beds = Column(Integer)
    baths = Column(Integer)
    area = Column(Integer)
    lot_area = Column(Integer)
    property = relationship("Property")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Townhome(Base):
    __tablename__ = 'townhomes'
    __table_args__ = {'schema': 'capstone'}
    id = Column(Integer, ForeignKey('capstone.properties.id'), primary_key=True)
    beds = Column(Integer)
    baths = Column(Integer)
    area = Column(Integer)
    lot_area = Column(Integer)
    property = relationship("Property")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Condo(Base):
    __tablename__ = 'condos'
    __table_args__ = {'schema': 'capstone'}
    id = Column(Integer, ForeignKey('capstone.properties.id'), primary_key=True)
    beds = Column(Integer)
    baths = Column(Integer)
    area = Column(Integer)
    lot_area = Column(Integer)
    property = relationship("Property")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Apartment(Base):
    __tablename__ = 'apartments'
    __table_args__ = {'schema': 'capstone'}
    id = Column(Integer, ForeignKey('capstone.properties.id'), primary_key=True)
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

def create_schema(engine, schema_name='capstone'):
    if not schema_exists(engine, schema_name):
        query = text(f"CREATE SCHEMA {schema_name};")
        engine.execute(query)
        Base.metadata.create_all(engine, checkfirst=True)
    else:
        print(f"The {schema_name} schema already exists.")
        Base.metadata.create_all(engine, checkfirst=True)

if __name__ == '__main__':
    engine = create_engine("postgresql://postgres: @localhost/capstone")
    create_schema(engine, 'capstone')

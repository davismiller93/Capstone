import csv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from capstone_schema import Address, Property, Price, SingleFamily, MultiFamily, Townhome, Condo, Apartment


class DataIngestion:
    def __init__(self, db_connection_string):
        self.engine = create_engine(db_connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def home_type_class(self, home_type):
        if home_type == 'SINGLE_FAMILY':
            return SingleFamily
        elif home_type == 'MULTI_FAMILY':
            return MultiFamily
        elif home_type == 'TOWNHOUSE':
            return Townhome
        elif home_type == 'CONDO':
            return Condo
        elif home_type == 'APARTMENT':
            return Apartment

    def create_objects(self, row):
        prop = Property(
            id=row['id'],
            status=row['statusType'],
            preforclosure=row['isPreforclosureAuction'].lower() == 'true',
        )
        self.session.add(prop)

        address = Address(
            id=row['id'],
            address=row['address'],
            street=row['addressStreet'],
            city=row['addressCity'],
            state=row['addressState'],
            zip_code=row['addressZipcode']
        )
        self.session.add(address)

        price = Price(
            id=row['id'],
            price=row['unformattedPrice'],
            zestimate=row['zestimate'],
            rent_zestimate=row['rentZestimate'],
            tax_value=row['taxAssessedValue'],
            property=prop
        )
        self.session.add(price)

        home_type = self.home_type_class(row['homeType'])(
            id=row['id'],
            beds=row['beds'],
            baths=row['baths'],
            area=row['area'],
            lot_area=row['lotAreaRaw'],
            property=prop
        )
        self.session.add(home_type)

        return address, prop, price, home_type

    def ingest_csv(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if the id already exists in the Property table
                existing_property = self.session.query(Property).filter_by(id=row['id']).first()
                if existing_property:
                    print(f"Skipping record with id {row['id']} as it already exists.")
                    continue

                # Check if the properties match the predefined types above
                home_type_callable = self.home_type_class(row['homeType'])
                if not home_type_callable:
                    print(f"Skipping record with id {row['id']} due to unsupported or missing home type.")
                    continue

                address, prop, price, home_type = self.create_objects(row)
                price.property = prop
                home_type.property = prop
                self.session.add_all([address, prop, price, home_type])

        self.session.commit()


if __name__ == '__main__':
    db_connection_string = "postgresql://postgres: @localhost/capstone"
    file_path = 'housing.csv'
    data_ingestion = DataIngestion(db_connection_string)
    data_ingestion.ingest_csv(file_path)

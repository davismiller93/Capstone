from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from capstone_schema import Property, Address, Price, SingleFamily, MultiFamily, Townhome, Condo, Apartment
import json

app = Flask(__name__)

engine = create_engine("postgresql://postgres: @localhost/capstone")
Session = sessionmaker(bind=engine)

@app.route('/properties', methods=['GET'])
def get_properties():
    session = Session()
    limit = int(request.args.get('limit', 10))  # Set a default limit of 10 properties

    properties = session.query(Property, Address, Price, SingleFamily, MultiFamily, Townhome, Condo, Apartment).\
        filter(Property.id == Address.id).\
        filter(Property.id == Price.id).\
        outerjoin(SingleFamily, Property.id == SingleFamily.id).\
        outerjoin(MultiFamily, Property.id == MultiFamily.id).\
        outerjoin(Townhome, Property.id == Townhome.id).\
        outerjoin(Condo, Property.id == Condo.id).\
        outerjoin(Apartment, Property.id == Apartment.id).\
        order_by(func.random()).\
        limit(limit).\
        all()

    session.close()

    properties_list = []

    for property, address, price, single_family, multi_family, townhome, condo, apartment in properties:
        property_dict = property.__dict__
        property_dict.pop("_sa_instance_state", None)

        property_dict["address"] = address.__dict__
        property_dict["address"].pop("_sa_instance_state", None)

        property_dict["price"] = price.__dict__
        property_dict["price"].pop("_sa_instance_state", None)

        if single_family:
            property_dict["home_type_data"] = {"single_family": single_family.__dict__}
            property_dict["home_type_data"]["single_family"].pop("_sa_instance_state", None)
        elif multi_family:
            property_dict["home_type_data"] = {"multi_family": multi_family.__dict__}
            property_dict["home_type_data"]["multi_family"].pop("_sa_instance_state", None)
        elif townhome:
            property_dict["home_type_data"] = {"townhome": townhome.__dict__}
            property_dict["home_type_data"]["townhome"].pop("_sa_instance_state", None)
        elif condo:
            property_dict["home_type_data"] = {"condo": condo.__dict__}
            property_dict["home_type_data"]["condo"].pop("_sa_instance_state", None)
        elif apartment:
            property_dict["home_type_data"] = {"apartment": apartment.__dict__}
            property_dict["home_type_data"]["apartment"].pop("_sa_instance_state", None)

        properties_list.append(property_dict)

    return jsonify(properties_list)

if __name__ == '__main__':
    app.run(debug=True)

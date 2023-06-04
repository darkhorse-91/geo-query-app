import sqlalchemy.orm as _orm
from geopy.geocoders import Nominatim
from geopy.distance import distance
import src.model.models as _models, src.schemas.schema as _schemas, src.model.database as _database


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()


def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email).first()


def get_users(db: _orm.Session, limit: int = 100):
    return db.query(_models.User).limit(limit).all()


def create_user(db: _orm.Session, user: _schemas.UserCreate):
    fake_hashed_password = user.password + "thisisnotsecure"
    db_user = _models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_addresses(db: _orm.Session, limit: int = 10):
    return db.query(_models.Address).limit(limit).all()


def create_address(db: _orm.Session, address: _schemas.AddressCreate, user_id: int):
    address_dict = {
        "address": address.dict().get('address'),
        "coordinates": get_address_coordinates(address.dict().get('address'))
    }

    address = _models.Address(**address_dict, owner_id=user_id)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def get_address(db: _orm.Session, address_id: int):
    return db.query(_models.Address).filter(_models.Address.id == address_id).first()


def delete_address(db: _orm.Session, address_id: int):
    db.query(_models.Address).filter(_models.Address.id == address_id).delete()
    db.commit()


def update_address(db: _orm.Session, address_id: int, address: _schemas.AddressCreate):
    db_address = get_address(db=db, address_id=address_id)
    db_address.address = address.address
    address_coordinates = get_address_coordinates(address.address)
    db_address.coordinates = address_coordinates
    db.commit()
    db.refresh(db_address)
    return db_address


def get_address_coordinates(address):
    geolocator = Nominatim(user_agent="geo-query-app")
    location = geolocator.geocode(address)
    coordinates = ""
    if location:
        coordinates = "Latitude : "+str(location.raw.get("lat"))+", Longitude: "+str(location.raw.get("lon"))
    return coordinates


#service to return the addresses within proximity (given distance)
def get_address_proximity(point: float, latitude: float, longitude: float, db: _orm.Session):
    db_data = db.query(_models.Address.coordinates, _models.Address.address).filter(_models.Address.coordinates != None).all()
    address_map = {}
    for data in db_data:
        address_map[data[1]] = [float(data[0].split(',')[0].split(':')[1]), float(data[0].split(',')[1].split(':')[1])]
    
    origin = [latitude, longitude]
    proximity_points = []
    for key in address_map.keys():
        if distance(address_map[key], origin) <= point:
            proximity_points.append(
            {
                'latitude': address_map[key][0],
                'longitude': address_map[key][1],
                'address': key
            })
    return proximity_points



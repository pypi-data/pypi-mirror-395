import pprint
from mambo.api.api import FastApi
from mambo.db.db_connection import DbConnection
from mambo.services.core_services import CoreServices

db = DbConnection()
services = CoreServices(db.engine)

api = FastApi(services)
api.run()

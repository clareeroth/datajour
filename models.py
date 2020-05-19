import peewee


db = peewee.SqliteDatabase(
  'detainees.db',
  pragmas={'foreign_keys': 1}
)

class Detainee(peewee.Model): 
  last_name = peewee.CharField()
  first_name = peewee.CharField()
  middle_name = peewee.CharField()
  suffix = peewee.CharField()
  sex = peewee.CharField()
  race = peewee.CharField()
  age = peewee.CharField()
  city = peewee.CharField()
  state = peewee.CharField()

  height = peewee.CharField()
  weight = peewee.CharField()
  eyes = peewee.CharField()
  hair = peewee.CharField()

  case_number = peewee.CharField()
  charge_description = peewee.CharField()
  charge_status = peewee.CharField()
  bail_amount = peewee.CharField()
  bond_type = peewee.CharField()
  court_date = peewee.CharField()
  court_time = peewee.CharField()
  court_of_jurisdiction = peewee.CharField()

  class Meta:
    database = db
    primary_key = peewee.CompositeKey(
            'last_name', 'first_name', 'middle_name'
        )

db.connect()
db.create_tables([Detainee])


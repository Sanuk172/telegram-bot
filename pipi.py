import sqlalchemy as db

engine = db.create_engine('sqlite:///dates.db')

connection = engine.connect()

metadata = db.MetaData()

dates = db.Table('dates', metadata,
                 db.Column('username', db.Text, nullable=False))

metadata.create_all(engine)

insertion_query = dates.insert().values([
    {'username': '1'},
    {'username': '2'},
    {'username': '4'}

])


connection.execute(insertion_query)

select_all_query = db.select(dates)
select_all_result = connection.execute(select_all_query)

print(select_all_result.fetchall())

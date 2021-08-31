import sqlalchemy

def data_base(user_id, users_id_for_send):
    # подключаемся к БД
    dsn = 'mysql+pymysql://alextuchak:qazwsxedc@alextuchak.mysql.pythonanywhere-services.com/alextuchak$VKinder'
    metadata = sqlalchemy.MetaData()
    engine = sqlalchemy.create_engine(dsn)
    con = engine.connect()

    # для каждого пользователя, которому ищем пару будет создаваться своя таблица.
    links = sqlalchemy.Table(f'MatchFor{user_id}', metadata,
                  sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                  sqlalchemy.Column('UsersIdForSend', sqlalchemy.String(40)),
                  )
    metadata.create_all(engine)
    return con.execute(links.insert().values(UsersIdForSend=users_id_for_send))


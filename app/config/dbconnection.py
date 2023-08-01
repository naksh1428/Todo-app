from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import dotenv_values
config = dotenv_values(".env")

#Use below code on prod env.
# sql_database_url = config.get("DATABASE_CONNECTION_URL")

sql_database_url = "mysql://root:root@localhost:3306/mydb"
engine = create_engine(sql_database_url)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = orm.declarative_base()
Base = declarative_base()

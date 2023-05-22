from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

class Database:
    def __init__(self, db_name="sqlite:///my_database.db"):
        self.engine = create_engine(db_name)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)



    def execute(self, query):
        result = self.session.execute(query)
        self.session.commit()
        return result

    def fetch(self, query):
        result = self.session.execute(query)
        return result.fetchall()

from sqlalchemy import create_engine, Column, Integer, String, Date, engine, interfaces
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import collate
from sqlalchemy.sql.expression import column


engine = create_engine('sqlite:///boks.db', echo = False)
Session = sessionmaker(bind=engine)
session = Session()
Dase = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column('Title'. String)
    author = Column('Author', String)
    published_date = Column('Published', Date)
    price = Column('Price', Integer)

    def __repr__(self):
        return f'Title: {self.title} Author: {self.author} Published: {self.published_date} Price: {self.price}'

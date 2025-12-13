from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

from datetime import datetime
import pandas as pd

Base = declarative_base()

class AbstractBase():
    
    @classmethod
    def truncate_table(cls, session):
        """Deletes all records from the table"""
        try:
            session.execute(text(f"DELETE FROM {cls.__tablename__}"))
            session.commit()
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Error deleting table: {e}")
        
    @classmethod
    def create_table(cls, engine):
        """Creates a table in the database"""
        Base.metadata.drop_all(engine, [cls.__table__])
        Base.metadata.create_all(engine, [cls.__table__])

    
    def add(self, session):
        """Adds a record to the database"""
        try:
            session.add(self)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise ValueError(f"Error inserting data: {e}")
        
    def delete(self, session):
        """Deletes a record from the database"""
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Error deleting: {e}")
        
    @classmethod
    def list_all(cls, session):
        """Returns a list of all records"""
        return session.query(cls).all()
    
    def update(self, session, *args, **kwargs):
        raise NotImplementedError("You must implement update method")


class CompanyRawData(AbstractBase, Base):
    __tablename__ = 'cbonds_company_raw_data'
    
    id_company = Column(Integer, primary_key=True)
    data = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    status = Column(String, nullable=False)
    success_flg = Column(Boolean, default=True)
    update_date_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
        
    @classmethod
    def get_by_id(cls, session, company_id):
        """Gets one record by company ID"""
        return session.query(CompanyRawData).filter_by(id_company=company_id).first()
            
    def update(self, session, new_data=None, new_file_path=None, new_success_flg=None, new_status=None):
        """Updates a record field"""
        if new_data is not None:
            self.data = new_data
        if new_file_path is not None:
            self.file_path = new_file_path
        if new_success_flg is not None:
            self.success_flg = new_success_flg
        if new_status is not None:
            self.status = new_status
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Error updating: {e}")

    @classmethod
    def get_successful_records(cls, session):
        """Gets all records with success_flg=True and returns a DataFrame"""
        records = session.query(CompanyRawData).filter_by(success_flg=True).all()
        df = pd.DataFrame([record.__dict__ for record in records])
        return df


class CompanyInfoData(AbstractBase, Base):
    __tablename__ = 'cbonds_company_info_data'
    
    id_company = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    ticker = Column(String, nullable=True)
    url = Column(String, nullable=True)
    isin = Column(String, nullable=True)
    currency_name = Column(String, nullable=True)
    update_date_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    @classmethod
    def get_by_id(cls, session, company_id):
        """Gets one record by company ID"""
        return session.query(CompanyInfoData).filter_by(id_company=company_id).first()
        
    def update(self, session, new_name=None, new_ticker=None, new_url=None, new_isin=None, new_currency_name=None):
        """Updates a record field"""
        if new_name is not None:
            self.name = new_name
        if new_ticker is not None:
            self.ticker = new_ticker
        if new_url is not None:
            self.url = new_url
        if new_isin is not None:
            self.isin = new_isin
        if new_currency_name is not None:
            self.currency_name = new_currency_name
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Error updating: {e}")


def init_table(engine):
    # Создаем табличку если нет её
    Base.metadata.create_all(engine)

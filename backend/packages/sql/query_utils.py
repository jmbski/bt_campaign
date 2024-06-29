import sys

from packages.sql.entities import Base

from sqlalchemy import (
    and_,
    create_engine, 
    insert,
    delete,
    update, 
)

from sqlalchemy.orm import scoped_session, sessionmaker, Session
from warskald.ws_config import EnvironmentProps

ENV_PROPS = EnvironmentProps()
APP_NAME = 'bt_campaign_mgr'
APP_PROPS = ENV_PROPS.get(APP_NAME)

engine = create_engine(APP_PROPS.db_uri)


# Create a configured "Session" class
session_factory = sessionmaker(bind=engine)

# Create a scoped session
DBSession = scoped_session(session_factory)

def props_to_filters(entity: Base, props: dict, loose: bool = False) -> list:
    """ Function to convert properties to filters """
    filters = []

    if(loose):
        for key, value in props.items():
            
            if(not hasattr(entity, key)):
                continue
            
            prop = getattr(entity, key)
            
            value_type = type(value)
            
            if(value_type == str):
                filters.append(prop.like(f"%{value}%"))
            elif(value_type == (int, float, bool)):
                filters.append(prop == value)
            elif(value_type == list):
                filters.append(prop.in_(value))
            elif(value_type == dict):
                filters.append(prop.contains(value))
            else:
                filters.append(prop == value)
            
                
    else:
        filters = [ getattr(entity, key) == value for key, value in props.items() if hasattr(entity, key) ]
    
    return filters

class QueryObject:
        
        def __init__(self, entity: Base, session: Session = None):
            if(entity is None):
                raise ValueError('entity must be provided')
            
            self.session = session if session else DBSession()
            self.entity: Base = entity
            
        def __enter__(self):
            return self.session
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close_session(True)
            if(exc_type):
                raise exc_type(exc_val)
            
        def close_session(self, commit: bool = False):
            """ Function to close a session """
            if(commit):
                self.session.commit()
            self.session.close()
            
        def clean_params(self, params: dict) -> dict:
            """ Cleans the parameters of a class by removing any that are not in the class 
                definition.
                
            Args:
                params (dict): The parameters to clean
                _class (type): The class to clean the parameters for
            """
            if(params is None):
                return {}
            
            return {key: value for key, value in params.items() if hasattr(self.entity, key)}
            
        def get(self, **where_props) -> Base:
            where_props = self.clean_params(where_props)
            return self.session.query(self.entity).filter_by(**where_props).first()
        
        def get_multiple(self, loose: bool = False, *cust_filters, **where_props) -> list[Base]:
            where_props = self.clean_params(where_props)
            
            filters = props_to_filters(self.entity, where_props, loose)
            if(cust_filters):
                filters.extend(cust_filters)
                
            return self.session.query(self.entity).filter(and_(*filters)).all()
        
        def save(self, **props) -> Base:
            props = self.clean_params(props)
            
            #entity = self.entity(**props)
            saved_obj = self.session.scalars(
                insert(self.entity)
                .values(props)
                .returning(self.entity)
            ).first()
            
            return saved_obj
        
        def save_bulk(self, data: list[dict]) -> list[Base]:
            
            data = [self.clean_params(props) for props in data]
            
            entities = [self.entity(**props) for props in data]
            
            self.session.add_all(entities)
            return entities
        
        def update(self, values: dict, **where_props) -> bool:
            where_props = self.clean_params(where_props)
            try:
                self.session.scalars(
                    update(self.entity)
                    .where(**where_props)
                    .values(values)
                    .returning(self.entity)
                ).first()
            except Exception as e:
                print(e.with_traceback(sys.exc_info()[2]))
                return e
            return True
            
        def delete(self, **where_props) -> int:
            where_props = self.clean_params(where_props)
            try:
                deleted_rows = self.session.scalars(
                    delete(self.entity)
                    .where(**where_props)
                    .returning(self.entity)
                ).all()
                return len(deleted_rows)
            except Exception as e:
                print(e.with_traceback(sys.exc_info()[2]))
                return e


    

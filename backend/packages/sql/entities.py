from __future__ import annotations
from typing import List
from inspect import isclass, isfunction
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey, 
    LargeBinary,
    
    String,
    Text,
    JSON,
    Table,
    PrimaryKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

def get_repr(entity: Base) -> str:
    """ Function to get the representation of an entity """
    repr_str = f'{entity.__class__.__name__}('
    for key, value in entity.__dict__.items():
        if(key.startswith('_') or isfunction(value) or isclass(value)):
            continue
        repr_str += f'{key}={value!r}, '
    repr_str = repr_str[:-2] + ')'
    return repr_str

class Base(DeclarativeBase):
    def to_json(self, debug_id: str = None) -> dict:
        print(f'getting json for {self.__class__.__name__}')
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_') and not isfunction(value) and not isclass(value)}
    
    def __repr__(self) -> str:
        return get_repr(self)

    
class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_email: Mapped[str] = mapped_column(String(255), nullable=False)
    
    rosters: Mapped[List['Roster']] = relationship(backref='owner')
    
class Mission(Base):
    __tablename__ = 'missions'
    mission_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mission_name: Mapped[str] = mapped_column(String(255), nullable=False)
    mission_description: Mapped[str] = mapped_column(Text)
    mission_data: Mapped[dict] = mapped_column(JSON)

class Roster(Base):
    __tablename__ = 'rosters'
    roster_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    roster_name: Mapped[str] = mapped_column(String(255), nullable=False)
    roster_description: Mapped[str] = mapped_column(Text)
    roster_owner: Mapped[int] = mapped_column(ForeignKey('users.user_id'), nullable=False)
    roster_data: Mapped[dict] = mapped_column(JSON)
    
    pilots: Mapped[List['Pilot']] = relationship(back_populates='roster')
    mechs: Mapped[List['Mech']] = relationship(back_populates='roster')
    #owner: Mapped['User'] = relationship(back_populates='rosters')
    
class Pilot(Base):
    __tablename__ = 'pilots'
    pilot_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pilot_name: Mapped[str] = mapped_column(String(255), nullable=False)
    pilot_callsign: Mapped[str] = mapped_column(String(255))
    gunnery_skill: Mapped[int] = mapped_column(BigInteger, nullable=False, default=4)
    piloting_skill: Mapped[int] = mapped_column(BigInteger, nullable=False, default=5)
    pilot_data: Mapped[dict] = mapped_column(JSON)
    portrait_path: Mapped[str] = mapped_column(String(255))
    
    roster_id: Mapped[int] = mapped_column(ForeignKey('rosters.roster_id'), nullable=False)
    roster: Mapped['Roster'] = relationship(back_populates='pilots')
    
    mech_id: Mapped[int] = mapped_column(ForeignKey('mechs.mech_id'))
    mech: Mapped['Mech'] = relationship(back_populates='pilot')

class Mech(Base):
    __tablename__ = 'mechs'
    mech_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mech_name: Mapped[str] = mapped_column(String(255), nullable=False)
    mech_variant: Mapped[str] = mapped_column(String(255), nullable=False)
    mech_data_id: Mapped[int] = mapped_column(ForeignKey('mech_data.mech_id'), nullable=False)
    mech_data: Mapped[dict] = mapped_column(JSON)
    mech_status: Mapped[str] = mapped_column(String(255), nullable=False)
    
    #mech_pilot_id: Mapped[int] = mapped_column(ForeignKey('pilots.pilot_id'))
    pilot: Mapped['Pilot'] = relationship(back_populates='mech')
    
    roster_id: Mapped[int] = mapped_column(ForeignKey('rosters.roster_id'), nullable=False)
    roster: Mapped['Roster'] = relationship(back_populates='mechs')
    
class Test(Base):
    __tablename__ = 'test'
    test_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_name: Mapped[str] = mapped_column(String(255), nullable=False)
    test_data: Mapped[bytes] = mapped_column(LargeBinary)
    
class MechDatum(Base):
    __tablename__ = 'mech_data'
    mech_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(String(255))
    mech_class: Mapped[str] = mapped_column(String(255))
    variant: Mapped[str] = mapped_column(String(255))
    tonnage: Mapped[int] = mapped_column(BigInteger)
    technology: Mapped[str] = mapped_column(String(255))
    cost: Mapped[int] = mapped_column(BigInteger)
    rules: Mapped[str] = mapped_column(Text)
    tro_id: Mapped[int] = mapped_column(BigInteger)
    tro: Mapped[str] = mapped_column(String(255))
    rs_id: Mapped[int] = mapped_column(BigInteger)
    rs: Mapped[str] = mapped_column(String(255))
    era_icon: Mapped[str] = mapped_column(String(255))
    date_introduced: Mapped[str] = mapped_column(String(255))
    era_id: Mapped[int] = mapped_column(BigInteger)
    era_start: Mapped[int] = mapped_column(BigInteger)
    image_url: Mapped[str] = mapped_column(String(255))
    is_featured: Mapped[bool] = mapped_column(Boolean)
    is_published: Mapped[bool] = mapped_column(Boolean)
    release: Mapped[int] = mapped_column(BigInteger)
    type: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255))
    battle_value: Mapped[int] = mapped_column(BigInteger)
    bf_type: Mapped[str] = mapped_column(String(255))
    bf_size: Mapped[int] = mapped_column(BigInteger)
    bf_move: Mapped[str] = mapped_column(String(255))
    bf_tmm: Mapped[int] = mapped_column(BigInteger)
    bf_armor: Mapped[int] = mapped_column(BigInteger)
    bf_structure: Mapped[int] = mapped_column(BigInteger)
    bf_threshold: Mapped[int] = mapped_column(BigInteger)
    bf_damage_short: Mapped[int] = mapped_column(BigInteger)
    bf_damage_short_min: Mapped[bool] = mapped_column(Boolean)
    bf_damage_medium: Mapped[int] = mapped_column(BigInteger)
    bf_damage_medium_min: Mapped[bool] = mapped_column(Boolean)
    bf_damage_long: Mapped[int] = mapped_column(BigInteger)
    bf_damage_long_min: Mapped[bool] = mapped_column(Boolean)
    bf_damage_extreme: Mapped[int] = mapped_column(BigInteger)
    bf_damage_extreme_min: Mapped[bool] = mapped_column(Boolean)
    bf_overheat: Mapped[int] = mapped_column(BigInteger)
    bf_point_value: Mapped[int] = mapped_column(BigInteger)
    bf_abilities: Mapped[str] = mapped_column(Text)
    skill: Mapped[int] = mapped_column(BigInteger)
    formated_tonnage: Mapped[str] = mapped_column(String(255))
    armor: Mapped[str] = mapped_column(Text)
    base_chassis_heat_sinks: Mapped[int] = mapped_column(BigInteger)
    capabilities: Mapped[str] = mapped_column(Text)
    capability: Mapped[str] = mapped_column(Text)
    center_leg: Mapped[list] = mapped_column(JSON)
    center_torso: Mapped[list] = mapped_column(JSON)
    cl_armor: Mapped[int] = mapped_column(BigInteger)
    cockpit: Mapped[str] = mapped_column(Text)
    config: Mapped[str] = mapped_column(Text)
    ct_armor: Mapped[int] = mapped_column(BigInteger)
    ct_armor_type: Mapped[str] = mapped_column(Text)
    deployment: Mapped[str] = mapped_column(Text)
    ejection: Mapped[str] = mapped_column(Text)
    engine: Mapped[str] = mapped_column(Text)
    era: Mapped[int] = mapped_column(BigInteger)
    fll_armor: Mapped[int] = mapped_column(BigInteger)
    frl_armor: Mapped[int] = mapped_column(BigInteger)
    front_left_leg: Mapped[list] = mapped_column(JSON)
    front_right_leg: Mapped[list] = mapped_column(JSON)
    gyro: Mapped[str] = mapped_column(Text)
    hd_armor: Mapped[int] = mapped_column(BigInteger)
    hd_armor_type: Mapped[str] = mapped_column(Text)
    head: Mapped[list] = mapped_column(JSON)
    heat_sinks: Mapped[str] = mapped_column(Text)
    hist: Mapped[str] = mapped_column(Text)
    history: Mapped[str] = mapped_column(Text)
    image_file: Mapped[str] = mapped_column(Text)
    image: Mapped[bytes] = mapped_column(LargeBinary)
    jump_mp: Mapped[int] = mapped_column(BigInteger)
    la_armor: Mapped[int] = mapped_column(BigInteger)
    la_armor_type: Mapped[str] = mapped_column(Text)
    lam: Mapped[str] = mapped_column(Text)
    left_arm: Mapped[list] = mapped_column(JSON)
    left_leg: Mapped[list] = mapped_column(JSON)
    left_torso: Mapped[list] = mapped_column(JSON)
    ll_armor: Mapped[int] = mapped_column(BigInteger)
    ll_armor_type: Mapped[str] = mapped_column(Text)
    lt_armor: Mapped[int] = mapped_column(BigInteger)
    lt_armor_type: Mapped[str] = mapped_column(Text)
    manufacturer: Mapped[str] = mapped_column(Text)
    mass: Mapped[int] = mapped_column(BigInteger)
    mech_name: Mapped[str] = mapped_column(Text)
    motive: Mapped[str] = mapped_column(Text)
    myomer: Mapped[str] = mapped_column(Text)
    nocrit: Mapped[str] = mapped_column(Text)
    notes: Mapped[str] = mapped_column(Text)
    overview: Mapped[str] = mapped_column(Text)
    primary_factory: Mapped[str] = mapped_column(Text)
    ra_armor: Mapped[int] = mapped_column(BigInteger)
    ra_armor_type: Mapped[str] = mapped_column(Text)
    rear_left_leg: Mapped[list] = mapped_column(JSON)
    rear_right_leg: Mapped[list] = mapped_column(JSON)
    right_arm: Mapped[list] = mapped_column(JSON)
    right_leg: Mapped[list] = mapped_column(JSON)
    right_torso: Mapped[list] = mapped_column(JSON)
    rl_armor: Mapped[int] = mapped_column(BigInteger)
    rl_armor_type: Mapped[str] = mapped_column(Text)
    rll_armor: Mapped[int] = mapped_column(BigInteger)
    rrl_armor: Mapped[int] = mapped_column(BigInteger)
    rt_armor: Mapped[int] = mapped_column(BigInteger)
    rt_armor_type: Mapped[str] = mapped_column(Text)
    rtc_armor: Mapped[int] = mapped_column(BigInteger)
    rtl_armor: Mapped[int] = mapped_column(BigInteger)
    rtr_armor: Mapped[int] = mapped_column(BigInteger)
    rules_level: Mapped[int] = mapped_column(BigInteger)
    source: Mapped[str] = mapped_column(Text)
    structure: Mapped[str] = mapped_column(Text)
    system_manufacturer: Mapped[dict] = mapped_column(JSON)
    system_mode: Mapped[dict] = mapped_column(JSON)
    tech_base: Mapped[str] = mapped_column(Text)
    version: Mapped[str] = mapped_column(Text)
    walk_mp: Mapped[int] = mapped_column(BigInteger)
    weapons: Mapped[list] = mapped_column(JSON)

ENTITY_MAP = {
    'User': User,
    'Mission': Mission,
    'Pilot': Pilot,
    'MechData': MechDatum,
}
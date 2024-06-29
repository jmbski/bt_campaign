# coding: utf-8
from __future__ import annotations
from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, Numeric, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from inspect import isclass, isfunction
from abc import ABC, abstractmethod

class AbstractBase(ABC):
    @abstractmethod
    def to_json(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError


Base: AbstractBase = declarative_base()
metadata = Base.metadata

def get_repr(self: AbstractBase) -> str:
    """ Function to get the representation of an entity """
    repr_str = f'{self.__class__.__name__}('
    for key, value in self.__dict__.items():
        if(key.startswith('_') or isfunction(value) or isclass(value)):
            continue
        repr_str += f'{key}={value!r}, '
    repr_str = repr_str[:-2] + ')'
    return repr_str

def to_json(self, debug_id: str = None) -> dict:
    print(f'getting json for {self.__class__.__name__}')
    return {key: value for key, value in self.__dict__.items() if not key.startswith('_') and not isfunction(value) and not isclass(value)}

Base.to_json = to_json
Base.__repr__ = get_repr

class MechDatum(Base):
    __tablename__ = 'mech_data'

    mech_id = Column(Integer, primary_key=True)
    group_name = Column(Text)
    mech_class = Column(Text)
    variant = Column(Text)
    tonnage = Column(Integer)
    technology = Column(Text)
    cost = Column(Integer)
    rules = Column(Text)
    tro_id = Column(Integer)
    tro = Column(Text)
    rs_id = Column(Integer)
    rs = Column(Text)
    era_icon = Column(Text)
    date_introduced = Column(Text)
    era_id = Column(Integer)
    era_start = Column(Integer)
    image_url = Column(Text)
    is_featured = Column(Integer)
    is_published = Column(Integer)
    release = Column(Numeric)
    type = Column(Text)
    role = Column(Text)
    battle_value = Column(Integer)
    bf_type = Column(Text)
    bf_size = Column(Integer)
    bf_move = Column(Text)
    bf_tmm = Column(Integer)
    bf_armor = Column(Integer)
    bf_structure = Column(Integer)
    bf_threshold = Column(Integer)
    bf_damage_short = Column(Integer)
    bf_damage_short_min = Column(Integer)
    bf_damage_medium = Column(Integer)
    bf_damage_medium_min = Column(Integer)
    bf_damage_long = Column(Integer)
    bf_damage_long_min = Column(Integer)
    bf_damage_extreme = Column(Integer)
    bf_damage_extreme_min = Column(Integer)
    bf_overheat = Column(Integer)
    bf_point_value = Column(Integer)
    bf_abilities = Column(Text)
    skill = Column(Integer)
    formated_tonnage = Column(Text)
    armor = Column(Text)
    base_chassis_heat_sinks = Column(Integer)
    capabilities = Column(Text)
    capability = Column(Text)
    center_leg = Column(LargeBinary)
    center_torso = Column(LargeBinary)
    cl_armor = Column(Integer)
    cockpit = Column(Text)
    config = Column(Text)
    ct_armor = Column(Integer)
    ct_armor_type = Column(Text)
    deployment = Column(Text)
    ejection = Column(Text)
    engine = Column(Text)
    era = Column(Integer)
    fll_armor = Column(Integer)
    frl_armor = Column(Integer)
    front_left_leg = Column(LargeBinary)
    front_right_leg = Column(LargeBinary)
    gyro = Column(Text)
    hd_armor = Column(Integer)
    hd_armor_type = Column(Text)
    head = Column(LargeBinary)
    heat_sinks = Column(Text)
    hist = Column(Text)
    history = Column(Text)
    image_file = Column(Text)
    jump_mp = Column(Integer)
    la_armor = Column(Integer)
    la_armor_type = Column(Text)
    lam = Column(Text)
    left_arm = Column(LargeBinary)
    left_leg = Column(LargeBinary)
    left_torso = Column(LargeBinary)
    ll_armor = Column(Integer)
    ll_armor_type = Column(Text)
    lt_armor = Column(Integer)
    lt_armor_type = Column(Text)
    manufacturer = Column(Text)
    mass = Column(Integer)
    mech_name = Column(Text)
    motive = Column(Text)
    myomer = Column(Text)
    nocrit = Column(Text)
    notes = Column(Text)
    overview = Column(Text)
    primary_factory = Column(Text)
    ra_armor = Column(Integer)
    ra_armor_type = Column(Text)
    rear_left_leg = Column(LargeBinary)
    rear_right_leg = Column(LargeBinary)
    right_arm = Column(LargeBinary)
    right_leg = Column(LargeBinary)
    right_torso = Column(LargeBinary)
    rl_armor = Column(Integer)
    rl_armor_type = Column(Text)
    rll_armor = Column(Integer)
    rrl_armor = Column(Integer)
    rt_armor = Column(Integer)
    rt_armor_type = Column(Text)
    rtc_armor = Column(Integer)
    rtl_armor = Column(Integer)
    rtr_armor = Column(Integer)
    rules_level = Column(Integer)
    source = Column(Text)
    structure = Column(Text)
    system_manufacturer = Column(LargeBinary)
    system_mode = Column(LargeBinary)
    tech_base = Column(Text)
    version = Column(Text)
    walk_mp = Column(Integer)
    weapons = Column(LargeBinary)


class Mech(Base):
    __tablename__ = 'mechs'

    mech_id = Column(Integer, primary_key=True)
    mech_name = Column(Text, nullable=False)
    mech_variant = Column(Text, nullable=False)
    mech_data_id = Column(ForeignKey('mech_data.mech_id'), nullable=False)
    mech_data = Column(LargeBinary)
    mech_status = Column(Text, nullable=False)
    mech_pilot_id = Column(ForeignKey('pilots.pilot_id'), unique=True)
    roster_id = Column(ForeignKey('rosters.roster_id'), nullable=False)

    mech_data1 = relationship('MechDatum')
    mech_pilot = relationship('Pilot', uselist=False, primaryjoin='Mech.mech_pilot_id == Pilot.pilot_id')
    roster = relationship('Roster')


class Mission(Base):
    __tablename__ = 'missions'

    mission_id = Column(Integer, primary_key=True)
    mission_name = Column(Text, nullable=False)
    mission_description = Column(Text)
    mission_data = Column(LargeBinary)


class Pilot(Base):
    __tablename__ = 'pilots'

    pilot_id = Column(Integer, primary_key=True)
    pilot_name = Column(Text, nullable=False, unique=True)
    pilot_callsign = Column(Text)
    gunnery_skill = Column(Integer, nullable=False, server_default=text("4"))
    piloting_skill = Column(Integer, nullable=False, server_default=text("5"))
    pilot_data = Column(LargeBinary)
    portrait_path = Column(Text)
    roster_id = Column(ForeignKey('rosters.roster_id'), nullable=False)
    mech_id = Column(ForeignKey('mechs.mech_id'))

    mech = relationship('Mech', primaryjoin='Pilot.mech_id == Mech.mech_id')
    roster = relationship('Roster')


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(Text, nullable=False)
    user_email = Column(Text, nullable=False)


class Roster(Base):
    __tablename__ = 'rosters'

    roster_id = Column(Integer, primary_key=True)
    roster_name = Column(Text, nullable=False)
    roster_description = Column(Text)
    roster_owner = Column(ForeignKey('users.user_id'), nullable=False)
    roster_data = Column(LargeBinary)

    user = relationship('User')

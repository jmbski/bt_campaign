from common import APP_NAME, KEY_SWAP
from modules import data_utils

from collections import defaultdict
from warskald import utils, AttrDict, EnvironmentProps
from warskald.utils import p_exists, p_join

ENV_PROPS = EnvironmentProps()
APP_PROPS = ENV_PROPS.get(APP_NAME)

IGNORED_MULTI_KEYS = [
    'source',
    'cargo',
    'history',
]

MUTLI_KEY_PROPS = [
    'system_mode',
    'system_manufacturer',
]

LIST_PROPS = [
    'right_arm',
    'rear_left_leg',
    'right_leg',
    'rear_right_leg',
    'center_leg',
    'left_arm',
    'right_torso',
    'head',
    'left_leg',
    'front_left_leg',
    'center_torso',
    'weapons',
    'left_torso',
    'front_right_leg'
]

class MtfReader:
    def __init__(self, path: str):
        self.path = path
        self.equipment = set()
        self.weapons = set()
        self.keys = set()
        
    def read_mtf(self) -> list[str]:
        if(not p_exists(self.path)):
            raise FileNotFoundError(f'MTF file not found at {self.path}')
        
        with open(self.path, 'r') as mtf_file:
            lines = mtf_file.readlines()
            
        return lines
    
    
    def parse_mtf(self) -> dict:
        lines = self.read_mtf()
        mtf_data = AttrDict()
        mtf_data.version = lines.pop(0).strip().split(':')[-1].strip()
        mtf_data.mech_name = lines.pop(0).strip()
        
        variant = lines.pop(0).strip()
        mtf_data.variant = variant if variant else 'N/A'
        
        list_open = False
        
        key = None
        
        for line in lines:
            line = line.strip()
            if(not line):
                list_open = False
                continue
            
            if(list_open and key in LIST_PROPS):
                if(key == 'weapons'):
                    weapon_values = line.split(',')
                    name = data_utils.split_case(weapon_values.pop(0))
                    location = weapon_values.pop(0)
                    if(len(weapon_values) > 0):
                        ammo_str = weapon_values.pop(0)
                        ammo = ammo_str.split(':')[-1].strip()
                        ammo = int(ammo) if ammo.isdigit() else -1
                    else:
                        ammo = -1
                        
                    mtf_data[key].append({
                        'name': name,
                        'location': location,
                        'ammo': ammo
                    })
                    
                else:
                    mtf_data[key].append(data_utils.split_case(line))
            
            elif(':' in line):
                
                key, value = line.split(':', 1)
                key = data_utils.normalize_key(key)
                
                self.keys.add(key)
                    
                if(key in MUTLI_KEY_PROPS):
                    if(key not in mtf_data):
                        mtf_data[key] = {}
                    if(line.count(':') > 1):
                        sub_key, sub_value = value.split(':', 1)
                    else:
                        sub_key = mtf_data.mech_name
                        sub_value = value
                    sub_key = data_utils.normalize_key(sub_key)
                    
                    mtf_data[key][sub_key] = sub_value
                    
                elif(key in LIST_PROPS):
                    if(key not in mtf_data):
                        mtf_data[key] = []
                    list_open = True
                    
                elif(key.endswith('_armor')):
                    type_key = f'{key}_type'
                    if(':' in value):
                        type_value, value = value.split(':', 1)
                        
                        mtf_data[type_key] = type_value
                    mtf_data[key] = int(value) if value.isdigit() else value
                
                else:
                    mtf_data[key] = int(value) if value.isdigit() else value
                
        return mtf_data
            
        
        
        
        
        
        
import json
import os
import re

from common import APP_NAME, KEY_SWAP
from modules import data_utils
from modules.mtf_reader import MtfReader
from packages.sql import QueryObject, entities
from tqdm import tqdm

from collections import defaultdict
from warskald.ws_config import EnvironmentProps
from warskald import utils, AttrDict

ENV_PROPS = EnvironmentProps()
APP_PROPS = ENV_PROPS.get(APP_NAME)



mul_keys = set()

def write_data(data: dict | list, file_name: str, indent: int = 4):
    path = APP_PROPS.output_dir
    if(not os.path.exists(path)):
        raise FileNotFoundError(f'Output directory not found at {path}')
    
    file_path = os.path.join(path, file_name)
    
    with open(file_path, 'w') as json_data:
        json.dump(data, json_data, indent=4)
        
def normalize_key(key: str) -> str:
    """ Swaps the class key from camel case to snake case.
    
    Args:
        key (str): The key to swap
    
    Returns:
        str: The swapped key
    """
    key = utils.to_snake_case(key).lower()
    norm_key = KEY_SWAP.get(key, key)
    mul_keys.add(norm_key)
    return norm_key

def normalize_keys(data: list | dict) -> list | dict:
    """ Normalizes the keys of a list or dictionary to lower case.
    
    Args:
        data (list | dict): The data to normalize
    
    Returns:
        list | dict: The normalized data
    """
    
    if(isinstance(data, list)):
        return [normalize_keys(item) for item in data]
    elif(isinstance(data, dict)):
        return {normalize_key(key): normalize_keys(value) for key, value in data.items()}
    else:
        return data
    

def parse_data():
    data_dir = APP_PROPS.data_dir
    if(not os.path.exists(data_dir)):
        raise FileNotFoundError(f'Data directory not found at {data_dir}')
    
    for file_name in os.listdir(data_dir):
        mul_keys.clear()
        if(file_name.startswith('normalized_')):
            continue
        
        file_path = os.path.join(data_dir, file_name)
        
        with open(file_path, 'r') as json_data:
            data = json.load(json_data)
            
        data = normalize_keys(data)
        print(f'Normalized keys for {file_name}')
        utils.pretty_print(list(mul_keys))
        new_file_name = f'normalized_{file_name}'
        write_data(data, new_file_name)
        

def upload_mul():
    query = QueryObject(entities.MulData)
    data_dir = APP_PROPS.output_dir
    if(not os.path.exists(data_dir)):
        raise FileNotFoundError(f'Data directory not found at {data_dir}')
    
    mul_path = os.path.join(data_dir, 'normalized_linked-units.json')
    with open(mul_path, 'r') as json_data:
        mul_data = json.load(json_data)
        
    query.save_bulk(mul_data)
    query.close_session(True)
    
def check_mtf_file(path: str):
    if(not os.path.exists(path)):
        raise FileNotFoundError(f'MTF file not found at {path}')
    
    with open(path, 'r') as reader:
        data: list[str] = reader.readlines()
        
        version, name, variant = data[:3]
        
        data = data[3:]
        
        keys = set()
        
        multi_colon = set()
        
        list_keys = set()
        
        last_was_key = False
        
        list_open = False
        
        for line in data:
            line = line.strip()
            
            if(line.startswith('#')):
                continue
            if(not line):
                list_open = False
                last_was_key = False
                continue
            if(':' in line and ',' not in line):
                if(line.count(':') > 1 and 'system' not in line.lower() and 'source' not in line.lower()):
                    multi_colon.add(line)
                    continue
                last_was_key = True
                key, value = line.split(':', 1)
                norm_key = normalize_key(key.strip())
                value_type = data_utils.parse_type(value.strip())
                keys.add((norm_key, value_type))
            
            else:
                if(last_was_key and not list_open):
                    list_open = True
                    list_keys.add(norm_key)
                    if(norm_key == 'rules_level'):
                        print(path)
                    continue
                last_was_key = False
            
        version_number = version.split(':')[-1].strip()
        name_exists = len(name.strip()) > 0
        variant_exists = len(variant.strip()) > 0
        
    return version_number, name_exists, variant_exists, keys, list_keys

def scan_mech_data():
    path = APP_PROPS.mech_data_dir
    if(not os.path.exists(path)):
        raise FileNotFoundError(f'Mech data directory not found at {path}')
    
    file_exts = set()
    mtf_vers_nums = set()
    mtf_vers_paths = {}
    mtf_vers_counts = defaultdict(int)
    mtf_empty_names = set()
    mtf_empty_variants = set()
    mtf_keys = set()
    mtf_multi_colon = set()
    
    for root, dirs, files in os.walk(path):
        for file_name in files:
            ext = os.path.splitext(file_name)[1]
            file_exts.add(ext)
            
            if(ext != '.mtf'):
                continue
            
            path = os.path.join(root, file_name)
            
            version_number, name_exists, variant_exists, keys, multi_colon = check_mtf_file(path)
            
            mtf_vers_counts[version_number] += 1
            
            mtf_vers_paths[version_number] = path
                
            mtf_vers_nums.add(version_number)
            
            mtf_keys.update(keys)
            
            mtf_multi_colon.update(multi_colon)
            
            if(not name_exists):
                mtf_empty_names.add(path)
            if(not variant_exists):
                mtf_empty_variants.add(path)
                
    mtf_keys = list(mtf_keys)
    mtf_keys.sort()
    mtf_keys = {key: value for key, value in mtf_keys}
    report = {
        'file_exts': list(file_exts),
        'mtf': {
            'version_numbers': list(mtf_vers_nums),
            'vers_paths': mtf_vers_paths,
            'vers_counts': dict(mtf_vers_counts),
            'keys': mtf_keys,
            'empty_names': list(mtf_empty_names),
            'empty_variants': list(mtf_empty_variants),
            'multi_colon': list(mtf_multi_colon),
        }
    }
    
    write_data(report, 'mech_data_scan.json')

def parse_mtf_data():
    path = APP_PROPS.mech_data_dir
    if(not os.path.exists(path)):
        raise FileNotFoundError(f'Mech data directory not found at {path}')
    
    mtf_data = []
    all_equipment = set()
    all_weapons = set()
    
    for root, dirs, files in os.walk(path):
        for file_name in files:
            ext = os.path.splitext(file_name)[1]
            
            if(ext != '.mtf'):
                continue
            
            path = os.path.join(root, file_name)
            
            reader = MtfReader(path)
            mtf_data.append(reader.parse_mtf())
            all_equipment.update(reader.equipment)
            all_weapons.update(reader.weapons)
            
    all_equipment = list(all_equipment)
    all_equipment.sort()
    all_equipment = [data_utils.split_case(equip) for equip in all_equipment]
    all_weapons = list(all_weapons)
    all_weapons.sort()
    
    all_keys = list(set([key for mtf in mtf_data for key in mtf.keys()]))
    all_keys.sort()
    utils.pretty_print(all_keys)
    write_data(mtf_data, 'mtf_data.json')
    
def upload_mtf():
    data_dir = APP_PROPS.output_dir
    if(not os.path.exists(data_dir)):
        raise FileNotFoundError(f'Data directory not found at {data_dir}')
    
    query = QueryObject(entities.MtfData)
    
    mtf_path = os.path.join(data_dir, 'mtf_data.json')
    
    with open(mtf_path, 'r') as json_data:
        mtf_data = json.load(json_data)
        
    query.save_bulk(mtf_data)
    query.close_session(True)
    
def combine_mtf_mul():
    mul_query = QueryObject(entities.MulData)
    mul_data = [ mul.to_json() for mul in mul_query.get_multiple() ]
    #mul_query.close_session()
    
    mtf_query = QueryObject(entities.MtfData)
    mtf_data = [ mtf.to_json() for mtf in mtf_query.get_multiple() ]
    
    combined_query = QueryObject(entities.CombinedMech)
    combined_query.delete()
    
    combined_data = []
    doubles = []
    no_match = []
    combined_count = 0
    for mul in tqdm(mul_data):
        variant = mul.get('variant', 'N/A').strip()
        mtf = list(filter(lambda mtf: variant == mtf.get('variant', 'N/A').strip() and mtf['mech_name'] in mul['name'], mtf_data))
        if(len(mtf) == 1):
            mtf_datum = mtf[0]
            
            combined_datum = {**mul, **mtf_datum}
            combined_datum['mul_id'] = mul['id']
            combined_datum['mtf_id'] = mtf_datum['id']
            del combined_datum['id']
            combined_data.append(combined_datum)
        elif(len(mtf) > 1):
            best_match = None
            best_score = 10000
            mul_name: str = mul['name']
            for i, mtf_sub in enumerate(mtf):
                mtf_name = mtf_sub['mech_name']
                score = len(mul_name.replace(mtf_name, '').strip())
                if(score < best_score):
                    best_score = score
                    best_match = i
                    
            mtf_match = mtf.pop(best_match)
            combined_datum = {**mul, **mtf_match}
            combined_datum['mul_id'] = mul['id']
            combined_datum['mtf_id'] = mtf_match['id']
            del combined_datum['id']
            combined_data.append(combined_datum)
            
            if(mtf_match is None):
                double = {
                    'mul': {
                        'name': mul['name'],
                        'variant': mul['variant']
                    },
                    'mtf': [ {'mech_name': mtf_sub['mech_name'],'variant': mtf_sub['variant'] } for mtf_sub in mtf ]
                }
                doubles.append(double)
        else:
            no_match.append(mul)
            
    write_data(doubles, 'doubles.json')
    write_data(no_match, 'no_match.json')
    
    print(f'doubles: {len(doubles)}, no_match: {len(no_match)}')
    combined_query.save_bulk(combined_data)
    combined_query.close_session(True)
    mul_query.close_session()
    mtf_query.close_session()
    
def check_doubles():
    """ data_dir = APP_PROPS.output_dir
    if(not os.path.exists(data_dir)):
        raise FileNotFoundError(f'Data directory not found at {data_dir}')
    path = os.path.join(data_dir, 'doubles.json')
    with open(path, 'r') as json_data:
        doubles = json.load(json_data) """
    pass
        
    
    
def main():
    parse_data()
    
    
if (__name__ == "__main__"):
    main()
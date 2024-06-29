import json
import os
import re

from common import APP_NAME, KEY_SWAP
from modules import data_utils
from modules.mtf_reader import MtfReader
from packages.sql import QueryObject, entities
from PIL import Image
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
        
def load_data(file_name: str) -> dict | list:
    path = APP_PROPS.output_dir
    
    if(not os.path.exists(path)):
        raise FileNotFoundError(f'Output directory not found at {path}')
    
    file_path = os.path.join(path, file_name)
    
    if(not os.path.exists(file_path)):
        raise FileNotFoundError(f'File not found at {file_path}')
    
    with open(file_path, 'r') as json_data:
        return json.load(json_data)
        
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
    

def parse_mul_data():
    data_dir = APP_PROPS.data_dir
    if(not os.path.exists(data_dir)):
        raise FileNotFoundError(f'Data directory not found at {data_dir}')
    
    print('Parsing MUL data')
    for file_name in tqdm(os.listdir(data_dir)):
        mul_keys.clear()
        if(file_name.startswith('normalized_')):
            continue
        
        file_path = os.path.join(data_dir, file_name)
        
        if(os.path.isdir(file_path)):
            continue
        with open(file_path, 'r') as json_data:
            data = json.load(json_data)
            
        data = normalize_keys(data)
        #print(f'Normalized keys for {file_name}')
        #utils.pretty_print(list(mul_keys))
        new_file_name = f'normalized_{file_name}'
        write_data(data, new_file_name)
        
def parse_mtf_data():
    path = APP_PROPS.mech_data_dir
    if(not os.path.exists(path)):
        raise FileNotFoundError(f'Mech data directory not found at {path}')
    
    mtf_data = []
    all_equipment = set()
    all_weapons = set()
    
    print('Parsing MTF data')
    for root, dirs, files in tqdm(os.walk(path)):
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
    #utils.pretty_print(all_keys)
    write_data(mtf_data, 'mtf_data.json')
        

def upload_mul():
    print('upload_mul has been deprecated')
    
    """ query = QueryObject(entities.MulData)
    data_dir = APP_PROPS.output_dir
    if(not os.path.exists(data_dir)):
        raise FileNotFoundError(f'Data directory not found at {data_dir}')
    
    mul_path = os.path.join(data_dir, 'normalized_linked-units.json')
    with open(mul_path, 'r') as json_data:
        mul_data = json.load(json_data)
        
    query.save_bulk(mul_data)
    query.close_session(True) """
    
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

def upload_mtf():
    print('upload_mtf has been deprecated')
    
    """ data_dir = APP_PROPS.output_dir
    if(not os.path.exists(data_dir)):
        raise FileNotFoundError(f'Data directory not found at {data_dir}')
    
    query = QueryObject(entities.MtfData)
    
    mtf_path = os.path.join(data_dir, 'mtf_data.json')
    
    with open(mtf_path, 'r') as json_data:
        mtf_data = json.load(json_data)
        
    query.save_bulk(mtf_data)
    query.close_session(True) """
    
def combine_mtf_mul():
    
    parse_mtf_data()
    parse_mul_data()
    
    mul_data = load_data('normalized_linked-units.json')
    mtf_data = load_data('mtf_data.json')
    
    combined_query = QueryObject(entities.MechDatum)
    combined_query.delete()
    
    combined_data = []
    doubles = []
    no_match = []
    
    for mul in tqdm(mul_data):
        variant = mul.get('variant', 'N/A').strip()
        mtf = list(filter(lambda mtf: variant == mtf.get('variant', 'N/A').strip() and mtf['mech_name'] in mul['name'], mtf_data))
        
        if(len(mtf) == 1):
            mtf_datum = mtf[0]
            
            combined_datum = {**mul, **mtf_datum}
            
            if('id' in combined_datum):
                del combined_datum['id']
            
            """ if('image_url' in combined_datum):
                img_name = os.path.basename(combined_datum['image_url'])
                img_path = os.path.join(APP_PROPS.imgs_dir, img_name)
                if(os.path.exists(img_path)):
                    with open(img_path, 'rb') as img_data:
                        img = img_data.read()
                    combined_datum['image'] = img """
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
            """ combined_datum = {**mul, **mtf_match}
            if('image_url' in combined_datum):
                img_name = os.path.basename(combined_datum['image_url'])
                img_path = os.path.join(APP_PROPS.imgs_dir, img_name)
                if(os.path.exists(img_path)):
                    with open(img_path, 'rb') as img_data:
                        img = img_data.read()
                    combined_datum['image'] = img """
            combined_datum = {**mul, **mtf_match}
            if('id' in combined_datum):
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
    
def test_sql():
    user_data = {
        'user_name': 'jmbski',
        'user_email': 'test@email.com',
    }
    user_query = QueryObject(entities.User)
    user_query.delete()
    
    user_obj = user_query.save(**user_data).to_json()
    user_query.close_session(True)
    
    roster_data = {
        'roster_owner': user_obj['user_id'],
        'roster_name': 'test_roster',
        'roster_description': 'test_desc',
        'roster_data': {},
    }
    roster_query = QueryObject(entities.Roster)
    roster_query.delete()
    roster = roster_query.save(**roster_data).to_json()
    roster_query.close_session(True)
    
    mech_data_query = QueryObject(entities.MechDatum)
    mech_base_data = mech_data_query.get_multiple(variant='AS7-S')[0].to_json()
    mech_data_query.close_session()
    
    mech_query = QueryObject(entities.Mech)
    mech_query.delete()
    mech_data = {
        'mech_name': mech_base_data['mech_name'],
        'mech_variant': mech_base_data['variant'],
        'mech_data_id': mech_base_data['mech_id'],
        'mech_data': mech_base_data,
        'mech_status': 'active',
        'mech_roster': roster['roster_id'],
        'roster_id': roster['roster_id'],
    }
    
    mech = mech_query.save(**mech_data).to_json()
    mech_query.close_session(True)
    
    pilot_data = {
        'pilot_name': 'test_pilot',
        'pilot_callsign': 'test_callsign',
        'gunnery_skill': 4,
        'piloting_skill': 4,
        'pilot_data': {},
        'portrait_path': 'test_portrait',
        'roster_id': roster['roster_id'],
        'mech_id': mech['mech_id'],
    }
    pilot_query = QueryObject(entities.Pilot)
    pilot_query.delete()
    pilot = pilot_query.save(**pilot_data).to_json()
    
    pilot_query.close_session(True)
    
    utils.pretty_print(pilot)
    
def test_image():
    if(not os.path.exists(APP_PROPS.imgs_dir)):
        raise FileNotFoundError(f'Images directory not found at {APP_PROPS.imgs_dir}')
    
    image_name = 'Atlas_AS7-S_(Hanssen).png'
    
    img_path = os.path.join(APP_PROPS.imgs_dir, image_name)
    
    if(not os.path.exists(img_path)):
        raise FileNotFoundError(f'Image not found at {img_path}')
    
    with open(img_path, 'rb') as img_data:
        img = img_data.read()
    
    test_query = QueryObject(entities.Test)
    
    test_data = {
        'test_name': 'test',
        'test_data': img,
    }
    
    test_query.save(**test_data)
    test_query.close_session(True)
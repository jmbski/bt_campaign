import re

from common import APP_NAME, KEY_SWAP

from warskald import utils, EnvironmentProps

ENV_PROPS = EnvironmentProps()
APP_PROPS = ENV_PROPS.get(APP_NAME)
    
def normalize_key(key: str) -> str:
    """ Swaps the class key from camel case to snake case.
    
    Args:
        key (str): The key to swap
    
    Returns:
        str: The swapped key
    """
    key = utils.to_snake_case(key).lower()
    norm_key = KEY_SWAP.get(key, key)
    
    return norm_key

def parse_type(value: str) -> str:
    float_pattern = r'^\d+\.\d+$'
    int_pattern = r'^\d+$'
    bool_pattern = r'^(true|false)$'
    
    if(re.match(float_pattern, value)):
        return 'float'
    elif(re.match(int_pattern, value)):
        return 'int'
    elif(re.match(bool_pattern, value)):
        return 'bool'
    else:
        return 'str'
    
def has_key(line: str) -> bool:
    return ':' in line and ',' not in line

def transform_label(input_label):
    # Define the regex pattern to match 'CL' or 'IS' followed by any number of alphabetic characters and digits
    pattern = re.compile(r'^(CL|IS)([A-Za-z0-9]+.*)')

    def format_label(match):
        prefix = match.group(1)
        rest_text = match.group(2)

        # Split the rest_text based on transitions between lowercase to uppercase or digits
        parts = re.findall(r'[A-Z][a-z]*|\d+|[A-Z]+', rest_text)

        # Combine the parts into readable label
        transformed_label = f"{prefix} {' '.join(parts)}".strip()
        return transformed_label

    # Apply the regex pattern and the formatting function
    transformed_label = pattern.sub(format_label, input_label)
    return transformed_label

def split_case(value: str) -> str:
    
    value = re.sub('([a-z0-9])([A-Z])', r'\1 \2', value)
    value = re.sub('(CL|IS)(\S)', r'\1 \2', value)
    
    return value#.lower()

def clean_params(params: dict, _class) -> dict:
    """ Cleans the parameters of a class by removing any that are not in the class 
        definition.
        
    Args:
        params (dict): The parameters to clean
        _class (type): The class to clean the parameters for
    """
    return {key: value for key, value in params.items() if hasattr(_class, key)}
from modules import data_parser, data_utils
from warskald import get_inputs, utils, EnvironmentProps
from packages.sql.query_utils import QueryObject
from packages.sql import entities

APP_NAME = 'bt_campaign_mgr'
ENV_PROPS = EnvironmentProps()
APP_PROPS = ENV_PROPS.get(APP_NAME)

def main():
    args = get_inputs()
    
    if(args.p):
        data_parser.parse_mul_data()
    if(args.s):
        query = QueryObject(entities.User)
        query.save(user_name='jmbski', user_email='stirgejr@gmail.com')
        query.close_session(True)
    if(args.u):
        data_parser.upload_mul()
    if(args.q):
        query = QueryObject(entities.MulData)
        result = query.get_multiple(loose=True, name=args.q)
        query.close_session()
        
        result = [item.to_json() for item in result]
        utils.pretty_print(result)
    if(args.S):
        data_parser.scan_mech_data()
    if(args.M):
        data_parser.parse_mtf_data()
    if(args.U):
        data_parser.upload_mtf()
    if(args.C):
        data_parser.combine_mtf_mul()
    if(args.t):
        data_parser.test_sql()
    if(args.T):
        data_parser.test_image()
    
if (__name__ == "__main__"):
    main()
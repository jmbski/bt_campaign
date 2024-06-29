import os
import subprocess

from typing import Callable
from warskald import EnvironmentProps, cmdx, utils

ENV_PROPS = EnvironmentProps()
APP_NAME = 'bt_campaign_mgr'
APP_PROPS = ENV_PROPS.get(APP_NAME)

class CONSTS:
    debug = False
    build_all = False
    
def exec_sql(sql: str, callback: Callable = None) -> None:
    try:
        process = subprocess.run(
            ['sqlite3', APP_PROPS.db_path],
            input=sql,
            text=True,     # If using Python <3.7, use `universal_newlines=True`
            capture_output=True,
            check=True
        )
        
        if(process.returncode == 0):
            if(callable(callback)):
                callback(process.stdout)
        else:
            print("An error occurred.")
            print("Error output:", process.stderr)
            
    except subprocess.CalledProcessError as e:
        print("An error occurred while executing command:")
        print(e.stderr)
        
def get_tables() -> list:
    commands = f'.tables'
    tables = []
    
    def get_table_names(stdout: str):
        table_lines = stdout.split('\n')
        for line in table_lines:
            tbl_names = line.split()
            tables.extend(tbl_names)
    
    exec_sql(commands, get_table_names)
    
    return tables
        
def gen_sqlalchemy_model():
    tables = get_tables()
    #path = os.path.join(APP_PROPS.sql_dir, '_models.py')
    #cmd = f'sqlacodegen sqlite:///{APP_PROPS.db_path} --tables {tables} --outfile {path}'
    #cmdx(cmd)
    
    sql_str = ''
    
    tables_sql = {}
    
    for table in tables:
        print(table)
        if('trigger' in table):
            continue
        
        cmd = f'.dump {table}'
        
        def get_table_schema(stdout: str):
            tables_sql[table] = stdout

        exec_sql(cmd, get_table_schema)
        table_sql = tables_sql[table].strip()
        sql_lines = table_sql.split('\n')[1:-1]
        print('\n')
        for line in sql_lines:
            print(line)
        
        
def rebuild_db():
    if(not os.path.exists(APP_PROPS.sql_dir)):
        raise FileNotFoundError(f"Directory {APP_PROPS.sql_dir} not found")
    
    files = os.listdir(APP_PROPS.sql_dir)
    files.sort()
    
    for file_name in files:
        if(file_name.endswith('.sql') and file_name.startswith('create')):
            if(not CONSTS.build_all and file_name in APP_PROPS.ignored_sql_files):
                print(f'Ignoring file: {file_name}')
                continue
            
            file_path = os.path.join(APP_PROPS.sql_dir, file_name)
            
            print(f'Running script: {file_name}')
            exec_sql(f'.read {file_path}', print)
            
def clean_db():
    if(not os.path.exists(APP_PROPS.db_path)):
        raise FileNotFoundError(f"File {APP_PROPS.db_path} not found")
    commands = f'.tables'

    def clean_tables(stdout: str):
        table_lines = stdout.split('\n')
        tables = []
        for line in table_lines:
            tbl_names = line.split()
            tables.extend(tbl_names)
        
        for table in tables:
            if(table in APP_PROPS.protected_sql_tables):
                print(f'Protected table: {table}')
                continue
            
            cmd = f'DROP TABLE {table};'
            print(f'Dropping table: {table}')
            exec_sql(cmd, print)
            
    exec_sql(commands, clean_tables)
    
    rebuild_db()
    
def main():
    args = utils.get_inputs()
    
    if(args.a):
        CONSTS.build_all = True
    
    if(args.r):
        rebuild_db()
    elif(args.c):
        clean_db()
    elif(args.s):
        gen_sqlalchemy_model()
            
if(__name__ == "__main__"):
    main()
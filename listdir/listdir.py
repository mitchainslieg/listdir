from datetime import datetime
from argparse import RawTextHelpFormatter
from logging.handlers import RotatingFileHandler
import glob
import time
import yaml
import zipfile
import hashlib
import os.path
import argparse
import logging
import logging.config
import configparser
import json

def setup_logging(default_path='log_config.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    
    """This function setups the logging function which will be used to print out progress, errors and etc.
    
    Arguments:
        default_path -- Contains the path of the YAML file
        default_level -- If the YAML file does not exist, logging.INFO will be the default level for basicConfig
        env_key -- return a path to logging configuration if it exist
    
    Returns:
        Returns a list that contains the md5 and sha1 value of a file
    """
    path = os.path.realpath(default_path)
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.warning('log_config.yaml doesn\'t exist!')
        logging.basicConfig(level=default_level)
    
def get_file_hasher(dir_path):
    
    """Gets the hash value of a file in both MD5 and SHA1
    
    Arguments:
        dir_path -- Contains the path of the file
    
    Returns:
        Returns a list that contains the md5 and sha1 value of a file
    """
    hasher_md5 = hashlib.md5()
    hasher_sha1 = hashlib.sha1()
    try:
        with open(dir_path, 'rb') as afile:
            buf = afile.read()
            hasher_md5.update(buf)
            hasher_sha1.update(buf)
    except Exception as e:
        print(e)
    return [hasher_md5.hexdigest(), hasher_sha1.hexdigest()]

def generate_file_info(file_rpath):

    """This function acts as a generator and reads all files from a given directory and 
            generates informations about that file

        Arguments:
            file_rpath -- Path or directory provided by the user

        Yields:
            A dictionary that contains information for each file inside the directory

    """

    logging.info(f"Fetching all files in {file_rpath}")
    files = glob.iglob(f"{file_rpath}/**/*.*", recursive=True)
    files_directory = [os.path.realpath(file_path) for file_path in files if os.path.isfile(file_path)]
    for file_dir in files_directory:
        file_info = {
            "parent_path" : os.path.dirname(file_dir),
            "file_name" : os.path.basename(file_dir),
            "file_size" : os.path.getsize(file_dir),
            "md5" : get_file_hasher(file_dir)[0],
            "sha1" : get_file_hasher(file_dir)[1]
        }
        yield file_info

def export_csv(dir_path, destination_file, include_date, include_time, generate_as_json):

    """Generates a file (csv or json type) containing path, name, size, md5 and sha1 of files within the directory
    
    Arguments:
        dir_path -- Contains the path of the directory or folder
        destination_file -- Contains the name the user want for his or her file
        include_date -- a boolean type variable, if set as true, the date is concatenated in the file name
        include_time -- a boolean type variable, if set as true, the time is concatenated in the file name
        generate_as_json -- a boolean type variable, if set as true, it generates a json file instead of a file with a csv format

    Returns:
        Returns e to print an exception, and if it executes successfully, returns True as default value for the function

    """

    timestamp = datetime.now()
    timestamp_date = timestamp.strftime("%Y-%m-%d")
    timestamp_time = timestamp.strftime("%H-%M-%S")

    if generate_as_json:
        destination_file += ".json"
    
    zip_name = destination_file
    if include_date and include_time:
        zip_name += f" {timestamp_date}_{timestamp_time}"
    elif include_date:
        zip_name += f" {timestamp_date}"
    elif include_time:
        zip_name += f" {timestamp_time}"
    
    file_rpath = os.path.realpath(dir_path)
    
    try:
        generated_filename = os.path.basename(destination_file)
        generated_zipname = os.path.basename(zip_name)

        if generate_as_json:
            with open(f"{destination_file}", "w") as new_file:
                json_data = []
                for line in generate_file_info(file_rpath):
                    json_data.append({
                        'parent_path' : line['parent_path'],
                        'file_name' : line['file_name'],
                        'file_size' : line['file_size'],
                        'md5' : line['md5'],
                        'sha1' : line['sha1']
                    })
                json.dump(json_data, new_file, indent=4)
                logging.info(f"Generating {generated_filename} and {generated_zipname}.zip")
        else:
            with open(destination_file, "w") as new_file:
                for line in generate_file_info(file_rpath):
                    new_file.write(f"\"{line['parent_path']}\",\"{line['file_name']}\",{line['file_size']},{line['md5']},{line['sha1']}\n")
                logging.info(f"Generating {generated_filename} and {generated_zipname}.zip")
        
        with zipfile.ZipFile(zip_name + '.zip', 'w') as zip_file:    
            zip_file.write(destination_file)
        
        logging.info(f"Success! {generated_filename} and {generated_zipname}.zip was generated!")

    except Exception as e:
        return e
    return True

def check_valid_path(path):

    """Checks the path if it is a valid directory
    
    Arguments:
        path -- Contains the path of the directory or folder
    
    Returns:
        Returns as True if the path is a directory or the path exist else if the path is the path directs to a file, it returns false
    """

    real_path = os.path.realpath(path)
    if os.path.isfile(real_path):
        return False
    return True if os.path.isdir(real_path) or os.path.exists(real_path) else False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Exports all file information into a file, it includes all files in a directory/folder.\n"
                                                            "Remove any succeeding back slash '\\' if it prints out any errors")
    parser.add_argument("directory", help="Full path of a folder", default='', nargs="?")
    parser.add_argument("file_name", help="File name for the output", default='', nargs="?")
    parser.add_argument("-d", "--date", action="store_true", help="Include date in the file name", default='')
    parser.add_argument("-t", "--time", action="store_true", help="Include time in the file name", default='')
    parser.add_argument("-j", "--json", action="store_true", help="Generates a file in a json format", default='')
    user_inp = parser.parse_args()

    # Setup logging and read config.ini for default values
    setup_logging()
    config = configparser.ConfigParser()
    config.read(os.path.realpath(f"config.ini"))

    if not os.path.exists(os.path.realpath('config.ini')):
        logging.warning("config.ini doesn't exist!")
    else:
        if not os.path.isdir(user_inp.directory):
            if "/" in user_inp.directory or "\\" in user_inp.directory:
                logging.error("Invalid Directory or File Name")
            else:
                if user_inp.directory == '':
                    file_name = config['default']['output_name']
                else:
                    file_name = user_inp.directory
                config_dir = os.path.realpath(config['default']['directory'])
                export_csv(config_dir, file_name, user_inp.date, user_inp.time, user_inp.json)
        elif user_inp.file_name == '':
            export_csv(user_inp.directory, os.path.realpath(config['default']['output_name']), user_inp.date, user_inp.time, user_inp.json)
        else:
            export_csv(user_inp.directory, user_inp.file_name, user_inp.date, user_inp.time, user_inp.json)
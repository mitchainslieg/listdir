from argparse import RawTextHelpFormatter
from datetime import datetime
import configparser
import zipfile
import hashlib
import argparse
import os.path
import glob
import time
    
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
    files = glob.iglob(f"{file_rpath}/**/*.*", recursive=True)
    files_directory = [os.path.realpath(file_path) for file_path in files if os.path.isfile(file_path)]
    for file_dir in files_directory:
        file_info = {
            "parent_path" : f"\"{os.path.dirname(file_dir)}\"",
            "file_name" : f"\"{os.path.basename(file_dir)}\"",
            "file_size" : os.path.getsize(file_dir),
            "md5" : get_file_hasher(file_dir)[0],
            "sha1" : get_file_hasher(file_dir)[1]
        }
        yield file_info

def export_csv(dir_path, csv_name, include_date, include_time):

    """Generates a file containing path, name, size, md5 and sha1 of files within the directory
    
    Arguments:
        dir_path -- Contains the path of the directory or folder
        csv_name -- Contains the name the user want for his or her CSV file
        include_date -- a boolean type variable, if set as true, the date is concatenated in the file name
        include_time -- a boolean type variable, if set as true, the time is concatenated in the file name

    Returns:
        Returns e to print an exception, and if it executes successfully, returns True as default value for the function

    """

    timestamp = datetime.now()
    timestamp_date = timestamp.strftime("%Y-%m-%d")
    timestamp_time = timestamp.strftime("%H-%M-%S")

    zip_name = csv_name
    if include_date and include_time:
        zip_name += f" {timestamp_date}_{timestamp_time}"
    elif include_date:
        zip_name += f" {timestamp_date}"
    elif include_time:
        zip_name += f" {timestamp_time}"
    
    file_rpath = os.path.realpath(dir_path)
    
    try:
        print("Running...")
        with open(csv_name, "w") as new_file:
            for line in generate_file_info(file_rpath):
                new_file.write(f"{line['parent_path']},{line['file_name']},{line['file_size']},{line['md5']},{line['sha1']}\n")
        
        with zipfile.ZipFile(zip_name + '.zip', 'w') as zip_file:    
            zip_file.write(csv_name)
            print("Success!")

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
    user_inp = parser.parse_args()

    config = configparser.ConfigParser()
    config.read('config.ini')

    if not os.path.isdir(user_inp.directory):
        if "/" in user_inp.directory or "\\" in user_inp.directory:
            print(f"Invalid path or file name")
        else:
            if user_inp.directory == '':
                file_name = config['default']['output_name']
            else:
                file_name = user_inp.directory
            config_dir = os.path.realpath(config['default']['directory'])
            export_csv(config_dir, file_name, user_inp.date, user_inp.time)
    elif user_inp.file_name == '':
        export_csv(user_inp.directory, os.path.realpath(config['default']['output_name']), user_inp.date, user_inp.time)
    else:
        export_csv(user_inp.directory, user_inp.file_name, user_inp.date, user_inp.time)
from argparse import RawTextHelpFormatter
import argparse
import os.path
import glob

def get_file_name(dir_path_glob):

    """Getting the file name from path
    
    Arguments:
        dir_path_glob -- Contains the path of the file
    
    Returns:
        File name from the path
        
    """

    split_path = dir_path_glob.split("\\")
    return '"' + split_path[len(split_path) - 1] + '"'

def get_dir_path(dir_path_glob):

    """From glob's path, it replaces all double back slash to one forward slash
    
    Arguments:
        dir_path_glob -- Contains the path of the file
    
    Returns:
        Returns the whole path of the file with double quote marks
    """

    replace_symb = dir_path_glob.replace("\\", "/")
    split_path = replace_symb.split("/")
    split_path.pop()
    return '"' + os.path.realpath("/".join(split_path)) + '"'

def get_file_size(dir_path_glob):

    """A function to get the file size
    
    Arguments:
        dir_path_glob -- Contains the path of the file

    Returns
        Returns the file size of the file using the getsize method from os.path

    """

    file_realpath = os.path.realpath(dir_path_glob)
    return os.path.getsize(file_realpath)

def export_csv(dir_path, csv_name):

    """Generates a CSV file containing path, name and size of files within the directory
    
    Arguments:
        dir_path -- Contains the path of the directory or folder
        csv_name -- Contains the name the user want for his or her CSV file

    Returns:
        Returns e to print an exception, and if it executes successfully, returns True as default value for the function

    """

    files = []
    if dir_path[len(dir_path) - 1] != '/':
        dir_path += '/'
    for root, directories, file_names in os.walk(os.path.realpath(dir_path)):
        files.extend(glob.glob(root + "/*.*", recursive=True))
    
    try:
        with open(csv_name, "w") as new_file:
            file_list = []
            for file_info in files:
                file_list.append(f"{get_dir_path(file_info)},{get_file_name(file_info)},{get_file_size(file_info)}")
            new_file.write("\n".join(file_list))
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
    parser = argparse.ArgumentParser(description="Exports all file information in a CSV file of all files in a directory/folder.\n"
                                                            "Remove any succeeding back slash '\\' if it prints out any errors")
    parser.add_argument("directory", type=str, help="Full path of a folder")
    parser.add_argument("file_name", type=str, help="CSV file name\nexample: file_name.csv")
    user_inp = parser.parse_args()
    if check_valid_path(user_inp.directory):
        destination_file = user_inp.file_name.split('.')
        if len(destination_file) > 1:
            if destination_file[len(destination_file) - 1] == 'csv':
                export_csv(user_inp.directory, ".".join(destination_file))
                print("Command Executed!")
            else:
                print("Invalid File name!")
        else:
            print("Command Executed!")
            export_csv(user_inp.directory, destination_file[0] + '.csv')
    else:
        print("Invalid path!")
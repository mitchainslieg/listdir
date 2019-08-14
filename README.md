## listdir.py
Generates a zip file that contains the CSV/JSON file. The csv/json/file includes the following:
1. Parent directory of the file
2. File name and file type
3. File size
4. The MD5 value of the file;
5. and the SHA1 value of the file

Basic syntax in command line
> python listdir.py [-h] [-d] [-t] [-j] [directory] [file_name]

Optional Arguments (1 new argument):
```
-d, --date Add the date today in zip file name
-t, --time Add the time today in zip file name
-j, --json Generates a json file instead of a csv file
```
> Both arguments are optional.

```
Note:
  - You can prove any name for the csv file without adding the .csv extension
  - Remove any succeeding backslash from the end of the directory to avoid any errors
  - If the file name and file type is not specified, there will be a default value from config.ini and is changeable
  - Upon executing any commands, there will be a log and will be enlisted in a rolling log file called logs.log
  - The rolling log file is limited to 5 MB each and a maximum of 5 log file
```

##Packaging
To install the package, on your command line type the following:
```
pip install -i https://test.pypi.org/simple/ date-time-pkg
```

Then import it by:
```
import date_time
```

Updates:
```
- Added a new optional argument to generate a json file
```
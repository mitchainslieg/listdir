## listdir.py
Generates a zip file that contains the CSV file (if there are no specified file name and file type). The csv / file includes the following (Separated by comma):
1. Parent directory of the file
2. File name and file type
3. File size
4. The MD5 value of the file;
5. and the SHA1 value of the file

Basic syntax in command line
> python listdir.py [-h] [-d] [-t] [directory] [file_name]

Added two (2) optional arguments:
```
-d, --date Add the date today in zip file name
-t, --time Add the time today in zip file name
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
- Added logging feature
```
## listdir.py
Generates a CSV file  of all files within a directory or folder, these includes:
- Full directory of a file
- The name of the file
- The size of the file

Basic syntax in command line
<<<<<<< Updated upstream
> python listdir.py [Directory] [CSV File Name]
=======
> python listdir.py [-h] [-d] [-t] [directory] [file_name]

Added two (2) optional arguments:
```
-d, --date Add the date today in final output file name
-t, --time Add the time today in final output file name
```
```
Both arguments are optional. There are default values for Directory and File Name and you can change it in the config.ini
```
>>>>>>> Stashed changes

```
Note:
  - Remove any succeeding backslash from the end of the directory
  - You can prove any name for the csv file without adding the .csv extension
```
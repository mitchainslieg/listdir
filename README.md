## listdir.py
Generates a file that list all the files within a directory or folder, these list includes:
1. The parent directory of the file
2. The file name
3. The size of the file
4. The MD5 value of the file
5. The SHA1 value of the file

Basic syntax in command line
> python listdir.py [Directory] [File Name]
```
Both arguments are optional. There are default values for Directory and File Name and you can change it in the config.ini
```

```
Note:
  - Remove any succeeding backslash from the end of the directory to avoid any errors
```
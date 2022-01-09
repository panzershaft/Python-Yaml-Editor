## YAML editing using python
- This program takes two yaml files as arguments
  - file1: This is a 'yaml' file with missing values you wish to fill, missing values are in a different yaml file
  - file2: This is the 'yaml' file which has the missing values with the keys which you need for file1
## How to execute ?
```
 python3 yaml_editor.py --f1 sample_files/values.yaml --f2 sample_files/change.yaml 
```
- NOTE: final yaml file will be found in the same folder of the f1 file.

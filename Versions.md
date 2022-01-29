### V1.0  
This is a calculator to transform schematics material list into it's original material list offering custom formula adding.  
This is made for fabric-schematics.Before using, please make sure that you've already got a csv-file (in game, you should export with pressing shift ).  


'\*\*.py -h|--help'  
'\*\*.py -i <path> [-o <path>] [args]'  

-w|--write: formula-writing mode, for every kind of item without default formula, the calculator will ask you if there is a new formula for it and save it as a new file.  
-s|--simple: to calculate all kinds of wood as one.(simplified_Chinese only)  
-f|--formula : to appoint a private formula. The formula should be in json type, like {"name":[["component_name", number], ...], ...}  
-m|--missing: to calculate with missing number.Without this argument,It will be done with Total number  


***
### v1.0.1  
Bug fixed.


***
### v1.1
Now the program will save no-formula item in the formula json.  

__CAUTION:__ 
The new json should be offered to the program higher than v1.1.  
If not, you may miss those items saved with no formula.
You'll now see the version at the end of the json file.

This version has no Windows version.
For Windows user, you may try edit the program file, replace "/" with "\\\\" in all directories to use this version.

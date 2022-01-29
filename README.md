# Minecraft-Item-List-Calculator
This is a calculator to transform schematics material list into it's original material list offering custom formula adding.


This is made for fabric-schematics.Before using, please make sure that you\'ve already 
got a csv-file (in game, you should export pressing shift ).


    ILC.sdm -h|--help

    ILC.sdm -i <path> [-o <path>] [args]
  
                        
-w|--write:            formula-writing mode, for every kind of item without default formula,
                        the calculator will ask you if there is a new formula for it and save
                        it as a new file.
  
-s|--simple:           to calculate all kinds of wood as one.(simplified_Chinese only)

-f|--formula <path>:   to appoint a private formula. The formula should be in json type, 
                        like {"name":[["component_name", number], ...], ...}

-m|--missing:          to calculate with missing number.Without this argument,It will be done
                        with Total number

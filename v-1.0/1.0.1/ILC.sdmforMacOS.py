#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   ILC.sdm
@Time    :   2022/01/26 17:55:01
@Author  :   SDreaM
@Version :   1.0.1
"""
import getopt
import json
import os
import sys
import time


def wood_only(name) -> str:
    wood_name = (('"橡木原木"', '"白桦原木"', '"云杉原木"', '"丛林原木"',
                  '"深色橡木原木"', '"金合欢原木"', '"绯红菌柄"', '"诡异菌柄"'),
                 ("橡木木", "白桦木", "云杉木", "丛林木", "深色橡木", "金合欢木", "绯红木", "诡异木"))
    if name in wood_name[0]:
        return '"原木"'
    for kind in wood_name[1]:
        if kind in name:
            return name.replace(kind, '木')
    return name


def main(argv):

    # Initialization.
    writing = False
    show_writing_help = True
    simple = False
    local_time = time.strftime("%y-%m-%j-%H:%M:%S", time.localtime(time.time()))
    input_dir = ""
    output_dir = ""
    formula_dir = ""
    program_dir = os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0])))
    help_str = ('\nThis is made for fabric-schematics.Before using, please make sure that you\'ve already \n'
                'got a csv-file (in game, you should export pressing shift ).\n\n'
                'ILC.sdm [-h|--help]\n'
                '        [-i <path> [-o <path>] [args]]\n\n'
                '-w|--write            formula-writing mode, for every kind of item without default formula,\n'
                '                      the calculator will ask you if there is a new formula for it and save\n'
                '                      it as a new file.\n'
                '-s|--simple           to calculate all kinds of wood as one.\n'
                '-f|--formula <path>   to appoint a private formula. The formula should be in json type.\n'
                '                      The json file is like {"name":[["component_name", number], ...], ...}\n'
                '-m|--missing          to calculate with missing number.Without this argument,It will be done\n'
                '                      with Total number'
                '')
    writing_help_str = ("\nIn formula-writing mode, the program will ask for a formula of each unknown item\n"
                        "You should input as <item_name>:<number(float)> in YOUR LANGUAGE.\n"
                        "Press enter only to see you've added for this item or input 's' or 'save' to save.\n"
                        "for wrong input, use command 'del' or 'delete' to delete your last adding.\n"
                        "If you wanna see this again, input '?' or 'help';"
                        "to not show this every time, input 'h' or 'hide'"
                        "For exit and save the formula, input 'x!'")
    number_index = 1
    origin_items = {}
    result_items = {}
    formula = {}

    # Get args.
    try:
        opts, args = getopt.getopt(argv, "hi:o:f:sw", ["formula=", "simple", "write"])
    except getopt.GetoptError:
        print("Bad arguments!!\n\n"+help_str)
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help_str)
            sys.exit(0)
        if opt == "-i":
            input_dir = arg
        elif opt == "-o":
            output_dir = arg
        elif opt in ("-f", "--formula"):
            formula_dir = arg
        elif opt in ("-w", "--write"):
            writing = True
        elif opt in ("-s", "--simple"):
            simple = True
        elif opt in ("-m", "--missing"):
            number_index = 2

    # Default path:
    if not input_dir:
        for for_file in os.listdir(program_dir + "/csv"):
            if for_file[-4:] == ".csv":
                input_dir = program_dir + "/csv/" + for_file
                break
    if not input_dir:
        print("No csv file existing. Please check and try again.")
        sys.exit(2)
    if not output_dir:
        output_dir = (program_dir + "/result/sdm_calculated_" + "material_list-" + local_time + ".csv")
    if not formula_dir:
        for for_file in os.listdir(program_dir + "/formula"):
            if for_file[-5:] == ".json":
                formula_dir = program_dir + "/formula/" + for_file
                break

    if formula_dir:
        # get formula
        with open(formula_dir, encoding="utf-8", mode="r") as ff:
            formula = json.loads(ff.read())
    elif not writing:
        if input("No formula file existing or appointed.\n"
                 "Do you want to use formula-writing mode?(Y to confirm.)") == "Y":
            writing = True
        else:
            sys.exit(2)

    formula_dir = (program_dir + "/formula/formula-" + local_time + ".json")

    # Get material list.
    with open(input_dir, encoding="utf-8-sig", mode="r") as fi:
        file_in_line = fi.read().splitlines()

    # File check.
    if file_in_line[0] != '"Item","Total","Missing","Available"':
        print("Unknown file. Please check and try again.")
        sys.exit(3)

    # split and save
    for item_name, item_number in ([[file_in_line[i].split(",")[0],
                                     int(file_in_line[i].split(",")[number_index])]
                                    for i in range(1, len(file_in_line))]):
        if simple:
            item_name = wood_only(item_name)
        if item_name in origin_items.keys():
            origin_items[item_name] += item_number
        else:
            origin_items[item_name] = item_number

    # count with formula:
    while origin_items:
        # create a queue
        queue = list(origin_items.keys())
        for item_name in queue:
            item_number = origin_items.pop(item_name)
            if (item_name not in formula.keys()) and writing:
                if show_writing_help:
                    print(writing_help_str)

                # 处理用户输入
                new_writing_formula = []
                print(item_name, end="")
                while (user_input := input(":")) != "s":
                    if user_input in ("?", "help"):
                        print(writing_help_str + "\n" + item_name)
                        show_writing_help = True
                    elif user_input in ("h", "hide"):
                        show_writing_help = False
                    elif ":" in user_input or "：" in user_input:
                        pairs = (user_input + "：").replace("：", ":").split(":", 2)
                        try:
                            new_item_number = float(pairs[1])
                            new_writing_formula.append(['"'+pairs[0]+'"', new_item_number])
                            print(new_writing_formula)
                        except ValueError:
                            print("Bad input.The right form is <item_name>:<number(float)>, try again", end="")
                        continue
                    elif user_input in ('del', 'delete'):
                        if len(new_writing_formula) > 0:
                            print("You deleted ", new_writing_formula.pop(-1), " for ", item_name,
                                  ". The rest is ", new_writing_formula,
                                  "\n", "Continue to add component or s to save", sep="", end="")
                        else:
                            print("There is nothing to be deleted. \n",
                                  "Add a component as <item_name>:<number(float)> or\n",
                                  "s to save", sep="", end="")
                    elif user_input == "x!":
                        with open(formula_dir, encoding="utf-8", mode="w") as ff:
                            ff.write(json.dumps(formula, ensure_ascii=False))
                    else:
                        if len(new_writing_formula) > 0:
                            print(item_name, ":", new_writing_formula, sep="")
                            print("Add another component as <item_name>:<number(float)> or\n",
                                  "s to save", end="")
                        else:
                            print("Add a component for ", item_name, "as <item_name>:<number(float)> or\n",
                                  "s to save", sep="", end="")
                if new_writing_formula:
                    formula[item_name] = new_writing_formula

            if item_name not in formula.keys():
                if item_name in result_items.keys():
                    result_items[item_name] += item_number
                else:
                    result_items[item_name] = item_number

            else:
                for component_name, component_number in formula[item_name]:
                    if component_name in origin_items.keys():
                        origin_items[component_name] += component_number * item_number
                    else:
                        origin_items[component_name] = component_number * item_number

    # Save file.
    with open(output_dir, encoding="utf-8", mode="w") as fo:
        fo.write('"Name","amount","%64"\n')
        for item_name, item_number in result_items.items():
            fo.write(item_name + "," + str(item_number) + "," + str(1+item_number//64) + "\n")

    # Save formula.
    if writing:
        with open(formula_dir, encoding="utf-8", mode="w") as ff:
            ff.write(json.dumps(formula, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1:])

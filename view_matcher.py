"""
File name: view_matcher.py
Author: Bryan Sweeney

The purpose of this project is to allow a user to find matching views from json for user
input selectors

When running, you will be asked to provide the selectors that you are looking to match.
Use the rules below when providing input:

For a class, simply enter the name
  example: Input
For an identifier, start with a #
   example: #container
For a className, start with a .
  example: .container

Multiple selectors can be used at the same time
To do so, seperate selectors by a space
  example Input #container
"""

import os
import json
import re


class ViewMatcher:
    def __init__(self, expression):
        self.matches = []
        self.match_type = ""
        self.tags = {}
        self.resolve_input(expression)

    def resolve_input(self, to_match):
        tags = re.split(" ", to_match)
        for str in tags:
            if (str[0] == "."):
                self.tags.update({"classNames":str[1:]})
            elif (str[0] == "#"):
                self.tags.update({"identifier":str[1:]})
            elif(str != " "):
                self.tags.update({"class":str})

    def find_matches(self, data):
        if (type(data) is type({})):
            if("class" in data):
                self.match(data)
                if("subviews" in data):
                    self.find_matches(data.get("subviews"))
                if ("contentView" in data):
                    self.find_matches(data.get("contentView"))
                if ("control" in data):
                    self.find_matches(data.get("control"))
            else:
                for key in data:
                    self.find_matches(data.get(key))
        elif (type(data) is type([])):
            for objects in data:
                self.find_matches(objects)

    def match(self, data):
        should_add = True
        for key in self.tags:
            if(key in data and key == "classNames" and self.tags.get(key) in data.get(key)):
                continue
            if(key in data and data.get(key) == self.tags.get(key)):
                continue
            else:
                should_add = False
        if(should_add):
            self.matches.append(data)

    def print_matches(self, to_match):
        print("There are " + str(len(self.matches)) + " matching views for: \'" + to_match + "\'")
        for object in self.matches:
            print(object)


json_file_path = os.getcwd() + "/view.json"
data = None
with open(json_file_path, "r") as read_file:
    data = json.load(read_file)


continue_flag = True

while (continue_flag):
    print("Please enter the selectors that you would like to have matched")
    tag_to_match = input()
    view_operator = ViewMatcher(tag_to_match)
    view_operator.find_matches(data)
    view_operator.print_matches(tag_to_match)
    print("Would you like to look for another match (y/n)")
    if (input() != "y"):
        continue_flag = False

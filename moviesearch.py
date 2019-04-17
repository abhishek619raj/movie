import sys
import pandas as pd
from pandas import DataFrame
import json
import re


data=r'moviedata.json'
print (data)

# Reads and converts json to dict.
def js_r(data):
   with open(data, encoding='utf-8') as f_in:
       return(json.load(f_in))

if __name__ == "__main__":
    my_dic_data = js_r(data)
    print(my_dic_data)

movie_name=input()
for i in my_dic_data:
    #here i have put movie name static now need to change it as user input
    if i['name'] == movie_name:
        print(i['popularity'])
        print(i['director'])
        print(i['genre'])
        print(i['imdb_score'])
        break
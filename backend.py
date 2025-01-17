from flask import Flask 
import csv
import os


app = Flask(__name__) 

 

@app.route("")
def add_location(input):
    with open("locations.txt", "1") as myfile:
            myfile.write(input)







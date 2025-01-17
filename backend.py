from flask import Flask 


app = Flask(__name__) 

 

@app.route("add")
def add_location(input):
    with open("locations.txt", "1") as myfile:
            myfile.write(input)







from flask import jsonify, abort, Flask, request
from flask_cors import CORS
import csv
import os
import pandas as pd
import re
import joblib


#for now the model should work with the local state from the user cause its atm for showcasing only
app = Flask(__name__) 
csv_file = "locations.csv"
model_file = "model.joblib"  # Path to your trained model file
model = joblib.load(model_file)  # Load the trained model
csv_file = "locations.csv"


suspicious_patterns = [
    r"(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|EXEC|xp_|\bOR\b|\bAND\b)",
    r"<.*?script.*?>|alert\(|onerror=|document\.cookie",
    r"\.\./|\.\.\\|%2e%2e%2f|%2e%2e%5c",
    r"--|;|#|\|\||&&"
]

@app.route("/add", methods=["POST"])
def add_location_to_csv():
    # Parse the JSON data from the request
    data = request.json
    vibe = data.get('vibe')
    groupsize = data.get('groupsize')
    time = data.get('time')
    budget = data.get('budget')
    location = data.get('location')

    # Check for suspicious input
    if check_for_security(vibe, groupsize, time, budget, location):
        abort(400, description="Suspicious input detected!")

    # Prepare input for prediction (depending on how your model is trained)
    input_data = [[vibe, time, budget, groupsize, location]]

    # Make the location prediction using the ML model
    predicted_location = model.predict(input_data)[0]

    # Create DataFrame to save to CSV (with the predicted location)
    df = pd.DataFrame(data={
        "vibe": [vibe], 
        "groupsize": [groupsize], 
        "time": [time], 
        "budget": [budget],
        "location": [location],
        "predicted_location": [predicted_location]
    })

    # Save the data to CSV
    if os.path.exists(csv_file):
        df.to_csv(csv_file, mode="a", header=False, index=False)
    else:
        df.to_csv(csv_file, index=False)

    # Return a success message with the predicted location
    return jsonify({
        "message": "Location added successfully!",
        "predicted_location": predicted_location
    }), 200

def check_for_security(vibe, groupsize, time, budget):
    inputs = [vibe, groupsize, time, budget]
    for input_string in inputs:
        for pattern in suspicious_patterns:
            if re.search(pattern, str(input_string), re.IGNORECASE):  # Look for suspicious patterns
                return True  
    return False 



if __name__ == "__main__":
    app.run(debug=True)
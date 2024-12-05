from flask import Flask, jsonify, request, render_template
#from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
import os
#from datetime import datetime

# Load the Excel file
excel_file_path = 'D:/Javeed/ITU/Fall 2024 SEM-1/HTML,CSS& Java Script/Project/project 1/foodsales/sampledatafoodsales_analysis.xlsx'
#excel_file_path = "sampledatafoodsales_analysis.xlsx"
#df = pd.read_excel(excel_file_path, sheet_name='FoodSales', engine='openpyxl')
df = pd.read_excel(excel_file_path, sheet_name='FoodSales')
print(df)

# Ensure 'Date' column is parsed as datetime with flexible formats
df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='%d-%b')

# Initialize Flask app
app = Flask(__name__)
CORS(app)

def get_public_ip():
    try:
        response = request.get('https://api.ipify.org?format=text')
        return response.text
    except Exception as e:
        return "Unable to fetch IP"

# Define the root route for testing purposes
@app.route('/', methods=['GET'])
def home():
    #return render_template('Foodsales.html')
    return "Flask server is running!"
    print("Current working directory:", os.getcwd())
    return render_template('index.html')
    
# Define the favicon route for testing purposes
@app.route('/favicon.ico', methods=['GET'])
def favicon():
    #return render_template('Foodsales.html')
    return "Favicon is running!"  
    
# Endpoint to get unique values for City and Category
@app.route('/get_initial_data', methods=['GET'])
def get_initial_data():
    cities = df['City'].dropna().unique().tolist()
    categories = df['Category'].dropna().unique().tolist()
    return jsonify({
        'cities': cities,
        'categories': categories
    })

@app.route('/get_filtered_data', methods=['GET'])
def get_filtered_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    city = request.args.get('city')
    category = request.args.get('category')

    # Convert dates from string to datetime if provided
    if start_date:
        start_date = pd.to_datetime(start_date, format='%Y-%m-%d', errors='coerce')
    if end_date:
        end_date = pd.to_datetime(end_date, format='%Y-%m-%d', errors='coerce')

    # Filter the DataFrame
    filtered_df = df.copy()

    if start_date:
        filtered_df = filtered_df[filtered_df['Date'] >= start_date]
    if end_date:
        filtered_df = filtered_df[filtered_df['Date'] <= end_date]
    if city:
        filtered_df = filtered_df[filtered_df['City'] == city]
    if category:
        filtered_df = filtered_df[filtered_df['Category'] == category]

    # Convert DataFrame to list of dictionaries for JSON response
    result = filtered_df.to_dict(orient='records')
    return jsonify(result)

#if __name__ == '__main__':
    # Run the Flask app and allow external connections (0.0.0.0)
    #app.run(host='0.0.0.0', port=5000, debug=False)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


#if __name__ == '__main__':
    #app.run(debug=True)
#if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True)


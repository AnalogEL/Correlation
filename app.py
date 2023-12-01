from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

# Read the CSV file
df = pd.read_csv('Book1.csv')

# Columns to display in the result
output_columns = ['No.', 'Device', 'Slot ID', 'Serial Number', 'Correlation Unit Device', 'Project Folder', 'Correlation Program', 'Laser Program', 'Machine Type', 'Reference ID', 'Test Status', 'BIN']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    user_input = request.form['user_input'].strip().lower()
    print(f"User entered device: {user_input}")

    # Extract numerical part from user input using regular expression
    user_number = re.search(r'\d+', user_input).group() if re.search(r'\d+', user_input) else None

    if user_number:
        # Filter rows where the numerical part of "Device" matches the user input
        filtered_df = df[df["Device"].str.extract(r'(\d+)', expand=False) == user_number]

        if not filtered_df.empty:
            # Select only the desired columns
            filtered_df = filtered_df[output_columns]
            # Convert the resulting DataFrame to HTML without the index column
            result_table = filtered_df.to_html(index=False)
            return render_template('result.html', result_table=result_table)
        else:
            return render_template('result.html', message="Sorry, data not found for the specified device.")
    else:
        return render_template('result.html', message="Invalid input. Please enter a numeric value.")

if __name__ == '__main__':
    app.run(debug=True)
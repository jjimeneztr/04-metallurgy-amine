# Amine Corrosion Rate Prediction Tool

## Overview

This project is a web-based tool designed to predict the corrosion rates of carbon steel and stainless steel in amine solutions containing acid gases (H2S and/or CO2). The tool is aligned with the guidelines outlined in DM#45 of API RP 571 and can handle multiple amine types, including MEA, DEA, and MDEA. It provides both bulk calculation and manual data entry options.

## Features

- Material Selection: Choose between carbon steel, low alloy steel, and 300 series stainless steel.
- Data Input:
    - Bulk Calculation: Upload data via an Excel file for batch processing.
    - Manual Entry: Enter data directly into the form for immediate calculation.
- Corrosion Rate Calculation: Predict corrosion rates based on input parameters such as operating temperature, acid gas loading, amine type, and more.
- Theme Switching: Toggle between light and dark themes for the interface.
- Interactive Tooltips: Hover over icons for detailed instructions and explanations.

## Technologies Used

- Frontend:
    - HTML5, CSS3 (Bootstrap)
    - JavaScript (jQuery, DataTables, Plotly)
- Backend:
- Python (Flask, NumPy, Pandas, SciPy)
- SQL Server (via pyodbc)

- Libraries:
    - html2pdf.js, xlsx, DataTables, Plotly

## Installation

1- Clone the Repository:

    git clone https://github.com/yourusername/amine-corrosion-tool.git
    cd amine-corrosion-tool

2- Set Up a Virtual Environment (Optional but recommended):

    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3- Install Required Packages:

    pip install -r requirements.txt

4- Set Up the Database:

    - Ensure that your SQL Server is configured according to the settings in config.json.

    - Update the config.json file with your database connection details.

5- Run the Application:

    flask run

6- Access the Application:

    - Navigate to http://127.0.0.1:5000 in your web browser.

## Usage

1- Navigate to the Tool: Use the navigation bar to select the standard you wish to use (e.g., API RP 941-2016, NACE SP0403-2015).

2- Input Data:
    - For bulk calculations, upload an Excel file with the required structure.
    - For manual calculations, enter the necessary parameters directly into the form.
3- Calculate: Click the "Calculate CR" button to get your corrosion rate.
4- Download Results: If using bulk calculation, download the results in an Excel file.

## Configuration

The application relies on a config.json file for database connection details. The configuration file should be placed in the root directory of the project.

Example config.json:
{
    "connectionstring": {
        "server": "your_server",
        "database": "your_database",
        "username": "your_username",
        "password": "your_password",
        "LOGIN_TABLE_NAME": "your_login_table",
        "ACTIVITY_TABLE_NAME": "your_activity_table",
        "IP": "your_ip",
        "PORT": "your_port",
        "HTTP_HTTPS": "http"
    }
}

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


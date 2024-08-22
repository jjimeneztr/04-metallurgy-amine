import pandas as pd
import numpy as np
import scipy.interpolate as interp
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('amine.html')

@app.route('/upload', methods=['POST'])
def upload_excel_file():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Cargar el archivo Excel
    df = pd.read_excel(file)
    df = df.fillna('')

    objetos = []

    for index, row in df.iterrows():
        if row['material'] == '300 Series SS':
            # Aquí calculamos el CR usando una llamada a la función de cálculo de CR
            cr_value = calcular_cr_300ss(row['acid_gas_loading'])
        elif row['material'] in ['CS', 'Low Alloy Steel']:
            cr_value = buscar_cr(row['acid_gas_loading'], row['temperature'], row['velocity'], row['HSAS'])
        else:
            cr_value = 'Unknown'

        # Convertir CR a un tipo de datos serializable
        if isinstance(cr_value, (np.ndarray, list)):
            cr_value = cr_value.tolist()  # Convertir ndarray a lista

        if isinstance(cr_value, list):
            # Si cr_value es una lista, tomar el primer elemento si es una lista de un solo valor
            if len(cr_value) == 1:
                cr_value = cr_value[0]
            else:
                cr_value = str(cr_value)  # Convertir a cadena si hay varios valores

        # Convertir CR a float si es un número
        if isinstance(cr_value, (int, float)):
            cr_value = float(cr_value)

        objeto = {
            'row_number': index + 1,
            'acid_gas_loading': row['acid_gas_loading'],
            'temperature': row['temperature'],
            'HSAS': row['HSAS'],
            'velocity': row['velocity'],
            'amine_type': row['amine_type'],
            'amine_concentration': row['amine_concentration'],
            'material': row['material'],
            'CR': cr_value
        }
        objetos.append(objeto)

    return jsonify({"data": objetos})

def calcular_cr_300ss(acid_gas_loading):
    """
    Calcula la velocidad de corrosión (CR) para acero inoxidable 300 Series.

    Args:
        acid_gas_loading: Carga de gas ácido (mol/mol).

    Returns:
        Diccionario con CR en mm/año y mpy.
    """
    # Se valida la carga de gas ácido.
    if acid_gas_loading < 0:
        raise ValueError("Carga de gas ácido no válida.")

    # Se actualizan los datos de la tabla.
    acid_gas_loading_values = [0.1, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.7]
    cr_mm_year_values = [0.03, 0.03, 0.03, 0.05, 0.05, 0.08, 0.1, 0.13]
    cr_mpy_values = [1, 1, 1, 2, 2, 3, 4, 5]

    # Se crean las funciones de interpolación para CR en mm/año y mpy.
    interpolator_cr_mm_year = interp.interp1d(acid_gas_loading_values, cr_mm_year_values, kind='linear')
    interpolator_cr_mpy = interp.interp1d(acid_gas_loading_values, cr_mpy_values, kind='linear')

    # Se calculan los valores de CR en mm/año y mpy.
    cr_mm_year = interpolator_cr_mm_year(acid_gas_loading)
    cr_mpy = interpolator_cr_mpy(acid_gas_loading)

    # result = {"cr_mm_year": cr_mm_year, "cr_mpy": cr_mpy}

    # print("Tipo de dato de cr_mm_year:", type(result["cr_mm_year"]))
    # print("Tipo de dato de cr_mpy:", type(result["cr_mpy"]))

    # Se devuelven los resultados en un diccionario.
    # return {"cr_mm_year": cr_mm_year, "cr_mpy": cr_mpy}
    return {"cr_mm_year": float(cr_mm_year), "cr_mpy": float(cr_mpy)}

@app.route('/calculate_cr_300ss', methods=['POST'])
def calculate_cr_300ss():
    data = request.get_json()
    try:
        acid_gas_loading = float(data['acidGasLoading'])
        
        result = calcular_cr_300ss(acid_gas_loading)
        
        result['cr_mm_year'] = float(result['cr_mm_year'])
        result['cr_mpy'] = float(result['cr_mpy'])
        
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error en el servidor.'}), 500

def buscar_cr(acid_gas_loading, temperature, velocity, hsas):
    """
    Function to find the CR value in a JSON file based on input parameters.

    Parameters:
        acid_gas_loading: Acid gas loading (float).
        temperature: Temperature (int).
        velocity: Velocity (float).
        hsas: HSAS (float).

    Returns:
        CR value (string) or None if not found.
    """
    # Load data from JSON file
    with open('acidgasloading.json') as f:
        data = json.load(f)

    preset_temperature_values = [88, 93, 104, 116, 127, 132]
    preset_acid_gas_loading_values = [0.1, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.7]
    preset_HSAS = [2, 3.0, 4.0]

    # Validate and find bounds for acid gas loading
    if acid_gas_loading < 0.1:
        rango_acid_gas_loading = "<0.1"
        lower_agl, upper_agl = None, 0.1
    else:
        lower_agl, upper_agl = find_immediate_bounds(acid_gas_loading, preset_acid_gas_loading_values)
        if lower_agl is None or upper_agl is None:
            return None

    # Validate and find bounds for temperature
    lower_temp, upper_temp = find_immediate_bounds(temperature, preset_temperature_values)
    if lower_temp is None or upper_temp is None:
        return None

    # Validate and find bounds for HSAS
    lower_hsas, upper_hsas = find_immediate_bounds(hsas, preset_HSAS)
    if lower_hsas is None or upper_hsas is None:
        return None

    # Get data for the acid gas loading range
    if acid_gas_loading < 0.1:
        rango_datos = data["acid_gas_loading"][rango_acid_gas_loading]
        rango_datos_lower = rango_datos_upper = rango_datos
    else:
        rango_datos_lower = data["acid_gas_loading"].get(str(lower_agl))
        rango_datos_upper = data["acid_gas_loading"].get(str(upper_agl))
        if rango_datos_lower is None or rango_datos_upper is None:
            return None

    # Validate HSAS
    hsas_str_lower = str(lower_hsas)
    hsas_str_upper = str(upper_hsas)

    if (hsas_str_lower not in rango_datos_lower["HSAS"] or
        hsas_str_upper not in rango_datos_upper["HSAS"]):
        return None
    
    datos_hsas_lower = rango_datos_lower["HSAS"][hsas_str_lower]
    datos_hsas_upper = rango_datos_upper["HSAS"][hsas_str_upper]

    # Validate and get CR values for the given temperature and velocity
    def get_cr(data, temp, vel):
        if str(temp) in data["temperature"]:
            temp_data = data["temperature"][str(temp)]
            vel_key = "<=6.1" if vel <= 6.1 else ">=6.1" if acid_gas_loading < 0.1 else "<=1.5" if vel <= 1.5 else ">=1.5"
            if vel_key in temp_data["velocity"]:
                return temp_data["velocity"][vel_key]["cr"]
        return None

    cr_lower_hsas_lower_temp = get_cr(datos_hsas_lower, lower_temp, velocity)
    cr_lower_hsas_upper_temp = get_cr(datos_hsas_lower, upper_temp, velocity)
    cr_upper_hsas_lower_temp = get_cr(datos_hsas_upper, lower_temp, velocity)
    cr_upper_hsas_upper_temp = get_cr(datos_hsas_upper, upper_temp, velocity)

    if not all([cr_lower_hsas_lower_temp, cr_lower_hsas_upper_temp, cr_upper_hsas_lower_temp, cr_upper_hsas_upper_temp]):
        return None

    # Convert CR values to float for interpolation
    cr_lower_hsas_lower_temp = get_numeric_value(cr_lower_hsas_lower_temp)
    cr_lower_hsas_upper_temp = get_numeric_value(cr_lower_hsas_upper_temp)
    cr_upper_hsas_lower_temp = get_numeric_value(cr_upper_hsas_lower_temp)
    cr_upper_hsas_upper_temp = get_numeric_value(cr_upper_hsas_upper_temp)

    # Check if conversion to float was successful
    if None in [cr_lower_hsas_lower_temp, cr_lower_hsas_upper_temp, cr_upper_hsas_lower_temp, cr_upper_hsas_upper_temp]:
        return None

    cr_lower_hsas_lower_temp = float(cr_lower_hsas_lower_temp)
    cr_lower_hsas_upper_temp = float(cr_lower_hsas_upper_temp)
    cr_upper_hsas_lower_temp = float(cr_upper_hsas_lower_temp)
    cr_upper_hsas_upper_temp = float(cr_upper_hsas_upper_temp)

    # Interpolate CR values for the given temperature, velocity, and HSAS
    cr_lower_temp = linear_interpolate(temperature, lower_temp, upper_temp, cr_lower_hsas_lower_temp, cr_lower_hsas_upper_temp)
    cr_upper_temp = linear_interpolate(temperature, lower_temp, upper_temp, cr_upper_hsas_lower_temp, cr_upper_hsas_upper_temp)
    cr = linear_interpolate(hsas, lower_hsas, upper_hsas, cr_lower_temp, cr_upper_temp)

    return cr

def find_immediate_bounds(value, preset_values):
    """
    Find the immediate lower and upper bounds for a value in a sorted list of preset values.

    Parameters:
        value: The value to find bounds for.
        preset_values: A sorted list of preset values.

    Returns:
        A tuple (lower, upper) with the immediate lower and upper bounds.
    """
    lower = None
    upper = None
    for v in sorted(preset_values):
        if v <= value:
            lower = v
        if v >= value:
            upper = v
            break
    if lower == value:
        upper = lower
    return lower, upper

def linear_interpolate(x, x0, x1, y0, y1):
    """
    Perform linear interpolation.

    Parameters:
        x: The x value to interpolate at.
        x0: The lower x value.
        x1: The higher x value.
        y0: The y value at x0.
        y1: The y value at x1.

    Returns:
        The interpolated y value.
    """
    if x0 == x1:
        return y0
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)

def get_numeric_value(data):
    """
    Extracts a numeric value from a dictionary with a single key-value pair.
    Args:
        data (dict): The dictionary to extract the value from.
    Returns:
        float: The extracted numeric value, or None if the dictionary is empty or the value is not numeric.
    Raises:
        ValueError: If the dictionary contains more than one key-value pair.
    """

    if len(data) != 1:
        raise ValueError("Dictionary must contain only one key-value pair.")

    # Get the only key
    key = list(data.keys())[0]

    # Check if the value is numeric
    try:
        return float(key)
    except ValueError:
        return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    data = request.json
    acid_gas_loading = data.get('acid_gas_loading')
    temperature = data.get('temperature')
    velocity = data.get('velocity')
    hsas = data.get('hsas')
    print(acid_gas_loading, temperature, velocity, hsas)

    if acid_gas_loading is None or temperature is None or velocity is None or hsas is None:
        return jsonify({"error": "Missing data"}), 400

    cr_value = buscar_cr(acid_gas_loading, temperature, velocity, hsas)
    print(cr_value)    
    return jsonify(cr_value)

if __name__ == '__main__':
    app.run(debug=True)

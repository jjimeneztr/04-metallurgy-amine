import json

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
    else:
        rango_datos_lower = data["acid_gas_loading"][str(lower_agl)]
        rango_datos_upper = data["acid_gas_loading"][str(upper_agl)]

    # Validate HSAS
    if str(lower_hsas) not in rango_datos_lower["HSAS"] or str(upper_hsas) not in rango_datos_upper["HSAS"]:
        return None
    datos_hsas_lower = rango_datos_lower["HSAS"][str(lower_hsas)]
    datos_hsas_upper = rango_datos_upper["HSAS"][str(upper_hsas)]

    # Validate and get CR values for the given temperature and velocity
    def get_cr(data, temp, vel):
        if str(temp) in data["temperature"]:
            temp_data = data["temperature"][str(temp)]
            if acid_gas_loading < 0.1:
                vel_key = "<=6.1" if vel <= 6.1 else ">=6.1"
            else:
                vel_key = "<=1.5" if vel <= 1.5 else ">=1.5"
            if vel_key in temp_data["velocity"]:
                return temp_data["velocity"][vel_key]["cr"]
        return None

    cr_lower_hsas_lower_temp = get_cr(datos_hsas_lower, lower_temp, velocity)
    cr_lower_hsas_upper_temp = get_cr(datos_hsas_lower, upper_temp, velocity)
    cr_upper_hsas_lower_temp = get_cr(datos_hsas_upper, lower_temp, velocity)
    cr_upper_hsas_upper_temp = get_cr(datos_hsas_upper, upper_temp, velocity)
    print(cr_lower_hsas_lower_temp)
    if not all([cr_lower_hsas_lower_temp, cr_lower_hsas_upper_temp, cr_upper_hsas_lower_temp, cr_upper_hsas_upper_temp]):
        return None

    # Convert CR values to float for interpolation
    cr_lower_hsas_lower_temp = get_numeric_value(cr_lower_hsas_lower_temp)
    cr_lower_hsas_upper_temp = get_numeric_value(cr_lower_hsas_upper_temp)
    cr_upper_hsas_lower_temp = get_numeric_value(cr_upper_hsas_lower_temp)
    cr_upper_hsas_upper_temp = get_numeric_value(cr_upper_hsas_upper_temp)

    cr_lower_hsas_lower_temp = float(cr_lower_hsas_lower_temp)
    cr_lower_hsas_upper_temp = float(cr_lower_hsas_upper_temp)
    cr_upper_hsas_lower_temp = float(cr_upper_hsas_lower_temp)
    cr_upper_hsas_upper_temp = float(cr_upper_hsas_upper_temp)

    # Interpolate CR values for the given temperature, velocity, and HSAS
    cr_lower_temp = linear_interpolate(temperature, lower_temp, upper_temp, cr_lower_hsas_lower_temp, cr_lower_hsas_upper_temp)
    cr_upper_temp = linear_interpolate(temperature, lower_temp, upper_temp, cr_upper_hsas_lower_temp, cr_upper_hsas_upper_temp)
    cr = linear_interpolate(hsas, lower_hsas, upper_hsas, cr_lower_temp, cr_upper_temp)

    return cr

# Example usage
# acid_gas_loading = 0.55
# temperature = 127
# velocity = 6.2
# hsas = 2
# Example usage DEA
acid_gas_loading = 0.05

temperature = 88

velocity = 5

hsas = 2

# amine type = DEA

# amine concentration = 34


cr = buscar_cr(acid_gas_loading, temperature, velocity, hsas)

if cr:
    print(f"CR para acid_gas_loading={acid_gas_loading}, temperature={temperature}, velocity={velocity} y HSAS={hsas}: {cr}")
else:
    print(f"No se encontró un valor de CR para los parámetros proporcionados.")


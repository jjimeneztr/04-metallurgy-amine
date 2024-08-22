import pandas as pd
import scipy.interpolate as interp

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

    # Se devuelven los resultados en un diccionario.
    return {"cr_mm_year": cr_mm_year, "cr_mpy": cr_mpy}

def main():
  """
  Función principal de la aplicación.
  """
  # Se presenta la ventana principal con la selección de material.
  material = input("Seleccione el material (CS o Low Alloy Steel vs. 300 Series SS): ")

  if material.upper() == "300 SERIES SS":
    # Se solicita la carga de gas ácido.
    acid_gas_loading = float(input("Ingrese la carga de gas ácido (mol/mol): "))

    # Se calcula y se muestra la velocidad de corrosión (CR).
    cr_data = calcular_cr_300ss(acid_gas_loading)

    print(f"CR para acid_gas_loading = {acid_gas_loading} mol/mol:")
    print(f"- mm/año: {cr_data['cr_mm_year']:.3f}")
    print(f"- mpy: {cr_data['cr_mpy']:.3f}")

  elif material.upper() in ("CS", "LOW ALLOY STEEL"):
    # Se solicitan los datos de entrada.
    operating_temp = float(input("Ingrese la temperatura de operación (°C o °F): "))
    acid_gas_loading = float(input("Ingrese la carga de gas ácido (mol/mol): "))
    amine_type = input("Ingrese el tipo de amina (MEA, DEA o MDEA): ").upper()
    amine_concentration = float(input("Ingrese la concentración de amina (wt%): "))
    hsas = float(input("Ingrese el contenido de HSAS (wt%): "))
    velocity = float(input("Ingrese la velocidad (ft/s o m/s): "))

    

  else:
    print("Material no válido.")

if __name__ == "__main__":
  main()

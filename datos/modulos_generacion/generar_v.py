import pandas as pd
import os

class GenerarCapacidadV:
    """
    Genera la capacidad V del estanque (L).
    """
    def __init__(self, V=1000000):  # p.ej. 1 millón de litros
        self.V = V

    def generar(self, guardar_csv=False, ruta_csv=None):
        df = pd.DataFrame([{'V': self.V}])
        if guardar_csv:
            if not ruta_csv:
                ruta_csv = os.path.join(os.getcwd(), "V.csv")
            df.to_csv(ruta_csv, index=False)
        return df

if __name__ == "__main__":
    gen = GenerarCapacidadV()
    print(gen.generar(guardar_csv=True))

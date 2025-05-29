import pandas as pd
import os

class GenerarVolumenInicial:
    """
    Genera V0: volumen inicial en el estanque (L).
    """
    def __init__(self, V0=0):
        self.V0 = V0

    def generar(self, guardar_csv=False, ruta_csv=None):
        df = pd.DataFrame([{'V0': self.V0}])
        if guardar_csv:
            if not ruta_csv:
                ruta_csv = os.path.join(os.getcwd(), "V0.csv")
            df.to_csv(ruta_csv, index=False)
        return df

if __name__ == "__main__":
    gen = GenerarVolumenInicial()
    print(gen.generar(guardar_csv=True))

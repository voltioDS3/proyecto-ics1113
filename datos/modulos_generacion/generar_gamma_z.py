import pandas as pd
import numpy as np
import os

class GenerarGammaZ:
    """
    Genera gamma_z: m² máximos instalables por sub-zona.
    """
    def __init__(self,
                 total_zonas=10,
                 gamma_range=(500, 2000)):
        self.Z = list(range(1, total_zonas+1))
        self.gamma_range = gamma_range

    def generar(self, guardar_csv=False, ruta_csv=None):
        datos = [{'z': z,
                  'gamma_z': np.random.uniform(*self.gamma_range)}
                 for z in self.Z]
        df = pd.DataFrame(datos)
        if guardar_csv:
            if not ruta_csv:
                ruta_csv = os.path.join(os.getcwd(), "gamma_z.csv")
            df.to_csv(ruta_csv, index=False)
        return df

if __name__ == "__main__":
    gen = GenerarGammaZ()
    print(gen.generar(guardar_csv=True))

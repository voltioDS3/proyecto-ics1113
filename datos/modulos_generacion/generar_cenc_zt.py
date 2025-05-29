import pandas as pd
import numpy as np
import os

class GenerarCostoEncendido:
    """
    Simula cenc_zt: costo de encender sub-zona z en mes t (CLP).
    """
    def __init__(self,
                 total_zonas=10,
                 total_meses=24,
                 costo_range_encendido=(30000, 60000),
                 inflation_rate=0.005):
        self.Z = list(range(1, total_zonas + 1))
        self.T = list(range(1, total_meses + 1))
        self.costo_range = costo_range_encendido
        self.inflation_rate = inflation_rate

    def generar(self, guardar_csv=False, ruta_csv=None):
        datos = []
        for z in self.Z:
            for t in self.T:
                base = np.random.uniform(*self.costo_range)
                infl = 1 + self.inflation_rate * (t - 1)
                ruido = np.random.normal(0, base * 0.05)
                cenczt = max(base * infl + ruido, 0)
                datos.append({'z': z, 't': t, 'cenc_zt': cenczt})
        df = pd.DataFrame(datos)
        if guardar_csv:
            if not ruta_csv:
                ruta_csv = os.path.join(os.getcwd(), "cenc_zt.csv")
            df.to_csv(ruta_csv, index=False)
        return df

if __name__ == "__main__":
    sim = GenerarCostoEncendido()
    df = sim.generar(guardar_csv=True)
    print(df.head())

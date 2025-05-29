import pandas as pd
import numpy as np
import os

class GenerarCostoApagado:
    """
    Simula capg_zt: costo de apagar sub-zona z en mes t (CLP).
    """
    def __init__(self,
                 total_zonas=10,
                 total_meses=24,
                 costo_range_apagado=(15000, 30000),
                 inflation_rate=0.005):
        self.Z = list(range(1, total_zonas + 1))
        self.T = list(range(1, total_meses + 1))
        self.costo_range = costo_range_apagado
        self.inflation_rate = inflation_rate

    def generar(self, guardar_csv=False, ruta_csv=None):
        datos = []
        for z in self.Z:
            for t in self.T:
                base = np.random.uniform(*self.costo_range)
                infl = 1 + self.inflation_rate * (t - 1)
                ruido = np.random.normal(0, base * 0.05)
                capgzt = max(base * infl + ruido, 0)
                datos.append({'z': z, 't': t, 'capg_zt': capgzt})
        df = pd.DataFrame(datos)
        if guardar_csv:
            if not ruta_csv:
                ruta_csv = os.path.join(os.getcwd(), "capg_zt.csv")
            df.to_csv(ruta_csv, index=False)
        return df

if __name__ == "__main__":
    sim = GenerarCostoApagado()
    df = sim.generar(guardar_csv=True)
    print(df.head())

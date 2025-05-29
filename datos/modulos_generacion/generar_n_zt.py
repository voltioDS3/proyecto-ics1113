import pandas as pd
import numpy as np
import os

class SimularMantenimientoConexionNzt:
    """
    Simula n_zt: costo de mantención de la conexión en zona z y mes t (CLP).
    """
    def __init__(self,
                 total_zonas=10,
                 total_meses=24,
                 costo_range_conexion=(15000, 30000),
                 inflation_rate=0.005):
        self.Z = list(range(1, total_zonas + 1))
        self.T = list(range(1, total_meses + 1))
        self.costo_range = costo_range_conexion
        self.inflation_rate = inflation_rate

    def generar(self, guardar_csv=False, ruta_csv=None):
        datos = []
        for z in self.Z:
            for t in self.T:
                base = np.random.uniform(*self.costo_range)
                infl = 1 + self.inflation_rate * (t - 1)
                ruido = np.random.normal(0, base * 0.05)
                nzt = max(base * infl + ruido, 0)
                datos.append({'z': z, 't': t, 'n_zt': nzt})
        df = pd.DataFrame(datos)
        if guardar_csv:
            if not ruta_csv:
                ruta_csv = os.path.join(os.getcwd(), "n_zt.csv")
            df.to_csv(ruta_csv, index=False)
        return df

if __name__ == "__main__":
    sim = SimularMantenimientoConexionNzt()
    df = sim.generar(guardar_csv=True)
    print(df.head())

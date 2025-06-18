import pandas as pd
import numpy as np
import os

class SimularCostoWzt:
    def __init__(self,
                 total_zonas=10,
                 total_meses=24,
                 costo_fijo_conexion=4142,
                 inflation_rate=0.005):
        self.Z = list(range(1, total_zonas + 1))
        self.T = list(range(1, total_meses + 1))
        self.costo_fijo = costo_fijo_conexion
        self.inflation_rate = inflation_rate

        n_easy = total_zonas // 2
        factors = [1.0] * n_easy + [1.3] * (total_zonas - n_easy)
        self.factor_dificultad = {z: factors[z-1] for z in self.Z}

    def generar(self, guardar_csv=False, ruta_csv=None):
        datos = []
        for z in self.Z:
            fz = self.factor_dificultad[z]
            for t in self.T:
                infl = 1 + self.inflation_rate * (t - 1)
                wzt = self.costo_fijo * fz * infl
                datos.append({'z': z, 't': t, 'w_zt': wzt})
        df = pd.DataFrame(datos)
        if guardar_csv:
            if not ruta_csv:
                ruta_csv = os.path.join(os.getcwd(), "w_zt.csv")
            df.to_csv(ruta_csv, index=False)
        return df

if __name__ == "__main__":
    sim = SimularCostoWzt(total_zonas=12, total_meses=24)
    df = sim.generar(guardar_csv=True)
    print(df.head())

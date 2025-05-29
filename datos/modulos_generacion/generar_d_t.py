import pandas as pd
import numpy as np
import os

class GenerarDemandaDt:
    """
    Simula dt: litros demandados en t por la población.
    """
    def __init__(self,
                 total_meses=24,
                 poblacion=150000,
                 consumo_diario=150,  # L/día por habitante
                 dias_mes=30):
        self.T = range(1, total_meses+1)
        self.poblacion = poblacion
        self.consumo_diario = consumo_diario
        self.dias = dias_mes

    def generar(self, guardar_csv=False, ruta_csv=None):
        datos = []
        for t in self.T:
            base = self.poblacion * self.consumo_diario * self.dias
            ruido = np.random.normal(0, base * 0.05)
            dt = max(base + ruido, 0)
            datos.append({'t': t, 'd_t': dt})
        df = pd.DataFrame(datos)
        if guardar_csv:
            if not ruta_csv:
                ruta_csv = os.path.join(os.getcwd(), "d_t.csv")
            df.to_csv(ruta_csv, index=False)
        return df

if __name__ == "__main__":
    gen = GenerarDemandaDt()
    df = gen.generar(guardar_csv=True)
    print(df.head())

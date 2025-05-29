import pandas as pd
import os

class GenerarK:
    """
    Genera K: capacidad de transporte mensual de cada cañería (L).
    """
    def __init__(self,
                 total_meses=24,
                 K=150000000):
        self.T = range(1, total_meses+1)
        self.K = K

    def generar(self, guardar_csv=False, ruta_csv=None):
        df = pd.DataFrame([{'t': t, 'K': self.K} for t in self.T])
        if guardar_csv:
            if not ruta_csv:
                ruta_csv = os.path.join(os.getcwd(), "K.csv")
            df.to_csv(ruta_csv, index=False)
        return df

if __name__ == "__main__":
    gen = GenerarK()
    print(gen.generar(guardar_csv=True).head())

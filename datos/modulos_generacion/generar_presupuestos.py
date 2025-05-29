import pandas as pd
import os

class GenerarPresupuestos:
    """
    Genera P1 en t=1, P2 en t=13, y 0 en los demás meses.
    """
    def __init__(self,
                 total_meses=24,
                 P1=500000000,  # CLP, ejemplo: 500 millones
                 P2=300000000): # CLP, ejemplo: 300 millones
        self.T = range(1, total_meses+1)
        self.P1 = P1
        self.P2 = P2

    def generar(self, guardar_csv=False, ruta_csv=None):
        datos = []
        for t in self.T:
            valor = self.P1 if t == 1 else (self.P2 if t == 13 else 0)
            datos.append({'t': t, 'P_t': valor})
        df = pd.DataFrame(datos)
        if guardar_csv:
            if not ruta_csv:
                ruta_csv = os.path.join(os.getcwd(), "presupuestos.csv")
            df.to_csv(ruta_csv, index=False)
        return df

if __name__ == "__main__":
    gen = GenerarPresupuestos()
    df = gen.generar(guardar_csv=True)
    print(df.head(15))

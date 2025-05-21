import pandas as pd
import os

class GenerarCostoC_t:
    def __init__(self, total_meses=24, costo_por_litro=1.31947):
        self.total_meses = total_meses
        self.costo_por_litro = costo_por_litro
        self.T = range(1, total_meses + 1)

    def generar_dataframe(self, guardar_csv=False, ruta_csv=None):
        columnas = ['t', 'c_t']
        datos = [[t, self.costo_por_litro] for t in self.T]
        df = pd.DataFrame(datos, columns=columnas)

        if guardar_csv:
            if ruta_csv is None:
                carpeta = os.path.dirname(__file__)
                ruta_csv = os.path.join(carpeta, "c_t.csv")
            df.to_csv(ruta_csv, index=False)
        return df

    def run(self, **kwargs):
        return self.generar_dataframe(**kwargs)


if __name__ == "__main__":
    generador = GenerarCostoC_t(total_meses=25)
    df = generador.run(guardar_csv=True, ruta_csv="output/c_t.csv")
    print(df.head())
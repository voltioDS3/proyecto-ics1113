import pandas as pd
import numpy as np
import os

class SimularExtracionq_zt:
    def __init__(self,
                 total_zonas=10,
                 total_meses=24,
                 zona_sur_dim=(1000, 3000),
                 zona_norte_dim=(2000, 3000),
                 coords_caneria_sur=(0, 1500),
                 coords_caneria_norte=(1000, 0),
                 maximo_mes_zona_sur=None,
                 maximo_mes_zona_norte=None):
        self.total_zonas = total_zonas
        self.total_meses = total_meses
        self.Z = range(total_zonas)
        self.T = range(1, total_meses + 1)

        self.zona_sur_dim = np.array(zona_sur_dim)
        self.zona_norte_dim = np.array(zona_norte_dim)
        self.coord_sur = np.array(coords_caneria_sur)
        self.coord_norte = np.array(coords_caneria_norte)

        # Diccionarios por defecto si no se proveen
        self.max_sur = maximo_mes_zona_sur or {
            'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0,
            'mayo': 3.5*30, 'junio': 1.5*30, 'julio': 4.5*30,
            'agosto': 11.5*30, 'septiembre': 10.7*30, 'octubre': 11*30,
            'noviembre': 5*30, 'diciembre': 0
        }
        self.max_norte = maximo_mes_zona_norte or {
            'enero': 0, 'febrero': 0, 'marzo': 6, 'abril': 0,
            'mayo': 3.8*30, 'junio': 2.1*30, 'julio': 5*30,
            'agosto': 10*30, 'septiembre': 9*30, 'octubre': 9.5*30,
            'noviembre': 5.8*30, 'diciembre': 0
        }

        # Listas donde guardaremos la info de las zonas
        self.zonas_sur = []
        self.zonas_norte = []

    def generar_zonas(self):
        """Genera coordenadas aleatorias para cada zona."""
        for z in self.Z:
            if z < self.total_zonas / 2:
                dims = self.zona_sur_dim
                lista = self.zonas_sur
            else:
                dims = self.zona_norte_dim
                lista = self.zonas_norte

            x = np.random.randint(dims[0])
            y = np.random.randint(dims[1])
            lista.append({'coord': np.array([x, y])})

    def _factor_distancia(self, x, ancho):
        centro = ancho / 2
        distancia = abs(x - centro)
        factor = 1 - 0.3 * (distancia / centro)
        return max(factor, 0)

    def asignar_produccion(self):
        """Calcula la producción mensual en cada zona."""
        meses = list(self.max_sur.keys())
        # Sur
        for zona in self.zonas_sur:
            x, y = zona['coord']
            prod = {}
            for mes in meses:
                prod[mes] = self._factor_distancia(x, self.zona_sur_dim[0]) * self.max_sur[mes] * 1e-6 *1.2
            zona['produccion'] = prod

        # Norte
        for zona in self.zonas_norte:
            x, y = zona['coord']
            prod = {}
            for mes in meses:
                prod[mes] = self._factor_distancia(x, self.zona_norte_dim[0]) * self.max_norte[mes] * 1e-6 *1.2
            zona['produccion'] = prod

    def calcular_distancias(self):
        """Añade la distancia a la cañería en cada zona."""
        for zona in self.zonas_sur:
            zona['distancia_a_caneria'] = np.linalg.norm(zona['coord'] - self.coord_sur)
        for zona in self.zonas_norte:
            zona['distancia_a_caneria'] = np.linalg.norm(zona['coord'] - self.coord_norte)

    def generar_dataframe(self, guardar_csv=False, ruta_csv=None):
        """Devuelve un DataFrame con toda la info de producción por mes."""
        nombres_meses = [
            'enero','febrero','marzo','abril','mayo','junio',
            'julio','agosto','septiembre','octubre','noviembre','diciembre'
        ]

        columnas = ['z'] + [str(i) for i in range(1, self.total_meses + 1)]
        datos = []

        # Sur
        for idx, zona in enumerate(self.zonas_sur, start=1):
            anual = [zona['produccion'][m] for m in nombres_meses]
            repet = (anual * ((self.total_meses // 12) + 1))[:self.total_meses]
            datos.append([idx] + repet)

        # Norte
        offset = len(self.zonas_sur)
        for idx, zona in enumerate(self.zonas_norte, start=1):
            anual = [zona['produccion'][m] for m in nombres_meses]
            repet = (anual * ((self.total_meses // 12) + 1))[:self.total_meses]
            datos.append([offset + idx] + repet)

        df = pd.DataFrame(datos, columns=columnas)
        df.index = range(1, self.total_zonas + 1)

        if guardar_csv:
            if ruta_csv is None:
                # ruta por defecto junto al script
                carpeta = os.path.dirname(__file__)
                ruta_csv = os.path.join(carpeta, "q_zt.csv")
            df.to_csv(ruta_csv, index=False)
        return df

    def run(self, **kwargs):
        """Convenience: ejecuta todo el flujo y devuelve el DataFrame."""
        self.generar_zonas()
        self.asignar_produccion()
        self.calcular_distancias()
        return self.generar_dataframe(**kwargs)


# --- Uso desde otra parte del código ---

# Por ejemplo, en tu función principal:
def main():
    sim = SimularExtracionq_zt(total_zonas=12, total_meses=36)
    df = sim.run(guardar_csv=True, ruta_csv="output/produccion.csv")
    print(df.head())

if __name__ == "__main__":
    main()

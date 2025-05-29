import pandas as pd
import numpy as np
import os

class SimularCostoKzt:
    """
    Simula el parámetro k_zt: costo de instalación por metro cuadrado
    de atrapaniebla en la zona z y mes t, para Alto Hospicio.
    """
    def __init__(self,
                 total_zonas=10,
                 total_meses=24,
                 # Rango de costo base (CLP/m²) de malla Raschel: US$0.315–0.63/m²,
                 # convertido a CLP con tipo de cambio ~936,53 CLP/USD :contentReference[oaicite:0]{index=0}
                 costo_range_base=(295, 590),
                 # Tasa de inflación mensual (e.g., 0.5%)
                 inflation_rate=0.005):
        self.total_zonas = total_zonas
        self.total_meses = total_meses
        self.Z = list(range(1, total_zonas + 1))
        self.T = list(range(1, total_meses + 1))

        # Ubicación única de todas las zonas (misma comuna) :contentReference[oaicite:1]{index=1}
        self.ubicacion = "Alto Hospicio, Provincia de Iquique, Región de Tarapacá, Chile"

        self.costo_base = costo_range_base
        self.inflation_rate = inflation_rate

        # Asignar factor de dificultad de acceso a cada "zona" (misma localidad)
        # mitad fácil (factor 1.0) y mitad difícil (factor aleatorio 1.2–1.5)
        n_easy = total_zonas // 2
        n_hard = total_zonas - n_easy
        factors = [1.0]*n_easy + list(np.random.uniform(1.2, 1.5, size=n_hard))
        np.random.shuffle(factors)
        self.dificultad = {z: factors[z-1] for z in self.Z}

    def generar(self, guardar_csv=False, ruta_csv=None):
        """
        Genera un DataFrame con columnas ['z', 't', 'k_zt'] en CLP.
        Si guardar_csv=True, exporta a ruta_csv.
        """
        datos = []
        for z in self.Z:
            factor_z = self.dificultad[z]
            for t in self.T:
                # coste material base aleatorio dentro del rango
                base = np.random.uniform(*self.costo_base)
                # ajuste por dificultad y por inflación acumulada
                factor_infl = 1 + self.inflation_rate * (t - 1)
                # ruido aleatorio (~±5% del base)
                ruido = np.random.normal(0, base * 0.05)
                kzt = max(base * factor_z * factor_infl + ruido, 0)
                datos.append({'z': z, 't': t, 'k_zt': kzt})

        df = pd.DataFrame(datos)
        if guardar_csv:
            if ruta_csv is None:
                ruta_csv = os.path.join(os.getcwd(), "k_zt.csv")
            df.to_csv(ruta_csv, index=False)
        return df

# --- Ejemplo de uso (solo código) ---
# sim = SimularCostoKzt(total_zonas=12, total_meses=36)
# df_kzt = sim.generar(guardar_csv=True, ruta_csv="k_zt.csv")
# print(df_kzt.head())

from modulos_generacion import generar_q_zt
from modulos_generacion import generar_c_t
TOTAL_ZONAS = 10
TOTAL_MESES = 25

def main():
    sim_q_zt = generar_q_zt.SimularExtracionq_zt(
        TOTAL_ZONAS,
        TOTAL_MESES
    )
    df = sim_q_zt.run(guardar_csv=True, ruta_csv="output/q_zt.csv")

    sim_c_t = generar_c_t.GenerarCostoC_t(
        total_meses=TOTAL_MESES,
        costo_por_litro=1.31947
    )
    df_c = sim_c_t.run(guardar_csv=True, ruta_csv="output/c_t.csv")
    # TODO generar los otros csv para los parametros
if __name__ == "__main__":
    main()
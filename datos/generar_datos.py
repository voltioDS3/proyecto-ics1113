from modulos_generacion import generar_q_zt
TOTAL_ZONAS = 10
TOTAL_MESES = 25

def main():
    sim_q_zt = generar_q_zt.SimularExtracionq_zt(
        TOTAL_ZONAS,
        TOTAL_MESES
    )
    df = sim_q_zt.run(guardar_csv=True, ruta_csv="output/q_zt.csv")

if __name__ == "__main__":
    main()
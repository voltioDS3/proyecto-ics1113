from modulos_generacion import generar_q_zt
from modulos_generacion import generar_c_t
from modulos_generacion import generar_capg_zt
from modulos_generacion import generar_cenc_zt
from modulos_generacion import generar_d_t
from modulos_generacion import generar_gamma_z
from modulos_generacion import generar_k
from modulos_generacion import generar_k_zt
from modulos_generacion import generar_m
from modulos_generacion import generar_presupuestos
from modulos_generacion import generar_n_zt
from modulos_generacion import generar_m_zt 

from modulos_generacion import generar_v
from modulos_generacion import generar_v0
from modulos_generacion import generar_w_zt

TOTAL_ZONAS = 20
TOTAL_MESES = 24
RUTA= "/output/"
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

    sim_capag = generar_capg_zt.GenerarCostoApagado(total_zonas=TOTAL_ZONAS,
                                                    total_meses=TOTAL_MESES,
                                                    )
    sim_capag.generar(guardar_csv=True, ruta_csv="output/Capg_zt.csv")


    sim_cenc = generar_cenc_zt.GenerarCostoEncendido(total_zonas=TOTAL_ZONAS,
                                                    total_meses=TOTAL_MESES)
    sim_cenc.generar(guardar_csv=True, ruta_csv="output/Cenc_zt.csv")


    sim_d_t = generar_d_t.GenerarDemandaDt(total_meses=TOTAL_MESES)
    sim_d_t.generar(guardar_csv=True, ruta_csv="output/d_t.csv")

    sim_gama_z = generar_gamma_z.GenerarGammaZ(total_zonas=TOTAL_ZONAS)
    sim_gama_z.generar(guardar_csv=True, ruta_csv="output/gamma_z.csv")

    sim_k = generar_k.GenerarK(total_meses=TOTAL_MESES)
    sim_k.generar(guardar_csv=True, ruta_csv="output/K.csv")

    sim_k_zt = generar_k_zt.SimularCostoKzt(total_zonas=TOTAL_ZONAS, total_meses=TOTAL_MESES)
    sim_k_zt.generar(guardar_csv=True, ruta_csv="output/k_zt.csv")

    sim_m = generar_m.calcular_M(gamma_path="output/gamma_z.csv") # TODO guardar de alguna forma

    sim_presupuestos = generar_presupuestos.GenerarPresupuestos(total_meses=TOTAL_MESES,
                                                                )
    sim_presupuestos.generar(guardar_csv=True, ruta_csv="output/P.csv")

    sim_n_zt = generar_n_zt.SimularMantenimientoConexionNzt(total_meses=TOTAL_MESES,
                                                            total_zonas=TOTAL_ZONAS)
    sim_n_zt.generar(guardar_csv=True, ruta_csv="output/n_zt.csv")


    sim_m_zt = generar_m_zt.SimularMantenimientoMzt(total_zonas=TOTAL_ZONAS,
                                                    total_meses=TOTAL_MESES)
    sim_m_zt.generar(guardar_csv=True, ruta_csv="output/m_zt.csv")

    sim_v = generar_v.GenerarCapacidadV()
    sim_v.generar(guardar_csv=True, ruta_csv="output/V.csv")

    sim_V_0 = generar_v0.GenerarVolumenInicial()
    sim_V_0.generar(guardar_csv=True, ruta_csv="output/V_o.csv")

    sim_w_zt = generar_w_zt.SimularCostoWzt(total_zonas=TOTAL_ZONAS,
                                            total_meses=TOTAL_MESES)
    sim_w_zt.generar(guardar_csv=True, ruta_csv="output/w_zt.csv")

if __name__ == "__main__":
    main()
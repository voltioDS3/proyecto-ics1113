from main import ModeloNiebla
import os

def correr_instancia(nombre_escenario, modificar_modelo):
    print(f"\nEjecutando: {nombre_escenario} ...")
    modelo = ModeloNiebla()
    modelo.cargarParametros()
    
    # modificación específica del escenario
    modificar_modelo(modelo)

    # define, optimiza y guarda resultados con nombre distinto
    modelo.definirModelo()
    obj = modelo.optimizar()

    if obj is not None:
        os.rename("resultados/optimos.csv", f"resultados/optimos_{nombre_escenario}.csv")
        print(f"Escenario '{nombre_escenario}' completo. Objetivo: {obj:.2f} millones de litros")
    else:
        print(f"Escenario '{nombre_escenario}' no resolvió correctamente")

def main():
    escenarios = [
        # escenarios individuales -----------------

        # escenario base sin modificar parámetros (referencia para comparación)
        ("gamma_base", lambda m: None),

        # aumenta en un 30% el parámetro gamma_z, que representa la capacidad de permisos en cada subzona
        ("gamma_mas30", lambda m: m.gamma_z.update({z: val * 1.3 for z, val in m.gamma_z.items()})),

        # disminuye en un 30% el parámetro gamma_z
        ("gamma_menos30", lambda m: m.gamma_z.update({z: val * 0.7 for z, val in m.gamma_z.items()})),

        # escenario base para q_zt (recolección por m2)
        ("q_base", lambda m: None),

        # aumenta en un 30% el parámetro q_zt, que representa la cantidad de agua recolectada por m2 en cada zona-tiempo
        ("q_mas30", lambda m: m.q_zt.update({
            z: {t: val * 1.3 for t, val in m.q_zt[z].items()} for z in m.q_zt
        })),

        # disminuye en un 30% el parámetro q_zt
        ("q_menos30", lambda m: m.q_zt.update({
            z: {t: val * 0.7 for t, val in m.q_zt[z].items()} for z in m.q_zt
        })),

        # escenarios mixtos -------------------------

        # escenario mixto: condiciones ideales, permisos altos y alta recolección
        ("mixto_optimo", lambda m: (
            m.q_zt.update({z: {t: val * 1.3 for t, val in m.q_zt[z].items()} for z in m.q_zt}),
            m.gamma_z.update({z: val * 1.3 for z, val in m.gamma_z.items()})
        )),

        # escenario mixto: condiciones críticas, baja recolección y pocas autorizaciones
        ("mixto_critico", lambda m: (
            m.q_zt.update({z: {t: val * 0.7 for t, val in m.q_zt[z].items()} for z in m.q_zt}),
            m.gamma_z.update({z: val * 0.7 for z, val in m.gamma_z.items()})
        )),

        # escenario mixto: ambiente húmedo pero restricciones severas de permisos
        ("mixto_humedo_restringido", lambda m: (
            m.q_zt.update({z: {t: val * 1.3 for t, val in m.q_zt[z].items()} for z in m.q_zt}),
            m.gamma_z.update({z: val * 0.7 for z, val in m.gamma_z.items()})
        )),

        # escenario mixto: ambiente seco pero se entregan muchos permisos para instalar
        ("mixto_seco_flexible", lambda m: (
            m.q_zt.update({z: {t: val * 0.7 for t, val in m.q_zt[z].items()} for z in m.q_zt}),
            m.gamma_z.update({z: val * 1.3 for z, val in m.gamma_z.items()})
        )),
    ]


    for nombre, modificador in escenarios:
        correr_instancia(nombre, modificador)

if __name__ == "__main__":
    main()

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
        # gamma_z
        ("gamma_base", lambda m: None),
        ("gamma_menos30", lambda m: m.gamma_z.update({z: val * 0.7 for z, val in m.gamma_z.items()})),
        ("gamma_mas30", lambda m: m.gamma_z.update({z: val * 1.3 for z, val in m.gamma_z.items()})),

        # K
        ("K_base", lambda m: setattr(m, "K", 150000000 * 1e-6)),
        ("K_menos", lambda m: setattr(m, "K", 100000000 * 1e-6)),
        ("K_mas", lambda m: setattr(m, "K", 200000000 * 1e-6)),

        # P_1
        ("P1_base", lambda m: setattr(m, "P_1", 500000000)),
        ("P1_menos", lambda m: setattr(m, "P_1", 300000000)),
        ("P1_mas", lambda m: setattr(m, "P_1", 700000000)),
    ]

    for nombre, modificador in escenarios:
        correr_instancia(nombre, modificador)

if __name__ == "__main__":
    main()

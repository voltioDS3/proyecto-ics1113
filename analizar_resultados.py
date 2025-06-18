import re, glob, os
import pandas as pd
import matplotlib.pyplot as plt

def objetivo(path_csv):
    with open(path_csv, encoding="utf-8") as f:
        lineas = [l.strip() for l in f if l.strip()]
    ultima = lineas[-1]

    if ',' in ultima and re.match(r'[0O]bjVal', ultima, flags=re.I):
        _, num = ultima.split(',', 1)
        val = float(num)
    else:
        m = re.search(r'([0-9]+(?:\.[0-9]+)?)', ultima)
        val = float(m.group(1)) if m else 0.0

    esc = re.search(r'optimos_(.*)\.csv', os.path.basename(path_csv)).group(1)
    return esc, round(val, 2)

def main():
    filas = [objetivo(p) for p in glob.glob("resultados/optimos_*.csv")]
    df = pd.DataFrame(filas, columns=["Escenario", "Objetivo (M L)"]).sort_values("Escenario")

    print("\nRESUMEN OBJETIVOS\n")
    print(df.to_string(index=False))

    df.to_csv("resultados/resumen_objetivos.csv", index=False)

    plt.figure(figsize=(10, 5))
    plt.bar(df["Escenario"], df["Objetivo (M L)"])
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Millones de litros")
    plt.title("Litros recolectados por escenario")
    plt.tight_layout()
    plt.savefig("resultados/grafico_objetivo.png")
    plt.show()

if __name__ == "__main__":
    main()

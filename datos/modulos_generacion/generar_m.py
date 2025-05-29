import pandas as pd

def calcular_M(gamma_path="gamma_z.csv"):
    """
    Lee el CSV de gamma_z y devuelve M = max(gamma_z).
    """
    df = pd.read_csv(gamma_path)
    return df['gamma_z'].max()

if __name__ == "__main__":
    M = calcular_M()
    print(f"Big-M: {M}")

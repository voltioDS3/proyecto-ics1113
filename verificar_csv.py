import pandas as pd

df = pd.read_csv("resultados/optimos_K_base.csv")
print(df.tail(10))  # Mostrar las últimas 10 filas

# Extra: intentar detectar ObjVal limpiando caracteres raros
df['variable'] = df['variable'].astype(str).str.strip().str.replace('\r', '', regex=False)
print(df[df['variable'] == "ObjVal"])

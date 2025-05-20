# Instalacion
## Clonar el repositorio
``` bash
git clone https://github.com/voltioDS3/proyecto-ics1113.git
```
## Crear entorno virtual
```bash
python -m venv gurobi-env
```
## Activar el entorno
```bash
source gurobi-env/bin/activate  # o .\gurobi-env\Scripts\activate en Windows
```
## Instalar las dependencias
```bash
pip install -r requirements.txt
```
---
#  Estructura

```
PROYECTO-ICS1113/
├── datos/                     # Carpeta con CSVs y scripts para generarlos
│   ├── output/                # los CSV con los parametros 
│   │   ├──q_zt.csv
│   │   ├──a_zt.csv
│   │   └── ... otros CSV ...
│   ├── modulos_generacion/    # los archivos que generan los CSV
│   │   ├──generar_q_zt.py
│   │   └──... otros .py ...
│   └── generar_datos.py               # Archivo que genera todos los csv necesarios segun cantidad de meses y zonas
└── main.py                    # Script de ejecución del modelo
```
---
# Descripcion del codigo

#### 1. `main.py`

Define la **clase** `ModeloNiebla`, que incluye:

* **Atributos principales**:

  * `T`: conjunto de períodos (1 a 24).
  * `Z`: conjunto de zonas (1 a 10).
  * `model`: instancia de Gurobi (`gp.Model`).
  * Rutas de archivos CSV de parámetros (capacidad, costos, distancias, etc.).

* **Métodos**:

  1. `cargarParametros()`

     * Debe leer CSVs desde `datos/` e inicializar matrices y diccionarios de parámetros.
     * Actualmente marcado como TODO.

  2. `definirModelo()`

     * Crea variables de decisión:

       * Continuas: `a_zt` , `x_zt`, `y_t`, `u_t`, `I_t`.
       * Binarias: `p_zt`, `b_zt`, `r_zt`, `s_zt`, `enc_zt`, `apg_zt`.
     * Agrega restricciones (pendientes de implementación).
     * Define objetivo de maximización:

       ```python
       self.model.setObjective(
           quicksum(a_zt[z, t] * q_zt[z][t]
                    for z in self.Z for t in self.T),
           GRB.MAXIMIZE
       )
       ```
     

  3. `optimizar()`

     * Ejecuta `model.optimize()`.
     * Revisa status:

       * Infactible: genera archivo de IIS (`modelo.ilp`).
       * No acotado o infactible/no acotado.
       * Retorna valor objetivo si solución óptima.

  4. `main()`

     * Instancia `ModeloNiebla`.
     * Llama a `cargarParametros()`, `definirModelo()`, `optimizar()`.

#### 2. `generar_datos.py`

Este script se encarga de **generar datos simulados** , actualmente solamente esta implementado para generar los datos de q_zt. La idea es que este archivo permita generar todos los datos necesarios en base a TOTAL_ZONAS y TOTAL_MES cosa de que todos los datos sean compatibles

### ¿Qué hace?

1. Define la cantidad total de zonas (`TOTAL_ZONAS = 10`) y meses (`TOTAL_MESES = 25`).
2. genera y guarda los CSV en `output/`.

---

import pandas as pd
from gurobipy import GRB, quicksum
import gurobipy as gp
import os
from os import path
import locale
BASE_DATOS = "./datos/output"
TOTAL_MESES = 24    
TOTAL_ZONAS = 20
class ModeloNiebla:

    def __init__(self):
        self.T = range(1,TOTAL_MESES+1)
        self.Z = range(1,TOTAL_ZONAS+1) #de la zona 1 a la zona 5 son zona sur, de la 6 hasta la 10 zona norte
        self.model = gp.Model() # modelo

        ruta_archivos = {
            'q_zt': path.join(BASE_DATOS, 'q_zt.csv'), # DF LISTO
            'c_t': path.join(BASE_DATOS, 'c_t.csv'),  # DF LISTO
            'csobre_t': path.join(BASE_DATOS, 'csobre_t.csv'), ## TODO costo sobre consumo experimental
            'k_zt': path.join(BASE_DATOS, 'k_zt.csv'), # TODO GENERAR DATOS
            'w_zt': path.join(BASE_DATOS, 'w_zt.csv'), # TODO GENERAR DATOS
            'm_zt': path.join(BASE_DATOS, 'm_zt.csv'), # TODO GENERAR DATOS
            'n_zt': path.join(BASE_DATOS, 'n_zt.csv'), # TODO GENERAR DATOS
            'P_1': path.join(BASE_DATOS, 'P_1.csv'), # TODO GENERAR DATOS
            'P_2': path.join(BASE_DATOS, 'P_2.csv'), # TODO GENERAR DATOS
            'V': path.join(BASE_DATOS, 'V.csv'), # TODO GENERAR DATOS
            'V_o': path.join(BASE_DATOS, 'V_o.csv'), # TODO GENERAR DATOS
            'd_t': path.join(BASE_DATOS, 'd_t.csv'), # TODO GENERAR DATOS
            'gamma_z': path.join(BASE_DATOS, 'gamma_z.csv'), # TODO GENERAR DATOS
            'K': path.join(BASE_DATOS, 'K.csv'), # TODO GENERAR DATOS
            'Cenc_zt': path.join(BASE_DATOS, 'Cenc_zt.csv'), # TODO GENERAR DATOS
            'Capg_zt': path.join(BASE_DATOS, 'Capg_zt.csv'), # TODO GENERAR DATOS
        }

        df = pd.read_csv(ruta_archivos['q_zt'])
        self.q_zt = {z+1: {int(t): df.loc[z, t] for t in df.columns if t.isdigit()} for z in df.index}
        df = pd.read_csv(ruta_archivos['c_t'])
        self.c_t = df.set_index('t')['c_t'].to_dict()

        ### TODO asignar los valores de los csv a estas variables ###
        self.k_zt = {z: {t: 0.0 for t in range(1, TOTAL_MESES + 1)} for z in range(1, TOTAL_ZONAS + 1)}
        self.w_zt = {z: {t: 0.0 for t in range(1, TOTAL_MESES + 1)} for z in range(1, TOTAL_ZONAS + 1)}
        self.m_zt = {z: {t: 0.0 for t in range(1, TOTAL_MESES + 1)} for z in range(1, TOTAL_ZONAS + 1)}
        self.n_zt = {z: {t: 0.0 for t in range(1, TOTAL_MESES + 1)} for z in range(1, TOTAL_ZONAS + 1)}
        self.Cenc_zt = {z: {t: 0.0 for t in range(1, TOTAL_MESES + 1)} for z in range(1, TOTAL_ZONAS + 1)}
        self.Capg_zt = {z: {t: 0.0 for t in range(1, TOTAL_MESES + 1)} for z in range(1, TOTAL_ZONAS + 1)}

        self.P_1 = 1
        self.P_2 = 1
        self.V = 50
        self.V_o = 1
        self.d_t = {t: 0.0 for t in range(1, TOTAL_MESES + 1)}
        self.gamma_z = {t: 0.0 for t in range(1, TOTAL_MESES + 1)}
        self.K = 1
        pass

    def cargarParametros(self):
        ruta = BASE_DATOS

        archivos_zt = {
            'k_zt': 'k_zt.csv',
            'w_zt': 'w_zt.csv',
            'm_zt': 'm_zt.csv',
            'n_zt': 'n_zt.csv',
            'Cenc_zt': 'Cenc_zt.csv',
            'Capg_zt': 'Capg_zt.csv'
        }

        for nombre_parametro, archivo in archivos_zt.items():
            df = pd.read_csv(path.join(ruta, archivo))

            # Suponemos que siempre hay columnas z, t y <nombre_parametro>
            parametro = {}
            for _, fila in df.iterrows():
                z = int(fila['z'])
                t = int(fila['t'])
                valor = fila[nombre_parametro]

                if z not in parametro:
                    parametro[z] = {}
                parametro[z][t] = valor

            setattr(self, nombre_parametro, parametro)

        # cargamos d_t.csv
        df_d_t = pd.read_csv(path.join(ruta, "d_t.csv"))
        self.d_t = {}
        for _, row in df_d_t.iterrows():
            t = int(row["t"])
            self.d_t[t] = float(row["d_t"])

        # cargamos gamma_z.csv
        df_gamma = pd.read_csv(path.join(ruta, "gamma_z.csv"))
        self.gamma_z = {}
        for _, row in df_gamma.iterrows():
            z = int(row["z"])
            self.gamma_z[z] = float(row["gamma_z"])

        # cargamos escalares
        self.P_1 = 500000000
        self.P_2 = 300000000
        self.V    = 10000000*1e-6
        self.V_o  = 0
        self.K    = 150000000*1e-6
        print(self.k_zt[1][23])
        print(self.Capg_zt[1][23])
        print(self.K)
        
    def definirModelo(self):
        
        a_zt = self.model.addVars(self.Z, self.T,lb=0.0,
                                  vtype=GRB.CONTINUOUS, name="a_zt") # TODO confirmar vtype
        
        p_zt = self.model.addVars(self.Z, self.T,
                                  vtype=GRB.BINARY, name="p_zt")
        
        x_zt = self.model.addVars(self.Z, self.T,lb=0.0,
                                  vtype=GRB.CONTINUOUS, name="x_zt")# TODO confirmar vtype
        
        b_zt = self.model.addVars(self.Z, self.T,
                                  vtype=GRB.BINARY, name="b_zt") 
        
        r_zt = self.model.addVars(self.Z, self.T,
                                  vtype=GRB.BINARY, name="r_zt")
        
        s_zt = self.model.addVars(self.Z, self.T,
                                  vtype=GRB.BINARY, name="s_zt")
        
        y_t = self.model.addVars(self.T,lb=0.0,
                                  vtype=GRB.CONTINUOUS, name="y_t")# TODO confirmar vtype
        
        u_t = self.model.addVars(self.T,lb=0.0,
                                  vtype=GRB.CONTINUOUS, name="u_t")# TODO confirmar vtype
        
        I_t = self.model.addVars(self.T,lb=0.0,
                                  vtype=GRB.CONTINUOUS, name="I_t")# TODO confirmar vtype
        
        enc_zt = self.model.addVars(self.Z, self.T,
                                  vtype=GRB.BINARY, name="enc_zt")
        
        apg_zt = self.model.addVars(self.Z, self.T,
                                  vtype=GRB.BINARY, name="apg_zt")
        
        self.model.update()

        #### RESTRICCIONES ####
        # TODO implementar restricciones

        self.model.addConstrs((a_zt[z, t] <= quicksum(x_zt[z, tau] for tau in range(1, t+1)) for z in self.Z for t in self.T),
                      name="R1: Metros cuadrados activos menor a instalados")

        self.model.addConstrs((quicksum(x_zt[z, t] for t in self.T) <= self.gamma_z[z] for z in self.Z),
                            name="R2: restriccion metros cuadrados por motivos ambientales")

        self.model.addConstrs((y_t[t-1] + quicksum(a_zt[z, t]*self.q_zt[z][t] for z in self.Z) + u_t[t] == y_t[t] + self.d_t[t] for t in range(2, TOTAL_MESES+1)),
                            name="R3: litros de agua a almacenar")

        self.model.addConstr((self.V_o + quicksum(a_zt[z, 1]* self.q_zt[z][1] for z in self.Z) + u_t[1] == y_t[1] + self.d_t[1]),
                            "R4: condicion borde litros agua almacenada")

        self.model.addConstrs((quicksum(a_zt[z, t]* self.q_zt[z][t] for z in range(1, int(TOTAL_ZONAS/2) + 1)) <= self.K for t in self.T),
                            name="R5: el agua recolectada en la zona SUR no puede superar K en mes t")

        self.model.addConstrs((quicksum(a_zt[z, t]* self.q_zt[z][t] for z in range(int(TOTAL_ZONAS/2) + 1, TOTAL_ZONAS + 1)) <= self.K for t in self.T),
                            name="R6: el agua recolectada en la zona NORTE no puede superar K en mes t")

        self.model.addConstr((self.P_1 - (quicksum(self.k_zt[z][1]*x_zt[z, 1] + self.w_zt[z][1]*r_zt[z, 1] + self.m_zt[z][1]*a_zt[z, 1] + self.n_zt[z][1]*s_zt[z, 1] + self.Cenc_zt[z][1]*enc_zt[z, 1] + self.Capg_zt[z][1]*apg_zt[z, 1] for z in self.Z)  + self.c_t[1]*u_t[1]) == I_t[1]),
                            name="R7: presupuesto mes 1")

        self.model.addConstrs((I_t[t-1] - (quicksum(self.k_zt[z][t]*x_zt[z, t] + self.w_zt[z][1]*r_zt[z, t] + self.m_zt[z][t]*a_zt[z, t] + self.n_zt[z][t]*s_zt[z, t] + self.Cenc_zt[z][t]*enc_zt[z, t] + self.Capg_zt[z][t]*apg_zt[z, t] for z in self.Z)  + self.c_t[t]*u_t[t]) == I_t[t] for t in range(2, int(TOTAL_MESES/2) + 1)),
                            name="R8: presupuesto meses 2 a 12")

        self.model.addConstr((I_t[12] - (quicksum(self.k_zt[z][13]*x_zt[z, 13] + self.w_zt[z][13]*r_zt[z, 13] + self.m_zt[z][13]*a_zt[z, 13] + self.n_zt[z][13]*s_zt[z, 13] + self.Cenc_zt[z][13]*enc_zt[z, 13] + self.Capg_zt[z][13]*apg_zt[z, 13] for z in self.Z)  + self.c_t[13]*u_t[13]) + self.P_2 == I_t[13]),
                            name="R9: presupuesto mes 13 con segundo ingreso por parte del gobierno")

        self.model.addConstrs((I_t[t-1] - (quicksum(self.k_zt[z][t]*x_zt[z, t] + self.w_zt[z][1]*r_zt[z, t] + self.m_zt[z][t]*a_zt[z, t] + self.n_zt[z][t]*s_zt[z, t] + self.Cenc_zt[z][t]*enc_zt[z, t] + self.Capg_zt[z][t]*apg_zt[z, t] for z in self.Z)  + self.c_t[t]*u_t[t]) == I_t[t] for t in range(int(TOTAL_MESES/2) + 2, TOTAL_MESES + 1)),
                            name="R10: presupuesto meses 14 a final")

        self.model.addConstrs((I_t[t] >= 0 for t in self.T),
                            name="R11: presupuesto no puede ser negativo")

        self.model.addConstrs((y_t[t] <= self.V for t in self.T),
                            name="R12: no se puede superar la capcidad de almaceniamiento")

        self.model.addConstrs((b_zt[z, t] <= quicksum(r_zt[z, tau] for tau in range(1, t+1)) for z in self.Z for t in self.T),
                            name="R13: una subzona solamente se puede activar si ya se construyo la caneria que la conecta")

        self.model.addConstrs((s_zt[z, t] <= quicksum(r_zt[z, tau] for tau in range(1, t+1)) for z in self.Z for t in self.T),
                            name="R14: Asegura que una caneria puede estar activa solo si ya se ha instalado")

        self.model.addConstrs((p_zt[z, t] <= b_zt[z, t] for z in self.Z for t in self.T),
                            name="R15: solamente se puede recolectar si la zona esta activa")

        M = 100000000000000000
        self.model.addConstrs((a_zt[z, t] <= M*p_zt[z, t] for z in self.Z for t in self.T),
                            name="R16: solamente se puede recolectar si la zona esta activa")

        self.model.addConstrs((quicksum(r_zt[z, t] for t in self.T) <= 1 for z in self.Z),
                            name="R17: se puede instalar solo una caneria por zona")

        self.model.addConstrs((x_zt[z, t] <= M*quicksum(r_zt[z, tau] for tau in range(1, t+1)) for z in self.Z for t in self.T),
                            name="R18: debe existir una caneria antes de instalar cualquier cantidad de metros cuadrados en la zona z en t")

        self.model.addConstrs((p_zt[z, t] <= s_zt[z, t] for z in self.Z for t in self.T),
                            name="R19: si hay atrapanieblas activos, entonces la caneria de la zona debe estar activa")

        self.model.addConstrs((enc_zt[z, t] >= b_zt[z, t] - b_zt[z, t-1] for z in self.Z for t in range(2, TOTAL_MESES+1)),
                            name="R20")

        self.model.addConstrs((enc_zt[z, t] <= b_zt[z, t] for z in self.Z for t in range(2, TOTAL_MESES+1)),
                            name="R21")

        self.model.addConstrs((enc_zt[z, t] <= 1 - b_zt[z, t-1] for z in self.Z for t in range(2, TOTAL_MESES+1)),
                            name="R22")

        self.model.addConstrs((apg_zt[z, t] >= b_zt[z, t-1] - b_zt[z, t] for z in self.Z for t in range(2, TOTAL_MESES+1)),
                            name="R23")

        self.model.addConstrs((apg_zt[z, t] <= b_zt[z, t-1] for z in self.Z for t in range(2, TOTAL_MESES+1)),
                            name="R24")

        self.model.addConstrs((apg_zt[z, t] <= 1 - b_zt[z, t] for z in self.Z for t in range(2, TOTAL_MESES+1)),
                            name="R25")

        self.model.addConstrs((b_zt[z, 1] == 0 for z in self.Z),
                            name="R26")
                
        #######################
        self.model.setObjective(quicksum(a_zt[z,t]*self.q_zt[z][t] for z in self.Z for t in self.T ), GRB.MAXIMIZE)

    def optimizar(self):
        self.model.optimize()

        if self.model.status == GRB.INFEASIBLE:
            # Imprimir las restricciones que hacen que el modelo sea infactible
            print('El modelo es infactible')
            self.model.computeIIS()
            self.model.write('modelo.ilp')
            self.model.computeIIS()  # También detecta infeasibilidades
            self.model.write("model.lp")  # Puedes ver los coeficientes y escalas
            return None

        elif self.model.status == GRB.UNBOUNDED:
            print('El modelo es no acotado')
            return None

        elif self.model.status == GRB.INF_OR_UNBD:
            print('El modelo es infactible o no acotado')
            return None
        
        else:
            os.makedirs("resultados", exist_ok=True)

            # guardar vars con sus optimos
            with open("resultados/optimos.csv", "w") as f:
                f.write("variable,valor\n")
                for v in self.model.getVars():
                    f.write(f"{v.VarName},{v.X}\n")
                f.write(f"ObjVal,{self.model.ObjVal}\n")
            
            return self.model.ObjVal

        #else:
            #return self.model.ObjVal
   

def main():
    modelo_niebla = ModeloNiebla()
    modelo_niebla.cargarParametros()
    modelo_niebla.definirModelo()
    modelo_niebla.optimizar()
   

if __name__ == "__main__":
    main()
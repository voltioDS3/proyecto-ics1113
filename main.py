import pandas as pd
from gurobipy import GRB, quicksum
import gurobipy as gp
from os import path
import locale
BASE_DATOS = "./datos/output"
TOTAL_MESES = 24    
TOTAL_ZONAS = 10
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


        pass

    def cargarParametros(self):
        # TODO implementar funcion

        """
        Esta funcion debe extraer los parametros de los csv para asignar valores a los parametros
        """
        pass
    def definirModelo(self):
        
        a_zt = self.model.addVars(self.Z, self.T,lb=0.0,
                                  vtype=GRB.CONTINUOUS, name="a_zt")
        
        p_zt = self.model.addVars(self.Z, self.T,
                                  vtype=GRB.BINARY, name="p_zt")
        
        x_zt = self.model.addVars(self.Z, self.T,lb=0.0,
                                  vtype=GRB.CONTINUOUS, name="x_zt")
        
        b_zt = self.model.addVars(self.Z, self.T,
                                  vtype=GRB.BINARY, name="b_zt")
        
        r_zt = self.model.addVars(self.Z, self.T,
                                  vtype=GRB.BINARY, name="r_zt")
        
        s_zt = self.model.addVars(self.Z, self.T,
                                  vtype=GRB.BINARY, name="s_zt")
        
        y_t = self.model.addVars(self.T,lb=0.0,
                                  vtype=GRB.CONTINUOUS, name="y_t")
        
        u_t = self.model.addVars(self.T,lb=0.0,
                                  vtype=GRB.CONTINUOUS, name="u_t")
        
        I_t = self.model.addVars(self.T,lb=0.0,
                                  vtype=GRB.CONTINUOUS, name="I_t")
        
        enc_zt = self.model.addVars(self.Z, self.T,
                                  vtype=GRB.BINARY, name="enc_zt")
        
        apg_zt = self.model.addVars(self.Z, self.T,
                                  vtype=GRB.BINARY, name="apg_zt")
        
        self.model.update()

        #### RESTRICCIONES ####
        # TODO implementar restricciones
        #######################
        q_zt = [[1,1,1] [2,2,2]] # TODO IMPLEMENTAR EN PARAMETROS
        self.model.setObjective(quicksum(a_zt[z][t]*q_zt[z][t] for z in self.Z for t in self.T ), GRB.MAXIMIZE)

    def optimizar(self):
        self.model.optimize()

        if self.model.status == GRB.INFEASIBLE:
            # Imprimir las restricciones que hacen que el modelo sea infactible
            print('El modelo es infactible')
            self.model.computeIIS()
            self.model.write('modelo.ilp')
            return None

        elif self.model.status == GRB.UNBOUNDED:
            print('El modelo es no acotado')
            return None

        elif self.model.status == GRB.INF_OR_UNBD:
            print('El modelo es infactible o no acotado')
            return None

        else:
            return self.ObjVal

        pass

def main():
    modelo_niebla = ModeloNiebla()
    modelo_niebla.cargarParametros()
    modelo_niebla.definirModelo()
    modelo_niebla.optimizar()

if __name__ == "__main__":
    main()
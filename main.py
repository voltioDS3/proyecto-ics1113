import pandas as pd
from gurobipy import GRB, quicksum
import gurobipy as gp
from os import path
import locale
BASE_DATOS = "./datos"
class Modelo:

    def __init__(self):
        self.T = range(1,24)
        self.Z = range(1,10) #de la zona 1 a la zona 5 son zona sur, de la 6 hasta la 10 zona norte
        self.model = gp.Model() # modelo

        ruta_archivos = {
            'q_zt': path.join('parametros', 'capacidad_carga.csv'),
            'costo_almacenamiento': path.join('parametros', 'costo_almacenamiento.csv'),
            'cargadores_existentes': path.join('parametros', 'cargadores_existentes.csv'),
            'costo_compra': path.join('parametros', 'costo_compra.csv'),
            'costo_instalacion_electrica': path.join('parametros', 'costo_instalacion_electrica.csv'),
            'infraestructura_existente': path.join('parametros', 'infraestructura_existente.csv'),
            'alpha': path.join('parametros', 'alpha.csv'),
            'delta': path.join('parametros', 'delta.csv'),
            'K': path.join('parametros', 'K.csv'),
            'AM': path.join('parametros', 'AM.csv'),
            'd_ij': path.join('parametros', 'distance.csv')
        }
        pass

    def cargarParametros(self):

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
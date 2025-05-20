import pandas as pd
from gurobipy import GRB, quicksum
import gurobipy as gp
from os import path
import locale

class Modelo:

    def __init__(self):
        self.T = range(1,24)
        self.Z = range(1,10) #de la zona 1 a la zona 5 son zona sur, de la 6 hasta la 10 zona norte
        self.model = gp.Model() # modelo
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
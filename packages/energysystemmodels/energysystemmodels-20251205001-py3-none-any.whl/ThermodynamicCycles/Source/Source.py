from ThermodynamicCycles.FluidPort.FluidPort import FluidPort
from CoolProp.CoolProp import PropsSI
import pandas as pd 
from datetime import datetime

class Object:
    def __init__(self):
        self.Timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #Input and Output Connector
       # self.Inlet=FluidPort() 
        self.Outlet=FluidPort()

        #Input Data
        self.fluid=None #"air"
        self.Ti_degC=None #15 #♣°C
        self.Pi_bar=None #1.01325
        self.F=None
        
        # Callback pour adapter le débit au réseau en aval
        self.Outlet.callback = self.on_flow_change
        
        #(ISO 2533) : 288.15K (15°C) / 1.01325 bar
        self.F_Sm3s=None
        self.F_Sm3h=None


        self.F_m3s=None
        
        self.F_m3h=None
        self.F_kgh=None

        # (DIN 1343) : 273.15K (0°C) / 1.01325 bar
        self.F_Nm3s=None
        self.F_Nm3h=None

     
        
        

        #Initial Values
        
        
        self.Q=0
        self.fluid_quality="liquid"
        self.df = pd.DataFrame()
    
    def on_flow_change(self):
        """
        Callback appelé lorsque self.Outlet.F change (débit demandé par le réseau en aval).
        Adapte automatiquement le débit de la source pour correspondre au réseau.
        """
        if hasattr(self, '_calculating'):
            return  # Éviter les boucles infinies pendant le calcul
        
        # Si le débit de sortie a changé (imposé par la pompe en aval), adapter
        if self.Outlet.F is not None and self.Outlet.F != self.F:
            print(f"🔄 SOURCE CALLBACK: Adaptation débit: {self.F:.3f} → {self.Outlet.F:.3f} kg/s")
            self._calculating_inverse = True
            try:
                self.F = self.Outlet.F
                # Recalculer les débits volumiques avec le nouveau débit massique
                if self.Pi_bar is not None and self.Ti_degC is not None and self.fluid is not None:
                    rho = PropsSI("D", "P", 100000*self.Pi_bar, "T", (self.Ti_degC+273.15), self.fluid)
                    self.F_m3h = self.F * 3600 / rho
                    print(f"   Nouveau débit volumique: {self.F_m3h:.2f} m³/h")
            finally:
                if hasattr(self, '_calculating_inverse'):
                    delattr(self, '_calculating_inverse')
       
    
        
    def calculate (self):
        # Marquer le début du calcul pour éviter les callbacks récursifs
        self._calculating = True
        
        try:
            if self.F_Sm3h is not None:
                self.F=self.F_Sm3h/3600*PropsSI("D", "P", 100000*1.01325, "T", (15+273.15), self.fluid)

            if self.F_Nm3h is not None:
                self.F=self.F_Nm3h/3600*PropsSI("D", "P", 100000*1.01325, "T", (0+273.15), self.fluid)
        
            if self.F_m3s is not None:
                self.F=self.F_m3s*PropsSI("D", "P", 100000*self.Pi_bar, "T", (self.Ti_degC+273.15), self.fluid)

            if self.F_m3h is not None:
                self.F=self.F_m3h/3600*PropsSI("D", "P", 100000*self.Pi_bar, "T", (self.Ti_degC+273.15), self.fluid)

            if self.F_kgh is not None:
                self.F=self.F_kgh/3600
        
            if self.F_Sm3s is not None:
                self.F=self.F_Sm3s*PropsSI("D", "P", 100000*1.01325, "T", (15+273.15), self.fluid)
        


            if self.F_Nm3s is not None:
                self.F=self.F_Nm3s*PropsSI("D", "P", 100000*1.01325, "T", (0+273.15), self.fluid)

            #print("self.F",self.F)
            if self.F is None:
                self.F=0


            self.Outlet.fluid=self.fluid
            
            # Temporairement désactiver le callback pendant la mise à jour
            temp_callback = self.Outlet.callback
            self.Outlet.callback = None
            
            self.Outlet.F=self.F
            self.Outlet.P=self.Pi_bar*100000
            
            # Réactiver le callback
            self.Outlet.callback = temp_callback

            #Inlet temperature calculation
            self.Outlet.h=PropsSI('H','P',self.Outlet.P,'T',self.Ti_degC+273.15,self.fluid)
            #print("sink h",self.Outlet.h)
            #calcul de l'état du fluid
            try:
                self.Ti_degC=PropsSI("T", "P", 100000*self.Pi_bar, "H", self.Outlet.h,self.fluid)-273.15
            except:
                self.Ti_degC=0-273.15

            try:
                pressure_critical = PropsSI("Pcrit", self.fluid)
                #print(pressure_critical)
            except:
                pass


            if (100000*self.Pi_bar)<PropsSI("Pcrit",self.fluid): #comparer à la pression critique
                Hv=PropsSI("H", "P", 100000*self.Pi_bar, "Q", 1, self.fluid)
               # print("Hv=",Hv)
                Hl=PropsSI("H", "P", 100000*self.Pi_bar, "Q", 0, self.fluid)
              #  print("Hl=",Hl)
                self.Q=1-((Hv-self.Outlet.h)/(Hv-Hl))
            
                if self.Q>=1:
                   # print(self.fluid+" vapeur"+"%.2f" % self.Q) #"%d" % 
                    self.fluid_quality="vapor"
                elif (self.Q<1 and self.Q>0):
                   # print(self.fluid+" diphasique"+"%.2f" % self.Q) #"%d" % 
                    self.fluid_quality="two-phase"
                else:
                    #print(self.fluid+" liquide"+"%.2f" % self.Q) #"%d" % 
                    self.fluid_quality="liquid"
               # print("Qualité=",self.Q)
            
            else:
                #print(self.fluid+" supercritique") #"%d" % 
                self.fluid_quality="supercritical"
            
         
            if (100000*self.Pi_bar)<PropsSI("Pcrit",self.fluid): #comparer à la pression critique
                if self.Q>1:
                    self.F_m3s=self.Outlet.F/PropsSI("D", "P", 100000*self.Pi_bar, "T", (self.Ti_degC+273.15), self.fluid)
                elif (self.Q<=1 and self.Q>=0):
                    self.F_m3s=self.Q*self.Outlet.F/PropsSI("D", "P", 100000*self.Pi_bar, "Q", 1, self.fluid)+(1-self.Q)*self.Outlet.F/PropsSI("D", "P", 100000*self.Pi_bar, "Q", 0, self.fluid)
                else:
                    self.F_m3s=self.Outlet.F/PropsSI("D", "P", 100000*self.Pi_bar, "T", (self.Ti_degC+273.15), self.fluid)        
            else:    
                self.F_m3s=self.Outlet.F/PropsSI("D", "P", 100000*self.Pi_bar, "T", (self.Ti_degC+273.15), self.fluid)
        
            self.F_Sm3s=self.Outlet.F/PropsSI("D", "P", 100000*1.01325, "T", (15+273.15), self.fluid)
            try:
                self.F_Nm3s=self.Outlet.F/PropsSI("D", "P", 100000*1.01325, "T", (0+273.15), self.fluid)
                self.F_Nm3h=self.F_Nm3s*3600
            except:
                self.F_Nm3s=None
                self.F_Nm3h=None


            self.F_Sm3h=self.F_Sm3s*3600
        

            self.F_m3h=self.F_m3s*3600
            self.F_kgh=self.Outlet.F*3600


            self.Outlet.calculate_properties()

            self.df = pd.DataFrame({'Source': [self.Timestamp,self.Outlet.fluid,round(self.Ti_degC,1),round(self.Pi_bar,2),round(self.F_Sm3h,1),self.F_Nm3h,round(self.F_m3h,1),round(self.F_kgh,3),round(self.F,3),round(self.F_m3s,3),round(self.F_Sm3s,3),self.Outlet.h], },
                      index = ['Timestamp','fluid','Ti_degC','Pi_bar','F_Sm3h','F_Nm3h','F_m3h', 'F_kgh','F_kgs','F_m3s','F_Sm3s','self.Outlet.h'])

            #réinitialiser les débits
            self.F_Sm3s=None
            self.F_Nm3s=None

            self.F_m3s=None
            self.F_Sm3h=None
            self.F_Nm3h=None
            self.F_m3h=None
            self.F_kgh=None
        
        finally:
            # Retirer le flag de calcul
            if hasattr(self, '_calculating'):
                delattr(self, '_calculating')
        
 

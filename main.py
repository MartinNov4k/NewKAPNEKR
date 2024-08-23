import math

class Krizovatka:
    def __init__(self, name, branch_count, speed ):
        self.name = name
        self.branch_count = branch_count
        self.speed = speed #rychlost na hlavni
        self.UKD_hlavni = None
        self.UKD_vedlejsi = None

        self.vjezdy = []
        self.lines = []
    
    

class Vjezd:
    def __init__(self, krizovatka, name, rule, orientace, rule_type=None):
        self.name = name
        self.rule = rule # hlavni / vedlejsi
        self.rule_type = rule_type # P4 P6
        self.krizovatka = krizovatka
        self.orientace = orientace
        self.volume = None #doplnit
        self.capacity = None 
        self.reserve = None 
        self.que_lenght = None
        self.delay = None
        self.stop_count = None
        self.ukd = None
        
        self.lines = []
        krizovatka.vjezdy.append(self)  #přidání do listu vjezdů u Křižovatky
        

class Pohyb:
    def __init__(self, smer, pocet_pruhu, intenzita, vjezd, krizovatka):
        vjezd.lines.append(self) 
        krizovatka.lines.append(self)
        
        self.vjezd = vjezd # kam patří
        self.kriz = krizovatka
        self.smer = smer # L S R left straight right
        self.pocet_pruhu = pocet_pruhu
        self.intenzita = intenzita
        self.rule = vjezd.rule
        self.rule_type = vjezd.rule_type
        self.druh = self.smer + "_" + self.rule # druh dopravního proudu  napr. "leve obcoeni z vedeljsi"
        
        
        self.cislo_proudu = self.urci_cislo_proudu()
        self.p0 = None # pravděpodobnost nevzdutí nadřazených
        self.stupen_podrazenosti = self.urci_stupen_podrazenosti()
        self.Tg = self.urceni_Tg() # kritický časový odstup
        self.Tf = self.urceni_Tf() # následný časový odstup
        self.intenzita_nadrazenych = self.vypocet_nadrazenych_I()
        #self.G = self.vypocet_G()
        #self.C = self.urci_C()
    
        
        
        
        
    def vypocet_G(self):
        G = (3600 / self.Tf ) * math.exp (-self.intenzita_nadrazenych /3600)*(self.Tg - (self.Tf /2))
        return G
    
    def urceni_Tg(self):
        Tg= None
        if  self.vjezd.krizovatka.speed == 50:
            if self.druh == "L_hlavni":
                Tg = 4.5
            elif self.druh == "R_vedlejsi":
                Tg = 4.7
            elif self.druh == "S_vedlejsi":
                Tg = 6.2
            elif self.druh == "L_vedlejsi":
                Tg = 6.3
            
            
        else:
            print("pro zadanou rychlost není výpočet k dispozici")    
            exit()
        return Tg
    def urceni_Tf(self):
        Tf= None
        if self.druh == "L_hlavni":
                Tf = 2.6
        if self.rule_type == "P4":

            if self.druh == "R_vedlesji":
                Tf = 3.1
            elif self.druh == "S_vedlesji":
                Tf = 3.3
            elif self.druh == "L_vedlejsi":
                Tf = 3.5
             
            
        
        elif self.rule_type == "P6":
    
            if self.druh == "R_vedlesji":
                Tf = 3.7
            elif self.druh == "S_vedlesji":
                Tf = 3.9
            if self.druh == "L_vedlejsi":
                Tf = 4.1
            
        
        return Tf
    
    def urci_stupen_podrazenosti(self):
        if self.vjezd.rule == "hlavni":
            if self.smer == "S" or self.smer == "R":
                stupen = 1
            elif self.smer == "L":
                stupen = 2
        elif self.vjezd.rule == "vedlejsi":
            if self.vjezd.krizovatka.branch_count == 4:
                if self.smer == "S":
                    stupen = 3
                if self.smer == "R":
                    stupen = 2
                if self.smer == "L":
                    stupen = 4
            if self.vjezd.krizovatka.branch_count == 3:
                if self.smer == "R":
                    stupen = 2
                if self.smer == "L":
                    stupen = 3
        return stupen   
    def urci_cislo_proudu(self):
        if self.vjezd.orientace == 1:
            if self.smer == "L":
                cislo_proudu = 1
            if self.smer == "S":
                cislo_proudu = 2
            if self.smer == "R":
                cislo_proudu = 3
                
        elif self.vjezd.orientace == 2:
            if self.smer == "L":
                cislo_proudu = 10
            if self.smer == "S":
                cislo_proudu = 11
            if self.smer == "R":
                cislo_proudu = 12
                
        elif self.vjezd.orientace == 3:
            if self.smer == "L":
                cislo_proudu = 7
            if self.smer == "S":
                cislo_proudu = 8
            if self.smer == "R":
                cislo_proudu = 9
                
        elif self.vjezd.orientace == 4:
            if self.smer == "L":
                cislo_proudu = 4
            if self.smer == "S":
                cislo_proudu = 5
            if self.smer == "R":
                cislo_proudu = 6
        return cislo_proudu
    
    def urci_C(self):
        if self.stupen_podrazenosti == 1:
            C = 1800 * self.pocet_pruhu
        elif self.stupen_podrazenosti == 2:
            C = self.G
        return C

    def vypocet_nadrazenych_I(self):
        if self.stupen_podrazenosti == 1:
            I_nadrazene = 0
        else :
            if self.cislo_proudu == 1:
                I_nadrazene = I_phb(self.kriz, 8) + I_phb(self.kriz, 9)
            elif self.cislo_proudu == 7:
                I_nadrazene = I_phb(self.kriz, 2) + I_phb(self.kriz, 3)
            elif self.cislo_proudu == 6:
                I_nadrazene = I_phb(self.kriz, 2) + 0.5 * I_phb(self.kriz, 3)
            elif self.cislo_proudu == 12:
                I_nadrazene = I_phb(self.kriz, 8) + 0.5 * I_phb(self.kriz, 9)
            elif self.cislo_proudu == 5:
                I_nadrazene = ( I_phb(self.kriz, 2) + 0.5 * I_phb(self.kriz, 3) + I_phb(self.kriz, 8) 
                               + I_phb(self.kriz, 9) + I_phb(self.kriz, 1) + I_phb(self.kriz, 7)
                )
            elif self.cislo_proudu == 11:
                I_nadrazene =( I_phb(self.kriz, 8) + 0.5 * I_phb(self.kriz, 9)
                + I_phb(self.kriz, 2) + I_phb(self.kriz, 3) + I_phb(self.kriz, 1) + I_phb(self.kriz, 7)   
                )
            elif self.cislo_proudu == 4:
                I_nadrazene =( I_phb(self.kriz, 2) + 0.5 * I_phb(self.kriz, 3)
                + I_phb(self.kriz, 8) +  0.5 * I_phb(self.kriz, 9) + I_phb(self.kriz, 1) + I_phb(self.kriz, 7) 
                + I_phb(self.kriz, 12)  + I_phb(self.kriz, 11)   
                )   
            elif self.cislo_proudu == 10:
                I_nadrazene =( I_phb(self.kriz, 8) + 0.5 * I_phb(self.kriz, 9)
                + I_phb(self.kriz, 2) +  0.5 * I_phb(self.kriz,3) + I_phb(self.kriz, 1) + I_phb(self.kriz, 7) 
                + I_phb(self.kriz, 6)  + I_phb(self.kriz, 5)   
                ) 
        return I_nadrazene
                
                
def show_all_pohyby(krizovatka):
    for pohyb in krizovatka.lines:
        print(pohyb.cislo_proudu, pohyb.smer, pohyb.intenzita, "vjezd:", pohyb.vjezd.name)
        
def I_phb(kritovatka, cislo):
    for proud in kritovatka.lines:
        if proud.cislo_proudu == cislo:
            hledana_intenzita = proud.intenzita
    return hledana_intenzita
       
### použití pokusné ###############################################################

cross1= Krizovatka("Dablicka x Bestakova", 4, 50)

vjezd1 = Vjezd(cross1, "Zapad", "hlavni", 1 )
vjezd2 = Vjezd (cross1,"Sever", "vedlejsi", 2, "P4")
vjezd3 = Vjezd (cross1,"Východ", "vedlejsi", 3)
vjezd4 = Vjezd (cross1,"Jih", "vedlejsi", 4, "P4")

pohyb1 = Pohyb("L", 1, 200, vjezd1 ,cross1)
pohyb2= Pohyb("S", 1, 500, vjezd1,cross1)
pohyb3= Pohyb("R", 1, 400, vjezd1,cross1)

pohyb4 = Pohyb("L", 1, 200, vjezd2,cross1)
pohyb5= Pohyb("S", 1, 500, vjezd2,cross1)
pohyb6= Pohyb("R", 1, 400, vjezd2,cross1)

pohyb7 = Pohyb("L", 1, 200, vjezd3,cross1)
pohyb8= Pohyb("S", 1, 500, vjezd3,cross1)
pohyb9= Pohyb("R", 1, 400, vjezd3,cross1)

pohyb10 = Pohyb("L", 1, 200, vjezd4,cross1)
pohyb11= Pohyb("S", 1, 500, vjezd4,cross1)
pohyb12= Pohyb("R", 1, 400, vjezd4,cross1)

""" print(pohyb1.Tf)
print(pohyb1.Tg)

print(pohyb1.smer)
print(pohyb1.druh)
print(vjezd1.orientace)
print(pohyb1.vjezd.name)
print(pohyb1.vjezd.krizovatka.name)

print(cross1.branch_count)

print(vjezd2.rule_type)

print(pohyb1.stupen_podrazenosti)

print(pohyb1.cislo_proudu)

 """
""" print(pohyb12.cislo_proudu)
print(pohyb6.cislo_proudu) """

show_all_pohyby(cross1)
print(I_phb(cross1, 1))
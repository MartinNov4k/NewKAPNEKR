import math

class Krizovatka:
    def __init__(self, name, branch_count, speed ):
        self.name = name
        self.branch_count = branch_count
        self.speed = speed #rychlost na hlavni
        self.UKD_hlavni = None
        self.UKD_vedlejsi = None

        self.vjezdy = []

class Vjezd:
    def __init__(self, name, rule, rule_type, krizovatka):
        self.name = name
        self.rule = rule # hlavni / vedlejsi
        self.rule_type = rule_type # P4 P6
        self.krizovatka = krizovatka
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
    def __init__(self, smer, pocet_pruhu, intenzita, vjezd):
        self.vjezd = vjezd # kam patří
        self.smer = smer # L S R left straight right
        self.pocet_pruhu = pocet_pruhu
        self.intenzita = intenzita
        self.C = None
        #self.G = self.vypocet_G()
        self.intenzita_nadrazenych = None
        self.p0 = None # pravděpodobnost nevzdutí nadřazených
        self.stupen_podrazenosti = None
        
        self.rule = vjezd.rule
        self.rule_type = vjezd.rule_type
        self.druh = self.smer + "_" + self.rule # druh dopravního proudu  napr. "leve obcoeni z vedeljsi"
        
        self.Tg = self.urceni_Tg() # kritický časový odstup
        self.Tf = self.urceni_Tf() # následný časový odstup
        vjezd.lines.append(self) 
        
    def vypocet_G(self):
        G = (3600 / self.Tf ) * math.exp (-self.intenzita_nadrazenych /3600)*(self.Tg - (self.Tf /2))
        return G
    
    def urceni_Tg(self):
        Tg= None
        if  self.vjezd.krizovatka.speed == 50:
            if self.druh == "L_hlavni":
                Tg = 4.5
            elif self.druh == "R_vedlesji":
                Tg = 4.7
            elif self.druh == "S_vedlesji":
                Tg = 6.2
            elif self.druh == "L_vedlejsi":
                Tg = 6.3
            else:
                print("chyba v druhu")  
            
        else:
            print("pro zadanou rychlost není výpočet k dispozici")    
            exit()
        return Tg
    def urceni_Tf(self):
        Tf= None
        if self.rule_type == "P4":
            if self.druh == "L_hlavni":
                Tf = 2.6
            elif self.druh == "R_vedlesji":
                Tf = 3.1
            elif self.druh == "S_vedlesji":
                Tf = 3.3
            elif self.druh == "L_vedlejsi":
                Tf = 3.5
            else:
                print(f"chyba v druhu u Tf_ {self.druh}")  
            
        
        elif self.rule_type == "P6":
            if self.druh == "L_hlavni":
                Tf = 2.6
            elif self.druh == "R_vedlesji":
                Tf = 3.7
            elif self.druh == "S_vedlesji":
                Tf = 3.9
            if self.druh == "L_vedlejsi":
                Tf = 4.1
            else:
                print(f"chyba v druhu u Tg_ {self.druh}")
        else: 
            print ("U TF je chyba v ruletype")
        return Tf
### použití pokusné

cross1= Krizovatka("Dablicka x Bestakova", 3, 50)

vjezd1 = Vjezd("Dablická", "hlavni", "P4", cross1)

pohyb1 = Pohyb("L", 1, 700, vjezd1)

print(pohyb1.Tf)
print(pohyb1.Tg)

print(pohyb1.smer)
print(pohyb1.druh)
print(pohyb1.vjezd.name)
print(pohyb1.vjezd.krizovatka.name)

print(cross1.branch_count)
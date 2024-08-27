import math

class Pohyb:
    def __init__(self, smer, pocet_pruhu, intenzita_VSE,intenzita_PV, vjezd, krizovatka):
        
        vjezd.lines.append(self) 
        krizovatka.lines.append(self)

        # primo zadane
        self.vjezd = vjezd # kam patří
        self.kriz = krizovatka
        self.smer = smer # L S R left straight right
        self.pocet_pruhu = pocet_pruhu
        self.intenzita = intenzita_VSE  #intenzita šechna vozidla
        self.intenzita_PV = intenzita_PV # nakladni vozidla 

        # prevzate
        self.rule = vjezd.rule
        self.rule_type = vjezd.rule_type

        # hned pocitne
        self.zohlednena_skladba = (self.intenzita - self.intenzita_PV) + 1.5 * self.intenzita_PV
        self.druh = self.smer + "_" + self.rule # druh dopravního proudu  napr. "leve obcoeni z vedeljsi"
        self.cislo_proudu = self.urci_cislo_proudu()
        self.Tg = self.urceni_Tg() # kritický časový odstup
        self.Tf = self.urceni_Tf() # následný časový odstup
        self.stupen_podrazenosti = self.urci_stupen_podrazenosti()

        # pozdeji pocitane _ zavisle 

        self._intenzita_nadrazenych = None
        self._G = None
        self._C = None
        self._av = None # stupen vytížení
        self._p = None # pravděpodobnost nevzdutí nadřazených
        self._L95 = None # delka fronty 95% casu   

    #lazy evaluation
    @property
    def intenzita_nadrazenych(self):
        if self._intenzita_nadrazenych is None:
            self._intenzita_nadrazenych = self.vypocet_nadrazenych_I()
        return self._intenzita_nadrazenych

    @property
    def G(self):
        if self.stupen_podrazenosti == 1:
            self._G = None
        else:
            if self._G is None:
                self._G = round(self.vypocet_G())
        return self._G

    @property
    def C(self):
        if self._C is None:
            self._C = self.urci_C()
        return self._C

    @property
    def av(self):
        if self._av is None:
            if self.C:
                self._av = self.zohlednena_skladba / self.C
        return self._av
    
    @property
    def p(self):
        if self._p is None:
            if self.C:
                p = 1 - self.av
                if p > 0 :
                    self._p = p
                else:
                    self._p = 0
                
        return self._p
    
    def vypocet_G(self):
        G = (3600 / self.Tf) * math.exp(-self.intenzita_nadrazenych / 3600 * (self.Tg - self.Tf / 2))
        return G
    
    def urceni_Tg(self):
        Tg= None
        V_85 =self.vjezd.krizovatka.speed # nejvyssi dovolena rychlost na hlavni
        if self.druh == "L_hlavni":
                Tg = 3.4 + 0.021 * V_85
        elif self.druh == "R_vedlejsi":
                Tg = 2.8 + 0.038 * V_85
        elif self.druh == "S_vedlejsi":
                Tg = 4.4 + 0.036 * V_85
        elif self.druh == "L_vedlejsi":
                Tg = 5.2 + 0.022 *V_85
            
       
        return Tg
    
    def urceni_Tf(self):
        Tf= None
        if self.druh == "L_hlavni":
                Tf = 2.6
        if self.rule_type == "P4":

            if self.druh == "R_vedlejsi":
                Tf = 3.1
            elif self.druh == "S_vedlejsi":
                Tf = 3.3        
            elif self.druh == "L_vedlejsi":
                Tf = 3.5
             
            
        
        elif self.rule_type == "P6":
    
            if self.druh == "R_vedlejsi":
                Tf = 3.7
            elif self.druh == "S_vedlejsi":
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
            
        elif self.stupen_podrazenosti == 3: # C5 C11
                C = Pohyb.P_phb(self.kriz, 1) * Pohyb.P_phb(self.kriz, 7) * self.G
                
        elif self.stupen_podrazenosti == 4 : #C4 #C10
            
            if self.cislo_proudu == 4:
                px = Pohyb.P_phb(self.kriz, 1) * Pohyb.P_phb(self.kriz, 7)
                p11 = Pohyb.P_phb(self.kriz, 11)
                C = self.G * Pohyb.P_phb(self.kriz, 12) * (1 / (1 + ((1- px) / px) + ((1 - p11)/p11) ))
                
            if self.cislo_proudu == 10:
                px = Pohyb.P_phb(self.kriz, 1) * Pohyb.P_phb(self.kriz, 7)
                p5 = Pohyb.P_phb(self.kriz, 5)
                C = self.G * Pohyb.P_phb(self.kriz, 12) * (1 / (1 + ((1- px) / px) + ((1 - p5)/p5) ))
                
        return C

    def vypocet_nadrazenych_I(self):
        if self.stupen_podrazenosti == 1:
            I_nadrazene = 0
        else :
            if self.cislo_proudu == 1:
                I_nadrazene = Pohyb.I_phb(self.kriz, 8) + Pohyb.I_phb(self.kriz, 9)
            elif self.cislo_proudu == 7:
                I_nadrazene = Pohyb.I_phb(self.kriz, 2) + Pohyb.I_phb(self.kriz, 3)
            elif self.cislo_proudu == 6:
                I_nadrazene = Pohyb.I_phb(self.kriz, 2) + 0.5 * Pohyb.I_phb(self.kriz, 3)
            elif self.cislo_proudu == 12:
                I_nadrazene = Pohyb.I_phb(self.kriz, 8) + 0.5 * Pohyb.I_phb(self.kriz, 9)
            elif self.cislo_proudu == 5:
                I_nadrazene = ( Pohyb.I_phb(self.kriz, 2) + 0.5 * Pohyb.I_phb(self.kriz, 3) + Pohyb.I_phb(self.kriz, 8) 
                               + Pohyb.I_phb(self.kriz, 9) + Pohyb.I_phb(self.kriz, 1) + Pohyb.I_phb(self.kriz, 7)
                )
            elif self.cislo_proudu == 11:
                I_nadrazene =( Pohyb.I_phb(self.kriz, 8) + 0.5 * Pohyb.I_phb(self.kriz, 9)
                + Pohyb.I_phb(self.kriz, 2) + Pohyb.I_phb(self.kriz, 3) + Pohyb.I_phb(self.kriz, 1) + Pohyb.I_phb(self.kriz, 7)   
                )
            elif self.cislo_proudu == 4:
                I_nadrazene =( Pohyb.I_phb(self.kriz, 2) + 0.5 * Pohyb.I_phb(self.kriz, 3)
                + Pohyb.I_phb(self.kriz, 8) +  0.5 * Pohyb.I_phb(self.kriz, 9) + Pohyb.I_phb(self.kriz, 1) + Pohyb.I_phb(self.kriz, 7) 
                + Pohyb.I_phb(self.kriz, 12)  + Pohyb.I_phb(self.kriz, 11)   
                )   
            elif self.cislo_proudu == 10:
                I_nadrazene =( Pohyb.I_phb(self.kriz, 8) + 0.5 * Pohyb.I_phb(self.kriz, 9)
                + Pohyb.I_phb(self.kriz, 2) +  0.5 * Pohyb.I_phb(self.kriz,3) + Pohyb.I_phb(self.kriz, 1) + Pohyb.I_phb(self.kriz, 7) 
                + Pohyb.I_phb(self.kriz, 6)  + Pohyb.I_phb(self.kriz, 5)   
                ) 
        return I_nadrazene
    
    @staticmethod
    def I_phb(kritovatka, cislo):
        for proud in kritovatka.lines:
            if proud.cislo_proudu == cislo:
                hledana_intenzita = proud.intenzita
        return hledana_intenzita
       
    @staticmethod
    def P_phb(kritovatka, cislo):
        for proud in kritovatka.lines:
            if proud.cislo_proudu == cislo:
                hledane_p = proud.p
        return hledane_p
    
    def vypis_vlastnosti(self):
        print("--")
        print(self.cislo_proudu)
        print(f"Vjezd: {self.vjezd.name}") # tady by se asi nemělo odkazovat na atribut z jine class
        print(f"Směr: {self.smer}")
        print(f"Přednost: {self.rule}")
        print(f"stupen podrazenosti {self.stupen_podrazenosti}")
        print(f"I nadrazenych {self.intenzita_nadrazenych}")
        print(f"pvoz {self.zohlednena_skladba}")
        print (f"G: {self.G}")
        
        print(f"av: {self.av}")
        print(f"p: {self.p}")
        print(f"C: {self.C}")
        print("--")
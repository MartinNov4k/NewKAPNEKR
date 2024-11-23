import math
from Pruh import Pruh
class Pohyb:
    def __init__(self, smer, intenzita_OA, intenzita_PV,intenzita_NAV, intenzita_M, intenzita_Cyklo, vjezd, krizovatka, id, pocet_pruhu, delka_pruhu_nebo_roszireni=None):
        
        vjezd.lines.append(self) 
        krizovatka.lines.append(self)

        # primo zadane
        self.vjezd = vjezd # kam patří
        self.kriz = krizovatka
        self.smer = smer # L S R left straight right
        self.pocet_pruhu = pocet_pruhu
        self.intenzita_OA = intenzita_OA  #intenzita OA
        self.intenzita_PV = intenzita_PV # nakladni vozidla 
        self.intenzita_NAV = intenzita_NAV # návěsy a kloubáky
        self.intenzita_M = intenzita_M # motorky
        self.intenzita_Cyklo = intenzita_Cyklo # cyklisti
        self.id = id # pořádí /id pruhu v rámci vjezdu (paprsku)
        self.delka_JP = delka_pruhu_nebo_roszireni

        # prevzate
        self.rule = vjezd.rule
        self.rule_type = vjezd.rule_type

        # hned pocitne
        self.zohlednena_skladba = self.zohlednena_skladba_count()
        self.intenzita = self.intenzita_OA +self. intenzita_PV + self.intenzita_NAV + self.intenzita_M + self.intenzita_Cyklo
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
        self._tw = None # střední doba zdržení
        self._spolecny_pruh = None #list cisel proudu ve společném pruhu -- asi zbytečné při refaktoru vhodně nahradit
        self._spolecny_pruh_instances = None # list instancí společných pruhů
        self._spolecny_pruh = None #list cisel proudu ve společném pruhu -- asi zbytečné při refaktoru vhodně nahradit
        self._spolecny_pruh_instances = None # list instancí společných pruhů
        self._C_spolecna = None #kapacita spolecneho pruhu
        self._rezerva = None # rezerva kapacity

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
            self._C = round(self.urci_C())
        return self._C

    @property


    def av(self):
        if self._av is None:
            if self.C:
                self._av = round(self.zohlednena_skladba / self.C , 2)
        return self._av
    
    @property
    def p(self):
        if self._p is None:
            if self.C:
                if self.cislo_proudu == 1:
                    if self.spolecny_pruh_instances:               #pruh není samostatný
                        av2 = Pohyb.find_pohyb(self.kriz, 2).av
                        av3 = Pohyb.find_pohyb(self.kriz, 3).av
                        p = max (0, 1 - (self.av / (1- av2 - av3 )))  #vzorec 6-14 "protože 1,7 nejsou samostatne)"
                        self._p = p
                        
                    else:              # je to samostatný pruh
                        if self.L95 < self.delka_JP: 
                            self._p = round(max(0, 1 - self.av),2) # vzorec 6-3
                        else: # delka kolony je větší než délka JP
                            print(f"L95> delka. JP {self.cislo_proudu}")

                            self._p =self.p_6_14_count(1,2,3)                                      
                            
                            
                    
                elif self.cislo_proudu == 7: 
                    if self.spolecny_pruh_instances:
                        av8 = Pohyb.find_pohyb(self.kriz, 8).av
                        if self.vjezd.krizovatka.branch_count == 4:
                            av9 = Pohyb.find_pohyb(self.kriz, 9).av
                        else:
                            av9 = 0
                        p = max (0, 1 - (self.av / (1- av8 - av9 )))
                        self._p = p
                        
                    else:
                        if self.L95 < self.delka_JP: 
                            self._p = round(max(0, 1 - self.av),2) # vzorec 6-3
                        else: # delka kolony je větší než délka JP
                            print(f"L95> delka. JP {self.cislo_proudu}")
                            
                            self._p =self.p_6_14_count(7,8,9) 
                            
                
                else:
                    p = round(1 - self.av, 2)  # vzorec 6-3
                    if p > 0 :
                        self._p = p
                    else:
                        self._p = 0
                
        return self._p
    
    @property
    def L95(self):
        if self._L95 is None:
            if self.C:
                self._L95 = round((3/2) * self.C * (self.av - 1 + math.sqrt((1 - self.av)**2 + 3 * (8 * self.av) / self.C)))
        return self._L95
    
    @property
    def spolecny_pruh(self):
        if self._spolecny_pruh is None:
            self._spolecny_pruh = self.spolecny_pruh_check()[0] 
            self._spolecny_pruh = self.spolecny_pruh_check()[0] 
        return self._spolecny_pruh
    
    @property
    def spolecny_pruh_instances(self):
        if self._spolecny_pruh_instances is None:
            self._spolecny_pruh_instances = self.spolecny_pruh_check()[1] 
        return self._spolecny_pruh_instances

    
    @property
    def spolecny_pruh_instances(self):
        if self._spolecny_pruh_instances is None:
            self._spolecny_pruh_instances = self.spolecny_pruh_check()[1] 
        return self._spolecny_pruh_instances

    @property
    def C_spolecna(self):
        if self._C_spolecna is None:
            self._C_spolecna = self.urci_spolecnou_C() # dodělat
        return self._C_spolecna
    
    @property
    def tw(self):
        if self._tw is None:
            self._tw = self.count_tw() 
        return self._tw
    
    @property
    def rezerva(self):
        if self._rezerva is None:
            self._rezerva = self._C - self.zohlednena_skladba
        return self._rezerva

    def count_tw(self):
        if self.C> 0:
            tw = 3600 / self.C + 3600 / 4 * ((self.av - 1) + ((self.av - 1) ** 2 +(8 * 3600 * min(self.av, 1) / (3600 * self.C)) )** 0.5)
        else:
            tw = 9999999999
        return round(tw)

    def zohlednena_skladba_count(self):
        zohledenna_skladba =self.intenzita_OA + self.intenzita_PV * 1.5 + self.intenzita_NAV * 2 + self.intenzita_M * 0.8 + self.intenzita_Cyklo * 0.5
        return round(zohledenna_skladba)

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
                if self.vjezd.krizovatka.branch_count == 4:
                    C = Pohyb.P_phb(self.kriz, 1) * Pohyb.P_phb(self.kriz, 7) * self.G
                elif self.vjezd.krizovatka.branch_count == 3:
                    C = Pohyb.P_phb(self.kriz, 7) * self.G

        elif self.stupen_podrazenosti == 4 : #C4 #C10
            
            if self.cislo_proudu == 4:
                
                px = Pohyb.P_phb(self.kriz, 1) * Pohyb.P_phb(self.kriz, 7)
                p11 = Pohyb.P_phb(self.kriz, 11)
                C = self.G * Pohyb.P_phb(self.kriz, 12) * (1 / (1 + ((1- px) / px) + ((1 - p11)/p11) ))
                
            if self.cislo_proudu == 10:
                px = Pohyb.P_phb(self.kriz, 1) * Pohyb.P_phb(self.kriz, 7)
                p5 = Pohyb.P_phb(self.kriz, 5)
                C = self.G * Pohyb.P_phb(self.kriz, 6) * (1 / (1 + ((1- px) / px) + ((1 - p5)/p5) ))
                
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
  
    def spolecny_pruh_check(self):
        spolecne_pruhy = []
        spolecne_pruhy_instances = []
        

        for pohyb in self.vjezd.lines:
            if pohyb.id == self.id and pohyb.cislo_proudu != self.cislo_proudu:
                spolecne_pruhy.append(pohyb.cislo_proudu) #cislo proudu
                spolecne_pruhy_instances.append(pohyb)  # odkazy na konkretni instance

        return spolecne_pruhy, spolecne_pruhy_instances
     
    def rozrazeni_pruhu(self):
        if not any(pruh.id == self.id for pruh in self.vjezd.pruhy):
            novy_pruh = Pruh(self.vjezd, self.id)
            novy_pruh.pohyby.append(self)
        else:    
            for pruh in self.vjezd.pruhy:
                if self.id == pruh.id and self not in pruh.pohyby:
                    pruh.pohyby.append(self)
                    break
        
    
    def urci_spolecnou_C(self):
        if self.stupen_podrazenosti > 1 and len(self.spolecny_pruh) >= 1 and self.vjezd.rule == "vedlejsi":  # vjezdy z vedlejsi
            
            if self.delka_JP is None and all(pohyb.delka_JP is None for pohyb in self.spolecny_pruh_instances[:2]): # ověření zda žádny z pohybů ze společných proudů nemá rozšíření
                # neni rozšíření ani na jednom společném pohybu
                sum_I = self.zohlednena_skladba
                sum_av = self.av
                for pohyb in self.vjezd.lines:
                    for spolecny_pruh in self.spolecny_pruh:
                        if pohyb.cislo_proudu == spolecny_pruh:
                            sum_I += pohyb.zohlednena_skladba
                            sum_av += pohyb.av
                            
                return sum_I /sum_av
        
            else:    # min jeden ze společných pohybu ma rozšíření
                if self.kriz.branch_count == 3:
                    pass # dodělat

                elif self.kriz.branch_count == 4:
                    if all(pohyb.delka_JP for pohyb in self.spolecny_pruh_instances[:2]): #nejednoznačné využívání vjezdů
                        pass #doplnit přislušné vzorce 

                    elif (                                                  ### rozšíření vpravo
                            self.smer == "R" and self.delka_JP
                        ) or (
                            self.spolecny_pruh_instances[0].delka_JP and
                            self.spolecny_pruh_instances[0].druh == "R"
                        ) or (
                            len(self.spolecny_pruh_instances) > 1 and
                            self.spolecny_pruh_instances[1].delka_JP and
                            self.spolecny_pruh_instances[1].druh == "R"
                        ):
                        
                        pass

                    elif (                                                  ### rozšíření vlevo
                            self.smer == "L" and self.delka_JP
                        ) or (
                            self.spolecny_pruh_instances[0].delka_JP and
                            self.spolecny_pruh_instances[0].druh == "L"
                        ) or (
                            len(self.spolecny_pruh_instances) > 1 and
                            self.spolecny_pruh_instances[1].delka_JP and
                            self.spolecny_pruh_instances[1].druh == "L"
                        ):
                        pass 


    
   
       
        elif self.vjezd.rule == "hlavni":  ###doupravit pocitani bez pruhu vlevo nebo s nim se zahrnuti delky 
            sum_I = self.zohlednena_skladba
            sum_av = self.av
            if self.delka_JP is None:
                for pohyb in self.vjezd.lines:
                    for spolecny_pruh in self.spolecny_pruh:
                        if pohyb.cislo_proudu == spolecny_pruh:
                            sum_I += pohyb.zohlednena_skladba
                            sum_av += pohyb.av
                c_spol = sum_I /sum_av
                if c_spol >= 1800:
                    return 1800
                else:
                    return c_spol
            elif self.delka_JP:
                pass
            elif self.delka_JP:
                # dodělat pro případy s odobočovací JP
                pass

        

        
        else:
            return None

    """ def urceni_spolecne_c_rozsireni_vpravo(self): #vzorec 6-10 dle TP 188
        I_ijk = 0  # i-L, j-S,k -R
        a_vi = 0 # vlevo
        a_vj = 0 
        av_k = 0

        for pohyb in self.spolecny_pruh_instances:
            I_ijk += pohyb.zohlednena_skladba


        a_vi = 0 # vlevo
          """
        


    

    def p_6_14_count(self,i,j,k):  # vzorec 6-14
        Ll= self.delka_JP
        fct_odmc = (Ll/6) + 1
        avi =  Pohyb.find_pohyb(self.kriz, i).av if Pohyb.find_pohyb(self.kriz, i) is not None else 0
        avj = Pohyb.find_pohyb(self.kriz, j).av if Pohyb.find_pohyb(self.kriz, j) is not None else 0
        avk = Pohyb.find_pohyb(self.kriz, k).av if Pohyb.find_pohyb(self.kriz, k) is not None else 0

        p = 1-(avi *((1+ (((avj + avk)**fct_odmc) / (1- (avj+avk)))) ** (1/fct_odmc)))  # vzorec 6-16

        return  max(0,p) 

    @staticmethod
    def I_phb(kritovatka, cislo):
        hledana_intenzita = 0
        for proud in kritovatka.lines:
            if proud.cislo_proudu == cislo:
                hledana_intenzita = proud.intenzita
            
        return hledana_intenzita
       
    @staticmethod
    def P_phb(kritovatka, cislo):
        hledane_p = 0
        for proud in kritovatka.lines:
            if proud.cislo_proudu == cislo:
                hledane_p = proud.p
        return hledane_p
    
    @staticmethod
    def find_pohyb(kritovatka, cislo):
        for proud in kritovatka.lines:
            if proud.cislo_proudu == cislo:
                hledany_pohyb = proud
        return hledany_pohyb
    
    
    
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
        print(f"L_95: {self.L95}")
        print(f"Tw: {self.tw}")
        print(f"Spol pruhy: {self.spolecny_pruh}")
        print(f"Spol C: {self.C_spolecna}")
        print("--")
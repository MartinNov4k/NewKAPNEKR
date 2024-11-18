import math

class Pruh:
    instances = []

    def __init__(self, vjezd, id):

        vjezd.pruhy.append(self)
        vjezd.krizovatka.pruhy.append(self)
        Pruh.instances.append(self)

        self.pohyby = []
        self.id = id  # id v rámci vjezdu
        self._name = None
        self.vjezd = vjezd
        self._zohlednena_skladba_sum = None
        self._av_sum = None
        self._capacity = None
        self._L95 = None # délka fronty
        self._tw = None
        self._av = None # self av neni v TP pro pruh, ale je to logicke
        self._rezerva = None # rezerva kapacity
        self._ukd = None

    @property
    def zohlednena_skladba_sum(self):
            if self._zohlednena_skladba_sum is None:
                self._zohlednena_skladba_sum = self.count_Pvoz() 
            return self._zohlednena_skladba_sum
    
    @property
    def av_sum(self):
        if self._av_sum is None:
            self._av_sum = self.count_av_sum() 
        return self._av_sum
    
    @property
    def name(self):
            if self._name is None:
                self._name = self.get_name() 
            return self._name
    @property
    def capacity(self):
        if self._capacity is None:
            self._capacity = round(self.count_capacity())
        return  self._capacity

    @property
    def L95(self):
        if self._L95 is None:
            self._L95 = self.count_L95()
        return  self._L95
    
    @property
    def tw(self):
        if self._tw is None:
            self._tw = self.count_tw()
        return self._tw
    
    @property
    def av(self):
        if self._av is None:
            self._av = round(self.zohlednena_skladba_sum / self.capacity,2)
        return self._av
    
    @property
    def rezerva(self):
        if self._rezerva is None:
            self._rezerva = self.capacity - self.zohlednena_skladba_sum
        return self._rezerva

    @property
    def ukd(self):
        if self._ukd is None:
            self._ukd = self.count_ukd()
        return self._ukd

    def count_Pvoz(self):
        Pvoz_sum = 0
        for pohyb in self.pohyby:
              Pvoz_sum += pohyb.zohlednena_skladba
        return Pvoz_sum
    
    def count_av_sum(self):
        av_sum = 0
        for pohyb in self.pohyby:
              av_sum += pohyb.av
        return av_sum

    def get_name(self):
        name = ""
        for pohyb in self.pohyby:
              name += pohyb.smer
        return name
    
    def count_L95(self):
        if self.capacity == 0:
            return None
        else:
            return round((3/2) * self.capacity * (self.av - 1 + math.sqrt((1 - self.av)**2 + 3 * (8 * self.av) / self.capacity)))

    def count_tw(self):
        if self.capacity > 0:
            tw = round(3600 / self.capacity + 3600 / 4 * ((self.av - 1) + ((self.av - 1) ** 2 +(8 * 3600 * min(self.av, 1) / (3600 * self.capacity)) )** 0.5))
        else:
            tw = None
        return tw

    def count_capacity(self):

        assert len(self.pohyby) > 0

        if len(self.pohyby) == 1:   # pruh má pouze jeden pohyb
              return self.pohyby[0].C
              
        else:  #pruh je společný
            if self.vjezd.rule == "vedlejsi":  # vjezdy z vedlejsi
            
                if all(pohyb.delka_JP is None for pohyb in self.pohyby): # ověření zda žádny z pohybů ze společných proudů nemá rozšíření
                    # neni rozšíření ani na jednom společném pohybu
                    sum_I = 0
                    sum_av = 0
                    for pohyb in self.pohyby:
                        sum_I += pohyb.zohlednena_skladba
                        sum_av += pohyb.av
                                
                    return sum_I /sum_av

                else:  # min jeden ze společných pohybu ma rozšíření
                    if self.vjezd.krizovatka.branch_count == 3:
                        pass # dodělat
        
                    elif self.vjezd.krizovatka.branch_count == 4:
                        # i-L, j-S,k -R
                        pohyb_i = self.najdi_pohyb("L")
                        pohyb_j = self.najdi_pohyb("S")
                        pohyb_k = self.najdi_pohyb("R")
                        Lu_vpravo = pohyb_k.delka_JP if pohyb_k is not None else 0
                        Lu_vlevo = pohyb_i.delka_JP if pohyb_i is not None else 0
                        pohyb_i_av = pohyb_i.av if pohyb_i is not None else 0
                        pohyb_j_av = pohyb_j.av if pohyb_j is not None else 0
                        pohyb_k_av = pohyb_k.av if pohyb_k is not None else 0
                        factor_odocniny_vpravo = (Lu_vpravo / 6) + 1
                        factor_odocniny_vlevo = (Lu_vlevo / 6) + 1

                        C_vpravo =  min(
                                            1800,
                                            self.zohlednena_skladba_sum / (
                                                (((pohyb_i_av + pohyb_j_av) ** factor_odocniny_vpravo) + (pohyb_k_av ** factor_odocniny_vpravo)) ** (1 / factor_odocniny_vpravo)
                                            )
                                        )
                        
                        C_vlevo = min(
                                        1800,
                                        self.zohlednena_skladba_sum / (
                                            ((pohyb_i_av ** factor_odocniny_vlevo) + ((pohyb_j_av + pohyb_k_av) ** factor_odocniny_vlevo)) ** (1 / factor_odocniny_vlevo)
                                        )
                                    )

                        if all(pohyb.delka_JP for pohyb in self.pohyby): #nejednoznačné využívání vjezdů vzorec 6-12
                            
                            return min (1800, (C_vlevo *( pohyb_i_av /(pohyb_i_av + pohyb_j_av +pohyb_k_av))) + (C_vpravo *( pohyb_j_av + pohyb_k_av )/(pohyb_i_av + pohyb_j_av +pohyb_k_av)))

                        elif any(pohyb.smer == "R" and pohyb.delka_JP for pohyb in self.pohyby): ### rozšíření vpravo vzorec dle TP 188 6-10
                           
                            return C_vpravo
                        
                        elif any(pohyb.smer == "L" and pohyb.JP for pohyb in self.pohyby): ### rozšíření vlevo vzorec dle TP 188 6-11
                            
                            return C_vlevo
                        
            elif self.vjezd.rule == "hlavni":  ###doupravit pocitani bez pruhu vlevo nebo s nim se zahrnuti delky 
                if not any(pohyb.smer == "L" and pohyb.delka_JP for pohyb in self.pohyby): # není odbočovák vlevo z hlavni, tady asi chyba protože samostatny pruh se zadava id a me delkouJP, ale vlastně to funguje, protože když ve spolecnych neni L vubec, tak se podminka splni
                    return min(1800, self.zohlednena_skladba_sum /self.av_sum )

                elif any(pohyb.smer == "L" and pohyb.delka_JP for pohyb in self.pohyby): #odbočovák vlevo je společný
                    pohyb_i = self.najdi_pohyb("L")
                    pohyb_j = self.najdi_pohyb("S")
                    pohyb_k = self.najdi_pohyb("R")
                    
                    pohyb_i_av = pohyb_i.av if pohyb_i is not None else 0
                    pohyb_j_av = pohyb_j.av if pohyb_j is not None else 0
                    pohyb_k_av = pohyb_k.av if pohyb_k is not None else 0

                    if pohyb_j_av + pohyb_k_av >= 1 and pohyb_i_av > 0:
                        
                        return 0
                    
                    elif  pohyb_i_av == 0:
                        return 1800
                    
                    elif pohyb_j_av + pohyb_k_av < 1 and pohyb_i_av > 0:
                        delka_leveho = pohyb_i.delka_JP 
                        factor = (delka_leveho / 6) + 1
                        c = self.zohlednena_skladba_sum / (((1 + ((pohyb_j_av + pohyb_k_av) ** factor) / (1 - pohyb_j_av - pohyb_k_av)) ** (1 / factor)) * pohyb_i_av)
                        
                        return min(1800, c)

    def count_ukd(self):
        if self.tw:
            if self.av < 1:
                if self.tw <= 10:
                    return "A"
                elif self.tw <= 20:
                    return "B"
                elif self.tw <= 30:
                    return "C"
                elif self.tw <= 45:
                    return "D"
                elif self.tw > 45:
                    return "E"
            else:
                return "F"
        else:
            return None

                    
                


    def vypis(self):
        print( self.vjezd.name, self.name,"pvoz:", self.zohlednena_skladba_sum, "Capacity:", self.capacity, "av:", self.av,  "Rezerva:",self.rezerva,"L95:", self.L95, "Tw:", self.tw, "UKD:", self.ukd)

    def najdi_pohyb(self, smer):
        return next((pohyb for pohyb in self.pohyby if pohyb.smer == smer), None)
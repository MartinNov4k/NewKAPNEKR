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
        self._capacity = None

    @property
    def zohlednena_skladba_sum(self):
            if self._zohlednena_skladba_sum is None:
                self._zohlednena_skladba_sum = self.count_Pvoz() 
            return self._zohlednena_skladba_sum
    
    @property
    def name(self):
            if self._name is None:
                self._name = self.get_name() 
            return self._name
    @property
    def capacity(self):
        if self._capacity is None:
            self._capacity = self.count_capacity()
        return  self._capacity

    def count_Pvoz(self):
        Pvoz_sum = 0
        for pohyb in self.pohyby:
              Pvoz_sum += pohyb.zohlednena_skladba
        return Pvoz_sum
    
    def get_name(self):
        name = ""
        for pohyb in self.pohyby:
              name += pohyb.smer
        return name
    
    def count_capacity(self):

        assert len(self.pohyby) > 0

        if len(self.pohyby) == 1:   # pruh má pouze jeden pohyb
              return self.pohyby[0].C
              
        else:  #pruh je společný
            if self.vjezd.rule == "vedlejsi":  # vjezdy z vedlejsi
            
                if all(pohyb.delka_JP is None for pohyb in self.pohyby[:3]): # ověření zda žádny z pohybů ze společných proudů nemá rozšíření
                    # neni rozšíření ani na jednom společném pohybu
                    sum_I = 0
                    sum_av = 0
                    for pohyb in self.pohyby:
                        sum_I += pohyb.zohlednena_skladba
                        sum_av += pohyb.av
                                
                    return sum_I /sum_av

                else:  # min jeden ze společných pohybu ma rozšíření
                    if self.kriz.branch_count == 3:
                        pass # dodělat
        
                    elif self.kriz.branch_count == 4:
                        if all(pohyb.delka_JP for pohyb in self.pohyby): #nejednoznačné využívání vjezdů
                            pass #doplnit přislušné vzorce 
                        
                        elif any(pohyb.smer == "R" and pohyb.JP for pohyb in self.pohyby): ### rozšíření vpravo vtoec dle TP 188 6-10
                            # i-L, j-S,k -R
                            pohyb_i = self.najdi_pohyb("L")
                            pohyb_j = self.najdi_pohyb("S")
                            pohyb_k = self.najdi_pohyb("R")
                            
                            Lu_vpravo = pohyb_k.delka_JP
                            factor_odocniny = (Lu_vpravo / 6) + 1
                            C_vpravo = self.zohlednena_skladba_sum / ((((pohyb_i.a + pohyb_j.a) ** factor_odocniny) + (pohyb_k.a ** factor_odocniny)) ** 1/factor_odocniny)

                            return C_vpravo
                        
                        elif any(pohyb.smer == "L" and pohyb.JP for pohyb in self.pohyby): ### rozšíření vpravo
                            pass
        

    def vypis(self):
        print(self.name , self.zohlednena_skladba_sum, self.vjezd.name, self.capacity)

    def najdi_pohyb(self, smer):
        return next((pohyb for pohyb in self.pohyby if pohyb.smer == smer), None)
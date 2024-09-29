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


        
             
       
    
        

    def vypis(self):
        print(self.name , self.zohlednena_skladba_sum, self.vjezd.name, self.capacity)
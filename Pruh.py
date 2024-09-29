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
    
    def vypis(self):
        print(self.name , self.zohlednena_skladba_sum, self.vjezd.name)
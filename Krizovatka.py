class Krizovatka:
    def __init__(self, name, branch_count, speed ):
        self.name = name
        self.branch_count = branch_count
        self.speed = speed #rychlost na hlavni
        self.UKD_hlavni = None
        self.UKD_vedlejsi = None

        self.vjezdy = []
        self.lines = []

    #### spatne- nemelo by bejt v teto class odkazovano na cizi atributy- pozdeji předělat
    def vypsat_vsechny_pohyby (self):
        for pohyb in self.lines:
            print(pohyb.cislo_proudu, pohyb.smer, pohyb.intenzita, "vjezd:", pohyb.vjezd.name)

    

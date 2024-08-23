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
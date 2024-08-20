class Vjezd:
    def __init__(self, name, rule):
        self.name = name
        self.rule = rule
        self.volume = None #doplnit
        self.capacity = None 
        self.reserve = None 
        self.que_lenght = None
        self.delay = None
        self.stop_count = None
        self.ukd = None


class Pohyb:
    def __init__(self, smer,pocet_pruhu):
        self.vjezd = None  # kam patří
        self.smer = smer
        self.pocet_pruhu = pocet_pruhu
        self.Cn = None
        self.Gn = None
        self.intenzita_nadrazenych = None
        self.Tg = None # kritický časový odstup
        self.Tf = None # následný časový odstup
        self.p0 = None # pravděpodobnost nevzdutí nadřazených
        self.stupen_podrazenosti = None
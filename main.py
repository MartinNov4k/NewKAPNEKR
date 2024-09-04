from Krizovatka import Krizovatka
from Pohyb import Pohyb
from Vjezd import Vjezd

### použití pokusné ###############################################################

cross1= Krizovatka("Dablicka x Bestakova", 4, 77)

Zapad = Vjezd(cross1, "Zapad", "hlavni", 1 )
Sever = Vjezd (cross1,"Sever", "vedlejsi", 2, "P6")
Vychod = Vjezd (cross1,"Východ", "hlavni", 3)
Jih = Vjezd (cross1,"Jih", "vedlejsi", 4, "P6")

pohyb1 = Pohyb("L", 22, 5, Zapad ,cross1, 1, 1)
pohyb2= Pohyb("S", 270, 85, Zapad, cross1, 1, 1)
pohyb3= Pohyb("R", 21, 15, Zapad, cross1, 1, 1)

pohyb4 = Pohyb("L", 12, 5, Jih, cross1, 1, 1)
pohyb5= Pohyb("S", 59, 7, Jih, cross1, 1, 1)
pohyb6= Pohyb("R",  29, 26, Jih, cross1, 1, 1)

pohyb7 = Pohyb("L", 117, 23, Vychod, cross1, 1, 1)
pohyb8= Pohyb("S", 230, 58, Vychod, cross1, 1, 1)
pohyb9= Pohyb("R", 144, 32, Vychod, cross1, 1, 1)

pohyb10 = Pohyb("L", 157, 32, Sever,cross1, 1, 1)
pohyb11= Pohyb("S", 21 ,1, Sever, cross1, 1, 1)
pohyb12= Pohyb("R", 6, 2, Sever, cross1, 1, 1)

""" print(pohyb1.Tf)
print(pohyb1.Tg)

print(pohyb1.smer)
print(pohyb1.druh)
print(vjezd1.orientace)
print(pohyb1.vjezd.name)
print(pohyb1.vjezd.krizovatka.name)

print(cross1.branch_count)

print(vjezd2.rule_type)

print(pohyb1.stupen_podrazenosti)

print(pohyb1.cislo_proudu)

 """
""" print(pohyb12.cislo_proudu)
print(pohyb6.cislo_proudu) """

cross1.vypsat_vsechny_pohyby()

print(Pohyb.I_phb(cross1, 1))

for pohyb in cross1.lines:
    pohyb.vypis_vlastnosti() 





""" for pohyb in Jih.lines:
    print(pohyb.cislo_proudu)
    print(pohyb.druh)
    print(pohyb.zohlednena_skladba)
    print( f"nadrazene proudy I {pohyb.intenzita_nadrazenych}")
    print( f"nadrazene proudy I {pohyb.intenzita_nadrazenych}")
    print(pohyb.av)
    print(pohyb.C)
    print(pohyb.C_spolecna)
    print("--") """
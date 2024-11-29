from logic_nerizena_krizoavtka.pohyb import Pohyb
from logic_nerizena_krizoavtka.vjezd import Vjezd
from logic_nerizena_krizoavtka.pruh import Pruh
from logic_nerizena_krizoavtka.krizovatka import Krizovatka

### použití pokusné ###############################################################

cross1= Krizovatka("Drnovská x Stochovská", 3, 40)

Zapad = Vjezd(cross1, "Zapad", "hlavni", 1 )
#Sever = Vjezd (cross1,"Sever", "vedlejsi", 2, "P6")
Vychod = Vjezd (cross1,"Východ", "hlavni", 3)
Jih = Vjezd (cross1,"Jih", "vedlejsi", 4, "P4")

#pohyb1 = Pohyb("L", 17, 4, 1, 0, 0, Zapad ,cross1, 1, 1,6)
pohyb2= Pohyb("S", 209, 15, 0, 0, 0, Zapad, cross1, 1, 1)
pohyb3= Pohyb("R", 240, 11, 0, 0 , 0, Zapad, cross1, 1, 1)


pohyb4 = Pohyb("L", 203, 8,0,0,0, Jih, cross1, 1, 1)
#pohyb5= Pohyb("S", 45, 5,2,0,7, Jih, cross1, 1, 1, 6)
pohyb6= Pohyb("R",  37, 3, 0 , 0, 0, Jih, cross1, 1, 1,6)

pohyb7 = Pohyb("L",56, 3,0,0,0, Vychod, cross1, 1, 1)
pohyb8= Pohyb("S", 261, 16, 0, 0, 0, Vychod, cross1, 1, 1)
#pohyb9= Pohyb("R", 109, 22, 10,0, 3, Vychod, cross1, 2, 1)

""" pohyb10 = Pohyb("L", 123, 18,14,0,2, Sever,cross1, 1, 1,6)
pohyb11= Pohyb("S", 16 ,1,0,0,4, Sever, cross1, 1, 1, 6)
pohyb12= Pohyb("R", 4, 2,0,0,0, Sever, cross1, 1, 1, 6)
 """
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

print(pohyb2.kriz.branch_count)



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



for pohyb in cross1.lines:
    pohyb.rozrazeni_pruhu()



for pruh in Pruh.instances:
    pruh.vypis()

cross1.vypis_av()
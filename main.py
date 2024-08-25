from Krizovatka import Krizovatka
from Pohyb import Pohyb
from Vjezd import Vjezd

### použití pokusné ###############################################################

cross1= Krizovatka("Dablicka x Bestakova", 4, 50)

vjezd1 = Vjezd(cross1, "Zapad", "hlavni", 1 )
vjezd2 = Vjezd (cross1,"Sever", "vedlejsi", 2, "P4")
vjezd3 = Vjezd (cross1,"Východ", "hlavni", 3)
vjezd4 = Vjezd (cross1,"Jih", "vedlejsi", 4, "P4")

pohyb1 = Pohyb("L", 1, 22, vjezd1 ,cross1)
pohyb2= Pohyb("S", 1, 270, vjezd1,cross1)
pohyb3= Pohyb("R", 1, 21, vjezd1,cross1)

pohyb4 = Pohyb("L", 1, 6, vjezd2,cross1)
pohyb5= Pohyb("S", 1, 21, vjezd2,cross1)
pohyb6= Pohyb("R", 1, 157, vjezd2,cross1)

pohyb7 = Pohyb("L", 1, 117, vjezd3,cross1)
pohyb8= Pohyb("S", 1, 230, vjezd3,cross1)
pohyb9= Pohyb("R", 1, 144, vjezd3,cross1)

pohyb10 = Pohyb("L", 1, 12, vjezd4,cross1)
pohyb11= Pohyb("S", 1, 59, vjezd4,cross1)
pohyb12= Pohyb("R", 1, 145, vjezd4,cross1)

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







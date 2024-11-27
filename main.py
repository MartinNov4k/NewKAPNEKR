from krizovatka import Krizovatka
from pohyb import Pohyb
from vjezd import Vjezd
from pruh import Pruh




## příklad zadání

cross1= Krizovatka("Dablicka x Bestakova", 4, 77)

Zapad = Vjezd(cross1, "Zapad", "hlavni", 1 )
Sever = Vjezd (cross1,"Sever", "vedlejsi", 2, "P6")
Vychod = Vjezd (cross1,"Východ", "hlavni", 3)
Jih = Vjezd (cross1,"Jih", "vedlejsi", 4, "P6")

pohyb1 = Pohyb("L", 17, 4, 1, 0, 0, Zapad ,cross1, 1, 1,6)
pohyb2= Pohyb("S", 182, 46, 39, 3, 0, Zapad, cross1, 2, 1)
pohyb3= Pohyb("R", 6, 15,0,0, 0, Zapad, cross1, 2, 1)


pohyb4 = Pohyb("L", 7, 5,0,0,0, Jih, cross1, 1, 1,6)
pohyb5= Pohyb("S", 45, 5,2,0,7, Jih, cross1, 1, 1, 6)
pohyb6= Pohyb("R",  103, 21,5,0,0, Jih, cross1, 1, 1,6)

pohyb7 = Pohyb("L", 95, 21,1,0,0, Vychod, cross1, 1, 1, 6)
pohyb8= Pohyb("S", 165, 23,35, 6, 1, Vychod, cross1, 2, 1)
pohyb9= Pohyb("R", 109, 22, 10,0, 3, Vychod, cross1, 2, 1)

pohyb10 = Pohyb("L", 123, 18,14,0,2, Sever,cross1, 1, 1,6)
pohyb11= Pohyb("S", 16 ,1,0,0,4, Sever, cross1, 1, 1, 6)
pohyb12= Pohyb("R", 4, 2,0,0,0, Sever, cross1, 1, 1, 6)


# výpis vybraných parametrů

cross1.vypsat_vsechny_pohyby()

print(Pohyb.I_phb(cross1, 1))

for pohyb in cross1.lines:
    pohyb.vypis_vlastnosti() 

print(pohyb1.kriz.branch_count)


for pohyb in cross1.lines:
    pohyb.rozrazeni_pruhu()


for pruh in Pruh.instances:
    pruh.vypis()

cross1.vypis_av()
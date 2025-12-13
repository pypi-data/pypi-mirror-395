import random
import sys
import time

monster_name = "Test"
monster_health = 60
monster_attack = 2.2
monster_attack_luck = None
requested_spare_points = 10
current_spare_points = 0
acts = ["Test et","Test etme"]
act_1 = f"{monster_name}'i test ettin. {monster_name} mutlu oldu."
act_spare_points1 = 1
act_2 = f"{monster_name}'i test etmedin. {monster_name} mutsuz oldu."
act_spare_points2 = 0
act_3 = ""
act_spare_points3 = 0
act_4 = ""
act_spare_points4 = 0
act_5 = ""
act_spare_points5 = 0
act_6 = ""
act_spare_points6 = 0
act_7 = ""
act_spare_points7 = 0
act_8 = ""
act_spare_points8 = 0
act_9 = ""
act_spare_points9 = 0
act_10 = ""
act_spare_points10 = 0

player_health = 20
player_max_health = 20
player_attack = 6
food_health = 2.5
food_amount = 5
how_many_spare_points_left = 0
spareable = False

def showmonstername():
    print(f"\n{monster_name} sana saldirdi!")



def food():
    global player_health,food_amount
    
    if player_health >= player_max_health:
        print("Canin zaten dolu.")
        monsterattack()

    if food_amount <= 0:
        print("Yemegin kalmadi.")
        monsterattack()

    else:
        eat_strings = ["Yemegi bir lokmada yedin.","Yemegi agzina tiktin.","Yemegi yillardir ilk kez yemek yiyormus gibi yedin."]
        random_eat_string = random.choice(eat_strings)
        player_health = player_health + food_health
        print(f"{random_eat_string} Canin {player_health} oldu.")
        food_amount = food_amount - 1
        print(f"{food_amount} kadar yemegin kaldi.")
        monsterattack()
    
    



def credits():
     print("\n patates adam'ın arkadaşı tarafından yapılmıştır. patates adam kendini biliyor.\n")
     choosing()


def monsterattack():
    global monster_attack_luck,player_health,monster_name
    monster_attack_luck = None
    monster_attack_luck = random.choices([True, False], weights=[70, 30])[0]

    if monster_attack_luck:

        player_health = player_health - monster_attack

        player_health = round(player_health,1)

        print(f"{monster_name} sana saldirdi. {player_health} canin kaldi.")

        choosing()

    else:
        print(f"{monster_name} sana saldirmadi.")

        choosing()
    


def actfunc(event=None):
            global player_health,monster_attack,current_spare_points,how_many_spare_points_left

            if current_spare_points <= requested_spare_points:

                act_count = 0

                act_count_array = []

                print("\nEylemler:\n")

                for i, deger in enumerate(acts, 1): 

                    print(f"{i}. {deger}")

                for act_count in range(1, len(acts)+1):

                    act_count_array.append(act_count)

                which_act = int(input("\n"))

                if which_act in act_count_array and 1 <= which_act <= len(acts):
                    
                    chosen_act_name = "act_" + str(which_act)

                    chosen_act_spare_point = globals()["act_spare_points" + str(which_act)]

                    current_spare_points += chosen_act_spare_point

                
                    if current_spare_points > requested_spare_points:
                        current_spare_points = requested_spare_points

                    chosen_act = globals()[chosen_act_name]
                    print(f"\n{chosen_act}")

                    how_many_spare_points_left = max(0, requested_spare_points - current_spare_points)

                    if current_spare_points < requested_spare_points:
                        print(f"({current_spare_points} bagislama puanin oldu. Canavari bagislamak icin {how_many_spare_points_left} daha puan lazim.)\n")
                    else:
                        print("Zaten yeterince bagislama puanin var!")


                    monsterattack()

                    
                else:
                    print("Öyle bir eylem yok!")
                    actfunc()
            else:
                current_spare_points = requested_spare_points
                print("Zaten yeterince bagislama puanin var!")
                choosing()



def spare():
    global how_many_spare_points_left,current_spare_points,spareable
    if current_spare_points == requested_spare_points:
        spareable = True
        choosing()
    else:
        how_many_spare_points_left = current_spare_points - requested_spare_points
        how_many_spare_points_left = how_many_spare_points_left * -1
        print(f"Yeterli bagislama puanin yok.Canavari bagislamak icin {how_many_spare_points_left} daha puan lazim.")
        monsterattack()

def choosing():

    global monster_name,monster_health,monster_name,player_attack,player_health,current_spare_points,spareable

    if spareable:
        print(f"{monster_name}'i bagisladin. Oyun bitti.")
        time.sleep(10)
        sys.exit()
        
    if player_health <= 0:

        print(f"\n{monster_name} seni oldurdu. Oyun bitti.")
        time.sleep(10)
        sys.exit()

    elif monster_health <= 0:

        print(f"\n{monster_name}'i vahsice katlettin. {monster_name} tozlarina ayrildi. Oyun bitti.")
        time.sleep(10)
        sys.exit()

    else:
    
        print("\nSaldir : S       Eylem : E       Yemek : Y       Bagisla : B\n")

        option = input()

        if option.upper() == "S":

            monster_health = monster_health - player_attack

            monster_health = round(monster_health,1)

            print(f"\n{monster_name}'a saldirdin. {monster_name}'in {monster_health} cani kaldi!\n")

            monsterattack()

            

        if option.upper() == "E":
            
            actfunc()

        if option.lower() == "credits":

            credits()

        if option.upper() == "Y":
             
            food()
        
        if option.upper() == "B":

            spare()

        else:

            print("Oyle bir secenek yok.")
            choosing()

       

def savasi_baslat():
    showmonstername()
    choosing()

def ne_yapcam():
    print("""
monster_name = "" --- canavarın adı
monster_health = 60 --- canavarın canı
monster_attack = 2.2 --- canavarın verdiği hasar
requested_spare_points = 10 --- canavarı bağışlamak için kaç puan lazım
acts = [] --- buraya eylemleri gir
act_1 = "" --- bu eylemi yaptıktan sonra çıkan mesajlar
act_spare_points1 = 0 --- bu eylemi yaptıktan sonra oyuncuya kaç tane bağışlama puanı verilecek
act_2 = "" --- diğeriyle aynı
act_spare_points2 = 0 --- diğeriyle aynı
act_3 = "" --- aynı
act_spare_points3 = 0 --- aynı
act_4 = "" --- aynı
act_spare_points4 = 0 --- aynı
act_5 = "" --- aynı
act_spare_points5 = 0 --- aynı
act_6 = "" --- aynı
act_spare_points6 = 0 --- aynı
act_7 = "" --- aynı
act_spare_points7 = 0 --- aynı
act_8 = "" --- aynı
act_spare_points8 = 0 --- aynı
act_9 = "" --- aynı
act_spare_points9 = 0 --- aynı
act_10 = "" --- aynı
act_spare_points10 = 0 --- aynı

player_max_health = 20 --- oyuncunun maksimum canı
player_attack = 6 --- oyuncunun canavara vereceği hasar
food_health = 2.5 --- yemeğin vereceği can
food_amount = 5 --- yemek miktarı
          
sakın (textbasedbattle.) yazdıktan sonra ne_yapcam ve savasi_baslat harici çıkan hiç bir functionu yazma.""")
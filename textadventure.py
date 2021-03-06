import random
import os
from item import *


class Inventory:
    def __init__(self, length):
        self.length = length
        self.slots = []

    def append_item(self, item):
        if len(self.slots) < self.length:
            self.slots.append(item)

    def remove_item(self, item_count):
        if len(self.slots) < self.length:
            self.slots.remove(self.slots[item_count])

class Chest:
    def __init__(self, loot = []):
        self.loot = loot
        self.name = "chest"
        if loot != []:
            rand = random.randint(0, 3)
            if rand == 0:
                self.loot = [Swort()]
            if rand == 1:
                self.loot = [Dagger()]
            if rand == 2:
                self.loot = [Club()]
            if rand == 3:
                self.loot = []
        self.loot = loot

    def open_chest(self, inventory):
        print("You look in the chest and see" , end='')
        for i in self.loot:
            print(" a " + i.name, end="")
        print(".")
        f = 0
        while True:
            toke = input('toke with:').lower().split(", ")
            for i in toke:
                for l in self.loot:
                    if i == l.name:
                        inventory.append_item(l)
            if f == 0:
                print('?')
            else:
                break

class Chest_in_ground:
    def __init__(self):
        self.loot = []
        self.name = "chest"
        rand = random.randint(0, 3)
        if rand == 0:
            self.loot = [Swort()]
        if rand == 1:
            self.loot = [Dagger()]
        if rand == 2:
            self.loot = [Diamond()]
        if rand == 3:
            self.loot = []

class Character:
    def __init__(self, hp, ad, xp, harmles, drop, name):
        self.hp = hp
        self.ad = ad
        self.name = name
        self.xp = xp
        self.harmles = harmles
        self.drop = drop

    def get_hit(self, ad, xp):
        self.hp = self.hp - ad * (xp/10)
        if self.hp <= 0:
            self.die()

    def is_dead(self):
        return self.hp <= 0

    def die(self):
        print(self.name + " died")

    def drop_item(self, m):
        m.state[m.x][m.y].item.append(self.drop)

class Goblin(Character):
    def __init__(self, xp):
        Character.__init__(self, 100, 10, xp, 0, Club(), "Goblin")

class Ork(Character):
    def __init__(self, xp):
        Character.__init__(self, 300, 30, xp, 0, Dagger(), "Ork")

class Hermit(Character):
    def __init__(self):
        Character.__init__(self, 100, 4, 50, 1, [], "Hermit")

    def talk_with(self):
        print("oh, hello.")

class Supply:
    def __init__(self, supply):
        self.supply = supply

    @staticmethod
    def gen_supply():
        rand = random.randint(0, 4)
        if rand == 0:
            return Supply([Swort(), Apple()])
        if rand == 1:
            return Supply([Bread(), Roll()])
        if rand == 2:
            return Supply([Swort(), Bread()])
        if rand == 3:
            return Supply([Apple(), Roll()])
        if rand == 4:
            return Supply([Apple(), Book()])

class Trader(Hermit):
    def __init__(self):
        Character.__init__(self, 100, 4, 50, 1, [], "Trader")
        self.supply = Supply.gen_supply()

    def trade(self, p, m, inventory):
        print("(type buy if you want to buy or type sell if you want to sell)")
        inp = input("trade>")
        if inp == "buy":
            while inp != "quit":
                print("trader's suply:", end=' ')
                for i in self.supply:
                    print("a " + i.name, end=" ")
                inp = input("buy>")
                for i in self.supply:
                    if inp == i.name:
                        inp = input("Do you want to buy " + i.name + " J/n : ")
                        if inp == "J":
                            inventory.append_item(i)
                            p.money -= i.worth
                            self.supply.remove(inp)
        elif inp == "sell":
            while inp != "quit":
                list_inventory(p, m, inventory)
                inp = input("sell>")
                for i in inventory.slots:
                    if inp == i.name:
                        inp = input("Do you want to sell " + i.name + " J/n : ")
                        if inp == "J":
                            p.money += i.worth
                            inventory.slots.remove(i)


class Player(Character):
    def __init__(self, name, hp, ad):
        self.xp = 0
        Character.__init__(self, hp, ad, self.xp, 1, [], name)
        self.max_hp = hp
        self.money = 0

    def die(self):
        exit("Wasted. Try again.")

    def rest(self):
        self.hp = self.max_hp


def get_enemies(self):
        return self.state[self.x][self.y].enemies
class Field:
    def __init__(self, enemies, item, in_ground):
        self.enemies = enemies
        self.item = item
        self.in_ground = in_ground

    def print_state(self):
        print("You look around and see" , end=' ')
        for i in self.enemies:
            print("an " + i.name, end=" ")
        for i in self.item:
            print("a " + i.name, end=" ")
        print("")

    @staticmethod
    def gen_random():
        rand = random.randint(0, 5)
        if rand == 0:
            return Field([], [], [])
        if rand == 1:
            return Field([Ork(random.randint(0, 5)), Hermit()], [], [])
        if rand == 2:
            return Field([Goblin(random.randint(0, 5)), Goblin(random.randint(0, 5)), Ork(random.randint(0, 5))], [Chest()], [])
        if rand == 3:
            return Field([Ork(random.randint(0, 5)), Trader()], [], [])
        if rand == 4:
            return Field([Goblin(random.randint(0, 5)),
            Goblin(random.randint(0, 5)), Ork(random.randint(0, 5))], [], [Chest_in_ground()])
        if rand == 5:
            return Field([Goblin(random.randint(0, 5)), Goblin(random.randint(0, 5)), Ork(random.randint(0, 5))], [], [])

class Map:
    def __init__(self, width, height):
        self.state = []
        self.x = 0
        self.y = 0
        for i in range(width):
            fields = []
            for j in range(height):
                fields.append(Field.gen_random())
            self.state.append(fields)
        for gx in range(width):
            for gy in range(height):
                if len(self.state[gx][gy].in_ground) != 0:
                    rand = random.randint(0, 1)
                    if rand == 0:
                        content = "this is the signpost to an treasure: go right then backward, and then dig"
                        self.state[gx-1][gy-1].item.append(Chest([Writen_Book("treasure", content)]))
                    if rand == 1:
                        content = "this is the signpost to an treasure: go right then dig"
                        self.state[gx-1][gy].item.append(Chest([Writen_Book("treasure", content)]))

    def print_state(self):
        self.state[self.x][self.y].print_state()

    def get_enemies(self):
        return self.state[self.x][self.y].enemies

    def get_item(self):
        return self.state[self.x][self.y].item

    def get_in_ground(self):
        return self.state[self.x][self.y].in_ground

    def ad_chest(self, loot):
        self.state[self.x][self.y].item.append(Chest(loot))

    def remove_item(self, item_count):
        self.state[self.x][self.y].item.remove(self.state[self.x][self.y].item[item_count])

    def forward(self):
        #print(self.x + self.y)
        if self.x == len(self.state) - 1:
            print("You see huge mountains , which you can't pass.")
        else:
            self.x = self.x + 1

    def backwards(self):
        #print(self.x + self.y)
        if self.x == 0:
            print("You see cliffs, but you can't jump safely.")
        else:
            self.x = self.x - 1

    def right(self):
        #print(self.x + self.y)
        if self.y == len(self.state[self.x]) - 1:
            print("You see huge mountains , which you can't pass.")
        else:
            self.y = self.y + 1

    def left(self):
        #print(self.x + self.y)
        if self.y == 0:
            print("You see cliffs, but you can't jump safely.")
        else:
            self.y = self.y - 1



def forward(p, m, inventory):
    m.forward()

def right(p, m, inventory):
    m.right()

def left(p, m, inventory):
    m.left()

def backwards(p, m, inventory):
    m.backwards()

def save(p, m, inventory):
    n = input("name:")
    f = open('/home/pi/Phthon-Projekte/textadventure/'+n, 'w')
    print(p.hp, file=f, flush=True)
    print(p.ad, file=f, flush=True)
    print(p.xp, file=f, flush=True)
    print(p.harmles, file=f, flush=True)
    print(p.drop, file=f, flush=True)
    print(p.name, file=f, flush=True)
    print(p.max_hp, file=f, flush=True)
    print(p.money, file=f, flush=True)
    for x in m.state:
        for y in x:
            for i1 in y.enemies:
                print(i1.name, file=f, flush=True)
            for i2 in y.item:
                print(i2.name, file=f, flush=True)
            for i3 in y.in_ground:
                print(i3.name, file=f, flush=True)
    print(m.x, file=f, flush=True)
    print(m.y, file=f, flush=True)
    print(inventory.slots, file=f, flush=True)
    print(inventory.length, file=f, flush=True)

def load(p, m, inventory):
    os.chdir("/home/pi/Phthon-Projekte/textadventure")
    files = os.system('ls')
    print(files)
    file_name = input("file:")
    f = open('/home/pi/Phthon-Projekte/textadventure/'+file_name, 'r')
    text = read(f).split('\n')


def quit_game(p, m, inventory):
    print("You commit suicide and leave this world.")
    exit(0)

def print_help(p, m, inventory):
    print("folloving commands are available: ", end=' ')
    for i in Commands.keys():
        print(i, end=", ")
    print("")

def pickup(p, m, inventory):
    item = m.get_item()
    for i in item:
        if i.name != "chest":
            inventory.append_item(i)
            item.remove(i)
    list_inventory(p, m, inventory)

def fight(p, m, inventory):
    enemies = m.get_enemies()
    #print(enemies[0].name)
    while len(enemies) > 0:
        if enemies[0].harmles != 1:
            enemies[0].get_hit(p.ad, p.xp)
            if enemies[0].is_dead():
                enemies[0].drop_item(m)
                enemies.remove(enemies[0])
            for i in enemies:
                if i.harmles != 1:
                    p.get_hit(i.ad, i.xp)
                    #i.xp = i.xp + 1
            print("You are wounded and have " + str(p.hp) + " hp left.")
            p.xp = p.xp + 1
        else:
            break

def rest(p, m, i):
    p.rest()

def talk_with(p, m, inventory):
    enemies = m.get_enemies()
    #print("t")
    for i in enemies:
        if i.name == "Hermit":
            i.talk_with()
        else:
            print("Ther is no Hermit wich you can talk with.")

def trade(p, m, inventory):
    enemies = m.get_enemies()
    #print("t")
    for i in enemies:
        if i.name == "Trader":
            i.trade(p, m, inventory)
        else:
            print("Ther is no Trater wich you can trade with.")

def list_inventory(p, m, inventory):
    print("inventory:" , end='')
    for i in inventory.slots:
        print(" a " + i.name, end="")
    print("")

def open_chest(p, m, inventory):
    item = m.get_item()
    if item[0].name == "chest":
        item[0].open_chest(inventory)

def dig(p, m, inventory):
    print("you dig and see:", end=' ')
    for i in m.get_in_ground():
        print(i.name)
        m.ad_chest(i.loot)
    print(' .')

def read_book(p, m, inventory):
    for i in inventory.slots:
        if i.name == 'book:treasure':
            print(i.show_content())
        else:
            print("there is no book in your inventory")


Commands = {
    'help' : print_help,
    'quit' : quit_game,
    'pickup' : pickup,
    'forward' : forward,
    'right' : right,
    'left' : left,
    'backwards' : backwards,
    'fight' : fight,
    'save' : save,
    'load' : load,
    'rest' : rest,
    'talk_with' : talk_with,
    'trade' : trade,
    'list_inventory' : list_inventory,
    'open_chest' : open_chest,
    'dig' : dig,
    'read_book' : read_book
}

if __name__ == '__main__':
    name = input("Enter your name ")
    map = Map(5, 5)
    p = Player(name, 200, 100)
    i = Inventory(10)
    print("(type help to list the commands available)\n")
    while True:
        command = input(name + "> ").lower().split(" ")
        if command[0] in Commands:
            Commands[command[0]](p, map, i)
        else:
            print("You run around in circles and don't know what to do.")
        map.print_state()
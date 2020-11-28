import sqlite3


class CoffeeInfo:
    def __init__(self, id, grade, roast, consistence, taste, cost, volume):
        self.id = id
        self.grade = grade
        self.roast = roast
        self.consistence = consistence
        self.taste = taste
        self.cost = cost
        self.volume = volume

    def get_id(self):
        return self.id

    def get_grade(self):
        return self.grade

    def get_roast(self):
        return self.roast

    def get_consistence(self):
        return self.consistence

    def get_taste(self):
        return self.taste

    def get_cost(self):
        return self.cost

    def get_volume(self):
        return self.volume


class CoffeeInfoManager:
    def __init__(self, filename="data/coffee.sqlite"):
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()

    def get_coffees_info(self):
        coffees = self.cur.execute("SELECT * FROM coffees").fetchall()
        return [CoffeeInfo(*e) for e in coffees]

    def update(self, id, new_id, grade, roast, consistence, taste, cost, volume):
        self.cur.execute("UPDATE coffees SET id=?, grade=?, roast=?, consistence=?, taste=?, cost=?, volume=?"
                         " WHERE id={}".format(id), [new_id, grade, roast, consistence, taste, cost, volume])
        self.conn.commit()

    def insert(self, id, grade, roast, consistence, taste, cost, volume):
        self.cur.execute("INSERT INTO coffees(id, grade, roast, consistence, taste, cost, volume) VALUES("
                         "?,?,?,?,?,?,?)", [id, grade, roast, consistence, taste, cost, volume])
        self.conn.commit()

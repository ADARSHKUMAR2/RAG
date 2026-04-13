class Chai:
    def __init__(self, sweetness, milk_level):
        self.sweetness = sweetness
        self.milk_level = milk_level

    def sip(self): 
        print("Sip chai")

    def add_sugar(self, amount):
        print("Added sugar  ")

myChai = Chai(sweetness=10, milk_level=5)
myChai.sip()
myChai.add_sugar(10)
class User():

    def __init__(self, chat_id, cup_radius, water_weight):
        self.chat_id = chat_id
        self.cup_radius = cup_radius
        self.water_weight = water_weight
    
    def get_id(self):
        return self.chat_id
    
    def get_radius(self):
        return self.cup_radius
    
    def update_radius(self, new_radius):
        self.cup_radius = new_radius
    
    def get_weight(self):
        return self.water_weight
    
    def update_weight(self, new_weight):
        self.water_weight = new_weight
class Ingredient:
    def __init__(self,name,quantity,unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit
    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self,value):
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(value)

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"
    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"
    def __eq__(self, other):
        if self.unit == other.unit and self.name == other.name:
            return True
        return False
    
class Recipe:
    def __init__(self,title,ingredients=None):
        self.title = title
        if ingredients is not None:
            self.ingredients = ingredients
        else:
            self.ingredients = []

    def add_ingredient(self,ingredient):
        for line in self.ingredients:
            if line == ingredient:
                line.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        if type(ratio) == int or type(ratio) == float:
            if ratio > 0:
                return True
        return False
    
    def scale(self,ratio):
        if self.is_valid_ratio(ratio) == False:
            raise ValueError("Неправильный ratio")
        new_ingredients = []
        for i in self.ingredients:
            ni = Ingredient(i.name,i.quantity*ratio,i.unit)
            new_ingredients.append(ni)
        return Recipe(self.title,new_ingredients)
    def __len__(self):
        return(len(self.ingredients))
    def __str__(self):
        s = self.title + ": "
        for i in self.ingredients:
            s += f"{i.name},"
        if len(self.ingredients) > 0:
            return s[:-1]
        else:
            return ""
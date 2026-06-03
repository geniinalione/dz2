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
class DietaryRecipe(Recipe):
    def __init__(self,title,diet_type,ingredients=None):
        super().__init__(title,ingredients)
        self.diet_type = diet_type
    def scale(self,ratio):
        n = super().scale(ratio)
        return DietaryRecipe(self.title,self.diet_type,n.ingredients)
    def __str__(self):
        return f"({self.diet_type}) {super().__str__()}"
    
class ShoppingList:
    def __init__(self,):
        self._items = []
    
    def add_recipe(self,recipe,portions):
        if portions > 0:
            sc = recipe.scale(portions)
            for line in sc.ingredients:
                self._items += [(line,recipe.title)]
        else:
            raise ValueError("Количество порций должно быть положительным")
    
    def remove_recipe(self,title):
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self):
        totals = {}
        for line in self._items:
            cur = (line[0].name,line[0].unit)
            if cur in totals:
                totals[cur] += line[0].quantity
            else:
                totals[cur] = line[0].quantity
        res = []
        for (name, unit), quantity in totals.items():
            res.append(Ingredient(name,quantity,unit))
        res.sort(key = lambda x: x.name)
        return res
    def __add__(self, other):
        new = ShoppingList()
        new._items = self._items + other._items
        return new
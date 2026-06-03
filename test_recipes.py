import pytest
from recipes import Ingredient, Recipe, DietaryRecipe, ShoppingList
def test_ingredient_init():
    ing = Ingredient("Соль",12, "кг")
    assert ing.name == "Соль"
    assert ing.quantity == 12.0
    assert ing.unit == "кг"

def test_ingredient_str():
    ing = Ingredient("Соль", 12, "кг")
    assert str(ing) == "Соль: 12.0 кг"

def test_ingredient_eq_same():
    a = Ingredient("Соль", 12, "кг")
    b = Ingredient("Соль", 13, "кг")
    assert a == b 

def test_ingredient_eq_diff_name():
    a = Ingredient("Сахар", 12, "кг")
    b = Ingredient("Соль", 13, "кг")
    assert a != b

def test_ingredient_eq_diff_unit():
    a = Ingredient("Соль", 12, "г")
    b = Ingredient("Соль", 12, "кг")
    assert a != b

def test_recipe_init():
    t = Ingredient("Соль дефолтная",12,"кг")
    a = Recipe("Соль",[t])
    assert a.title == "Соль"
    assert a.ingredients == [t]
    assert len(a) == 1

def test_add_new():
    r = Recipe("Соль")
    r.add_ingredient(Ingredient("Соль солённая", 12, "кг"))
    assert len(r) == 1
    assert r.ingredients[0].name == "Соль солённая"


def test_recipe_add_duplicate():
    r = Recipe("Соль")
    r.add_ingredient(Ingredient("Соль солённая", 12, "кг"))
    r.add_ingredient(Ingredient("Соль солённая", 13, "кг"))
    assert len(r) == 1
    assert r.ingredients[0].quantity == 25.0

def test_recipe_scale():
    r = Recipe("Соль")
    r.add_ingredient(Ingredient("Соль", 12, "кг"))
    r2 = r.scale(2)
    assert r2 is not r
    assert r2.ingredients[0].quantity == 24.0
    assert r.ingredients[0].quantity == 12.0

def test_recipe_scale_invalid():
    r = Recipe("Соль")
    r.add_ingredient(Ingredient("Соль", 12, "кг"))
    with pytest.raises(ValueError):
        r.scale(-1)

def test_recipe_len():
    r = Recipe("Суп")
    r.add_ingredient(Ingredient("Вода", 1, "л"))
    r.add_ingredient(Ingredient("Соль", 10, "г"))
    assert len(r) == 2

def test_shopping_add():
    r = Recipe("Соль")
    r.add_ingredient(Ingredient("Соль обычная", 12, "кг"))
    s = ShoppingList()
    s.add_recipe(r, 1)
    assert len(s.get_list()) == 1

def test_shopping_sum():
    r1 = Recipe("Суп")
    r1.add_ingredient(Ingredient("Соль", 12, "кг"))
    r2 = Recipe("Пельмени")
    r2.add_ingredient(Ingredient("Соль", 13, "кг"))
    s = ShoppingList()
    s.add_recipe(r1, 1)
    s.add_recipe(r2, 1)
    result = s.get_list()
    assert len(result) == 1
    assert result[0].quantity == 25.0

def test_shopping_invalid_portions():
    r = Recipe("Суп")
    r.add_ingredient(Ingredient("Соль", 12, "кг"))
    s = ShoppingList()
    with pytest.raises(ValueError):
        s.add_recipe(r, 0)

def test_shopping_remove():
    r1 = Recipe("Суп")
    r1.add_ingredient(Ingredient("Соль", 12, "кг"))
    r2 = Recipe("Пельмени")
    r2.add_ingredient(Ingredient("Сахар", 13, "кг"))
    s = ShoppingList()
    s.add_recipe(r1, 1)
    s.add_recipe(r2, 1)
    s.remove_recipe("Суп")
    result = s.get_list()
    assert len(result) == 1
    assert result[0].name == "Сахар"

def test_shopping_add_operator():
    r1 = Recipe("Суп")
    r1.add_ingredient(Ingredient("Соль", 12, "кг"))
    r2 = Recipe("Пельмени")
    r2.add_ingredient(Ingredient("Сахар", 13, "кг"))
    s1 = ShoppingList(); s1.add_recipe(r1, 1)
    s2 = ShoppingList(); s2.add_recipe(r2, 1)
    s3 = s1 + s2
    assert s3 is not s1
    assert len(s3.get_list()) == 2
    
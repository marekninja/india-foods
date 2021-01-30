import pandas as pd
import numpy as np
import copy

pd.read_csv('data/indian_food.csv')
india = pd.read_csv('data/indian_food.csv')
india = india.replace(-1, np.nan)
india = india.replace("-1", np.nan)
india.diet = india.diet.astype("category")
india.flavor_profile = india.flavor_profile.astype("category")
india.course = india.course.astype("category")
india.state = india.state.astype("category")
# india.region = india.region.astype("category")
india = india.fillna(india.mean().apply(np.ceil))
india = india.drop(['region'], axis=1)

def get_data():
    return india

def get_ingredients():
    ing = india.ingredients.apply(lambda x: x.split(',')).tolist()
    merged = [item.lstrip() for sublist in ing for item in sublist]
    return list(sorted(set(merged),key=str.lower))

def get_diet():
    return list(india.diet.cat.categories)

def get_course():
    return list(india.course.cat.categories)

def get_states():
    return list(india.state.cat.categories)

def get_regions():
    return list(india.region.cat.categories)

def get_flavors():
    return list(india.flavor_profile.cat.categories)

def get_preparation():
    return list(india.prep_time)

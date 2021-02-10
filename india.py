import pandas as pd
import numpy as np
import copy

india = pd.read_csv('data/india_prepared.csv')


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

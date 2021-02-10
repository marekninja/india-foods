import pandas as pd
import numpy as np
import copy

india = pd.read_csv('data/indian_food.csv')
india = india.replace(-1, np.nan)
india = india.replace("-1", np.nan)

india.diet = india.diet.astype("category")
india[['flavor_profile']] = india[['flavor_profile']].fillna(value="surprise")
india.flavor_profile = india.flavor_profile.astype("category")
india.course = india.course.astype("category")
india[['state']] = india[['state']].fillna(india[['state']].mode().iloc[0])
india.state = india.state.astype("category")
# india.region = india.region.astype("category")
india = india.fillna(india.mean().apply(np.ceil))
india = india.drop(['region'], axis=1)
india.ingredients = india.ingredients.str.lower()
india.to_csv('india_prepared.csv', index=False)
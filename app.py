from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load the dataset
data = pd.read_csv('indian_food.csv')

# Strip any whitespace from column names
data.columns = data.columns.str.strip()

# Fill NaN values in relevant columns to prevent issues
columns_to_check = ['ingredients', 'diet', 'flavor_profile', 'course', 'state', 'region', 'prep_time', 'cook_time']
for column in columns_to_check:
    if column in data.columns:
        data[column] = data[column].fillna('')

# Function to recommend food based on various filters
def recommend_food(ingredients=None, state=None, region=None, diet=None, flavor_profile=None, course=None):
    recommendations = []
    
    # Normalize inputs for comparison
    ingredients = [ingredient.lower().strip() for ingredient in ingredients.split(',')] if ingredients else []
    state = state.lower().strip() if state else None
    region = region.lower().strip() if region else None
    diet = diet.lower().strip() if diet else None
    flavor_profile = flavor_profile.lower().strip() if flavor_profile else None
    course = course.lower().strip() if course else None
    
    for index, row in data.iterrows():
        food_ingredients = row['ingredients'].lower().split(',')
        food_ingredients = [ingredient.strip() for ingredient in food_ingredients]

        # Check if all provided ingredients are in the food ingredients
        ingredient_match = all(ingredient in food_ingredients for ingredient in ingredients) if ingredients else True
        # Check state or region matches
        state_match = state in row['state'].lower() if state else True
        region_match = region in row['region'].lower() if region else True
        # Check diet matches
        diet_match = diet in row['diet'].lower() if diet else True
        # Check flavor profile matches
        flavor_match = flavor_profile in row['flavor_profile'].lower() if flavor_profile else True
        # Check course matches
        course_match = course in row['course'].lower() if course else True
        
        # If all criteria match, add to recommendations
        if ingredient_match and state_match and region_match and diet_match and flavor_match and course_match:
            recommendations.append({
                'name': row['name'],
                'prep_time': row['prep_time'],
                'cook_time': row['cook_time'],
                'diet': row['diet'],
                'flavor_profile': row['flavor_profile'],
                'course': row['course'],
                'state': row['state'],
                'region': row['region'],
            })

    return recommendations if recommendations else [{"name": "No recipes found."}]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    ingredients = request.form['ingredients']
    region = request.form['region']
    state = request.form['state']
    diet = request.form['diet']
    flavor_profile = request.form['flavor_profile']
    course = request.form['course']

    recommendations = recommend_food(ingredients=ingredients, state=state, region=region, 
                                      diet=diet, flavor_profile=flavor_profile, course=course)

    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)

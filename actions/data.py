from munch import Munch

# by default ingredients amounts are fixed for one person
recipes = {
            'Carbonara': Munch.fromDict({'ingredients': [
                {'name': 'egg yolks', 'amount': 2, 'unit': None},
                {'name': 'cheek lard', 'amount': 45, 'unit': 'grams'},
                {'name': 'Pecorino Romano cheese', 'amount': 40, 'unit': 'grams'},
                {'name': 'spaghetti', 'amount': 100, 'unit': 'grams'}
            ]}),
            'Amatriciana': Munch.fromDict({'ingredients': [
                {'name': 'tomato sauce', 'amount': 100, 'unit': 'grams'},
                {'name': 'cheek lard', 'amount': 45, 'unit': 'grams'},
                {'name': 'Pecorino Romano cheese', 'amount': 20, 'unit': 'grams'},
                {'name': 'spaghetti', 'amount': 100, 'unit': 'grams'}
            ]}),
            'Cacio e pepe': Munch.fromDict({'ingredients': [
                {'name': 'Pecorino Romano cheese', 'amount': 60, 'unit': 'grams'},
                {'name': 'spaghetti', 'amount': 100, 'unit': 'grams'},
                {'name': 'pepper', 'amount': None, 'unit': None}
            ]}),
            'Crepes': Munch.fromDict(
                {'ingredients': [
                    {'name': 'butter', 'amount': None, 'unit': None},
                    {'name': '00 flour', 'amount': 83, 'unit': 'grams'},
                    {'name': 'eggs', 'amount': 1, 'unit': None},
                    {'name': 'whole milk', 'amount': 167, 'unit': 'milliliters'}
                ]},
                {'steps': [
                    {'description': 'Break the eggs in a large bowl.'},
                    {'description': 'Pour the milk and whisk until they the eggs get incorporate in it.'},
                    {'description': 'Sift the flour over the bowl while mixing.'},
                    {'description': 'Whisk until you obtain a smooth batter.'},
                    {'description': 'Let the batter rest in the fridge for 30 minutes.'},
                    {'description': 'Take the batter out of the fridge and give it a quick mix.'},
                    {'description': 'Heat a pan on medium heat.'},
                    {'description': 'Grease the pan with some butter.'},
                    {'description': 'Pour roughly two table spoons of batter on the pan and swirl it around so the bottom of the pan is evenly coated.'},
                    {'description': 'Cook it for about 45 seconds until golden.'},
                    {'description': 'Use a palette to flip the crepe on the other side and cook it for about 30 seconds.'},
                    {'description': 'Slide the crepe on a plate to be served. Then you can cook another.'}
                ]}
            ),
            'Waffles': Munch.fromDict({'ingredients': [
                {'name': '00 flour', 'amount': 140, 'unit': 'grams'},
                {'name': 'eggs', 'amount': 3, 'unit': None},
                {'name': 'sugar', 'amount': 140, 'unit': 'grams'},
                {'name': 'salt', 'amount': 1, 'unit': 'teaspoon'},
                {'name': 'butter', 'amount': 110, 'unit': 'grams'},
                {'name': 'vanilla pods', 'amount': 1, 'unit': None},
                {'name': 'baking powder', 'amount': 1, 'unit': 'grams'}
            ]})
}
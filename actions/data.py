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
            'Muffins': Munch.fromDict({'ingredients': [
                {'name': 'butter', 'amount': 60, 'unit': 'grams'},
                {'name': 'sugar', 'amount': 66, 'unit': 'grams'},
                {'name': 'eggs', 'amount': 1, 'unit': None},
                {'name': 'pepper', 'amount': None, 'unit': None},
                {'name': '00 flour', 'amount': '132', 'unit': 'grams'},
                {'name': 'milk', 'amount': 68, 'unit': 'grams'},
                {'name': 'dark chocolate chips', 'amount': 50, 'unit': 'grams'},
                {'name': 'baking powder', 'amount': 5, 'unit': 'grams'},
                {'name': 'bicarbonate', 'amount': 0.5, 'unit': 'teaspoon'},
                {'name': 'salt', 'amount': None, 'unit': None}
            ]}),
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
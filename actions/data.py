from munch import Munch

# by default ingredients amounts are fixed for one person
recipes = {
            'Carbonara': Munch.fromDict({
                'ingredients': [
                    {'name': 'egg yolks', 'amount': 2, 'unit': None},
                    {'name': 'guanciale', 'amount': 45, 'unit': 'grams'},
                    {'name': 'Pecorino Romano cheese', 'amount': 40, 'unit': 'grams'},
                    {'name': 'spaghetti', 'amount': 100, 'unit': 'grams'},
                    {'name': 'black pepper', 'amount': None, 'unit': None},
                    {'name': 'salt', 'amount': 'as you prefer, but don\'t exagerate since the cheese is already salty', 'unit': None}
                ],
                'steps': [
                    {
                        'description': 'Fill a pot with water and put it on the heat to boil.\nAdd some salt to the water, but not too much since Pecorino is alreay a very salty cheese.',
                        'ingredients': [5]
                    },
                    {
                        'description': 'While you wait for the water to boil, remove the rind from the guanciale and then cut the guanciale in short strips.',
                        'ingredients': [1]
                    },
                    {
                        'description': 'Put the strips on a pan on medium heat for about two minutes, until they are brown and a bit crisp but not too much.\nNo oil nor butter is needed.',
                        'ingredients': [3]
                    },
                    {'description': 'When the guanciale is ready, put it on a plate to cool down. Leave the liquid fat lost by the guanciale in the pan.'},
                    {
                        'description': 'When the water will start boiling, add the spaghetti. Remember to stir it occasionally until about two minutes before tender.',
                        'ingredients': [3]
                    },
                    {
                        'description': 'Meanwhile, grate the Pecorino in a bowl and combine it with the egg yolks and pepper to obtain a smooth cream.\nAdd a table spoon of pasta cooking water if it is too firm.',
                        'ingredients': [2, 0, 4]
                    },
                    {'description': 'When the pasta is ready, still undercooked, drain it but reserve some cooking water.'},
                    {
                        'description': 'Put the pasta in the pan with the fat lost by the guanciale and half cup of pasta cooking water and turn on the heat.\nLet it simmer until cooked and add cooking water if it becomes too dry.',
                        'ingredients': [1]
                    },
                    {'description': 'When the pasta is ready, turn off the heat, add the guanciale and stir it vigorously for 30 seconds.'},
                    {'description': 'Now add the yolk and cheese cream and stir it vigorously again.'},
                    {
                        'description': 'Serve on a plate with some pepper and grated Pecorino on top.',
                        'ingredients': [2]
                    }
                ]
            }),
            'Amatriciana': Munch.fromDict({
                'ingredients': [
                    {'name': 'peeled tomatoes', 'amount': 100, 'unit': 'grams'},
                    {'name': 'guanciale', 'amount': 45, 'unit': 'grams'},
                    {'name': 'Pecorino Romano cheese', 'amount': 18, 'unit': 'grams'},
                    {'name': 'spaghetti', 'amount': 100, 'unit': 'grams'},
                    {'name': 'salt', 'amount': None, 'unit': None}
                ],
                'steps': [
                    {'description': 'Fill a pot with water and put it on the heat to boil.\nAdd some salt to the water.'},
                    {'description': 'While you wait for the water to boil, remove the rind from the guanciale and then cut the guanciale in short strips.'},
                    {'description': 'Put the strips on a pan on medium heat for about two minutes, until they are brown and a bit crisp but not too much.\nNo oil nor butter is needed.'},
                    {'description': 'When the guanciale is ready, put it on a plate to cool down. Leave the liquid fat lost by the guanciale in the pan.'},
                    {'description': 'When the water will start boiling, add the spaghetti. Remember to stir it occasionally until about two minutes before tender.'},
                    {'description': 'Put in the pan the peeled tomatoes, crush them by hand or using a tool and cook them for about 10 minutes.'},
                    {'description': 'Turn off the heat and add the guanciale and some salt.'},
                    {'description': 'When the pasta is ready, still undercooked, drain it but reserve some cooking water.'},
                    {'description': 'Add the spaghetti directly in the pan with sauce.\nLet it cook and add just a bit of pasta cooking water if needed.'},
                    {'description': 'When the pasta is ready, serve it on a plate with some grated Pecorino on top.'}
                ]
            }),
            'Cacio e pepe': Munch.fromDict({
                'ingredients': [
                    {'name': 'Pecorino Romano cheese', 'amount': 60, 'unit': 'grams'},
                    {'name': 'spaghetti', 'amount': 100, 'unit': 'grams'},
                    {'name': 'black pepper', 'amount': None, 'unit': None},
                    {'name': 'salt', 'amount': None, 'unit': None}
                ],
                'steps': [
                    {'description': 'Fill a pot with water and put it on the heat to boil.\nAdd some salt to the water, but not too much since Pecorino is alreay a very salty cheese.'},
                    {'description': 'When the water will start boiling, add the spaghetti. Remember to stir it occasionally until about two minutes before tender.'},
                    {'description': 'While you wait for the pasta to cook, grate the Pecorino.'},
                    {'description': 'Put in a pan some pasta cooking water with a generous amount of pepper at medium heat.'},
                    {'description': 'When the pasta is ready, still undercooked, drain it but reserve the cooking water.'},
                    {'description': 'Add the pasta on the pan and let it finish cooking with the pepper.\nAdd one or two table spoons of pasta cooking water if it seems too dry.'},
                    {'description': 'Meanwhile, the grated Pecorino in a bowl and add half cup of pasta cooking water.'},
                    {'description': 'Mix until you obtain a smooth cream. Add more water if needed.'},
                    {'description': 'When the pasta si ready turn off the heat and add the Pecorino cream. Mix vigorously.'},
                    {'description': 'Serve on a plate with a bit more Pecorino and pepper on top.'}
                ]
            }),
            'Crepes': Munch.fromDict({
                'ingredients': [
                    {'name': 'butter', 'amount': None, 'unit': None},
                    {'name': '00 flour', 'amount': 83, 'unit': 'grams'},
                    {'name': 'eggs', 'amount': 1, 'unit': None},
                    {'name': 'whole milk', 'amount': 167, 'unit': 'milliliters'}
                ],
                'steps': [
                    {'description': 'Break the eggs in a large bowl.'},
                    {'description': 'Pour the milk and whisk until the eggs get incorporated in it.'},
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
                ]
            })
}
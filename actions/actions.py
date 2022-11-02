# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from math import ceil
from typing import Any, Optional, Text, Dict, List
from munch import Munch
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, FollowupAction, EventType
from difflib import SequenceMatcher
import numpy as np
from regex import R

from actions.data import recipes

# active recipe state


class State():
    recipe_key = None
    num_people = None
    step_idx = None


state = State()
shoplist = list()
pagelen = 5


def say(dispatcher: CollectingDispatcher, message: str) -> None:
    dispatcher.utter_message(text=message)


def utt(dispatcher: CollectingDispatcher, utter: str) -> None:
    dispatcher.utter_message(response=utter)


def similarity_score(seq1: str, seq2: str) -> float:
    return SequenceMatcher(a=seq1.lower(), b=seq2.lower()).ratio()


def seek(tracker: Tracker, dispatcher: CollectingDispatcher, delta: int):

    if state.recipe_key is None:
        # no recipe is currently running
        utt(dispatcher, 'utter_no_recipe_running')
        utt(dispatcher, 'utter_start_from_here')
        return []

    steps = recipes[state.recipe_key].steps

    # user wants to go back
    state.step_idx = max(-1, state.step_idx + delta)

    if state.step_idx < 0:
        # step negative: ingredients
        return [FollowupAction(name="action_list_ingredients")]
    elif state.step_idx < len(steps):
        # step positive and inside recipe boundaries
        step = steps[state.step_idx]
        say(dispatcher, step.description)

        return []
    else:
        # recipe completed
        utt(dispatcher, 'utter_recipe_completed')
        utt(dispatcher, 'utter_start_from_here')
        return []


def format_ingredient(ing, num, description=False):
    out = ''

    if ing.amount is not None and not isinstance(ing.amount, str):
        # if the ingredient amount has been specified, it's the numerical value, use it
        # otherwise the amount is either None or a string representing some description

        if ing.unit is not None:
            # both amount and unit: 30 grams of cheese
            out = f"{ing.amount * num} {ing.unit} of {ing.name}"
        else:
            # just the amount: 2 egg yolks
            out = f"{ing.amount * num} {ing.name}"
    else:
        # no amount specified, or a string

        if description:
            # if amount is None then the user can use the ingredient as he/she prefers
            # if it's not None then it's a short description
            out = 'to your preference' if ing.amount is None else ing.amount
        else:
            # not called by the how_much action, no need for additional information
            # the ingredient doesn't have an amount or unit
            out = str(ing.name)
    return out


# class ActionProposeRecipes(Action):

#     def name(self) -> Text:
#         return "action_propose_recipes"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         say(dispatcher, "Here are some recipes you can try:")
#         description = ", ".join([r["name"] for r in recipes])
#         say(dispatcher, f"{description}")

#         return []

# SELECT RECIPE TO COOK
class AskRecipe(Action):
    '''
    the name follows the convention action_ask_<form_name>_<slot_name>
    thus this action will be activated whenever <slot_name> will be required
    '''

    def name(self) -> Text:
        return "action_ask_recipe"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        utt(dispatcher, 'utter_propose_recipes')
        description = ", ".join([r for r in recipes.keys()])
        say(dispatcher, f"{description}")
        utt(dispatcher, 'utter_choose_one_recipe')

        return [SlotSet('recipe', None), SlotSet('number', None)]


class ActionValidateSelectRecipeForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_select_recipe_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:
        slots_mapped_in_domain.insert(1, 'number')
        return slots_mapped_in_domain

    def validate_recipe(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        query = tracker.get_slot('recipe')

        sim = np.array([similarity_score(query, r) for r in recipes.keys()])
        idx = np.argmax(sim)

        if sim[idx] >= 0.8:
            matched_recipe = list(recipes.keys())[idx]
            # say(dispatcher, f"I understand you want to cook {matched_recipe}")
        else:
            matched_recipe = None
            say(dispatcher, "I don't know this recipe or i didn't understand the name correctly.\nCan you repeat or try another recipe?")

        return {"recipe": matched_recipe}

    async def extract_number(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:

        # 'entities': [{'entity': 'recipe', 'start': 11, 'end': 20, 'confidence_entity': 0.999663591384887, 'value': 'carbonara', 'extractor': 'DIETClassifier'}]

        ents = tracker.latest_message['entities']
        ents_names = [ent['entity'] for ent in ents]
        text = tracker.latest_message['text']

        # if the number slot was already set, skip all this
        # otherwise it will get set to None and rasa will ask
        # the user a number again, in an endless cycle
        if tracker.get_slot('number') is None:
            if 'number' in ents_names:
                # if a number entity was extracted, use that value
                num_idx = ents_names.index('number')
                return {"number": ents[num_idx]['value']}
            elif (' me' in text or 'me ' in text):
                # if no number entity was present, but the user
                # said something along the lines of "just for me"
                # use 1 as value
                return {"number": '1'}
            else:
                # if no number entity was extracted
                # and the user is not cooking for him/herself
                # leave the slot empty, no number was provided
                return {"number": None}
        return {}

    def validate_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        num = tracker.get_slot('number')

        if num is None:
            return {"number": None}
        elif num.isdigit():
            return {"number": num}
        else:
            say(dispatcher, 'Sorry I didn\'t understand.')
            return {"number": None}

    def validate_confirm_recipe_form(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        return {"confirm_recipe_form": tracker.get_slot('confirm_recipe_form')}


class ActionSubmitRecipeForm(Action):

    def name(self) -> Text:
        return "action_submit_recipe_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        confirm = tracker.get_slot('confirm_recipe_form')

        if not confirm:
            return [SlotSet("recipe", None), SlotSet("number", None), SlotSet("confirm_recipe_form", None), FollowupAction(name="action_ask_recipe")]

        state.recipe_key = tracker.get_slot('recipe')
        state.num_people = int(tracker.get_slot('number'))
        state.step_idx = -1

        return [SlotSet("recipe", None), SlotSet("number", None), SlotSet("confirm_recipe_form", None), FollowupAction(name="action_list_ingredients")]


class ActionListIngredients(Action):

    def name(self) -> Text:
        return "action_list_ingredients"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if state.recipe_key is None:
            # no recipe is currently running
            utt(dispatcher, 'utter_no_recipe_running')
            utt(dispatcher, 'utter_start_from_here')
            return []

        ings = recipes[state.recipe_key].ingredients

        utt(dispatcher, "utter_present_ingredients")

        for ing in ings:
            say(dispatcher, format_ingredient(ing, state.num_people))

        utt(dispatcher, 'utter_user_ready')

        return []


class ActionNextStep(Action):

    def name(self) -> Text:
        return "action_next_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        utt(dispatcher, 'utter_next_step')
        return seek(tracker, dispatcher, 1)


class ActionRepeat(Action):

    def name(self) -> Text:
        return "action_repeat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        steps = recipes[state.recipe_key].steps

        # user wants to repeat current step
        say(dispatcher, 'Of course')

        if state.step_idx < 0:
            return [FollowupAction(name="action_list_ingredients")]
        else:
            step = steps[state.step_idx]
            say(dispatcher, step.description)

            return []


class ActionBackwardStep(Action):

    def name(self) -> Text:
        return "action_backward_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        delta = int(tracker.get_slot('number')) if tracker.get_slot(
            'number') is not None else 1

        return seek(tracker, dispatcher, -delta)


class ActionSkipStep(Action):

    def name(self) -> Text:
        return "action_skip_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        delta = tracker.get_slot('number')

        if delta is not None:
            delta = int(delta)
            utt(dispatcher, 'utter_skip_steps')
            return seek(tracker, dispatcher, delta)
        elif 'this step' in tracker.latest_message['text']:
            utt(dispatcher, 'utter_next_step')
            return seek(tracker, dispatcher, 1)
        else:
            say(dispatcher, 'Sorry, I didn\'t understand how many steps you\'d like to skip')
            return []


class ActionHowMuchIng(Action):

    def name(self) -> Text:
        return "action_how_much_ing"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if state.recipe_key is None:
            utt(dispatcher, 'utter_no_recipe_running')
            utt(dispatcher, 'utter_start_from_here')
            return [SlotSet('ingredient', None)]


        # requested ingredient
        query = tracker.get_slot('ingredient')

        # current state
        ings = recipes[state.recipe_key].ingredients
        step = recipes[state.recipe_key].steps[state.step_idx]

        if query is not None:
            sim = np.array([similarity_score(query, i.name) for i in ings])
            idx = np.argmax(sim)

            if sim[idx] >= 0.8:
                matched_ing = ings[idx]
                # pass step index because the ingredient list is treated differently from the steps
                say(dispatcher, format_ingredient(
                    matched_ing, state.num_people, description=True))
            else:
                utt(dispatcher, 'utter_repeat_ing')
        elif len(step.ingredients) == 1:
            # its the only ingredient used
            ing_idx = step.ingredients[0]
            ing = ings[ing_idx]
            say(dispatcher, format_ingredient(
                ing, state.num_people, description=True))
        else:
            # there are more than 1 ingredient in the list
            # ask which one the user is asking about
            names = [ings[idx].name for idx in step.ingredients]
            say(dispatcher, f'In this step {len(names)} ingredients are used:')
            say(dispatcher, ', '.join(names))

            utt(dispatcher, 'utter_specify_ingredient')

        return [SlotSet('ingredient', None)]


class ActionAddCurrentRecipeToList(Action):
    # adds active recipe to the shopping list

    def name(self) -> Text:
        return "action_add_current_recipe_to_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if state.recipe_key is None:
            # no recipe is currently running
            # run a form to select the recipe to add
            return [FollowupAction(name="action_ask_recipe")]

        ings = recipes[state.recipe_key].ingredients

        shoplist.extend([format_ingredient(ing, state.num_people)
                        for ing in ings])
        print(shoplist)

        return [SlotSet("recipe", None), SlotSet("number", None)]


# SELECT RECIPE TO SHOP
# this form required the same exact slots that the select_recipe form requires
# so, the same action to list the recipes and the same utterances will be used
# but the submit action will be different, since the goal of the form is different
class ActionValidateSelectRecipeShopForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_select_recipe_shop_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:
        slots_mapped_in_domain.insert(1, 'number')
        return slots_mapped_in_domain

    def validate_recipe(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        query = tracker.get_slot('recipe')

        sim = np.array([similarity_score(query, r) for r in recipes.keys()])
        idx = np.argmax(sim)

        if sim[idx] >= 0.8:
            matched_recipe = list(recipes.keys())[idx]
        else:
            matched_recipe = None
            say(dispatcher, "I don't know this recipe or i didn't understand the name correctly.\nCan you repeat or try another recipe?")

        return {"recipe": matched_recipe}

    async def extract_number(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:

        # 'entities': [{'entity': 'recipe', 'start': 11, 'end': 20, 'confidence_entity': 0.999663591384887, 'value': 'carbonara', 'extractor': 'DIETClassifier'}]

        ents = tracker.latest_message['entities']
        ents_names = [ent['entity'] for ent in ents]
        text = tracker.latest_message['text']

        # if the number slot was already set, skip all this
        # otherwise it will get set to None and rasa will ask
        # the user a number again, in an endless cycle
        if tracker.get_slot('number') is None:
            if 'number' in ents_names:
                # if a number entity was extracted, use that value
                num_idx = ents_names.index('number')
                return {"number": ents[num_idx]['value']}
            elif (' me' in text or 'me ' in text):
                # if no number entity was present, but the user
                # said something along the lines of "just for me"
                # use 1 as value
                return {"number": '1'}
            else:
                # if no number entity was extracted
                # and the user is not cooking for him/herself
                # leave the slot empty, no number was provided
                return {"number": None}
        return {}

    def validate_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        num = tracker.get_slot('number')

        if num is None:
            return {"number": None}
        elif num.isdigit():
            return {"number": num}
        else:
            say(dispatcher, 'Sorry I didn\'t understand.')
            return {"number": None}

    def validate_confirm_recipe_form(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        return {"confirm_recipe_form": tracker.get_slot('confirm_recipe_form')}


class ActionSubmitRecipeToShopForm(Action):

    def name(self) -> Text:
        return "action_submit_recipe_shop_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        confirm = tracker.get_slot('confirm_recipe_form')

        if not confirm:
            return [SlotSet("recipe", None), SlotSet("number", None), SlotSet("confirm_recipe_form", None), FollowupAction(name="action_ask_recipe")]

        recipe_key_shop = tracker.get_slot('recipe')
        ings = recipes[recipe_key_shop].ingredients
        num_shop = int(tracker.get_slot('number'))

        shoplist.extend([format_ingredient(ing, num_shop) for ing in ings])
        utt(dispatcher, 'utter_recipe_added_to_list')

        return [SlotSet("recipe", None), SlotSet("number", None), SlotSet("confirm_recipe_form", None)]


class ActionShowShoppingList(Action):

    def name(self) -> Text:
        return "action_show_shopping_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        page = tracker.get_slot('number')

        # validate for typos
        if page is not None:
            if page.isdigit():
                page = int(page)
            else:
                say(dispatcher, 'I couldn\'t understand the page you requested so I\'ll show you page 1.')
                page = 1
        else:
            page = 1

        if len(shoplist) > 0:
            totpages = ceil(len(shoplist)/pagelen)

            elems = shoplist[(page-1)*pagelen:page*pagelen]

            if len(elems) > 0:
                say(dispatcher,
                    f'Showing page {page} of {totpages} of your shopping list.\nYou can ask me what I can do with the shopping list at any time.')

                for idx, elem in enumerate(elems):
                    say(dispatcher, f'{idx+1+((page-1)*pagelen)} {elem}')
            else:
                say(dispatcher,
                    f'Page {page} doesn\'t exist, your shopping list has {totpages} pages')
        else:
            say(dispatcher, 'Your shopping list is empty')

        return [SlotSet('number', None)]


class ActionRemoveShopItem(Action):

    def name(self) -> Text:
        return "action_remove_shop_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        item_id = tracker.get_slot('number')

        if item_id is not None and item_id.isdigit():
            item_id = int(item_id)
            item = shoplist.pop(item_id)
            say(dispatcher, f'I reomved {item} from your shopping list')
        else:
            say(dispatcher, 'I\'m sorry I coudn\'t understand')

        return [SlotSet('number', None)]


class ActionAddShopIng(Action):

    def name(self) -> Text:
        return "action_add_shop_ing"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        amount = tracker.get_slot('number')
        unit = tracker.get_slot('unit')
        name = tracker.get_slot('ingredient')
        
        if amount is not None:
            if amount.isdigit():
                amount = int(amount)
            else:
                try:
                    amount = float(amount)
                except:
                    pass

        if name is not None:
            ing = Munch.fromDict({'name': name, 'unit': unit, 'amount': amount})
            shoplist.append(format_ingredient(ing, 1))
        else:
            say(dispatcher, 'I coudn\'t understand what ingredient you\'d like to add to your list. Can you repeat?')
        
        return [SlotSet('number', None), SlotSet('unit', None), SlotSet('ingredient', None)]

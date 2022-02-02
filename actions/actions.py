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

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, FollowupAction, EventType
from difflib import SequenceMatcher
import numpy as np

from actions.data import recipes


def say(dispatcher: CollectingDispatcher, message: str) -> None:
    dispatcher.utter_message(text=message)

def resp(dispatcher: CollectingDispatcher, utter: str) -> None:
    dispatcher.utter_message(response=utter)


def similarity_score(seq1: str, seq2: str) -> float:
    return SequenceMatcher(a=seq1.lower(), b=seq2.lower()).ratio()


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


class AskSelectRecipeFormRecipe(Action):
    def name(self) -> Text:
        return "action_ask_select_recipe_form_recipe"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        
        resp(dispatcher, 'utter_propose_recipes')
        description = ", ".join([r for r in recipes.keys()])
        say(dispatcher, f"{description}")
        resp(dispatcher, 'utter_choose_one_recipe')

        return []


class ActionValidateSelectRecipeForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_select_recipe_form"

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
    
    def validate_number_people(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        num = tracker.get_slot('number_people')
        # say(dispatcher, f"Received: {num}")
        return {"number_people": num}

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
            return [SlotSet("recipe", None), SlotSet("number_people", None), SlotSet("confirm_recipe_form", None), FollowupAction(name="select_recipe_form")]

        return [FollowupAction(name="action_list_ingredients")]


class ActionListIngredients(Action):

    def name(self) -> Text:
        return "action_list_ingredients"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        recipe_key = tracker.get_slot('recipe')
        ings = recipes[recipe_key].ingredients
        num = int(tracker.get_slot('number_people'))

        resp(dispatcher, "utter_present_ingredients")

        for ing in ings:
            if not ing.amount is None:
                if not ing.unit is None:
                    # both amount and unit: 30 grams of cheese
                    say(dispatcher, f"{ing.amount*num} {ing.unit} of {ing.name}")
                else:
                    # just the amount: 2 egg yolks
                    say(dispatcher, f"{ing.amount*num} {ing.name}")
            else:
                # none of the two: pepper to your liking
                say(dispatcher, f"{ing.name} to your liking")

        return []
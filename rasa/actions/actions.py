# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        # return "action_course_info"

        return "action_person_info"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"If you are asking about {tracker.slots['person']}, Best Human Ever!!! ;-) ")
        # dispatcher.utter_message(text=f"If you are asking about {tracker.slots['course']}, (COMP 474): Prerequisite: COMP 352 or COEN 352. Rule-based expert systems, "
        #                               f"blackboard architecture, and agent-based. Knowledge acquisition and representation. Uncertainty and conflict resolution."
        #                               f" Reasoning and explanat!!! ;-) ")


        return []

class ActionCourse(Action):

    def name(self) -> Text:
        return "action_course_info"

        #return "action_person_info"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #dispatcher.utter_message(text=f"If you are asking about {tracker.slots['person']}, Best Human Ever!!! ;-) ")
        dispatcher.utter_message(text=f"If you are asking about {tracker.slots['course']}, (COMP 474): Prerequisite: COMP 352 or COEN 352. Rule-based expert systems, "
                                      f"blackboard architecture, and agent-based. Knowledge acquisition and representation. Uncertainty and conflict resolution."
                                      f" Reasoning and explanat!!! ;-) ")


        return []

class ActionCourseTopic(Action):

    def name(self) -> Text:
        return "action_course_topic"

        #return "action_person_info"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #dispatcher.utter_message(text=f"If you are asking about {tracker.slots['person']}, Best Human Ever!!! ;-) ")
        dispatcher.utter_message(text=f"If you are asking about {tracker.slots['topic']}, the following courses based on frequencies of the topic are follows: COMP474, COMP472")

        return []

class ActionCourseEvent(Action):

    def name(self) -> Text:
        return "action_course_event"

        #return "action_person_info"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #dispatcher.utter_message(text=f"If you are asking about {tracker.slots['person']}, Best Human Ever!!! ;-) ")
        dispatcher.utter_message(text=f"If you are asking about {tracker.slots['event']}, the event includes all topices, such as rdf format, open data link...) ")

        return []
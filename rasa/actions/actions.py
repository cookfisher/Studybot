# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import requests
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

        # request server

        query_var = """
                Prefix dbr: <http://dbpedia.org/resource/>
                Prefix focu: <http://focu.io/schema#>
                Prefix focudata: <http://focu.io/data#>
                Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                Prefix teach: <http://linkedscience.org/teach/ns#>
                Prefix vivo: <http://vivoweb.org/ontology/core#>
                Prefix xsd: <http://www.w3.org/2001/XMLSchema#>

                SELECT (COUNT(distinct ?course) as ?count)
                WHERE
                {
                    ?course a teach:Course.
                }
            """

        response = requests.post('http://localhost:3030/focu/query', data={'query': query_var})
        res = response.json()
        print('res is',res)
        res_1= res['results']['bindings']
        print('res after removing binding')
        ans = []

        print(res['results']['bindings'])
        dispatcher.utter_message(text=f"If you are asking about {tracker.slots['course']}, {res_1}")
        #dispatcher.utter_message(text=f"If you are asking about {tracker.slots['person']}, Best Human Ever!!! ;-) ")
        # dispatcher.utter_message(text=f"If you are asking about {tracker.slots['course']}, (COMP 474): Prerequisite: COMP 352 or COEN 352. Rule-based expert systems, "
        #                               f"blackboard architecture, and agent-based. Knowledge acquisition and representation. Uncertainty and conflict resolution."
        #                               f" Reasoning and explanat!!! ;-) ")

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
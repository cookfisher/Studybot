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
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")

        return []


class ActionPerson(Action):

    def name(self) -> Text:
        return "action_person_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f"If you are asking about {tracker.slots['person']}, Best Human Ever!!! ;-) ")

        return []


# 1. How many courses in each subject?
class Query1(Action):
    def name(self) -> Text:
        return "query_1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query_var = """
               PREFIX dbo: <http://dbpedia.org/ontology/>
               Prefix aiiso: <http://purl.org/vocab/aiiso/schema#>
               Prefix dbr: <http://dbpedia.org/resource/>
               Prefix focu: <http://focu.io/schema#>
               Prefix focudata: <http://focu.io/data#>
               Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
               Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               Prefix teach: <http://linkedscience.org/teach/ns#>
               Prefix vivo: <http://vivoweb.org/ontology/core#>
               Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
               SELECT ?suject_name (COUNT(distinct ?course) as ?course_number)
               WHERE
               {
                 ?course a teach:Course.
                 ?course focu:subject ?course_subject.
                 ?course_subject a focu:Subject.
                 ?course_subject aiiso:name ?suject_name.
               }
               GROUP BY ?suject_name
            """
        response = requests.post('http://localhost:3030/focu/sparql', data={'query': query_var})
        res = response.json()
        ans = []
        for row in res['results']['bindings']:
            ans.append([row['suject_name']['value'], row['course_number']['value']])

        dispatcher.utter_message(
            text=f"All courses with its subjects are listed as following: {ans}, HaHa, there are so many but it is just what you asked (^-^)")

        return []


# 2. Which lectures does course COMP474 have?
class Query2(Action):
    def name(self) -> Text:
        return "query_2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # query body
        # entity com474
        query_var = """
                PREFIX dbo: <http://dbpedia.org/ontology/>
                Prefix aiiso: <http://purl.org/vocab/aiiso/schema#>
                Prefix dbr: <http://dbpedia.org/resource/>
                Prefix focu: <http://focu.io/schema#>
                Prefix focudata: <http://focu.io/data#>
                Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                Prefix teach: <http://linkedscience.org/teach/ns#>
                Prefix vivo: <http://vivoweb.org/ontology/core#>
                Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?course_title ?lecture_name
                WHERE
                {
                  focudata:COMP474 teach:courseTitle ?course_title.
                  ?lecture focu:offeredIn focudata:COMP474.
                  ?lecture aiiso:name ?lecture_name.
                  ?lecture aiiso:code ?lecture_code.
                }
                ORDER BY ?lecture_code
            """
        response = requests.post('http://localhost:3030/focu/sparql', data={'query': query_var})
        res = response.json()
        ans = []
        for row in res['results']['bindings']:
            ans.append(row['lecture_name']['value'])
        dispatcher.utter_message(text=f"COMP474 have the following lectures: {ans}")

        return []


# 3. Which topics are associated with course COMP472?
class Query3(Action):
    def name(self) -> Text:
        return "query_3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # query body
        # entity com472
        query_var = """
                Prefix aiiso: <http://purl.org/vocab/aiiso/schema#>
                Prefix dbr: <http://dbpedia.org/resource/>
                Prefix focu: <http://focu.io/schema#>
                Prefix focudata: <http://focu.io/data#>
                Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                Prefix teach: <http://linkedscience.org/teach/ns#>
                Prefix vivo: <http://vivoweb.org/ontology/core#>
                Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?topics
                WHERE
                {
                  ?topics focu:topicAssociateWith focudata:COMP472.
                }
            """
        response = requests.post('http://localhost:3030/focu/sparql', data={'query': query_var})
        res = response.json()
        ans = []
        for row in res['results']['bindings']:
            ans.append(row['topics']['value'])
        dispatcher.utter_message(text=f"The course COMP472 is associated with the following topics {ans}")

        return []


# 4. Which courses have the subject COMP?
class Query4(Action):
    def name(self) -> Text:
        return "query_4"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query_var = """
                Prefix aiiso: <http://purl.org/vocab/aiiso/schema#>
                Prefix dbr: <http://dbpedia.org/resource/>
                Prefix focu: <http://focu.io/schema#>
                Prefix focudata: <http://focu.io/data#>
                Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                Prefix teach: <http://linkedscience.org/teach/ns#>
                Prefix vivo: <http://vivoweb.org/ontology/core#>
                Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?course
                WHERE
                {
                  ?course a teach:Course.
                  ?course focu:subject focudata:COMP .
                }
            """
        response = requests.post('http://localhost:3030/focu/sparql', data={'query': query_var})
        res = response.json()
        ans = []
        for row in res['results']['bindings']:
            ans.append(row['course']['value'])
        dispatcher.utter_message(text=f"The following courses have the subject COMP: {ans}")

        return []


# 5. What’s the content of the lectures of COMP474?
class Query5(Action):
    def name(self) -> Text:
        return "query_5"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query_var = """
                Prefix aiiso: <http://purl.org/vocab/aiiso/schema#>
                Prefix dbr: <http://dbpedia.org/resource/>
                Prefix focu: <http://focu.io/schema#>
                Prefix focudata: <http://focu.io/data#>
                Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                Prefix teach: <http://linkedscience.org/teach/ns#>
                Prefix vivo: <http://vivoweb.org/ontology/core#>
                Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?lecture ?name ?content
                WHERE
                {
                  ?lecture aiiso:name ?name.
                  ?lecture focu:offeredIn focudata:COMP474 .
                  ?lecture focu:content ?content.
                  ?lecture aiiso:code ?lecture_code.
                }
                ORDER BY ?lecture_code
            """
        response = requests.post('http://localhost:3030/focu/sparql', data={'query': query_var})
        res = response.json()
        ans = []
        for row in res['results']['bindings']:
            ans.append([row['lecture']['value'], row['name']['value'], row['content']['value']])
        dispatcher.utter_message(text=f"The content of the lectures of COMP474 has the following contents : [ans] ")

        return []


# 6. What’s the course description of COMP472?
class Query6(Action):
    def name(self) -> Text:
        return "query_6"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query_var = """
                Prefix aiiso: <http://purl.org/vocab/aiiso/schema#>
                Prefix dbr: <http://dbpedia.org/resource/>
                Prefix focu: <http://focu.io/schema#>
                Prefix focudata: <http://focu.io/data#>
                Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                Prefix teach: <http://linkedscience.org/teach/ns#>
                Prefix vivo: <http://vivoweb.org/ontology/core#>
                Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?course_title ?description
                WHERE
                {
                  focudata:COMP472 teach:courseTitle ?course_title.
                  focudata:COMP472 teach:courseDescription ?description.

                }
            """
        response = requests.post('http://localhost:3030/focu/sparql', data={'query': query_var})
        res = response.json()
        ans = []
        for row in res['results']['bindings']:
            ans.append([row['course_title']['value'], row['description']['value']])
        dispatcher.utter_message(text=f"The course description of COMP472 is {ans}")

        return []


# 7. In which lectures is the subject “Knowledge Graph” covered?
class Query7(Action):
    def name(self) -> Text:
        return "query_7"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query_var = """
                Prefix aiiso: <http://purl.org/vocab/aiiso/schema#>
                Prefix dbr: <http://dbpedia.org/resource/>
                Prefix focu: <http://focu.io/schema#>
                Prefix focudata: <http://focu.io/data#>
                Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                Prefix teach: <http://linkedscience.org/teach/ns#>
                Prefix vivo: <http://vivoweb.org/ontology/core#>
                Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?subject_name ?lecture ?lecture_name
                WHERE
                {
                  focudata:Knowledge_Graph aiiso:name ?subject_name.
                  focudata:Knowledge_Graph focu:topicAssociateWith ?lecture.
                  ?lecture aiiso:name ?lecture_name.
                }
            """
        response = requests.post('http://localhost:3030/focu/sparql', data={'query': query_var})
        res = response.json()
        ans = []
        subject_name = []
        for row in res['results']['bindings']:
            ans.append([row['lecture']['value'], ' named ', row['lecture_name']['value']])
            subject_name = row['subject_name']['value']
        dispatcher.utter_message(text=f"{ans} cover the subject of {subject_name}")

        return []


# 8. What’s the lab content for labs in COMP474?
class Query8(Action):
    def name(self) -> Text:
        return "query_8"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query_var = """
                Prefix aiiso: <http://purl.org/vocab/aiiso/schema#>
                Prefix dbr: <http://dbpedia.org/resource/>
                Prefix focu: <http://focu.io/schema#>
                Prefix focudata: <http://focu.io/data#>
                Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                Prefix teach: <http://linkedscience.org/teach/ns#>
                Prefix vivo: <http://vivoweb.org/ontology/core#>
                Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?lab ?name ?content
                WHERE
                {
                  ?lecture focu:offeredIn focudata:COMP474 .
                  ?lab focu:labAssociatedWith ?lecture.
                  ?lab aiiso:name ?name.
                  ?lab aiiso:code ?lab_code.
                  ?lab focu:content ?content.
                }
                ORDER BY ?lab_code
            """
        response = requests.post('http://localhost:3030/focu/sparql', data={'query': query_var})
        res = response.json()
        ans = []
        for row in res['results']['bindings']:
            ans.append(
                [row['lab']['value'], ' named ', row['name']['value'], ' has the content of ', row['content']['value']])
        dispatcher.utter_message(text=f"The lab content for the labs in COMP474 are the following: {ans}")

        return []


# 9. What’s the course outline of COMP474?
class Query9(Action):
    def name(self) -> Text:
        return "query_9"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query_var = """
                Prefix aiiso: <http://purl.org/vocab/aiiso/schema#>
                Prefix dbr: <http://dbpedia.org/resource/>
                Prefix focu: <http://focu.io/schema#>
                Prefix focudata: <http://focu.io/data#>
                Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                Prefix teach: <http://linkedscience.org/teach/ns#>
                Prefix vivo: <http://vivoweb.org/ontology/core#>
                Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?course_title ?course_outline
                WHERE
                {
                  focudata:COMP474 teach:courseTitle ?course_title.
                  focudata:COMP474 focu:outline ?course_outline.

                }
            """
        response = requests.post('http://localhost:3030/focu/sparql', data={'query': query_var})
        res = response.json()
        ans = []
        for row in res['results']['bindings']:
            ans.append([row['course_title']['value'], row['course_outline']['value']])
        dispatcher.utter_message(text=f"The course outline of COMP474 is {ans}")

        return []


# 10. What’s the DBpedia link for each topic?
class Query10(Action):
    def name(self) -> Text:
        return "query_10"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query_var = """
                Prefix aiiso: <http://purl.org/vocab/aiiso/schema#>
                Prefix dbr: <http://dbpedia.org/resource/>
                Prefix focu: <http://focu.io/schema#>
                Prefix focudata: <http://focu.io/data#>
                Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                Prefix teach: <http://linkedscience.org/teach/ns#>
                Prefix vivo: <http://vivoweb.org/ontology/core#>
                Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?topic ?topic_name ?dbpedia_link
                WHERE
                {
                  ?topic a focu:Topic.
                  ?topic aiiso:name ?topic_name.
                  ?topic rdfs:seeAlso ?dbpedia_link.
                }
                LIMIT 25
            """
        response = requests.post('http://localhost:3030/focu/sparql', data={'query': query_var})
        res = response.json()
        ans = []
        for row in res['results']['bindings']:
            ans.append([row['topic_name']['value'], ' with link of ', row['dbpedia_link']['value']])
        dispatcher.utter_message(
            text=f"The DBpedia links for each topic are following: {ans}... There are so many, and I only list the first 25 of them, and if I list all of them, the console will crash (^-^)")

        return []
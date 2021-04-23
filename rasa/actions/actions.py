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
# import spacy
# from spacy.matcher import Matcher

def query(pass_query):
    # request server
    query_var = pass_query
    response = requests.post('http://localhost:3030/focu/query', data={'query': query_var})
    res = response.json()
    res_1 = res['results']['bindings']
    print(res['results']['bindings'])
    return res_1

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

# question 2. course description
class ActionCourse(Action):

    def name(self) -> Text:
        return "action_course_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # print('course is ', tracker.slots['course'])
        chosen_course = tracker.slots['course']
        # request server
        q1 = """
                Prefix dbr: <http://dbpedia.org/resource/>
                Prefix focu: <http://focu.io/schema#>
                Prefix focudata: <http://focu.io/data#>
                Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                Prefix teach: <http://linkedscience.org/teach/ns#>
                Prefix vivo: <http://vivoweb.org/ontology/core#>
                Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?description
                WHERE
                {focudata:"""
        q2 = """teach:courseDescription ?description.}
            """
        query_var = q1 + chosen_course + ' ' + q2

        json_return = query(query_var)
        result = []
        for item in json_return:
            result.append(item['description']['value'])
        dispatcher.utter_message(text=f"If you are asking about {tracker.slots['course']}, the results are as follows:{result}")

        return []

# question 4. which courses cover this topic
class ActionCourseTopic(Action):

    def name(self) -> Text:
        return "action_course_topic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        chosen_topic = tracker.slots['topic']
        # print('the slots name is', tracker.slots['topic'])

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
            {{
              focudata:{t} focu:topicAssociateWith ?course. 
            }}
        """.format(t=chosen_topic)

        json_return = query(query_var)
        result = []
        for item in json_return:
            result.append(item['course']['value'])

        dispatcher.utter_message(text=f"If you are asking about {chosen_topic}, the courses are as follows: ,{result}")

        return []


#question  3. what topics are covered in lab
class ActionCourseEvent(Action):

    def name(self) -> Text:
        return "action_course_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        chosen_type = tracker.slots['event']
        chosen_course = tracker.slots['course']
        # print(chosen_course)
        # print('chosen type',chosen_type)
        chosen_event = chosen_course+'_'+chosen_type
        # print('the event name is',chosen_event)

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
            {{
              focudata:{t} focu:topicAssociateWith ?course.
            }}
        """.format(t=chosen_event)

        json_return = query(query_var)
        result = []
        for item in json_return:
            result.append(item['topic']['value'])
        dispatcher.utter_message(text=f"If you are asking about {chosen_event}, the event includes all topics, such as{result} ")

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
            text=f"The number of courses in each subject are listed as following: {ans}, "
                 f"HaHa, there are so many but it is just what you asked (^-^)")

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

        # intent = tracker.latest_message['intent']
        # # print(intent)
        # ents = tracker.latest_message['entities']
        # # print(ents)
        # ssstt = tracker.latest_message['text']
        # # print(ssstt)
        # ssx = ssstt[9:16]
        # # print(ssx)
        # s = ssx
        # nlp = spacy.load("en_core_web_sm")
        # matcher = Matcher(nlp.vocab)
        # pattern = [[{"POS": "NOUN"}]]
        # matcher.add("CLASS_PATTERN", pattern)
        # #        doc=nlp(ssstt)
        # #        print("below is pattern from spacy")
        # #        print(doc)
        # #        doc=nlp("Upcoming iPhone X release date leaked")
        # doc = nlp(ssstt)
        # matches = matcher(doc)
        # k = ""
        # # print(matches)
        # for match_id, start, end in matches:
        #     matched_span = doc[start:end]
        #     if "COMP" in matched_span.text:
        #         k = matched_span.text
        #     # print(matched_span.text)
        # # print(k)
        # #        sst=tracker.latest_message['entities'][0]['value']
        # #        print(sst)
        # dispatcher.utter_message(text="this is from query 3 " + s)

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
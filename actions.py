# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
#
#
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import spacy
from spacy.matcher import Matcher



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

#        response = requests.post('http://localhost:3030/focu/query', data={'query': query_var})
#        res = response.json()
#        print('res is',res)
#        res_1= res['results']['bindings']
#        print('res after removing binding')
#        ans = []
#
#        print(res['results']['bindings'])
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
        
#copy paste below content
class Query1(Action):
    def name(self) -> Text:
        return "query_1"
    
    def run(self,dispatcher:CollectingDispatcher,
            tracker: Tracker, domain:Dict[Text,Any])->List[Dict[Text,Any]]:
        
        #query body
        #模糊大范围搜索不需要entity
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
# for loop 获取result内容进行输出
#        response = requests.post('http://localhost:3030/focu/query', data={'query': query_var})
#        res = response.json()
        
        dispatcher.utter_message(text=f"this is from query 1")
        
        return[]

class Query2(Action):
    def name(self) -> Text:
        return "query_2"
    
    def run(self,dispatcher:CollectingDispatcher,
            tracker: Tracker, domain:Dict[Text,Any])->List[Dict[Text,Any]]:
                
        #query body
        #entity com474
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
# for loop 获取result内容进行输出
#        response = requests.post('http://localhost:3030/focu/query', data={'query': query_var})
#        res = response.json()
        
        dispatcher.utter_message(text=f"this is from query 2")
        
        return[]

class Query3(Action):
    def name(self) -> Text:
        return "query_3"
    
    def run(self,dispatcher:CollectingDispatcher,
            tracker: Tracker, domain:Dict[Text,Any])->List[Dict[Text,Any]]:
                
        #query body
        #entity com472
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
#
#        response = requests.post('http://localhost:3030/focu/query', data={'query': query_var})
#        res = response.json()
#        s=tracker.slots['course']
#        print(s)

#——————————————————————————————————————————————
# 动态获取
#——————————————————————————————————————————————
        intent=tracker.latest_message['intent']
        print(intent)
        ents=tracker.latest_message['entities']
        print(ents)
        ssstt=tracker.latest_message['text']
        print(ssstt)
        ssx=ssstt[9:16]
        print(ssx)
        s=ssx
        
# pattern
        nlp=spacy.load("en_core_web_sm")
        matcher = Matcher(nlp.vocab)
        pattern=[[{"POS":"NOUN"}]]
        matcher.add("CLASS_PATTERN",pattern)
#        doc=nlp(ssstt)
#        print("below is pattern from spacy")
#        print(doc)
#        doc=nlp("Upcoming iPhone X release date leaked")
        doc=nlp(ssstt)
        matches=matcher(doc)
        k=""
        print(matches)
        for match_id, start, end in matches:
            matched_span=doc[start:end]
            k=matched_span.text
            print(matched_span.text)
        print(k)
#        sst=tracker.latest_message['entities'][0]['value']
#        print(sst)
        dispatcher.utter_message(text="this is from query 3 "+s)
        
        return[]

class Query4(Action):
    def name(self) -> Text:
        return "query_4"
    
    def run(self,dispatcher:CollectingDispatcher,
            tracker: Tracker, domain:Dict[Text,Any])->List[Dict[Text,Any]]:
                
        #query body
        #写死的query无需entity
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
#for loop 打印结果result
#        response = requests.post('http://localhost:3030/focu/query', data={'query': query_var})
#        res = response.json()
        
        dispatcher.utter_message(text=f"this is from query 4")
        
        return[]

class Query5(Action):
    def name(self) -> Text:
        return "query_5"
    
    def run(self,dispatcher:CollectingDispatcher,
            tracker: Tracker, domain:Dict[Text,Any])->List[Dict[Text,Any]]:
                
        #query body
        #
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
#for loop 打印结果result
#        response = requests.post('http://localhost:3030/focu/query', data={'query': query_var})
#        res = response.json()
        
        dispatcher.utter_message(text=f"this is from query 5")
        
        return[]

class Query6(Action):
    def name(self) -> Text:
        return "query_6"
    
    def run(self,dispatcher:CollectingDispatcher,
            tracker: Tracker, domain:Dict[Text,Any])->List[Dict[Text,Any]]:
                
        #query body
        #
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
#
#        response = requests.post('http://localhost:3030/focu/query', data={'query': query_var})
#        res = response.json()
        
        dispatcher.utter_message(text=f"this is from query 6")
        
        return[]

class Query7(Action):
    def name(self) -> Text:
        return "query_7"
    
    def run(self,dispatcher:CollectingDispatcher,
            tracker: Tracker, domain:Dict[Text,Any])->List[Dict[Text,Any]]:
                
        #query body
        #写死的query无需entity
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
#for loop 打印结果result
#        response = requests.post('http://localhost:3030/focu/query', data={'query': query_var})
#        res = response.json()
        
        dispatcher.utter_message(text=f"this is from query 7")
        
        return[]

class Query8(Action):
    def name(self) -> Text:
        return "query_8"
    
    def run(self,dispatcher:CollectingDispatcher,
            tracker: Tracker, domain:Dict[Text,Any])->List[Dict[Text,Any]]:
                
        #query body
        #写死的query无需entity
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
#for loop 打印结果result
#        response = requests.post('http://localhost:3030/focu/query', data={'query': query_var})
#        res = response.json()
        
        dispatcher.utter_message(text=f"this is from query 8")
        
        return[]

class Query9(Action):
    def name(self) -> Text:
        return "query_9"
    
    def run(self,dispatcher:CollectingDispatcher,
            tracker: Tracker, domain:Dict[Text,Any])->List[Dict[Text,Any]]:
                
        #query body
        #写死的query无需entity
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
#f
#        response = requests.post('http://localhost:3030/focu/query', data={'query': query_var})
#        res = response.json()
        
        dispatcher.utter_message(text=f"this is from query 9")
        
        return[]

class Query10(Action):
    def name(self) -> Text:
        return "query_10"
    
    def run(self,dispatcher:CollectingDispatcher,
            tracker: Tracker, domain:Dict[Text,Any])->List[Dict[Text,Any]]:
                
        #query body
        #写死的query无需entity
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
            """
#for loop 打印结果result
#        response = requests.post('http://localhost:3030/focu/query', data={'query': query_var})
#        res = response.json()
        
        dispatcher.utter_message(text=f"this is from query 10")
        
        return[]
#until here

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

# question : course description
class ActionCourse(Action):
    # require  the course description
    def name(self) -> Text:
        return "action_course_info"
        #return "action_person_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('course is ', tracker.slots['course'])
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

# question . which courses cover this topic
class ActionCourseTopic(Action):

    def name(self) -> Text:
        return "action_course_topic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        chosen_topic = tracker.slots['topic']
        print('the slots name is', tracker.slots['topic'])

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

        # dispatcher.utter_message(text=f"If you are asking about {tracker.slots['person']}, Best Human Ever!!! ;-) ")
        dispatcher.utter_message(text=f"If you are asking about {chosen_topic}, the courses are as follows: ,{result}")

        return []
#question  , what topics are covered in lab
class ActionCourseEvent(Action):

    def name(self) -> Text:
        return "action_course_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        chosen_type = tracker.slots['event']
        chosen_course = tracker.slots['course']
        print(chosen_course)
        print('chosen type',chosen_type)
        chosen_event = chosen_course+'_'+chosen_type
        print('the event name is',chosen_event)

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
        #
        # #dispatcher.utter_message(text=f"If you are asking about {tracker.slots['person']}, Best Human Ever!!! ;-) ")
        dispatcher.utter_message(text=f"If you are asking about {chosen_event}, the event includes all topics, such as{result} ")

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
        result = query(query_var)

        dispatcher.utter_message(text=f"This is from query 1 : {result}")
        
        return[]

class Query2(Action):
    def name(self) -> Text:
        return "query_2"
    
    def run(self,dispatcher:CollectingDispatcher,
            tracker: Tracker, domain:Dict[Text,Any])->List[Dict[Text,Any]]:
                
        #query body
        #entity com474
        query_two = """
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
        query_two_result = query(query_two)

        dispatcher.utter_message(text=f"This is from query 2: {query_two_result}")
        
        return[]

class Query3(Action):
    def name(self) -> Text:
        return "query_3"
    
    def run(self,dispatcher:CollectingDispatcher,
            tracker: Tracker, domain:Dict[Text,Any])->List[Dict[Text,Any]]:
                
        #query body
        #entity com472
        query_three = """
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
        query_three_result = query(query_three)

        dispatcher.utter_message(text=f"This is from query about course description: {query_three_result}")
        
        #dispatcher.utter_message(text=f"this is from query 3 {}")
        
        return[]

class Query4(Action):
    def name(self) -> Text:
        return "query_4"
    
    def run(self,dispatcher:CollectingDispatcher,
            tracker: Tracker, domain:Dict[Text,Any])->List[Dict[Text,Any]]:
                
        #query body
        #写死的query无需entity
        query_four = """
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
        query_four_result = query(query_four)

        dispatcher.utter_message(text=f"This is from query about topics covered in course: {query_four_result}")
        # results = query(query_var)
        # dispatcher.utter_message(text=f"this is from query 4 {results}")
        
        return[]

class Query5(Action):
    def name(self) -> Text:
        return "query_5"
    
    def run(self,dispatcher:CollectingDispatcher,
            tracker: Tracker, domain:Dict[Text,Any])->List[Dict[Text,Any]]:
                
        #query body
        #
        query_five = """
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
        query_five_result = query(query_five)

        dispatcher.utter_message(text=f"This is from query 5: {query_five_result}")
        
        # dispatcher.utter_message(text=f"this is from query 5")
        
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
        result = query(query_var)

        dispatcher.utter_message(text=f"this is from query 6 {result}")

        #dispatcher.utter_message(text=f"this is from query 6")
        
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

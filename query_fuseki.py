import requests
from prettytable import PrettyTable

# #SPARQL printing the subject, predicate and object
# query_var = 'SELECT ?subject ?predicate ?object WHERE { ?subject ?predicate ?object} LIMIT 5'

# #Using the post method to query on Apache Fuseki Server
# #Make sure you give the right IP and port address details correctly and the server should be running
# #Here Studybot is the dataset name which I have created and uploaded my knowlegde graph
# #Make sure the Fuseki Server is running
# response = requests.post('http://localhost:3030/StudyBot/sparql',
#        data={'query': query_var})
#
# res = response.json()
# #Prints the response of the SPARQL query
# print(res)
#
# #Lets try printing the values from the json output
# print("\nPrinting the values of subject predicate and object")
# t = PrettyTable(['Subject', 'Predicate','Object'])
# t.align['Subject'] = "l"
# t.align['Predicate'] = "l"
# t.align['Object'] = "l"
# for row in res['results']['bindings']:
#     t.add_row([row['subject']['value'],row['predicate']['value'],row['object']['value']])
# print(t)

#q 1. How many courses in each subject?
query_var = '''PREFIX dbo: <http://dbpedia.org/ontology/>
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
LIMIT 5
'''
response = requests.post('http://localhost:3030/StudyBot/sparql',
       data={'query': query_var})

res = response.json()
print(res)
ans = []

for row in res['results']['bindings']:
    ans.append([row['suject_name']['value'], row['course_number']['value']])
print('answer 1 are : ', ans)

#q 2. Which lectures does course COMP474 have?
query_var1 = '''PREFIX dbo: <http://dbpedia.org/ontology/>
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
'''

response = requests.post('http://localhost:3030/StudyBot/sparql',
       data={'query': query_var1})

res1 = response.json()
#Prints the response of the SPARQL query
print(res1)
ans1 = []
for row in res1['results']['bindings']:
    ans1.append(row['lecture_name']['value'])

print('answer 2 are : ', ans1)

#q3 3. Which topics are associated with course COMP472?
query_var3 = '''Prefix aiiso: <http://purl.org/vocab/aiiso/schema#>
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
}'''

response = requests.post('http://localhost:3030/StudyBot/sparql',
       data={'query': query_var3})

res3 = response.json()
#Prints the response of the SPARQL query
# print(res3)
ans3 = []
for row in res3['results']['bindings']:
    ans3.append(row['topics']['value'])

print('answer 3 are :', ans3)


from rdflib import URIRef, Literal, Namespace, Graph
from rdflib.namespace import XSD, RDF, RDFS
from pathlib import Path
from os import getcwd
import pandas as pd

g = Graph()

FC = Namespace('http://focu.io/schema#')
FCD = Namespace('http://focu.io/data#')
DBR = Namespace('http://dbpedia.org/resource/')
VIVO = Namespace('http://vivoweb.org/ontology/core#')
AIISO = Namespace('http://purl.org/vocab/aiiso/schema#')
TEACH = Namespace('http://linkedscience.org/teach/ns#')

g.bind('focu', FC)
g.bind('focudata', FCD)
g.bind('dbr', DBR)
g.bind('vivo', VIVO)
g.bind('aiiso', AIISO)
g.bind('teach', TEACH)


# Class and Property
lab = FC['Lab']
g.add((lab, RDF.type, RDFS.Class))
g.add((lab, RDFS['subClassOf'], TEACH['Lecture']))
g.add((lab, RDFS.label, Literal('Lab', lang='en')))
g.add((lab, RDFS.comment, Literal('Lab Class', lang='en')))

tut = FC['Tutorial']
g.add((tut, RDF.type, RDFS.Class))
g.add((tut, RDFS['subClassOf'], TEACH['Lecture']))
g.add((tut, RDFS.label, Literal('Tutorial', lang='en')))
g.add((tut, RDFS.comment, Literal('Tutorial Class', lang='en')))

topic = FC['Topic']
g.add((topic, RDF.type, RDFS.Class))
g.add((topic, RDFS.label, Literal('Topic', lang='en')))
g.add((topic, RDFS.comment, Literal('Topic Class', lang='en')))

slide = FC['Slide']
g.add((slide, RDF.type, RDFS.Class))
g.add((slide, RDFS.label, Literal('Slide', lang='en')))
g.add((slide, RDFS.comment, Literal('Slide', lang='en')))

worksheet = FC['Worksheet']
g.add((worksheet, RDF.type, RDFS.Class))
g.add((worksheet, RDFS.label, Literal('Worksheet', lang='en')))
g.add((worksheet, RDFS.comment, Literal('Worksheet', lang='en')))

reading = FC['Reading']
g.add((reading, RDF.type, RDFS.Class))
g.add((reading, RDFS.label, Literal('Reading', lang='en')))
g.add((reading, RDFS.comment, Literal('Reading', lang='en')))

course_outline = FC['CourseOutline']
g.add((course_outline, RDF.type, RDFS.Class))
g.add((course_outline, RDFS.label, Literal('Course Outline', lang='en')))
g.add((course_outline, RDFS.comment, Literal('Course Outline', lang='en')))

subj = FC['Subject']
g.add((subj, RDF.type, RDFS.Class))
g.add((subj, RDFS.label, Literal('Subject', lang='en')))
g.add((subj, RDFS.comment, Literal('Subject Class', lang='en')))

subject_pro = FC['subject']
g.add((subject_pro, RDF.type, RDF.Property))
g.add((subject_pro, RDFS.label, Literal('subject', lang='en')))
g.add((subject_pro, RDFS.comment, Literal('Course subject.', lang='en')))
g.add((subject_pro, RDFS.domain, TEACH['Course']))
g.add((subject_pro, RDFS.range, FC['Subject']))

outline = FC['outline']
g.add((outline, RDF.type, RDF.Property))
g.add((outline, RDFS.label, Literal('outline', lang='en')))
g.add((outline, RDFS.comment, Literal('Course outline.', lang='en')))
g.add((outline, RDFS.domain, TEACH['Course']))
g.add((outline, RDFS.range, FC['CourseOutline']))

content = FC['content']
g.add((content, RDF.type, RDF.Property))
g.add((content, RDFS.label, Literal('content', lang='en')))
g.add((content, RDFS.comment, Literal('Lab content or tutorial content.', lang='en')))
g.add((content, RDFS.domain, FC['Lab']))
g.add((content, RDFS.domain, FC['Tutorial']))
g.add((content, RDFS.range, FC['Slide']))
g.add((content, RDFS.range, FC['Worksheet']))
g.add((content, RDFS.range, FC['Reading']))
g.add((content, RDFS.range, VIVO['Video']))

labAssociat = FC['labAssociateWith']
g.add((labAssociat, RDF.type, RDF.Property))
g.add((labAssociat, RDFS.label, Literal('lab associated with a specific lecture', lang='en')))
g.add((labAssociat, RDFS.comment, Literal('lab associated with a specific lecture', lang='en')))
g.add((labAssociat, RDFS.domain, FC['Lab']))
g.add((labAssociat, RDFS.range, TEACH['Lecture']))

tutAssociat = FC['tutorialAssociateWith']
g.add((tutAssociat, RDF.type, RDF.Property))
g.add((tutAssociat, RDFS.label, Literal('tutorial associated with a specific lecture', lang='en')))
g.add((tutAssociat, RDFS.comment, Literal('tutorial associated with a specific lecture', lang='en')))
g.add((tutAssociat, RDFS.domain, FC['Tutorial']))
g.add((tutAssociat, RDFS.range, TEACH['Lecture']))

topicAssociat = FC['topicAssociateWith']
g.add((topicAssociat, RDF.type, RDF.Property))
g.add((topicAssociat, RDFS.label, Literal('topics', lang='en')))
g.add((topicAssociat, RDFS.comment, Literal('topics that are covered in a course or a lecture in a course.', lang='en')))
g.add((topicAssociat, RDFS.domain, FC['Topic']))
g.add((topicAssociat, RDFS.range, TEACH['Lecture']))
g.add((topicAssociat, RDFS.range, TEACH['Course']))

offeredAt = FC['offeredAt']
g.add((offeredAt, RDF.type, RDF.Property))
g.add((offeredAt, RDFS.label, Literal('offered in', lang='en')))
g.add((offeredAt, RDFS.comment, Literal('a course is offered at a univeristy.', lang='en')))
g.add((offeredAt, RDFS.domain, TEACH['Course']))
g.add((offeredAt, RDFS.range, VIVO['University']))

offeredIn = FC['offeredIn']
g.add((offeredIn, RDF.type, RDF.Property))
g.add((offeredIn, RDFS.label, Literal('lecture in', lang='en')))
g.add((offeredIn, RDFS.comment, Literal('a lecture is in a course.', lang='en')))
g.add((offeredIn, RDFS.domain, TEACH['Lecture']))
g.add((offeredIn, RDFS.range, TEACH['Course']))

# data
concordia = FCD['Concordia_University']
g.add((concordia, RDF.type, VIVO['University']))
g.add((concordia, AIISO['name'], Literal('Concordia University')))
g.add((concordia, RDFS.seeAlso, DBR['Concordia_University']))

# 2 examples
video1 = URIRef('https://www.youtube.com/watch?v=P18EdAKuC1U')
g.add((video1, RDF.type, VIVO['Video']))

slide1 = URIRef(Path(getcwd() + '\COMP474\Lectures\slides01.pdf').as_uri())
g.add((slide1, RDF.type, FC['Slide']))

slide2 = URIRef(Path(getcwd() + '\COMP474\Lectures\slides02.pdf').as_uri())
g.add((slide2, RDF.type, FC['Slide']))

worksheet1 = URIRef(Path(getcwd() + '\COMP474\Lectures\worksheet01.pdf').as_uri())
g.add((worksheet1, RDF.type, FC['Worksheet']))

reading1 = URIRef(Path(getcwd() + '\COMP474\Lectures\py_tut.pdf').as_uri())
g.add((reading1, RDF.type, FC['Reading']))

outline1 = URIRef(Path(getcwd() + '\COMP474\course_outline_comp474_6741_w2021.pdf').as_uri())
g.add((outline1, RDF.type, FC['CourseOutline']))

lec1 = FCD['COMP474_lecture1']
g.add((lec1, RDF.type, TEACH['Lecture']))
g.add((lec1, AIISO['name'], Literal('Introduction to Intelligent Systems')))
g.add((lec1, AIISO['code'], Literal('1', datatype=XSD['integer'])))
g.add((lec1, FC['content'], slide1))
g.add((lec1, FC['content'], video1))
g.add((lec1, FC['offeredIn'], FCD['COMP474']))

lec2 = FCD['COMP474_lecture2']
g.add((lec2, RDF.type, TEACH['Lecture']))
g.add((lec2, AIISO['name'], Literal('Knowledge Graphs')))
g.add((lec2, AIISO['code'], Literal('2', datatype=XSD['integer'])))
g.add((lec2, FC['content'], slide2))
g.add((lec2, FC['content'], worksheet1))
g.add((lec2, FC['content'], reading1))
g.add((lec2, FC['offeredIn'], FCD['COMP474']))

class2 = FCD['COMP474']
# g.add((class2, TEACH['courseDescription'], Literal(
#     "agent‑based. Knowledge acquisition and representation. Uncertainty and conflict resolution. Reasoning and "
#     "explanation. Design of intelligent systems. Project. Lectures: three hours per week. Laboratory: two hours per "
#     "week.")))
g.add((class2, FC['outline'], outline1))

# class3 = FCD['COMP472']
# g.add((class3, TEACH['courseDescription'], Literal(
#     "Intelligence. Then it covers knowledge representation, heuristic search, game playing and planning. Finally, "
#     "it introduces the topics of machine learning, genetic algorithms and natural language processing. A project is "
#     "required. Lectures: three hours per week. Laboratory: two hours per week.")))


slide3 = URIRef(Path(getcwd() + '\COMP472\Lectures\intro-Winter2020.pdf').as_uri())
g.add((slide3, RDF.type, FC['Slide']))

slide4 = URIRef(Path(getcwd() + '\COMP472\Lectures\search-Winter2020.pdf').as_uri())
g.add((slide4, RDF.type, FC['Slide']))

lec3 = FCD['COMP472_lecture1']
g.add((lec3, RDF.type, TEACH['Lecture']))
g.add((lec3, AIISO['name'], Literal('Artificial Intelligence: Introduction')))
g.add((lec3, AIISO['code'], Literal('1', datatype=XSD['integer'])))
g.add((lec3, FC['content'], slide3))
g.add((lec3, FC['offeredIn'], FCD['COMP472']))

lec4 = FCD['COMP472_lecture2']
g.add((lec4, RDF.type, TEACH['Lecture']))
g.add((lec4, AIISO['name'], Literal('Artificial Intelligence: State Space Search')))
g.add((lec4, AIISO['code'], Literal('2', datatype=XSD['integer'])))
g.add((lec3, FC['content'], slide4))
g.add((lec4, FC['offeredIn'], FCD['COMP472']))


lab1 = FCD['COMP474_lab1']
g.add((lab1, RDF.type, FC['Lab']))
g.add((lab1, AIISO['name'], Literal('COMP474_Lab_1')))
g.add((lab1, AIISO['code'], Literal('1', datatype=XSD['integer'])))
g.add((lab1, FC['content'], URIRef('https://moodle.concordia.ca/moodle/mod/page/view.php?id=2608092')))
g.add((lab1, FC['labAssociatedWith'], FCD['COMP474_lecture1']))

lab2 = FCD['COMP474_lab2']
g.add((lab2, RDF.type, FC['Lab']))
g.add((lab2, AIISO['name'], Literal('COMP474_Lab_2')))
g.add((lab2, AIISO['code'], Literal('2', datatype=XSD['integer'])))
g.add((lab2, FC['content'], URIRef('https://moodle.concordia.ca/moodle/mod/page/view.php?id=2575768')))
g.add((lab2, FC['labAssociatedWith'], FCD['COMP474_lecture2']))
g.add((lab2, RDFS.seeAlso, URIRef('https://rdflib.readthedocs.io/en/stable/index.html')))

slide5 = URIRef(Path(getcwd() + '\COMP472\Lectures\COMP_472_Lab1.pdf').as_uri())
g.add((slide5, RDF.type, FC['Slide']))

slide6 = URIRef(Path(getcwd() + '\COMP472\Lectures\COMP_472_Lab2.pdf').as_uri())
g.add((slide6, RDF.type, FC['Slide']))

lab3 = FCD['COMP472_lab1']
g.add((lab3, RDF.type, FC['Lab']))
g.add((lab3, AIISO['name'], Literal('COMP472_Lab_1')))
g.add((lab3, AIISO['code'], Literal('1', datatype=XSD['integer'])))
g.add((lab3, FC['content'], slide5))
g.add((lab3, FC['labAssociatedWith'], FCD['COMP472_lecture1']))

lab4 = FCD['COMP472_lab2']
g.add((lab4, RDF.type, FC['Lab']))
g.add((lab4, AIISO['name'], Literal('COMP472_Lab_2')))
g.add((lab4, AIISO['code'], Literal('2', datatype=XSD['integer'])))
g.add((lab4, FC['content'], slide6))
g.add((lab4, FC['labAssociatedWith'], FCD['COMP472_lecture2']))
g.add((lab4, RDFS.seeAlso, URIRef('https://rdflib.readthedocs.io/en/stable/index.html')))


topic1 = FCD['Knowledge_Graph']
g.add((topic1, RDF.type, FC['Topic']))
g.add((topic1, AIISO['name'], Literal('Knowledge Graph')))
g.add((topic1, FC['topicAssociateWith'], FCD['COMP474']))
g.add((topic1, FC['topicAssociateWith'], FCD['COMP474_lecture2']))
g.add((topic1, RDFS.seeAlso, DBR['Knowledge_Graph']))

topic2 = FCD['Expert_system']
g.add((topic2, RDF.type, FC['Topic']))
g.add((topic2, AIISO['name'], Literal('Expert System')))
g.add((topic2, FC['topicAssociateWith'], FCD['COMP474']))
g.add((topic2, RDFS.seeAlso, DBR['Expert_system']))

topic3 = FCD['Breadth-first_search']
g.add((topic3, RDF.type, FC['Topic']))
g.add((topic3, AIISO['name'], Literal('Breadth-first_search')))
g.add((topic3, FC['topicAssociateWith'], FCD['COMP472']))
g.add((topic3, FC['topicAssociateWith'], FCD['COMP472_lecture2']))
g.add((topic3, RDFS.seeAlso, DBR['Breadth-first_search']))

topic4 = FCD['Depth-first_search']
g.add((topic4, RDF.type, FC['Topic']))
g.add((topic4, AIISO['name'], Literal('Depth-first_search')))
g.add((topic4, FC['topicAssociateWith'], FCD['COMP472']))
g.add((topic4, FC['topicAssociateWith'], FCD['COMP472_lecture2']))
g.add((topic4, RDFS.seeAlso, DBR['Depth-first_search']))


def subject_generator(subject_name):
    subject = FCD[subject_name]
    g.add((subject, RDF.type, FC['Subject']))
    g.add((subject, AIISO['name'], Literal(subject_name)))


def course_generator(subject, catalog, long_title, units, description):
    class1 = FCD[subject + catalog]
    g.add((class1, RDF.type, TEACH['Course']))
    g.add((class1, TEACH['courseTitle'], Literal(long_title)))
    g.add((class1, VIVO['courseCredits'], Literal(units, datatype=XSD['decimal'])))
    g.add((class1, FC['subject'], FCD[subject]))
    g.add((class1, AIISO['code'], Literal(catalog, datatype=XSD['integer'])))
    g.add((class1, TEACH['courseDescription'], Literal(description)))
    # g.add((class1, RDFS.seeAlso, DBR['Concordia_University']))
    g.add((class1, FC['offeredAt'], FCD['Concordia_University']))
    # g.add((class1, FC['outline'], Literal('utline.....Intelligent Systems')))


table1 = pd.read_csv("CU_SR_OPEN_DATA_CATALOG_DESC.csv", header=0)
table2 = pd.read_csv("CU_SR_OPEN_DATA_CATALOG-37272173.csv", header=0)

table_merged = pd.merge(table1, table2, on='Course ID', how='inner')

subjects = []
course_ids = []

for index, row in table_merged.iterrows():
    if row['Subject'] not in subjects:
        subjects.append(row['Subject'])
    if row['Course ID'] not in course_ids:
        course_ids.append(row['Course ID'])
        course_generator(row['Subject'], row['Catalog'], row['Long Title'], row['Class Units'], row['Descr'])

for item in subjects:
    subject_generator(item)

g.serialize(format='nt', destination="school.nt")


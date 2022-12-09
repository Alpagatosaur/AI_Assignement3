# -*- coding: utf-8 -*-
import random
import time

from rdflib.namespace import RDF, RDFS, XSD, SOSA, TIME, Namespace, NamespaceManager
from rdflib import Graph, Literal, URIRef
from paho.mqtt import client as mqtt_client


broker = 'test.mosquitto.org'
topic = "teds22/group05/pressure"

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(10, 100)}'

QUDT11 = Namespace("http://qudt.org/1.1/schema/qudt#")
QUDTU11 = Namespace("http://qudt.org/1.1/vocab/unit#")
CDT = Namespace("http://w3id.org/lindt/custom_datatypes#")
BASE = Namespace("http://example.org/data/")

namespace_manager = NamespaceManager(Graph())
sem_web = URIRef(broker)

namespace_manager.bind("rdf", RDF)
namespace_manager.bind("rdfs", RDFS)
namespace_manager.bind("xsd", XSD)
namespace_manager.bind("sosa", SOSA)
namespace_manager.bind("time", TIME)

namespace_manager.bind("qudt-1-1", QUDT11)
namespace_manager.bind("qudt-unit-1-1", QUDTU11)
namespace_manager.bind("cdt", CDT)
namespace_manager.bind("base", BASE)

g = Graph()
g.namespace_manager = namespace_manager

earth = Literal("earthAtmosphere")
iphone7 = Literal("iphone7/35-207306-844818-0")
sensor = Literal("sensor/35-207306-844818-0/BMP282")
sensorAtm = Literal("sensor/35-207306-844818-0/BMP282/atmosphericPressure")

g.add((earth, RDF.type, SOSA.FeatureOfInterest))
g.add((earth, RDFS.label, Literal("Atmosphere of Earth", lang='en')))

g.add((iphone7, RDF.type, SOSA.FeatureOfInterest))
g.add((iphone7, RDFS.label, Literal("IPhone 7 - IMEI 35-207306-844818-0", lang='en')))
g.add((iphone7, RDFS.comment, Literal("IPhone 7 - IMEI 35-207306-844818-0 - John Doe", lang='en')))
g.add((iphone7, SOSA.hosts, sensor))

g.add((sensor, RDF.type, SOSA.Sensor))
g.add((sensor, RDFS.label, Literal("Bosch Sensortec BMP282", lang='en')))
g.add((sensor, SOSA.observes, sensorAtm))

count_msg = 0

def on_message(client, userdata, message):
    global count_msg
    print("message received  " ,str(message.payload.decode("utf-8")))
    time.sleep(1)
    message = message.payload.decode('utf-8')
    
    [reading, dt] = message.split('|')

    obsvervation = Literal(f"Observation/{count_msg}")
    g.add((obsvervation, RDF.type, SOSA.Observation))
    g.add((obsvervation, SOSA.observedProperty, sensorAtm))
    g.add((obsvervation, SOSA.hasFeatureOfInterest, earth))
    g.add((obsvervation, SOSA.observedProperty, sensorAtm))

    pressure = Literal(reading, datatype=CDT.ucum)
    datetime_2017 = Literal(dt, datatype=XSD.dateTime)
    g.add((obsvervation, SOSA.hasSimpleResult, pressure))
    g.add((obsvervation, SOSA.resultTime, datetime_2017))
    count_msg += 1


    
# START
client = mqtt_client.Client(client_id)

# Attach "on_message" callback function (even handle) to "on_message" event
client.on_message = on_message

print("connect to broker ", broker)
client.connect(broker)

print("Subscribe ", topic)
client.subscribe(topic)

client.loop_start()

while count_msg < 1:
    time.sleep(1)

print("Unsubscribe")
client.unsubscribe(topic)
# Wait 4 s
time.sleep(4)


client.loop_stop()

print("Disconnect")
client.disconnect()

g.serialize(destination="pressure.ttl")

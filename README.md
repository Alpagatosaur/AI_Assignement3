# AI_Assignement3

## Write a Python file called publisher.py

The Python code in this file should:

    Create a MQTT client instance, and start the message loop.
    Connect to the MQTT broker on the Mosquitto MQTT development server, i.e. test.mosquitto.org.
    Publish 10 simulated pressure readings to the topic teds22/groupXX/pressure (where XX is your group number) on the MQTT Server, with a one second delay between each publish. You can use the following code to simulate a sensor reading (note, that the message is a string with a datetime and a reading separated with a pipe character |):

    mu, sigma = 1200.00, 1.0
    reading = f'{round(np.random.normal(mu, sigma), 2):.2f}'        
    dt = datetime.datetime.now()
    dt = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    message = f'{reading}|{dt}'

    When you publish this message using the MQTT client instance's publish() method, make sure to set the parameter qos=2. This guarantees that the message will be delivered to the MQTT server exactly once. To create a delay of 1 second, you can use time.sleep(1).
    When 10 messages have been published to the MQTT server, the MQTT client should wait for 4 seconds, stop the message loop, and disconnect from the MQTT server.

## Write a Python file called subscriber.py

The Python code in this file should:

    Create a MQTT client instance, assign an on_message callback function, and start the message loop.
    Connect to the MQTT broker on the Mosquitto MQTT development server, i.e. test.mosquitto.org.
    Subscribe to the topic teds22/groupXX/pressure (where XX is your group number) on the MQTT Server.
    Then wait until 10 messages have been received from the MQTT server (see below under "RDF Graph" for what needs to be done for each message).
    When 10 messages have been received, the MQTT client should unsubscribe from the topic, wait for 4 seconds, stop the message loop, disconnect from the MQTT server, and finally serialize the RDF graph to the Turtle format, and save this to a file called pressure.ttl.

RDF Graph

    Study the B.1 iPhone Barometer 

Links to an external site. example. There you will find a number of prefixes for a number of namespaces. Most of these can be imported as pre-defined namespaces in RDFLib, i.e. from rdflib.namespace import RDF, RDFS, XSD, SOSA, TIME. For the remaining prefixes (qudt-1-1, qudt-unit-1-1, cdt and base), you can import and use the Namespace class from RDFLib, i.e. from rdflib import Namespace, to define namespaces for them, e.g. using the variables QUDT11, QUDTU11, CDT and BASE.
At the top of the file subscriber.py, you want to define the RDF Graph from the B.1 iPhone Barometer
Links to an external site. example up to, but not including <Observation/346344>.
Then, when a message is received in your on_message callback function, you want to extract the payload (the actual message), and add an observation to your RDF Graph. The observation will have the same structure as the <Observation/346344> in the B.1 iPhone Barometer

    Links to an external site. example, but you want to add <Observation/YY> for each message received, where YY starts at 1 and is incremented for each received message, e.g. <Observation/1>, <Observation/2>, ..., <Observation/n>.
    When you have extracted the payload from the message, you need to split the message string to get the reading and the datetime value, which can be done using, e.g. [reading, dt] = msg.split('|'). These values need to be inserted as Literal strings (objects) associated with the subject <Observation/YY> for the predicates sosa:hasSimpleResult and sosa:resultTime respectively.

## Write a Python file called query.py

The Python code in this file should:

    Load the saved file pressure.ttl into a RDF Graph.
    Use a SPARQL query, to extract all the pressure readings (and associated datetime time stamp) from the Graph. Furthermore, the readings should be sorted in ascending order with respect to the datetime.
    Print the results from the SPARQL query to the terminal. Here's a sample output:
    2021-05-06T14:39:04Z | 1205.81
    2021-05-06T14:39:05Z | 1204.01
    2021-05-06T14:39:06Z | 1206.59
    2021-05-06T14:39:07Z | 1206.10
    2021-05-06T14:39:08Z | 1205.88
    2021-05-06T14:39:09Z | 1206.88
    2021-05-06T14:39:10Z | 1204.51
    2021-05-06T14:39:11Z | 1205.76
    2021-05-06T14:39:12Z | 1204.06
    2021-05-06T14:39:13Z | 1204.26

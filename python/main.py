############################################
# PRODUCE and CONSUME a message to/from QUIX
############################################


from quixstreams import Application
import os

###########################################
# fill in your Quix details and credentials
###########################################
# https://quix.io/docs/apis/portal-api/setup.html#api-reference-documentation

os.environ["Quix__Portal__Api"] = ""
os.environ["Quix__Organisation__Id"] = ""
os.environ["Quix__Workspace__Id"] = ""
os.environ["Quix__Sdk__Token"] = "" # also known as Streaming Token


app = Application(
    consumer_group="test", 
    auto_offset_reset="earliest")

topic = app.topic("test")

with app.get_producer() as producer:
    producer.produce(topic.name, '{"message": "Hello, World!"}', 'hello-world')


sdf = app.dataframe(topic)
sdf.print()
sdf.update(lambda row: print("SUCCESS!"))

if __name__ == "__main__":
    app.run(sdf)
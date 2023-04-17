import pika
import pymongo

connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.28.0.1'))
channel = connection.channel()

channel.queue_declare(queue='insert_record_queue', durable=True)

client = pymongo.MongoClient("mongodb://database:27017/", username='root', password='ccproject')
db = client["mydatabase"]
col = db["students"]

def callback(ch, method, properties, body):
    data = body.decode().split(',')
    name = data[0].strip()
    srn = data[1].strip()
    section = data[2].strip()
    mydict = {"name": name, "srn": srn, "section": section}
    x = col.insert_one(mydict)
    print(x.inserted_id,flush=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='insert_record_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C',flush=True)
channel.start_consuming()

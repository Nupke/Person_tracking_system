from paho.mqtt.client import MQTT_LOG_ERR
from app import mqtt
from app import socketio
from flask_socketio import emit
import json
from app.models import User, Device ,Position
from app import db


@socketio.on('connect', namespace='/test')
def connect():
    # need visibility of the global thread object
    # global thread
    emit('my response', {'data':'Connected'})
    mqtt.subscribe("detectionv1/sensor/ble_devices_scanner/state")
    mqtt.subscribe("detectionv2/sensor/ble_devices_scanner/state")
    mqtt.subscribe("detectionv3/sensor/ble_devices_scanner/state")
    mqtt.subscribe("sensors/drone01/altitude")
    print('client has been connected')

    #Start the random number generator thread only if the thread has not been started before.
    # if not thread.isAlive():
    #     print("Starting Thread")
    #     thread = socketio.start_background_task(randomNumberGenerator)

@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['message'])
    socketio.emit('dump', {'data': 'Published to topic {}'.format(data['message'])})


@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data["detectionv1/sensor/ble_devices_scanner/state"])
    mqtt.subscribe(data["detectionv2/sensor/ble_devices_scanner/state"])
    mqtt.subscribe(data["detectionv3/sensor/ble_devices_scanner/state"])


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print('on_connect client : {} userdata :{} flags :{} rc:{}'.format(client, userdata, flags, rc))
    mqtt.subscribe("sensors/#")


@socketio.on('disconnect', namespace='/test')
def disconnect():
    print('Client disconnected')

@mqtt.on_message()
def handle_message(client, userdata, message):
    json_payload = json.loads(message.payload)

    data = dict(
        topic=message.topic,
        #payload=message.payload.decode()
        timestamp=json_payload['timestamp'],
        address=json_payload['address'],
        rssi=json_payload['rssi'],
        name=json_payload['name'],
    )


    # user = User.query.filter_by(username=form.username.data).first()
    # mac_address = Device.query.filter_by(mac_addres = )
    print('on_message client :message.payload :{}'.format(data))
    print('topic{}'.format(message.topic))
    #print('payload{}'.format(message.payload))

    socketio.emit('dump', {'data': data}, namespace='/test')


    # socketio.emit('newnumber', {'number': data}, namespace='/test')
    # socketio.emit('dump', {'data': data}, namespace='/test')
    # socketio.sleep(1)



@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    if level == MQTT_LOG_ERR:
        print('Error: {}'.format(buf))



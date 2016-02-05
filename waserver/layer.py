# -*- cofing utf-8 -*-
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_groups.protocolentities import InfoGroupsIqProtocolEntity
import threading
import logging
import paho.mqtt.client as mqtt
import json
import sys
import config

class SendLayer(YowInterfaceLayer):

    def __init__(self):
        super(SendLayer, self).__init__()
        if not ('noconn' in sys.argv):
            self.client = mqtt.Client()
            self.client.on_connect = self.onMqttConnect
            self.client.on_message = self.onMqttMessage

            self.client.connect(config.MQTT_HOST, config.MQTT_PORT, 60)
            self.client.loop_start()

        self.callbackQueue = {}
        self.ackQueue = []
        self.lock = threading.Condition()

    def onMqttConnect(self, client, userdata, flags, rc):
        client.subscribe("whatsapp/outgoing")
        client.subscribe("whatsapp/cmd")

    def onMqttMessage(self, client, userdata, msg):
        payload = json.loads(str(msg.payload))
        if msg.topic == "whatsapp/outgoing":
            self.send(payload["phone"], payload["message"])
        elif msg.topic == "whatsapp/cmd":
            if payload["cmd"] == "group_info":
                self.group_info(payload)
    def normalizeJid(self, number):
        if '@' in number:
            return number
        elif "-" in number:
            return "%s@g.us" % number

        return "%s@s.whatsapp.net" % number

    def send(self, phone, message):
        self.lock.acquire()
        messageEntity = TextMessageProtocolEntity(message.encode('utf8'), to = self.normalizeJid(phone))

        self.ackQueue.append(messageEntity.getId())
        self.toLower(messageEntity)
        self.lock.release()

    def group_info(self, payload):
        jid = payload["phone"]
        callback = payload["callback"]
        entity = InfoGroupsIqProtocolEntity(self.normalizeJid(jid))
        self.callbackQueue[entity.getId()] = callback;
        self.toLower(entity)

    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        self.lock.acquire()
        if entity.getId() in self.ackQueue:
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))
            print("Message sent")

        self.lock.release()

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        print(messageProtocolEntity)
        if messageProtocolEntity.getType() == "text":
            self.client.publish("whatsapp/incoming", json.dumps({
                "phone": messageProtocolEntity.getFrom(False),
                "message": messageProtocolEntity.getBody()
            }))
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))

    @ProtocolEntityCallback("iq")
    def onIq(self, entity):
        print(entity)
        if hasattr(entity, "participants"):
            callback = self.callbackQueue[entity.getId()]
            del self.callbackQueue[entity.getId()]
            result = {
                "cmd": "group_info",
                "callback": callback,
                "groupId": entity.getGroupId(),
                "participants": entity.getParticipants(),
                "subject": entity.getSubject()
            }

            self.client.publish("whatsapp/iq", json.dumps(result))

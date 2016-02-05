# Axiom

Axiom is a python program that connects to a mqtt server and provides an interface to the WhatsApp messaging service.

## Installation

1. Clone this repo.
2. Install dependencies
```
pip install yowsup2 paho-mqtt
```
3. Edit `waserver/config.py`. Credentials can be required from the yowsup2 cli. See [here](https://github.com/tgalal/yowsup/wiki/yowsup-cli-2.0).
4. Run
```
python waserver/waserver.py
```

### Docker
1. Create a `waserver/config-prod.py`
2. The build the image with the provided `Dockerfile`. The seperate config files allow for different dev/production configs.

## MQTT interface
### Incoming messages
To receive messages subscribe to `whatsapp/incoming`.
A message will look like this:
```json
{
  "phone": "4915112345678",
  "message": "Hello from a human being!"
}
```
Phone number in this example would normally be spelled `+49 151 12345678`.
For group messages, the phone number is in the form `4915112345678-1400000000` (phone number of the group creator and unix timestamp of creation).

### Sending messages
To send messages, publish to `whatsapp/outgoing`:

```json
{
  "phone": "4915112345678",
  "message": "Hello from a bot!"
}
```

### Commands

Currently there is only on command implemented

#### Group Info

To receive group info (members, title), publish to `whatsapp/cmd`
```json
{
  "cmd": "group_info",
  "phone": "4915112345678-1400000000",
  "callback": "any_string_here"
}
```

The callback will be used to identify the response to this command. It is advisable to use a UUID for this.
The response will be published to the `whatsapp/iq` topic:
```json
{
  "cmd": "group_info",
  "callback": "any_string_here",
  "groupId": "4915112345678-1400000000",
  "participants": {
    "4915112345678": "admin",
    "4915187654321": null,
  },
  "subject": "Example group"
}
```

import dataclasses
from dataclasses import dataclass


@dataclass
class DecodedMQTTTopic:
    envelope_type: str = ""
    src: str = ""
    dst: str = ""
    message_type: str = ""
    remainder: list[str] = dataclasses.field(default_factory=list)

    def __str__(self) -> str:
        return f"DecodedMQTTTopic {self.envelope_type}/{self.src}/{self.message_type} remainder:{self.remainder}"


class MQTTTopic:
    """Valid Gridworks MQTT topic is one of:

     - ENVELOPE_TYPE/SRC/to/DST/MESSAGE_TYPE, for example:
       'gw/hw1-isone-ma-boston-scada/to/a/report-event',
       meaning a message using envelope format 'gw', from
       'hw1-isone-ma-boston-scada', to the ATN ('a') with message type
       'report-event'. Note that SRC is the GNode Alias (a long name) whereas
       DST is the Spaceheat Name.

     - ENVELOPE_TYPE/SRC/to/DST, for example:
       'gw/hw1-isone-ma-boston-scada/to/a',
       meaning a message using envelope format 'gw', from
       'hw1-isone-ma-boston-scada' to the ATN ('a'). Message type must be
       inferred the contents of the envelope.

     - ENVELOPE_TYPE/SRC, for example:
       'gw/hw1-isone-ma-boston-scada',
       meaning a message using envelope format 'gw', from
       'hw1-isone-ma-boston-scada' Destination and message type must be inferred
       the contents of the envelope.

     - ENVELOPE_TYPE, for example: 'gw', meaning a message using envelope format
       'gw'. Source, destination and message type must be inferred the contents
       of the envelope.

     - ENVELOPE_TYPE/SRC/to/DST/MESSAGE_TYPE/OTHER/STUFF, for example:
       'gw/hw1-isone-ma-boston-scada/to/a/report-event/bla/bla',
       meaning a message using envelope format 'gw', from
       'hw1-isone-ma-boston-scada', to the ATN ('a') with message type
       'report-event', with extra components OTHER and STUFF that may be used by
       code down-stream code. OTHER and STUFF will available in the remainer
       attribute of the decoded topic. In this example the remainder would be
       ['bla', 'bla']

     - Note that if the third level down is not "to", everthing from that third
       level down is put in the remainder, so that, for example
       'gw/hw1-isone-ma-boston-scada/X/a/report-event/bla/bla', would be
       interpreted as evenlope 'gw', source 'hw1-isone-ma-boston-scada' and
       remainder ['X', 'a', 'report-event', 'bla', 'bla'].

     - If the third level is "to" but there is no fourth level,
       destination and message type will be empty but "to" not be placed in the
       in the remainder.

    The only valid component separator is '/'.

    '.' is not a valid character inside the mqtt topic. It must be replaced with
    '-'.

    It is an error for the message type contained inside the envelope to differ
    from one specified in the topic.
    """

    DOT = "."
    DOT_REPLACEMENT = "-"

    @classmethod
    def encode(cls, envelope_type: str, src: str, dst: str, message_type: str) -> str:
        return f"{envelope_type}/{src}/to/{dst}/{message_type}".replace(
            cls.DOT, cls.DOT_REPLACEMENT
        )

    @classmethod
    def encode_subscription(cls, envelope_type: str, src: str, dst: str) -> str:
        return cls.encode(envelope_type, src, dst, "#")

    @classmethod
    def decode(cls, topic: str) -> DecodedMQTTTopic:
        if not topic:
            raise ValueError("ERROR. Topic must have at least one character")
        topic = str(topic).replace(cls.DOT_REPLACEMENT, cls.DOT)
        split = topic.split("/")
        envelope_type = split[0]
        # for example: 'gw'
        remainder: list[str]
        if len(split) == 1:
            src = ""
            dst = ""
            message_type = ""
            remainder = []
        # for example: 'gw/hw1-isone-ma-boston-scada'
        elif len(split) == 2:
            src = split[1]
            dst = ""
            message_type = ""
            remainder = []
        # len > 2
        elif split[2] != "to":
            src = split[1]
            dst = ""
            message_type = ""
            remainder = split[2:]
        elif len(split) == 3:
            src = split[1]
            dst = ""
            message_type = ""
            remainder = []
        # for example: 'gw/hw1-isone-ma-boston-scada/to/a'
        elif len(split) == 4:
            src = split[1]
            dst = split[3]
            message_type = ""
            remainder = []
        # for example: 'gw/hw1-isone-ma-boston-scada/to/a/report-event'
        #          or: 'gw/hw1-isone-ma-boston-scada/to/a/report-event/x'
        else:
            src = split[1]
            dst = split[3]
            message_type = split[4]
            remainder = split[5:]
        return DecodedMQTTTopic(
            envelope_type=envelope_type,
            src=src,
            dst=dst,
            message_type=message_type,
            remainder=remainder,
        )

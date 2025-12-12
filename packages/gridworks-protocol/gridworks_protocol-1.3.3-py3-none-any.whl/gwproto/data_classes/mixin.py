import json


class StreamlinedSerializerMixin:
    @property
    def streamlined_serialize(self) -> str:
        return json.dumps(
            {key: value for key, value in self.__dict__.items() if value is not None}
        )

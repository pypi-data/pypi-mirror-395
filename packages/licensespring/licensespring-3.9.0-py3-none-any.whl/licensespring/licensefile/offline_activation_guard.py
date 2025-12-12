import base64
import json
from datetime import datetime, timezone


class OfflineActivationGuard:
    def __init__(self) -> None:
        pass

    def set_id(self, id: str):
        self._id = id

    def set_device_id(self, device_id: str):
        self._device_id = device_id

    def set_date_created(self):
        self._date_created = datetime.now(timezone.utc).replace(tzinfo=None)

    def to_json(self) -> str:
        data = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()

            else:
                data[key] = value

        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def from_json(cls, data: dict):
        obj = cls()

        for key, value in data.items():
            if key == "_date_created":
                if value.endswith("Z"):
                    value = value[:-1]

                setattr(obj, key, datetime.fromisoformat(value).replace(tzinfo=None))

            else:
                setattr(obj, key, value)
        return obj


class OfflineActivation:
    def __init__(self) -> None:
        self._guard = None

    def set_data(self, data: str):
        self._data = data

    def set_use_guard(self, use_guard: bool):
        self._use_guard = use_guard

    def set_is_activation(self, is_activation: bool):
        self._is_activation = is_activation

    def decode_offline_activation(self):
        decoded_data = base64.b64decode(self._data).decode()
        return json.loads(decoded_data)

    def create_guard_file(self, offline_activation: OfflineActivationGuard):
        self._guard = offline_activation

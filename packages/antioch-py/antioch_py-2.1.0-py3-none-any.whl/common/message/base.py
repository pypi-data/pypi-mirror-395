import json
import re
from abc import ABC
from typing import Any, ClassVar, TypeVar

import ormsgpack
import yaml
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound="Message")


class MessageError(Exception):
    """
    Base exception for Message errors.
    """


class SerializationError(MessageError):
    """
    Raised when serialization (pack, to_json) fails.
    """


class DeserializationError(MessageError):
    """
    Raised when deserialization (unpack, from_json) fails.
    """


class FileAccessError(MessageError):
    """
    Raised when file operations fail.
    """


class MismatchError(MessageError):
    """
    Raised when type doesn't match expected type or deserialization fails.
    """

    def __init__(self, expected: str | None, actual: str | None, details: str | None = None):
        self.expected = expected
        self.actual = actual
        self.details = details

        expected_str = "<untyped>" if expected is None else f"'{expected}'"
        actual_str = "<untyped>" if actual is None else f"'{actual}'"
        message = f"Type mismatch: expected {expected_str}, got {actual_str}"
        if details is not None:
            message += f" - {details}"

        super().__init__(message)


class Message(BaseModel, ABC):
    """
    Base class for user-defined data types supporting serialization and deserialization.

    To add a type identifier, simply set a '_type' class variable. Otherwise, the message will
    have type=null in the serialized format.

    ```python
    class MyMessage(Message):
        _type = "my_message"
        field1: str
        field2: int
    ```
    """

    _type: ClassVar[str | None] = None

    model_config = {
        "extra": "forbid",
        "frozen": False,
        "arbitrary_types_allowed": True,
    }

    def __init_subclass__(cls, **kwargs):
        """
        Validate type format when subclass is defined.
        """

        super().__init_subclass__(**kwargs)
        if cls._type is not None and not re.compile(r"^[a-z0-9][a-z0-9\-_/]*$").match(cls._type):
            raise ValueError(
                f"Invalid type '{cls._type}' for {cls.__name__} (must be lowercase alphanumeric with hyphens, underscores, or slashes)"
            )

    def __str__(self) -> str:
        """
        Return a clean string representation of the message.

        :return: A formatted string showing the message type and field values.
        """

        # Create key=value pairs for all fields
        field_strs = []
        for field_name, field_value in self:
            formatted_value = f'"{field_value}"' if isinstance(field_value, str) else str(field_value)
            field_strs.append(f"{field_name}={formatted_value}")

        return f"<{self.__class__.__name__}: {' '.join(field_strs)}>"

    def __repr__(self) -> str:
        """
        Return a detailed representation that can reconstruct the object.

        :return: A string representation suitable for debugging.
        """

        return super().__repr__()

    def __hash__(self) -> int:
        """
        Make Message hashable for use in sets and as dict keys.

        :return: Hash value based on class type, type, and field values.
        """

        field_items = sorted(self.model_dump().items())
        return hash((self.__class__.__name__, self.get_type(), tuple(field_items)))

    def __eq__(self, other: Any) -> bool:
        """
        Compare messages based on class, type identifier, and field values.

        :param other: The other object to compare with.
        :return: True if messages are equal, False otherwise.
        """

        if not isinstance(other, self.__class__):
            return False
        if self.get_type() != other.get_type():
            return False

        return self.model_dump() == other.model_dump()

    @classmethod
    def get_type(cls) -> str | None:
        """
        Get the type identifier for this message class.

        :return: The type string if set, None otherwise.
        """

        return cls._type

    @staticmethod
    def pack_json(data: dict[str, Any]) -> bytes:
        """
        Pack an arbitrary dict into a message envelope with null type.

        This allows flexible telemetry without requiring Message implementations.
        The dict is wrapped in an envelope with type=None and serialized to MessagePack.

        :param data: Dictionary to pack.
        :return: The MessagePack bytes.
        :raises SerializationError: If serialization fails.
        """

        try:
            envelope = {"type": None, "data": data}
            return ormsgpack.packb(envelope)
        except Exception as e:
            raise SerializationError(f"Failed to serialize dict: {e}") from None

    @classmethod
    def unpack(cls: type[T], data: bytes) -> T:
        """
        Deserialize a message from bytes using MessagePack.

        This validates that the type in the envelope matches the expected type
        for this class.

        :param data: The MessagePack bytes to deserialize.
        :return: The deserialized message.
        :raises DeserializationError: If deserialization fails.
        :raises MismatchError: If the type doesn't match.
        """

        try:
            envelope = ormsgpack.unpackb(data)
            cls._validate_envelope(envelope)

            # Check type matches
            if envelope["type"] != cls.get_type():
                raise MismatchError(expected=cls.get_type(), actual=envelope["type"])

            return cls(**envelope["data"])
        except (MismatchError, DeserializationError):
            raise
        except ValidationError as e:
            first_error = e.errors()[0]
            field_path = " -> ".join(str(loc) for loc in first_error["loc"])
            error_msg = first_error["msg"]
            raise DeserializationError(f"Validation failed at {field_path}: {error_msg}") from None
        except Exception as e:
            if "msgpack" in str(e).lower() or "unpackb" in str(e):
                raise DeserializationError("Failed to deserialize message") from None
            raise DeserializationError(f"Failed to deserialize message: {e}") from None

    @classmethod
    def from_json(cls: type[T], json_str: str) -> T:
        """
        Deserialize a message from a JSON string.

        This validates that the type in the envelope matches the expected type.

        :param json_str: The JSON string to deserialize.
        :return: The deserialized message.
        :raises DeserializationError: If deserialization fails or JSON is invalid.
        :raises MismatchError: If the type doesn't match.
        """

        try:
            envelope = json.loads(json_str)
            cls._validate_envelope(envelope)

            # Check type matches
            if envelope["type"] != cls.get_type():
                raise MismatchError(expected=cls.get_type(), actual=envelope["type"])

            return cls(**envelope["data"])
        except json.JSONDecodeError:
            raise DeserializationError("Invalid JSON format") from None
        except (MismatchError, DeserializationError):
            raise
        except ValidationError as e:
            first_error = e.errors()[0]
            field_path = " -> ".join(str(loc) for loc in first_error["loc"])
            error_msg = first_error["msg"]
            raise DeserializationError(f"Validation failed at {field_path}: {error_msg}") from None
        except Exception as e:
            raise DeserializationError(f"Failed to deserialize from JSON: {e}") from None

    @classmethod
    def from_yaml(cls: type[T], yaml_str: str) -> T:
        """
        Deserialize a message from a YAML string.

        This validates that the type in the envelope matches the expected type.

        :param yaml_str: The YAML string to deserialize.
        :return: The deserialized message.
        :raises DeserializationError: If deserialization fails or YAML is invalid.
        :raises MismatchError: If the type doesn't match.
        """

        try:
            envelope = yaml.safe_load(yaml_str)
            cls._validate_envelope(envelope)

            # Check type matches
            if envelope["type"] != cls.get_type():
                raise MismatchError(expected=cls.get_type(), actual=envelope["type"])

            return cls(**envelope["data"])
        except yaml.YAMLError as e:
            raise DeserializationError(f"Invalid YAML format: {e}") from None
        except (MismatchError, DeserializationError):
            raise
        except ValidationError as e:
            first_error = e.errors()[0]
            field_path = " -> ".join(str(loc) for loc in first_error["loc"])
            error_msg = first_error["msg"]
            raise DeserializationError(f"Validation failed at {field_path}: {error_msg}") from None
        except Exception as e:
            raise DeserializationError(f"Failed to deserialize from YAML: {e}") from None

    @classmethod
    def load(cls: type[T], file_path: str, format: str | None = None) -> T:
        """
        Load a message from a file.

        The format is determined by the file extension if not specified.
        Supported formats: json, yaml, msgpack

        :param file_path: Path to load the file from.
        :param format: Optional format override ('json', 'yaml', 'msgpack').
        :return: The loaded message.
        :raises FileAccessError: If the file cannot be read.
        :raises DeserializationError: If deserialization fails.
        :raises MismatchError: If the type doesn't match.
        """

        # Determine format from extension if not specified
        if format is None:
            if file_path.endswith(".json"):
                format = "json"
            elif file_path.endswith((".yaml", ".yml")):
                format = "yaml"
            elif file_path.endswith((".msgpack", ".mp")):
                format = "msgpack"
            else:
                raise FileAccessError(f"Cannot determine format from extension: {file_path}")

        try:
            # Read and deserialize based on format
            if format == "json":
                with open(file_path) as f:
                    return cls.from_json(f.read())
            elif format == "yaml":
                with open(file_path) as f:
                    return cls.from_yaml(f.read())
            elif format == "msgpack":
                with open(file_path, "rb") as f:
                    return cls.unpack(f.read())
            else:
                raise FileAccessError(f"Unsupported format: {format}")
        except (DeserializationError, MismatchError):
            raise
        except FileNotFoundError:
            raise FileAccessError(f"File not found: {file_path}") from None
        except Exception as e:
            raise FileAccessError(f"Failed to load from {file_path}: {e}") from None

    @staticmethod
    def extract_type(data: bytes) -> str | None:
        """
        Extract the type identifier from a serialized message without full deserialization.

        This is useful for dynamic message routing where you need to determine the message
        type before deciding how to deserialize it.

        :param data: The MessagePack bytes to extract type from.
        :return: The type string, or None if no type is set.
        :raises DeserializationError: If the data cannot be parsed.

        Example:
        ```python
        packed = some_message.pack()
        msg_type = Message.extract_type(packed)
        match msg_type:
            case "user_profile":
                profile = UserProfile.unpack(packed)
            case "order_update":
                order = OrderUpdate.unpack(packed)
            case _:
                raise ValueError(f"Unknown message type: {msg_type}")
        ```
        """

        try:
            envelope = ormsgpack.unpackb(data)
            Message._validate_envelope(envelope)
            return envelope["type"]
        except (ValueError, TypeError) as e:
            raise DeserializationError(f"Failed to extract message type: {e}") from None
        except RecursionError:
            raise DeserializationError("Message structure too deeply nested") from None

    @staticmethod
    def extract_type_from_json(json_str: str) -> str | None:
        """
        Extract the type identifier from a JSON string without full deserialization.

        This is the JSON equivalent of extract_type for when messages are
        serialized as JSON instead of MessagePack.

        :param json_str: The JSON string to extract type from.
        :return: The type string, or None if no type is set.
        :raises DeserializationError: If the JSON cannot be parsed.
        """

        try:
            data = json.loads(json_str)
            Message._validate_envelope(data)
            return data["type"]
        except json.JSONDecodeError:
            raise DeserializationError("Invalid JSON format") from None

    @staticmethod
    def extract_data_as_json(data: bytes) -> dict:
        """
        Extract the data field from a serialized message as a dictionary.

        Useful for generic message handling where the exact type is unknown.

        :param data: The MessagePack bytes to extract data from.
        :return: The data field as a dictionary.
        :raises DeserializationError: If the data cannot be parsed.
        """

        try:
            envelope = ormsgpack.unpackb(data)
            Message._validate_envelope(envelope)
            return envelope["data"]
        except Exception as e:
            raise DeserializationError(f"Failed to extract message data: {e}") from None

    def pack(self) -> bytes:
        """
        Serialize the message to bytes using MessagePack.

        The message is wrapped in an envelope with the type identifier before
        serialization to match the Rust format.

        :return: The MessagePack bytes.
        :raises SerializationError: If serialization fails.
        """

        try:
            envelope = {
                "type": self.get_type(),
                "data": self.model_dump(mode="python", by_alias=True),
            }
            return ormsgpack.packb(envelope)
        except Exception as e:
            raise SerializationError(f"Failed to serialize message: {e}") from None

    def to_json(self, indent: int | None = None) -> str:
        """
        Serialize the message to a JSON string.

        The message is wrapped in an envelope with the type identifier.

        :param indent: Number of spaces to indent for pretty printing.
        :return: The JSON string.
        :raises SerializationError: If serialization fails.
        """

        try:
            envelope = {
                "type": self.get_type(),
                "data": self.model_dump(mode="python", by_alias=True),
            }
            return json.dumps(envelope, indent=indent)
        except Exception as e:
            raise SerializationError(f"Failed to serialize to JSON: {e}") from e

    def to_yaml(self) -> str:
        """
        Serialize the message to a YAML string.

        The message is wrapped in an envelope with the type identifier.

        :return: The YAML string.
        :raises SerializationError: If serialization fails.
        """

        try:
            return yaml.dump(self.to_dict(), default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise SerializationError(f"Failed to serialize to YAML: {e}") from None

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize with standard envelope structure.

        :return: The serialized object.
        """

        return {
            "type": self.get_type(),
            "data": self.model_dump(mode="python", by_alias=True),
        }

    def save(self, file_path: str, format: str | None = None) -> None:
        """
        Save the message to a file.

        The format is determined by the file extension if not specified.
        Supported formats: json, yaml, msgpack

        :param file_path: Path to save the file to.
        :param format: Optional format override ('json', 'yaml', 'msgpack').
        :raises FileAccessError: If the file cannot be written.
        :raises SerializationError: If serialization fails.
        """

        # Determine format from extension if not specified
        if format is None:
            if file_path.endswith(".json"):
                format = "json"
            elif file_path.endswith((".yaml", ".yml")):
                format = "yaml"
            elif file_path.endswith((".msgpack", ".mp")):
                format = "msgpack"
            else:
                raise FileAccessError(f"Cannot determine format from extension: {file_path}")

        try:
            # Serialize based on format
            if format == "json":
                content = self.to_json(indent=2)
                mode = "w"
            elif format == "yaml":
                content = self.to_yaml()
                mode = "w"
            elif format == "msgpack":
                content = self.pack()
                mode = "wb"
            else:
                raise FileAccessError(f"Unsupported format: {format}")

            # Write to file
            with open(file_path, mode) as f:
                f.write(content)
        except SerializationError:
            raise
        except Exception as e:
            raise FileAccessError(f"Failed to save to {file_path}: {e}") from None

    @staticmethod
    def _validate_envelope(envelope: Any) -> None:
        """
        Validate envelope structure.

        :param envelope: The envelope to validate.
        :raises DeserializationError: If envelope structure is invalid.
        """

        if not isinstance(envelope, dict):
            raise DeserializationError("Invalid message format: expected dictionary")
        if "type" not in envelope or "data" not in envelope:
            raise DeserializationError("Invalid message format: missing 'type' or 'data' field")

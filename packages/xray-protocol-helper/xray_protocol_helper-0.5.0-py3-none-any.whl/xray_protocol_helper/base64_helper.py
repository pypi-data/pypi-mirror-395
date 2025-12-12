import base64
import json
import logging
from typing import Optional


class Base64Helper:
    BOLLOCKS_LENGTH = 4

    @classmethod
    def fix_length(cls, encoded_base64_data):
        return encoded_base64_data + (len(encoded_base64_data) % cls.BOLLOCKS_LENGTH) * "="

    @classmethod
    def decode_base64(cls, encoded_base64_data) -> Optional[str]:
        """
            Decode base64
        """
        try:
            return base64.urlsafe_b64decode(cls.fix_length(encoded_base64_data=encoded_base64_data)).decode()
        except Exception as e:
            logging.error(f"error in decode `{encoded_base64_data}`, e: {e}")
            return None

    @classmethod
    def convert_json_to_dict(cls, jsonify_dict_data):
        try:
            result = json.loads(jsonify_dict_data)
            if type(result) == dict:
                return result
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logging.error(f"error in decode json `{jsonify_dict_data}`, e: {e}")

    @classmethod
    def decode_dict_base64(cls, encoded_dict_data) -> Optional[dict]:
        """
            Get dict from base64
        """
        jsonify_dict_data = cls.decode_base64(encoded_base64_data=encoded_dict_data)
        if not jsonify_dict_data:
            return
        return cls.convert_json_to_dict(jsonify_dict_data=jsonify_dict_data)

    @classmethod
    def encode_base64(cls, str_data: str) -> str:
        """
            Convert str to base64
        """
        return base64.urlsafe_b64encode(str_data.encode("utf-8")).decode("utf-8")

    @classmethod
    def encode_dict_base64(cls, dict_data: dict) -> str:
        """
            Convert dict to base64
        """
        jsonify_dict_data = json.dumps(dict_data)
        return cls.encode_base64(str_data=jsonify_dict_data)

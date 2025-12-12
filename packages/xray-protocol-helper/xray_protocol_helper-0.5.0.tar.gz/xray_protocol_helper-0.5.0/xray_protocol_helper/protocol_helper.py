import dataclasses
from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urlparse, parse_qs, quote
import urllib.parse as up

from xray_protocol_helper.base64_helper import Base64Helper
from xray_protocol_helper.xray_json_creator.xray_config_util import XrayConfigUtil


@dataclasses.dataclass
class XrayDecodeData:
    uri: str
    protocol: str
    address: str
    port: int
    sni: str = None
    host: str = None

    def __post_init__(self):
        if self.sni and "*." in self.sni:
            self.sni = self.sni.replace("*.", "")
        if self.host and "*." in self.host:
            self.host = self.host.replace("*.", "")


class AbstractXrayProtocol(ABC):
    REPLACE_DATA_LIST = ("\'", "\"", "`")

    def __init__(self, uri: str = None, config: dict = None):
        self.uri = uri
        self.config = config

    @property
    def pars_result(self):
        return urlparse(self.uri)

    @property
    def uri_body(self):
        return self.uri.split("://")[1]

    @property
    def dict_uri(self) -> dict:
        return Base64Helper.decode_dict_base64(encoded_dict_data=self.uri_body)

    @classmethod
    def clean_uri_string(cls, uri):
        uri = uri.strip()
        for replace_char in cls.REPLACE_DATA_LIST:
            uri = uri.replace(replace_char, "")
        uri = uri.split("#")[0]
        return uri

    def get_data(self) -> Optional[XrayDecodeData]:
        if self.uri is None and self.config:
            self.uri = self._get_uri_from_config()
        self._clean_uri()
        self._validate_uri()
        return self._get_data_from_uri()

    @abstractmethod
    def _get_uri_from_config(self) -> str:  # pragma: no cover
        pass

    @abstractmethod
    def _get_data_from_uri(self) -> Optional[XrayDecodeData]:  # pragma: no cover
        pass

    def _clean_uri(self):
        self.uri = self.clean_uri_string(uri=self.uri)

    def _validate_uri(self):
        result = XrayConfigUtil().get_xray_config(uri=self.uri, port=1080)
        if not result.status:
            raise ValueError("uri is not valid")


class VmessProtocol(AbstractXrayProtocol):
    def _get_data_from_uri(self) -> Optional[XrayDecodeData]:
        dict_url = self.dict_uri
        if not dict_url:
            return  # pragma: no cover
        address = dict_url.get("add")
        port = dict_url.get("port")
        sni = dict_url.get("sni")
        sni = None if sni == "" else sni
        host = dict_url.get("host")
        host = None if host == "" else host
        return XrayDecodeData(uri=self.uri, protocol="vmess", address=address, port=port, sni=sni, host=host)

    def _clean_uri(self):
        super()._clean_uri()
        dict_uri = self.dict_uri
        if not dict_uri:
            return
        dict_uri["ps"] = ""
        dict_uri = dict(sorted(dict_uri.items()))
        self.uri = f"vmess://{Base64Helper.encode_dict_base64(dict_data=dict_uri)}"

    def _get_uri_from_config(self) -> str:
        network_protocol = self._get_network_protocol()
        config_dict = self._call_network_protocol_func(network_protocol)
        return f"vmess://{Base64Helper.encode_dict_base64(config_dict)}"

    def _get_network_protocol(self):
        return self.config.get("outbounds", [{}])[0].get("streamSettings", {}).get("network", None)

    def _call_network_protocol_func(self, network_protocol):
        network_protocol_functions = {
            "ws": self.vmess_dict_ws_network,
            "grpc": self.vmess_dict_grpc_network,
            "tcp": self.vmess_dict_tcp_network,
        }
        network_protocol_func = network_protocol_functions.get(network_protocol)
        if network_protocol_func is None:
            raise ValueError("not found protocol")
        return network_protocol_func()

    @dataclasses.dataclass
    class CommonVmessData:
        config: dict

        def __post_init__(self):
            self.outbound_setting = self.config.get("outbounds", [{}])[0]
            self.stream_settings = self.outbound_setting.get("streamSettings", {})
            self.vnext_setting = self.outbound_setting.get("settings", {}).get("vnext", [{}])[0]
            self.address = self.vnext_setting.get("address", "")
            self.port = self.vnext_setting.get("port", "")
            if not self.address or not self.port:
                raise ValueError("address or port not found")
            self.id = self.vnext_setting.get("users", [{}])[0].get("id", "")
            self.alter_id = self.vnext_setting.get("users", [{}])[0].get("alterId", 64)

    def vmess_dict_ws_network(self):
        common_vmess_data = self.CommonVmessData(config=self.config)
        return {
            "ps": "",
            "add": common_vmess_data.address,
            "port": common_vmess_data.port,
            "tls": common_vmess_data.stream_settings.get("security", ""),
            "id": common_vmess_data.id,
            "aid": common_vmess_data.alter_id,

            "host": common_vmess_data.stream_settings.get("wsSettings", {}).get("headers", {}).get("Host", ""),
            "net": "ws",
            "path": common_vmess_data.stream_settings.get("wsSettings", {}).get("path", ""),
            "type": common_vmess_data.vnext_setting.get("users", [{}])[0].get("security", ""),
            "sni": common_vmess_data.stream_settings.get("tlsSettings", {}).get("serverName", "")
        }

    def vmess_dict_grpc_network(self):
        common_vmess_data = self.CommonVmessData(config=self.config)
        return {
            "v": "2",
            "ps": "",
            "add": common_vmess_data.vnext_setting.get("address", ""),
            "port": common_vmess_data.vnext_setting.get("port", ""),
            "id": common_vmess_data.id,
            "aid": common_vmess_data.alter_id,
            "net": "grpc",
            "type": "none",
            "host": "",
            "path": common_vmess_data.stream_settings.get("grpcSettings", {}).get("serviceName", ""),
            "tls": common_vmess_data.stream_settings.get("security", ""),
            "sni": common_vmess_data.stream_settings.get("tlsSettings", {}).get("serverName", ""),
            "scy": common_vmess_data.vnext_setting.get("users", [{}])[0].get("security", "")
        }

    def vmess_dict_tcp_network(self):
        common_vmess_data = self.CommonVmessData(config=self.config)
        return {
            "v": "2",
            "ps": "",
            "add": common_vmess_data.vnext_setting.get("address", ""),
            "port": common_vmess_data.vnext_setting.get("port", ""),
            "id": common_vmess_data.id,
            "aid": common_vmess_data.alter_id,
            "net": "tcp",
            "type": common_vmess_data.stream_settings.get("tcpSettings", {}).get("header", {}).get("type", ""),
            "host": common_vmess_data.stream_settings.get("tcpSettings", {}).get("header", {}).get("request", {})
                                                                            .get("headers", {}).get("Host", [])[0],
            "path": common_vmess_data.stream_settings.get("tcpSettings", {}).get("header", {}).get("request", {}).get(
                "path", [])[0],
            "tls": common_vmess_data.stream_settings.get("security", "")

        }


class VlessProtocol(AbstractXrayProtocol):
    PROTOCOL = "vless"

    def _get_data_from_uri(self) -> Optional[XrayDecodeData]:
        return self.get_vless_data()

    def get_vless_data(self, pars_result=None) -> Optional[XrayDecodeData]:
        if pars_result is None:
            pars_result = self.pars_result
        address = pars_result.hostname
        port = pars_result.port
        pars_query = parse_qs(pars_result.query)
        try:
            host = pars_query["host"][0]
            host = None if host == "" else host
        except KeyError:
            host = None
        try:
            sni = pars_query["sni"][0]
            sni = None if sni == "" else sni
        except KeyError:
            sni = None
        return XrayDecodeData(uri=self.uri, protocol=self.PROTOCOL, address=address, port=port, sni=sni, host=host)

    def _get_uri_from_config(self) -> str:
        network_protocol = self._get_network_protocol()
        return self._call_network_protocol_func(network_protocol)

    def _get_network_protocol(self):
        return self.config.get("outbounds", [{}])[0].get("streamSettings", {}).get("network", None)

    def _call_network_protocol_func(self, network_protocol):
        network_protocol_functions = {
            "ws": self.vless_uri_ws_network,
            "grpc": self.vless_uri_grpc_network,
            "tcp": self.vless_uri_tcp_network
        }
        network_protocol_func = network_protocol_functions.get(network_protocol)
        if network_protocol_func is None:
            raise ValueError("not found protocol")
        return network_protocol_func()

    @dataclasses.dataclass
    class CommonVlessData:
        config: dict

        def __post_init__(self):
            self.outbound_setting = self.config.get("outbounds", [{}])[0]
            self.stream_settings = self.outbound_setting.get("streamSettings", {})
            self.vnext_setting: dict = self.outbound_setting.get("settings", {}).get("vnext", [{}])[0]
            self.address = self.vnext_setting.get("address")
            self.port = self.vnext_setting.get("port")
            if not self.address or not self.port:
                raise ValueError("address or port not found")
            self.vless_settings = self.vnext_setting.get("users", [{}])[0]
            self.id = self.vless_settings.get("id")
            self.encryption = self.vless_settings.get("encryption", "")
            self.security = self.stream_settings.get("security", "")
            self.network_type = self.stream_settings.get("network", "")

    def vless_uri_ws_network(self):
        common_vless_data = self.CommonVlessData(config=self.config)
        path = quote(common_vless_data.stream_settings.get("wsSettings", {}).get("path", ""), safe="")
        vless_host = common_vless_data.stream_settings.get("wsSettings", {}).get("headers", {}).get("Host", "")
        vless_host = vless_host.replace(" ", "").strip()
        return f"vless://{common_vless_data.id}@{common_vless_data.address}:{common_vless_data.port}?" \
               f"path={path}&" \
               f"security={common_vless_data.security}&" \
               f"encryption={common_vless_data.encryption}&" \
               f"host={vless_host}&" \
               f"type={common_vless_data.network_type}"

    def vless_uri_tcp_network(self) -> str:
        common_vless_data = self.CommonVlessData(config=self.config)
        params = {
            "encryption": common_vless_data.encryption,
            "type": common_vless_data.network_type,
            "headerType": common_vless_data.stream_settings.get("tcpSettings", {}).get("header", {}).get("type",
                                                                                                         "none"),
            "security": common_vless_data.security
        }
        params = {k: v for k, v in params.items() if v not in [None, "", "none"]}
        return f"vless://{common_vless_data.id}@{common_vless_data.address}:{common_vless_data.port}?{up.urlencode(params)}"

    def vless_uri_grpc_network(self):
        common_vless_data = self.CommonVlessData(config=self.config)
        service_name = common_vless_data.stream_settings.get("grpcSettings", {}).get("serviceName", "")
        sni = common_vless_data.stream_settings.get("tlsSettings", {}).get("serverName", "")
        return f"vless://{common_vless_data.id}@{common_vless_data.address}:{common_vless_data.port}?" \
               f"mode=gun&" \
               f"security={common_vless_data.security}&" \
               f"encryption={common_vless_data.encryption}&" \
               f"type={common_vless_data.network_type}&" \
               f"serviceName={service_name}&" \
               f"sni={sni}"


class ShadowSocksProtocol(VlessProtocol):
    PROTOCOL = "ss"

    def _get_data_from_uri(self) -> Optional[XrayDecodeData]:
        if "@" in self.uri:
            return self.get_vless_data()

        decode_data = Base64Helper.decode_base64(self.uri_body)
        if not decode_data:
            return
        part_result = urlparse(f"ss://{decode_data}")
        return self.get_vless_data(pars_result=part_result)

    def _get_uri_from_config(self) -> str:
        base_config = self.config.get("outbounds", [{}])[0].get("settings", {}).get("servers", [{}])[0]
        address = base_config.get("address")
        port = base_config.get("port")
        method = base_config.get("method", "")
        password = base_config.get("password", "")
        body_base = f"{method}:{password}"
        encode_data = Base64Helper.encode_base64(body_base)
        return f"ss://{encode_data}@{address}:{port}"


class TrojanProtocol(VlessProtocol):
    PROTOCOL = "trojan"

    def _get_uri_from_config(self) -> str:  # pragma: no cover
        return ""


class SocksProtocol(VlessProtocol):
    PROTOCOL = "socks"

    def _get_uri_from_config(self) -> str:  # pragma: no cover
        return ""


class ProtocolHelper:
    PROTOCOL_CLASS = {
        "vmess": VmessProtocol,
        "vless": VlessProtocol,
        "ss": ShadowSocksProtocol,
        "shadowsocks": ShadowSocksProtocol,
        "trojan": TrojanProtocol,
        "socks": SocksProtocol
    }

    def __init__(self, uri: str = None, config: dict = None):
        self.uri = uri
        self.config = config

    def get_protocol_object(self, protocol) -> AbstractXrayProtocol:
        protocol_class = self.PROTOCOL_CLASS.get(protocol)
        if protocol_class is None:
            raise ValueError("not found protocol")
        return protocol_class(uri=self.uri, config=self.config)

    def get_data(self) -> Optional[XrayDecodeData]:
        if self.uri:
            self.uri = AbstractXrayProtocol.clean_uri_string(uri=self.uri)
            protocol = urlparse(self.uri).scheme
        elif self.config:
            protocol = self.config.get("outbounds", [{}])[0].get("protocol", "")
        else:
            return None
        protocol_obj = self.get_protocol_object(protocol=protocol)
        return protocol_obj.get_data()


if __name__ == '__main__':
    import json

    with open("/home/user/PycharmProjects/xray_protocol_helper/temp.json", "r") as file:
        json_data = json.load(file)
    for x in json_data:
        xray = ProtocolHelper(config=x).get_data()
        print(xray)

from werkzeug.routing import BaseConverter


class EntityUUIDConverter(BaseConverter):
    """This converter only accepts entity UUID-like strings; lowercase and no dashes
       1824ab251764ed6dfaa78b37b41e0f7d.

    To use, add the following rule to the app:
    app.url_map.converters["entity_uuid"] = EntityUUIDConverter

    Rule('/object/<entity_uuid:identifier>')
    """

    regex = r"^[a-f0-9]{32}$"

    def to_python(self, value: str) -> str:
        return value

    def to_url(self, value: str) -> str:
        return value


class SenNetIDConverter(BaseConverter):
    """This converter only accepts SenNet ID-like strings SNT123.ABCD.567.

    To use, add the following rule to the app:
    app.url_map.converters["sennet_id"] = SenNetIDConverter

    Rule('/object/<sennet_id:identifier>')
    """

    regex = r"^SNT[0-9]{3}.[A-Z]{4}.[0-9]{3}$"

    def to_python(self, value: str) -> str:
        return value

    def to_url(self, value: str) -> str:
        return value


class SenNetEntityIDConverter(BaseConverter):
    """This converter only accepts entity UUID-like strings; lowercase and no dashes,
       1824ab251764ed6dfaa78b37b41e0f7d or SenNet ID-like strings, SNT123.ABCD.567.

    To use, add the following rule to the app:
    app.url_map.converters["entity_id"] = EntityIDConverter

    Rule('/object/<entity_id:identifier>')
    """

    regex = r"(?:^SNT[0-9]{3}.[A-Z]{4}.[0-9]{3}$)|(?:^[a-f0-9]{32}$)"

    def to_python(self, value: str) -> str:
        return value

    def to_url(self, value: str) -> str:
        return value


class HuBMAPIDConverter(BaseConverter):
    """This converter only accepts HuBMAP ID-like strings HBM123.ABCD.567.

    To use, add the following rule to the app:
    app.url_map.converters["hubmap_id"] = HuBMAPIDConverter

    Rule('/object/<hubmap_id:identifier>')
    """

    regex = r"^HBM[0-9]{3}.[A-Z]{4}.[0-9]{3}$"

    def to_python(self, value: str) -> str:
        return value

    def to_url(self, value: str) -> str:
        return value


class HuBMAPEntityIDConverter(BaseConverter):
    """This converter only accepts entity UUID-like strings; lowercase and no dashes,
       1824ab251764ed6dfaa78b37b41e0f7d or HuBMAP ID-like strings, HBM123.ABCD.567.

    To use, add the following rule to the app:
    app.url_map.converters["entity_id"] = HuBMAPEntityIDConverter

    Rule('/object/<entity_id:identifier>')
    """

    regex = r"(?:^HBM[0-9]{3}.[A-Z]{4}.[0-9]{3}$)|(?:^[a-f0-9]{32}$)"

    def to_python(self, value: str) -> str:
        return value

    def to_url(self, value: str) -> str:
        return value

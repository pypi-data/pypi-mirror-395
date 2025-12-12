import pytest
from flask import Flask

from atlas_consortia_commons import converter


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.mark.parametrize(
    "input,expected_result",
    [
        ("1824ab251764ed6dfaa78b37b41e0f7d", 200),
        ("b251764ed6dfaa78", 404),
    ],
)
def test_entity_uuid_converter(app, input, expected_result):
    """Test that the entity uuid converter works as expected."""
    app.url_map.converters["entity_uuid"] = converter.EntityUUIDConverter

    @app.route("/<entity_uuid:identifier>")
    def test_route(identifier):
        return "OK", 200

    with app.test_client() as client:
        res = client.get(f"/{input}")
        assert res.status_code == expected_result


@pytest.mark.parametrize(
    "input,expected_result",
    [
        ("SNT652.BMSZ.387", 200),
        ("HBM652.BMSZ.387", 404),
        ("1824ab251764ed6dfaa78b37b41e0f7d", 404),
        ("b251764ed6dfaa78", 404),
    ],
)
def test_sennet_id_converter(app, input, expected_result):
    """Test that the SenNet id converter works as expected."""
    app.url_map.converters["sennet_id"] = converter.SenNetIDConverter

    @app.route("/<sennet_id:identifier>")
    def test_route(identifier):
        return "OK", 200

    with app.test_client() as client:
        res = client.get(f"/{input}")
        assert res.status_code == expected_result


@pytest.mark.parametrize(
    "input,expected_result",
    [
        ("SNT652.BMSZ.387", 200),
        ("1824ab251764ed6dfaa78b37b41e0f7d", 200),
        ("HBM652.BMSZ.387", 404),
        ("b251764ed6dfaa78", 404),
    ],
)
def test_sennet_entity_id_converter(app, input, expected_result):
    """Test that the SenNet entity uuid converter works as expected."""
    app.url_map.converters["entity_id"] = converter.SenNetEntityIDConverter

    @app.route("/<entity_id:identifier>")
    def test_route(identifier):
        return "OK", 200

    with app.test_client() as client:
        res = client.get(f"/{input}")
        assert res.status_code == expected_result


@pytest.mark.parametrize(
    "input,expected_result",
    [
        ("HBM652.BMSZ.387", 200),
        ("SNT652.BMSZ.387", 404),
        ("1824ab251764ed6dfaa78b37b41e0f7d", 404),
        ("b251764ed6dfaa78", 404),
    ],
)
def test_hubmap_id_converter(app, input, expected_result):
    """Test that the HuBMAP id converter works as expected."""
    app.url_map.converters["hubmap_id"] = converter.HuBMAPIDConverter

    @app.route("/<hubmap_id:identifier>")
    def test_route(identifier):
        return "OK", 200

    with app.test_client() as client:
        res = client.get(f"/{input}")
        assert res.status_code == expected_result


@pytest.mark.parametrize(
    "input,expected_result",
    [
        ("HBM652.BMSZ.387", 200),
        ("1824ab251764ed6dfaa78b37b41e0f7d", 200),
        ("SNT652.BMSZ.387", 404),
        ("b251764ed6dfaa78", 404),
    ],
)
def test_hubmap_entity_id_converter(app, input, expected_result):
    """Test that the HuBMAP entity id converter works as expected."""
    app.url_map.converters["entity_id"] = converter.HuBMAPEntityIDConverter

    @app.route("/<entity_id:identifier>")
    def test_route(identifier):
        return "OK", 200

    with app.test_client() as client:
        res = client.get(f"/{input}")
        assert res.status_code == expected_result

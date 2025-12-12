"""Performance benchmarks using pytest-benchmark.

These tests measure the performance of core operations to track
performance regressions over time.
"""

import pytest

from msn_weather_wrapper import Location, WeatherClient
from msn_weather_wrapper.models import WeatherData


@pytest.mark.benchmark(group="client")
def test_client_initialization_benchmark(benchmark):
    """Benchmark WeatherClient initialization time."""
    result = benchmark(WeatherClient)
    assert result is not None


@pytest.mark.benchmark(group="client")
def test_client_context_manager_benchmark(benchmark):
    """Benchmark WeatherClient context manager overhead."""

    def context_manager_usage():
        with WeatherClient() as client:
            return client

    result = benchmark(context_manager_usage)
    assert result is not None


@pytest.mark.benchmark(group="models")
def test_location_creation_benchmark(benchmark):
    """Benchmark Location model instantiation."""
    result = benchmark(Location, city="London", country="UK")
    assert result.city == "London"
    assert result.country == "UK"


@pytest.mark.benchmark(group="models")
def test_location_with_coordinates_benchmark(benchmark):
    """Benchmark Location creation with coordinates."""
    result = benchmark(
        Location, city="Tokyo", country="Japan", latitude=35.6762, longitude=139.6503
    )
    assert result.latitude == 35.6762
    assert result.longitude == 139.6503


@pytest.mark.benchmark(group="models")
def test_weather_data_creation_benchmark(benchmark):
    """Benchmark WeatherData model instantiation."""
    location = Location(city="Paris", country="France")

    def create_weather():
        return WeatherData(
            location=location,
            temperature=20.5,
            condition="Partly Cloudy",
            humidity=65,
            wind_speed=15.2,
        )

    result = benchmark(create_weather)
    assert result.temperature == 20.5
    assert result.condition == "Partly Cloudy"


@pytest.mark.benchmark(group="parsing")
def test_temperature_parsing_benchmark(benchmark):
    """Benchmark temperature value parsing."""
    from msn_weather_wrapper.client import WeatherClient

    client = WeatherClient()
    html_content = '<span class="cur-temp">72°</span>'

    def parse_temp():
        return client._extract_temperature(html_content)  # type: ignore

    result = benchmark(parse_temp)
    assert result is not None


@pytest.mark.benchmark(group="parsing")
def test_condition_parsing_benchmark(benchmark):
    """Benchmark weather condition extraction."""
    from msn_weather_wrapper.client import WeatherClient

    client = WeatherClient()
    html_content = '<div data-id="CurrentDescription">Sunny</div>'

    def parse_condition():
        return client._extract_condition(html_content)  # type: ignore

    result = benchmark(parse_condition)
    assert result == "Sunny"


@pytest.mark.benchmark(group="conversion")
def test_fahrenheit_to_celsius_benchmark(benchmark):
    """Benchmark temperature conversion from Fahrenheit to Celsius."""
    from msn_weather_wrapper.client import WeatherClient

    client = WeatherClient()

    def convert_temp():
        return client._fahrenheit_to_celsius(72)  # type: ignore

    result = benchmark(convert_temp)
    assert abs(result - 22.22) < 0.01


@pytest.mark.benchmark(group="conversion")
def test_mph_to_kmh_benchmark(benchmark):
    """Benchmark wind speed conversion from MPH to km/h."""
    from msn_weather_wrapper.client import WeatherClient

    client = WeatherClient()

    def convert_speed():
        return client._mph_to_kmh(10)  # type: ignore

    result = benchmark(convert_speed)
    assert abs(result - 16.09) < 0.01


@pytest.mark.benchmark(group="validation")
def test_location_validation_benchmark(benchmark):
    """Benchmark Location model validation."""

    def create_and_validate():
        return Location(
            city="New York",
            country="USA",
            latitude=40.7128,
            longitude=-74.0060,
        )

    result = benchmark(create_and_validate)
    assert result.city == "New York"


@pytest.mark.benchmark(group="validation")
def test_weather_data_validation_benchmark(benchmark):
    """Benchmark WeatherData model validation with all fields."""
    location = Location(city="Berlin", country="Germany")

    def create_and_validate():
        return WeatherData(
            location=location,
            temperature=15.5,
            condition="Cloudy",
            humidity=70,
            wind_speed=20.0,
        )

    result = benchmark(create_and_validate)
    assert result.humidity == 70
    assert result.wind_speed == 20.0


@pytest.mark.benchmark(group="string-ops")
def test_location_repr_benchmark(benchmark):
    """Benchmark Location __repr__ method."""
    location = Location(city="Sydney", country="Australia")

    def get_repr():
        return repr(location)

    result = benchmark(get_repr)
    assert "Sydney" in result
    assert "Australia" in result


@pytest.mark.benchmark(group="string-ops")
def test_weather_data_repr_benchmark(benchmark):
    """Benchmark WeatherData __repr__ method."""
    location = Location(city="Mumbai", country="India")
    weather = WeatherData(
        location=location,
        temperature=28.0,
        condition="Hot",
        humidity=80,
        wind_speed=10.0,
    )

    def get_repr():
        return repr(weather)

    result = benchmark(get_repr)
    assert "Mumbai" in result
    assert "28.0" in result

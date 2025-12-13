"""Template for new integration tests."""

from .. import testing


def template_demo(expo=0.2, npoints=10):
    for _ in range(2):
        template_test(expo=expo, npoints=npoints)


@testing.integration_fixture
def template_fixture1():
    print("setup 'template_fixture1'")
    yield "value1"
    print("teardown 'template_fixture1' always called, also when test fails")


@testing.integration_fixture
def template_fixture2(template_fixture1):
    print("execute 'template_fixture2'")
    assert template_fixture1 == "value1"
    return "value2"


@testing.integration_test
def template_test(template_fixture1, template_fixture2, expo=0.2, npoints=10):
    assert template_fixture1 == "value1"
    assert template_fixture2 == "value2"

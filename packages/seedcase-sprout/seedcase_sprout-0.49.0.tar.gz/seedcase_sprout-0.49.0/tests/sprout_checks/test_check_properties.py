from pathlib import Path

import check_datapackage as cdp
from pytest import fixture, mark, raises

from seedcase_sprout.check_properties import (
    DataResourceError,
    check_package_properties,
    check_properties,
    check_resource_properties,
)
from seedcase_sprout.examples import example_resource_properties
from seedcase_sprout.properties import (
    ContributorProperties,
    LicenseProperties,
    PackageProperties,
    ResourceProperties,
    SourceProperties,
)
from seedcase_sprout.sprout_checks.required_fields import (
    PACKAGE_SPROUT_REQUIRED_FIELDS,
    RESOURCE_SPROUT_REQUIRED_FIELDS,
)


@fixture
def properties():
    return PackageProperties(
        name="package-1",
        id="abc1",
        title="Package 1",
        description="A package.",
        version="1.0.0",
        created="2024-05-14T05:00:01+00:00",
        licenses=[LicenseProperties(name="a-license")],
        contributors=[ContributorProperties(title="a contributor")],
        sources=[SourceProperties(title="a source")],
        resources=[
            ResourceProperties(
                name="resource-1",
                title="Resource 1",
                description="A resource.",
            ),
            ResourceProperties(
                name="resource-2",
                title="Resource 2",
                description="A second resource.",
            ),
        ],
    )


def test_passes_correct_properties(properties):
    """Should pass if all required properties are present and correct."""
    assert check_properties(properties) == properties
    assert check_package_properties(properties) == properties
    assert check_resource_properties(properties.resources[0]) == properties.resources[0]
    assert check_resource_properties(properties.resources[1]) == properties.resources[1]


@mark.parametrize("resources", [None, [], [ResourceProperties()]])
def test_check_package_properties_excludes_resource_properties(properties, resources):
    """Should pass if there are no resources or if individual resources are
    incorrect."""
    properties.resources = resources

    assert check_package_properties(properties) == properties


def test_check_package_properties_flags_bad_resource_type(properties):
    """Should raise an error if the `resources` property as a whole is the wrong
    type."""
    properties.resources = 123

    with raises(cdp.DataPackageError):
        check_package_properties(properties)


def test_error_incorrect_argument():
    """Should be an error if it isn't a `*Properties` object."""
    with raises(TypeError):
        check_properties(ResourceProperties())

    with raises(TypeError):
        check_resource_properties(PackageProperties())

    with raises(TypeError):
        check_properties("")

    with raises(TypeError):
        check_properties([1, 2, 3])

    with raises(TypeError):
        check_package_properties([1, 2, 3])

    with raises(TypeError):
        check_package_properties("")

    with raises(TypeError):
        check_resource_properties([1, 2, 3])

    with raises(TypeError):
        check_resource_properties("")


@mark.parametrize("field", PACKAGE_SPROUT_REQUIRED_FIELDS)
def test_error_missing_required_package_properties(properties, field):
    """Should be an error if a required package properties is missing."""
    delattr(properties, field)

    # All properties checks
    with raises(cdp.DataPackageError):
        check_properties(properties)

    # Package only checks
    with raises(cdp.DataPackageError):
        check_package_properties(properties)


def test_check_in_strict_mode(properties):
    """Properties should be checked in strict mode."""
    properties.name = "a name with spaces"

    # All properties checks
    with raises(cdp.DataPackageError):
        check_properties(properties)

    # Package only checks
    with raises(cdp.DataPackageError):
        check_package_properties(properties)


@mark.parametrize("name", PACKAGE_SPROUT_REQUIRED_FIELDS)
@mark.parametrize("value", ["", []])
def test_error_blank_package_properties(properties, name, value):
    """Should be an error when a required package field is blank."""
    setattr(properties, name, value)

    # All properties checks
    with raises(cdp.DataPackageError):
        check_properties(properties)

    # Package only checks
    with raises(cdp.DataPackageError):
        check_package_properties(properties)


@mark.parametrize(
    "field, value",
    [
        ("contributors", ContributorProperties(title="")),
        ("sources", SourceProperties(title="")),
        ("licenses", LicenseProperties(name="")),
        ("licenses", LicenseProperties(path="")),
    ],
)
def test_error_blank_nested_properties(properties, field, value):
    """Should have errors when the nested required properties are blank."""
    setattr(properties, field, [value])

    # All properties checks
    with raises(cdp.DataPackageError):
        check_properties(properties)

    # Package only checks
    with raises(cdp.DataPackageError):
        check_package_properties(properties)


# Resource properties specific --------------------------------------------


def test_passes_good_resource_properties():
    """Should pass good resource properties."""
    properties = example_resource_properties()

    assert check_resource_properties(properties) == properties


def test_data_resource_error():
    """`DataResourceError` message should be formatted correctly."""
    properties = example_resource_properties()
    properties.name = None

    with raises(DataResourceError) as error:
        check_resource_properties(properties)

    # TODO: remove all references to "package"
    # assert "package" not in str(error.value)
    assert "resources[0]" not in str(error.value)


def test_errors_flagged_for_fields_with_multipart_name():
    """Errors should be flagged when the name of the field has more than one word."""
    properties = example_resource_properties()
    assert properties.schema
    properties.schema.primary_key = []

    with raises(DataResourceError):
        check_resource_properties(properties)


@mark.parametrize(
    "field",
    RESOURCE_SPROUT_REQUIRED_FIELDS,
)
def test_error_missing_required_resource_properties(properties, field):
    """Should be an error if a required resource properties is missing."""
    delattr(properties.resources[0], field)

    # All properties checks
    with raises(cdp.DataPackageError):
        check_properties(properties)

    # Resource only checks
    with raises(DataResourceError):
        check_resource_properties(properties.resources[0])


@mark.parametrize("name", RESOURCE_SPROUT_REQUIRED_FIELDS)
def test_error_blank_resource_properties(properties, name):
    """Should be an error when one required resource field is blank."""
    setattr(properties.resources[0], name, "")

    # All properties checks
    with raises(cdp.DataPackageError):
        check_properties(properties)

    # Resource only checks
    with raises(DataResourceError):
        check_resource_properties(properties.resources[0])


@mark.parametrize(
    "path", ["", [], 123, str(Path("resources", "1")), "/bad/path/data.csv"]
)
def test_error_no_resource_name_in_path(properties, path):
    """Should be an error when the resource name isn't in the path or the path is
    empty."""
    properties.resources[0].path = path

    # All properties checks
    with raises(cdp.DataPackageError):
        check_properties(properties)

    # Resource only checks
    with raises(DataResourceError):
        check_resource_properties(properties.resources[0])


def test_excludes_path_or_data_required(properties):
    """When both path and data are missing, only path should be flagged."""
    delattr(properties.resources[0], "path")

    # All properties checks
    with raises(cdp.DataPackageError) as error1:
        check_properties(properties)
    assert "`data`" not in str(error1.value)

    # Resource only checks
    with raises(DataResourceError) as error2:
        check_resource_properties(properties.resources[0])
    assert "`data`" not in str(error2.value)


def test_does_not_suggest_path_can_be_array(properties):
    """Should not suggest that path can be an array."""
    properties.resources[0].path = 123

    # All properties checks
    with raises(cdp.DataPackageError) as error1:
        check_properties(properties)
    assert "array" not in str(error1.value)

    # Resource only checks
    with raises(DataResourceError) as error2:
        check_resource_properties(properties.resources[0])
    assert "array" not in str(error2.value)


def test_does_not_suggest_path_should_match_regex(properties):
    """Should not suggest that the path has to match a general path regex."""
    properties.resources[0].path = "/bad/path"

    # All properties checks
    with raises(cdp.DataPackageError) as error1:
        check_properties(properties)
    assert "not match" not in str(error1.value)

    # Resource only checks
    with raises(DataResourceError) as error2:
        check_resource_properties(properties.resources[0])
    assert "not match" not in str(error2.value)


def test_does_not_suggest_path_array_should_be_non_empty(properties):
    """Should not suggest that a path that is an array should not be empty."""
    properties.resources[0].path = []

    # All properties checks
    with raises(cdp.DataPackageError) as error1:
        check_properties(properties)
    assert "non-empty" not in str(error1.value)

    # Resource only checks
    with raises(DataResourceError) as error2:
        check_resource_properties(properties.resources[0])
    assert "non-empty" not in str(error2.value)

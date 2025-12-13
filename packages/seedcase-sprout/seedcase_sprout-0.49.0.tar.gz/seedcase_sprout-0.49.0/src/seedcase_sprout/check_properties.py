from dataclasses import replace
from typing import Any

import check_datapackage as cdp

from seedcase_sprout.internals.create import _create_resource_data_path
from seedcase_sprout.internals.functionals import _map
from seedcase_sprout.properties import PackageProperties, ResourceProperties
from seedcase_sprout.sprout_checks.is_resource_name_correct import (
    _is_resource_name_correct,
)
from seedcase_sprout.sprout_checks.required_fields import (
    PACKAGE_SPROUT_REQUIRED_FIELDS,
    RESOURCE_SPROUT_REQUIRED_FIELDS,
)


def check_package_properties(properties: Any) -> PackageProperties:
    """Check `PackageProperties` (not `ResourceProperties`) against the requirements.

    Package `properties` are checked against the Data Package standard and the following
    Sprout-specific requirements:

    - Sprout-specific required fields are present.
    - Required fields are not blank.

    Args:
        properties: The package properties to check.

    Returns:
        The `properties` if all checks pass.

    Raises:
        DataPackageError: an error flagging issues in the package properties.
    """
    package_properties = _check_is_package_properties_type(properties)
    _generic_check_properties(
        package_properties,
        exclusions=[
            cdp.Exclusion(jsonpath="$.resources[*] | $.resources[*].*"),
            cdp.Exclusion(jsonpath="$.resources", type="required"),
            cdp.Exclusion(jsonpath="$.resources", type="minItems"),
        ],
    )
    return package_properties


def check_properties(properties: Any) -> PackageProperties:
    """Check that all `properties` match Sprout's requirements.

    If the resources property hasn't been filled in yet, this will only check
    the package properties. The `properties` are checked against the Data
    Package standard and the following Sprout-specific requirements:

    - Sprout-specific required fields are present
    - Required fields are not blank

    If the resources property *has* been filled in, these resource properties will also
    be checked:

    - `path` is of type string.
    - `path` includes resource name.
    - `data` is not set.

    Args:
        properties: The properties to check.

    Returns:
        The `properties` if all checks pass.

    Raises:
        DataPackageError: an error flagging issues in the properties.
    """
    package_properties = _check_is_package_properties_type(properties)
    if not package_properties.resources:
        check_package_properties(package_properties)
    else:
        _generic_check_properties(package_properties)
    return package_properties


class DataResourceError(Exception):
    """Error listing issues in a data resource."""

    def __init__(
        self,
        issues: list[cdp.Issue],
    ) -> None:
        """Create a `DataResourceError` from `cdp.Issue`s."""
        issues = _map(
            issues,
            lambda issue: replace(
                issue,
                jsonpath=issue.jsonpath.replace(".resources[0]", "", 1),
            ),
        )
        message = cdp.explain(issues).replace("`datapackage.json`", "resource", 1)
        super().__init__(message)


def check_resource_properties(properties: Any) -> ResourceProperties:
    """Checks that only the resource `properties` match Sprout's requirements.

    All resource `properties` are checked against the Data Package standard and
    the following Sprout-specific requirements:

    - Sprout-specific required fields are present.
    - Required fields are not blank.
    - `path` is of type string.
    - `path` includes resource name.
    - `data` is not set.

    Args:
        properties: The resource properties to check.

    Returns:
        Outputs the `properties` if all checks pass.

    Raises:
        DataResourceError: an error flagging issues in the resource properties.
    """
    resource_properties = _check_is_resource_properties_type(properties)
    issues = _generic_check_properties(
        PackageProperties(resources=[resource_properties]),
        exclusions=[cdp.Exclusion(jsonpath="$.*")],
        error=False,
    )
    if issues:
        raise DataResourceError(issues) from None

    return resource_properties


def _generic_check_properties(
    properties: PackageProperties,
    exclusions: list[cdp.Exclusion] = [],
    error: bool = True,
) -> list[cdp.Issue]:
    """A generic check for Sprout-specific requirements on the Frictionless standard.

    All `properties`, excluding those in `exclusions`, are checked against the Data
    Package standard as well as the following Sprout-specific requirements:

    - Sprout-specific required fields are present
    - Required fields are not blank
    - Resource `path` is of type string
    - Resource `path` includes resource name
    - Resource `data` is not set

    Args:
        properties: The full package properties to check, including resource properties.
        exclusions: A list of exclusions for any checks to ignore.
        error: Whether to raise an error if any issues are found.

    Returns:
        Outputs the `properties` object if all checks pass.

    Raises:
        DataPackageError: an error flagging issues in the properties.
    """
    package_required_checks = _map(
        PACKAGE_SPROUT_REQUIRED_FIELDS,
        lambda field: cdp.RequiredCheck(
            jsonpath=f"$.{field}",
            message=f"'{field}' is a required property",
        ),
    )

    resource_required_checks = _map(
        RESOURCE_SPROUT_REQUIRED_FIELDS,
        lambda field: cdp.RequiredCheck(
            jsonpath=f"$.resources[*].{field}",
            message=f"'{field}' is a required property",
        ),
    )

    not_blank_resource_fields = _map(
        RESOURCE_SPROUT_REQUIRED_FIELDS, lambda field: f"$.resources[*].{field}"
    )
    not_blank = cdp.CustomCheck(
        jsonpath=(
            f"$.{' | '.join(PACKAGE_SPROUT_REQUIRED_FIELDS)} "
            "| $.contributors[*].title"
            "| $.sources[*].title"
            "| $.licenses[*].name"
            "| $.licenses[*].path"
            f"| {' | '.join(not_blank_resource_fields)}"
        ),
        message="This property must not be empty.",
        check=lambda value: bool(value),
        type="not-blank",
    )
    resource_path_string = cdp.CustomCheck(
        jsonpath="$.resources[*].path",
        message="Resource path must be of type string.",
        check=lambda value: isinstance(value, str),
        type="resource-path-string",
    )
    resource_path_format = cdp.CustomCheck(
        jsonpath="$.resources[*]",
        message=(
            "Resource path must have the format "
            "`resources/<resource-name>/data.parquet`."
        ),
        check=lambda value: _check_resource_path_format(value),
        type="resource-path-format",
    )
    # TODO: This will never fail, as `data` property is removed in `Properties`. Fix?
    no_resource_data = cdp.CustomCheck(
        jsonpath="$.resources[*].data",
        message=(
            "Sprout doesn't use the `data` field, instead it expects data "
            "in separate files that are given in the `path` field."
        ),
        check=lambda value: value is None,
        type="no-inline-data",
    )
    exclude_resource_data = cdp.Exclusion(jsonpath="$.resources[*].data")
    exclude_resource_path_or_data_required = cdp.Exclusion(
        jsonpath="$.resources[*]", type="required"
    )
    # Sprout only uses string for path, so don't need this check.
    exclude_resource_path_type = cdp.Exclusion(
        jsonpath="$.resources[*].path", type="type"
    )
    # Sprout has its own rules for naming of the paths.
    exclude_resource_path_pattern = cdp.Exclusion(
        jsonpath="$.resources[*].path", type="pattern"
    )
    # Sprout doesn't allow path to be an array, so exclude this.
    exclude_resource_path_min_items = cdp.Exclusion(
        jsonpath="$.resources[*].path", type="minItems"
    )

    return cdp.check(
        properties.compact_dict,
        config=cdp.Config(
            strict=True,
            exclusions=[
                exclude_resource_data,
                exclude_resource_path_or_data_required,
                exclude_resource_path_type,
                exclude_resource_path_pattern,
                exclude_resource_path_min_items,
            ]
            + exclusions,
            extensions=cdp.Extensions(
                required_checks=package_required_checks + resource_required_checks,
                custom_checks=[
                    not_blank,
                    resource_path_string,
                    resource_path_format,
                    no_resource_data,
                ],
            ),
        ),
        error=error,
    )


def _check_resource_path_format(resource_properties: Any) -> bool:
    """Checks if the data path in the resource properties has the correct format.

    As the path is constructed from the resource name, its format can only be checked
    if the resource name is correct.
    """
    if not isinstance(resource_properties, dict):
        return True

    name = resource_properties.get("name")
    path = resource_properties.get("path")

    if (
        # Do not check path if name is incorrect
        not _is_resource_name_correct(name)
        # Do not check path if not string
        or not isinstance(path, str)
        # Do not check path if blank
        or path == ""
    ):
        return True

    expected_path = _create_resource_data_path(str(name))
    return path == expected_path


def _check_is_package_properties_type(properties: Any) -> PackageProperties:
    if not isinstance(properties, PackageProperties):
        raise TypeError(
            f"Expected properties to be a PackageProperties object,"
            f"but the object is {type(properties)}"
        )
    return properties


def _check_is_resource_properties_type(properties: Any) -> ResourceProperties:
    if not isinstance(properties, ResourceProperties):
        raise TypeError(
            f"Expected properties to be a ResourceProperties object,"
            f"but the object is {type(properties)}"
        )
    return properties

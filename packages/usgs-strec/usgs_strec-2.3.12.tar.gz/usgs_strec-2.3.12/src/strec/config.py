# stdlib imports
import logging
import pathlib

# third party libraries
from configobj import ConfigObj, flatten_errors, get_extra_values
from validate import ValidateError, Validator


def get_select_config(select_conf):
    select_spec = pathlib.Path(__file__).parent / "data" / "selectspec.conf"
    config = ConfigObj(str(select_conf), configspec=str(select_spec))
    validator = get_custom_validator()
    results = config.validate(validator, copy=True)
    if not isinstance(results, bool):
        return None, results
    return config, results


def get_custom_validator():
    """
    Returns a validator suitable for validating the ShakeMap config
    files.

    Returns:
        :class:`Validator`: A Validator object.

    """
    fdict = {
        "nanfloat_type": nanfloat_type,
        "nanfloat_list": nanfloat_list,
    }
    validator = Validator(fdict)
    return validator


def config_error(config, results):
    """
    Parse the results of a ConfigObj validation and log the errors.
    Throws a RuntimeError exception  upon completion if any errors or
    missing sections are encountered.

    Args:
        config (ConfigObj): The ConfigObj instance representing the
            parsed config.
        results (dict): The dictionary returned by the validation of
            the 'config' arguments.

    Returns:
        Nothing: Nothing

    Raises:
        RuntimeError: Should always raise this exception.
    """
    errs = 0
    for section_list, key, _ in flatten_errors(config, results):
        if key is not None:
            logging.error(
                'The "%s" key in the section "%s" failed validation'
                % (key, ", ".join(section_list))
            )
            errs += 1
        else:
            logging.error(
                f"The following section was missing:{', '.join(section_list)} "
            )
            errs += 1
    if errs:
        raise RuntimeError(
            "There %s %d %s in configuration."
            % ("was" if errs == 1 else "were", errs, "error" if errs == 1 else "errors")
        )


def check_extra_values(config, logger):
    """
    Checks the config and warns the user if there are any extra entries
    in their config file. This function is based on suggested usage in the
    ConfigObj manual.

    Args:
        config (ConfigObj): A ConfigObj instance.
        logger (logger): The logger to which to write complaints.

    Returns:
        Nothing: Nothing.
    """
    warnings = 0
    for sections, name in get_extra_values(config):
        # this code gets the extra values themselves
        the_section = config
        for section in sections:
            the_section = the_section[section]

        # the_value may be a section or a value
        the_value = the_section[name]

        section_or_value = "value"
        if isinstance(the_value, dict):
            # Sections are subclasses of dict
            section_or_value = "section"

        section_string = ", ".join(sections) or "top level"
        logger.warning(
            "Extra entry in section: %s: %s %r is not in spec."
            % (section_string, section_or_value, name)
        )
        warnings += 1
    if warnings:
        logger.warning(
            "The extra value(s) may be the result of deprecated "
            "entries or other changes to the config files; please "
            "check the conifg files in shakemap/data for the most "
            "up to date specs."
        )


def nanfloat_type(value):
    """
    Checks to see if value is a float, or NaN, nan, Inf, -Inf, etc.
    Raises a ValidateError exception on failure.

    Args:
        value (str): A string representing a float NaN or Inf.

    Returns:
        float: The input value converted to its float equivalent.

    """
    try:
        out = float(value)
    except ValueError:
        raise ValidateError(value)
    return out


def nanfloat_list(value, min):
    """
    Checks to see if value is a list of floats, including NaN and Inf.
    Raises a ValidateError exception on failure.

    Args:
        value (str): A string representing a list of floats.

    Returns:
        list: The input string converted to a list of floats.

    """
    min = int(min)
    if isinstance(value, str) and (value == "None" or value == "[]"):
        value = []
    if isinstance(value, str):
        value = [value]
    if isinstance(value, list) and not value:
        value = []
    if not isinstance(value, list):
        logging.error(f"'{value}' is not a list")
        raise ValidateError()
    if len(value) < min:
        logging.error("extent list must contain %i entries" % min)
        raise ValidateError()
    try:
        out = [float(a) for a in value]
    except ValueError:
        logging.error("%s is not a list of %i floats" % (value, min))
        raise ValidateError()
    return out

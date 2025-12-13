"""Config parser module with a custom configuration parser."""

import configparser


class PureSectionConfigParser(configparser.RawConfigParser):
    """A configuration parser that retrieves section data without defaults."""

    _defaults: dict

    def options(self, section: str) -> list:
        """Return a list of option names for the given section, excluding defaults.

        This method temporarily removes default options to ensure only explicitly
        defined options in the given section are returned.

        Args:
            section (str): The section name.

        Returns:
            list: A list of option names in the specified section.

        """
        _d = self._defaults.copy()
        try:
            self._defaults.clear()
            return super().options(section)
        finally:
            self._defaults.update(_d)

    def optionxform(self, option: str) -> str:
        """Preserve the case of option names.

        By default, `optionxform` in `RawConfigParser` converts option names to lowercase.
        This overridden method ensures that option names remain unchanged.

        Args:
            option (str): The option name.

        Returns:
            str: The unmodified option name.

        """
        return option

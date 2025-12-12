"""Example application demonstrating a typical Juham application.

Usage:
------

python myapp.py --init --myapp_serialization_format JsonFormat
python myapp.py 

"""

from masterpiece import Application
from juham_core import Juham
from typing_extensions import override


class MyHome(Application):
    """Application demonstrating the structure of typical masterpiece applications.
    When run, the application prints out its instance hierarchy:

    Example:
        trump
        └─ tower


    """

    def __init__(self, name: str = "tower") -> None:
        """Initialize the home application with the given name.

        Instance attributes can be initialized from class attributes,
        through a serialization file, or from constructor parameters.

        Args:
            name (str): The name of the application.
        """
        super().__init__(name)
        self.create_home()
        self.install_plugins()

    def create_home(self) -> None:
        """Create a default built-in home structure, which can be overridden
        by the instance hierarchy defined in the serialization file. See --file
        startup argument.
        """
        juham = Juham("tower")
        self.add(juham)

    @override
    def run(self) -> None:
        """Start the application."""
        super().run()

        # Print out the instance hierarchy
        self.print()


def main() -> None:
    """Main function that initializes, instantiates, and runs the application."""

    # 1. Initialize the application group ID, which is used to locate the configuration files
    # There can be multiple applications in the same group, sharing the same configuration files
    MyHome.init_app_id("trump")

    # 2. Make this app plugin-aware. See the 'masterpiece_plugin' project for a minimal plugin example.
    MyHome.load_plugins()

    # 3. Initialize class attributes from the configuration files at ~/.[appname]/[config]/*
    # the desired configuration can be chosen from any number of configurations
    # with `--config [configuration]` startup argument.
    Application.load_configuration()

    # 4. Create the application, instance attributes are being
    # initialized from the class attributes to configure the application
    # to use, for example, a specific serialization format, and MQTT broker.
    home = MyHome("tower")

    # 5. Deserialize instances from the serialization file if specified and exists
    # if not, then with run with the default  configuration.
    home.deserialize()

    # 6. Start event processing or the application's main loop
    # this will return only when the the network loop is stopped.
    home.run()

    # 7. Save the application's state to a serialization file if specified, so
    # that when we next time start the application, it will start from the
    # same state as it was when it was stopped.
    home.serialize()

    # 8. Try to be nice
    home.info(f"{home.name} stopped, have a nice day!")


if __name__ == "__main__":
    main()

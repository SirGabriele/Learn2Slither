class InitialisationException(Exception):
    def __init__(self, property_name: str):
        self._prebuild_message: str = ("Initialisation error: Failed to "
                                       "initialise '{}'")

        super().__init__(self._prebuild_message.format(property_name))

class PredictException(Exception):
    '''
    :param message_override: Overrides the default \'An exception has occurred\' with custom message.

    **EXAMPLE:**

       .. code-block:: python
            
            # Imports
            from virtualitics_sdk import PredictException
            . . .
            # Example usage 
            # throwing exception in some function 
            def example_func(self, flow_metadata, pyvip_client=None):
                api_key = parse_api_key(api_key_connection)
                    if not api_key:
                        raise PredictException("You need a valid API key stored in the connection store")
    '''
    message: str
    def __init__(self, message_override: str = '') -> None: ...

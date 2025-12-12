import collections

"""This file houses a blackboard singleton. The function of this class is to hold information that there will be a
single instance of across the program, but may be used at multiple places and layers within the program tree.
At a minimum, this is expected to house the config data, logger, data_share class object and the page tracker"""

class BlackBoard:
    # Set the singleton controls
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = BlackBoard()
        return cls._instance
    
    # Set up class variables
    def __init__(self):
        self.config = None
        self.logger = None
        self.data_share = None

        # Define a page history queue
        self.page_history = collections.deque(10*[3], 10)
        
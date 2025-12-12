from abc import ABC, abstractmethod

class VKPy:

    def __init__(self):
        pass

    RANDOM_STATE = 42
    NUMBER_OF_DASHES = 100
    

    def __str__(self):
        return (f"VKPy : RANDOM_STATE = {cls.RANDOM_STATE} | DASHES ={cls.NUMBER_OF_DASHES}")
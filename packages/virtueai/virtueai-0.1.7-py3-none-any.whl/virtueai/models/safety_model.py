from abc import ABC, abstractmethod

class SafetyModel(ABC):
    @abstractmethod
    def safety_check(self, query: str) -> bool:
        pass
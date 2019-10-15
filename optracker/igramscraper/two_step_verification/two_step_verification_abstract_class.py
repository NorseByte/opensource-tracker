from abc import ABC, abstractmethod


class TwoStepVerificationAbstractClass(ABC):

    @abstractmethod
    def get_verification_type(self, possible_values):
        """
        :param possible_values: array of possible values
        :return: string
        """
        pass

    @abstractmethod
    def get_security_code(self):
        """

        :return: string
        """
        pass

from .two_step_verification_abstract_class import TwoStepVerificationAbstractClass


class ConsoleVerification(TwoStepVerificationAbstractClass):

    def get_verification_type(self, choices):
        if (len(choices) > 1):
            possible_values = {}
            print('Select where to send security code')

            for choice in choices:
                print(choice['label'] + ' - ' + str(choice['value']))
                possible_values[str(choice['value'])] = True

            selected_choice = None

            while (not selected_choice in possible_values.keys()):
                if (selected_choice):
                    print('Wrong choice. Try again')

                selected_choice = input('Your choice: ').strip()
        else:
            print('Message with security code sent to: ' + choices[0]['label'])
            selected_choice = choices[0]['value']

        return selected_choice

    def get_security_code(self):
        """

        :return: string
        """
        security_code = ''
        while (len(security_code) != 6 and not security_code.isdigit()):
            if (security_code):
                print('Wrong security code')

            security_code = input('Enter security code: ').strip()

        return security_code

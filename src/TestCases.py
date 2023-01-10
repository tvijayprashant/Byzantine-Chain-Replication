class TestCases:

    def __init__(self, testCaseName, masterDict):
        self.clientToResultDictionary = dict()
        self.testCaseName = testCaseName
        self.masterDict = masterDict

    def verify(self, clientNumber, clientResultDict, resDict):
        if(self.testCaseName == 'stresstest'):
            print('Verifying Test case:{} client:{}'.format(self.testCaseName, clientNumber))
            print('Expected Dict :  ' + str(self.masterDict))
            print('Actual Dict   :  ' + str(clientResultDict))
            return self.masterDict == clientResultDict
        else:
            print('Verifying Test case:{} client:{}'.format(self.testCaseName, clientNumber))
            print('Expected Dict :  ' + str(resDict))
            print('Actual Dict   :  ' + str(clientResultDict))
            return resDict == clientResultDict

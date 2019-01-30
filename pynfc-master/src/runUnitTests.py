import unittest
from pollForAction import PollForAction, FileParser

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_canCreatePollForActionWithZeroArgs(self):
        pfa = PollForAction()

    def test_canCreatePollForActionWithOneArgs(self):
        pfa = PollForAction(1)
    
    def test_canTellIfAFileIsExists(self):
	self.assertTrue(None == PollForAction().argIsValidFile(None)) # NONE returns NONE 
        self.assertTrue(None == PollForAction().argIsValidFile("empty"))
        self.assertTrue(None == PollForAction().argIsValidFile(1))
        self.assertTrue(None == PollForAction().argIsValidFile([1,1]))
        self.assertTrue("./runUnitTests.py" == PollForAction().argIsValidFile("./runUnitTests.py"))

    def test_countDefaultOptions(self):
        self.assertTrue(0 == PollForAction().getOptionsCount())

    def test_fileParserOnValidEmptyFile(self):
	options = FileParser().parse_config("./testDataDir/empty.kwargs")
        lops = len(options)
        self.assertEqual( 0 , lops )

    def test_fileParserOnValidSingleEntryFile(self):
        options = FileParser().parse_config("./testDataDir/singleValue.kwargs")
        lops = len(options)
        self.assertEqual( 1 , lops )
        self.assertEqual("Lion King",options["00000"])

    def test_fileParserOnValidSingleEntryFile(self):
        options = FileParser().parse_config("./testDataDir/fiveValue.kwargs")
        lops = len(options)
        self.assertEqual( 5 , lops )
        self.assertEqual("Escape",options["ELVES"])

    def test_configurePollerFromFile(self):
        poller = PollForAction()
        poller.configureFromFile("./testDataDir/fiveValue.kwargs")
        self.assertTrue(5 == poller.getOptionsCount())
        self.assertEqual("Escape",poller.lookupActionFromOptions("ELVES"))
        self.assertEqual(None,poller.lookupActionFromOptions("GNOMES"))

if __name__ == '__main__':
    unittest.main()

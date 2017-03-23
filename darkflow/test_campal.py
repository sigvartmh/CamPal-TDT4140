import unittest

def findPerson(detectedObject):
    pt1 = (detectedObject['topleft']['x'],detectedObject['topleft']['y'])
    pt2 = (detectedObject['bottomright']['x'],detectedObject['bottomright']['y'])
    return (pt1, pt2)

class getObjectLocationTestCase(unittest.TestCase):
    def setUp(self):
        self.id_object = identifiedObject={'label': 'person', 'confidence': 0.88409609, 'topleft': {'x': 578, 'y': 275}, 'bottomright': {'x': 1044, 'y': 711}}

class findObjectTestCase(getObjectLocationTestCase):
    def runTest(self):
        self.assertEqual(findPerson(self.id_object),((578, 275),(1044 , 711)))

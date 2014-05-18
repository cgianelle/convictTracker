'''
Created on May 18, 2014

@author: chris
'''
import unittest

from trackerDB import database


class Test(unittest.TestCase):
    @classmethod  
    def setUpClass(cls): 
        cls.path = '/tmp/tracker.db'
        cls.trackerDB = database.TrackerDB(cls.path)
        cls.trackerDB.createDatabase(force=True)
        
        #Populate movement table
        cls.movements = [('Pushups', 'Pushups', 'An exercise in which you lay on your stomach and raise and lower your body by straightening and bending your arms'),
                     ('Pullups', 'Pullups', 'A pull-up is a compound, pull-type exercise which works a large number of muscles in your back, shoulders, and arms at the same time.A pull-up is a compound, pull-type exercise which works a large number of muscles in your back, shoulders, and arms at the same time.A pull-up is a compound, pull-type exercise which works a large number of muscles in your back, shoulders, and arms at the same time.'),
                     ('Squats', 'Squats', 'The squat is a compound, full body exercise that trains primarily the muscles of the thighs, hips and buttocks, quads (vastus lateralus, medialis and intermedius and rectus femoris), hamstrings, as well as strengthening the bones, ligaments and insertion of the tendons throughout the lower body.'),
                     ('LegRaises', 'Leg Raises', 'Leg raises are a great way to target the lower portion of the abdominals. In conjunction with a good bodybuilding diet, leg raises will give a flat and toned look to your lower abdominal section.'),
                     ('HandstandPushups', 'Handstand Pushups', 'Type of push-up exercise where the body is positioned in a handstand'),
                     ('Bridges', 'Bridges', "The Bridge is an excellent Pilates torso stability exercise.")
                     ]
        
        for movement in cls.movements:
            i,n,d = movement
            cls.trackerDB.addMovement(i,n,d)
        

    def testGetMovements(self):
        #get all movements from DB
        movementsDB = self.trackerDB.getMovements()
        
        if not movementsDB:
            self.fail('List of movements is empty when there should be 6 items')
        
        #check to see if the table has be populated
        for movement in self.movements:
            m = [i for i,v in enumerate(movementsDB) if v[1] == movement[1]]
            if not m:
                self.fail("Unable to locate movement " + movement[1])
                
    def testGetMovementPass(self):
        try:
            self.trackerDB.getMovement('Leg Raises')
        except database.UnknownMovement:
            self.fail('Unable to locate movement, Leg Raises')
            
    def testGetMovementFail(self):
        try:
            self.trackerDB.getMovement('Hop Scotch')
            self.fail('Located movement, Hop Scotch. This should have failed')
        except database.UnknownMovement:
            #if exception was thrown then the api is able to indicate when it can't find something
            pass
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
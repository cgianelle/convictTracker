'''
Created on May 18, 2014

@author: chris
'''
import unittest
import os
from trackerDB import database


class DBTest(unittest.TestCase):


    def setUp(self):
        self.path = '/tmp/tracker.db'
        self.trackerDB = database.TrackerDB(self.path)


    def tearDown(self):
        self.trackerDB = None


    def testCreateDatabase(self):
        self.trackerDB.createDatabase(force=False)
        if not os.path.exists(self.path):
            self.fail('The tracker database was not created.') 
    
    def testMovements(self):
        #Populate movement table
        movements = [('Pushups', 'Pushups', 'An exercise in which you lay on your stomach and raise and lower your body by straightening and bending your arms'),
                     ('Pullups', 'Pullups', 'A pull-up is a compound, pull-type exercise which works a large number of muscles in your back, shoulders, and arms at the same time.A pull-up is a compound, pull-type exercise which works a large number of muscles in your back, shoulders, and arms at the same time.A pull-up is a compound, pull-type exercise which works a large number of muscles in your back, shoulders, and arms at the same time.'),
                     ('Squats', 'Squats', 'The squat is a compound, full body exercise that trains primarily the muscles of the thighs, hips and buttocks, quads (vastus lateralus, medialis and intermedius and rectus femoris), hamstrings, as well as strengthening the bones, ligaments and insertion of the tendons throughout the lower body.'),
                     ('LegRaises', 'Leg Raises', 'Leg raises are a great way to target the lower portion of the abdominals. In conjunction with a good bodybuilding diet, leg raises will give a flat and toned look to your lower abdominal section.'),
                     ('HandstandPushups', 'Handstand Pushups', 'Type of push-up exercise where the body is positioned in a handstand'),
                     ('Bridges', 'Bridges', "The Bridge is an excellent Pilates torso stability exercise.")
                     ]
        
        for movement in movements:
            i,n,d = movement
            self.trackerDB.addMovement(i,n,d)
        
        #get all movements from DB
        movementsDB = self.trackerDB.getMovements()
        
        if not movementsDB:
            self.fail('List of movements is empty when there should be 6 items')
        
        #check to see if the table has be populated
        for movement in movements:
            m = [i for i,v in enumerate(movementsDB) if v[1] == movement[1]]
            if not m:
                self.fail("Unable to locate movement " + movement[1])
                
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
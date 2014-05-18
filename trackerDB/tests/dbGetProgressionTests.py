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
            
        cls.progressions = [('Pushups',1,'WallPushups','Wall Pushups','Pushups done standing against a wall'),
                            ('Pushups',2,'InclinePushups','Incline Pushups','Standing pushups done at a 45 degree angle.'),
                            ('Pushups',3,'KneelingPushups','Kneeling Pushups','Pushups done from the knees'),
                            ('Pushups',4,'HalfPushups','Half Pushups','Pushups done to about halfway'),
                            ('Pushups',5,'FullPushups','Full Pushups','Regular pushups'),
                            ('Pushups',6,'ClosePushups','Close Pushups','Like regular pushups, but with hands together'),
                            ('Pushups',7,'UnevenPushups','Uneven Pushups','One hand is raised higher that the other'),
                            ('Pushups',8,'HalfOneArmPushups','Half One Arm Pushups','One Arm pushups done half way'),
                            ('Pushups',9,'LeverPushups','Lever Pushups','One hand on the ground, the other on a ball'),
                            ('Pushups',10,'OneArmPushups','One Arm Pushups','Pushups done with one arm')]
        
        for progression in cls.progressions:
            m,d,i,n,e = progression
            cls.trackerDB.addProgression(m,d,i,n,e)
                        


    def testGetProgeressions(self):
        progressionsDB = self.trackerDB.getProgressions()
        
        if not progressionsDB:
            self.fail('List of Progressions is empty')
        
        #check to see if the table has be populated
        for progression in self.progressions:
            m = [i for i,v in enumerate(progressionsDB) if v[3] == progression[3]]
            if not m:
                self.fail("Unable to locate movement " + progression[3])
                
    def testGetProgressionFail(self):
        try:
            self.trackerDB.getProgression('Uneven Lever')
            self.fail('Located Progression, Uneven Lever, should have failed')
        except database.UnknownProgression:
            pass
 
    def testGetProgressionPass(self):
        try:
            self.trackerDB.getProgression('Uneven Pushups')
        except database.UnknownProgession:
            self.fail('Unable to locate movement, Uneven Pushups')
 
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
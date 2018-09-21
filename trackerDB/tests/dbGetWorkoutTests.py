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

        cls.workouts = [('2014-05-18',None),
                    ('2014-05-17','ABCD'),
                    ('2014-05-16',None)]
        
        for workout in cls.workouts:
            d,n = workout
            cls.trackerDB.addWorkout(d,n)

    def testGetWorkouts(self):
        workoutDB = self.trackerDB.getWorkouts()
        
        if not workoutDB:
            self.fail("No workouts in the database")
            
        for workout in self.workouts:
            w = [i for i,v in enumerate(workoutDB) if v[1] == workout[0]]
            if not w:
                self.fail("Unable to locate movement " + workout[0])            
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
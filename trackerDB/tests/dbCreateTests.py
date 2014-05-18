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
        if os.path.exists(self.path):
            os.remove(self.path)

    def testCreateDatabase(self):
        print 'testCreateDatabase'
        self.trackerDB.createDatabase(force=False)
        if not os.path.exists(self.path):
            self.fail('The tracker database was not created.') 
    
                
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
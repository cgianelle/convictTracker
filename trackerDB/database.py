'''
Created on May 18, 2014

ConvictTracker Database schema
Used to keep track of the workout progressions

Tables:

BEGIN;
CREATE TABLE "track_movement" (
    "movementId" varchar(32) NOT NULL PRIMARY KEY,
    "movementName" varchar(32) NOT NULL,
    "movementDesc" text NOT NULL
)
;
CREATE TABLE "track_progression" (
    "movement_id" varchar(32) NOT NULL REFERENCES "track_movement" ("movementId"),
    "difficulty" integer NOT NULL,
    "progressionId" varchar(64) NOT NULL PRIMARY KEY,
    "progressionName" varchar(64) NOT NULL,
    "progressionDesc" text NOT NULL
)
;
CREATE TABLE "track_workout" (
    "id" integer NOT NULL PRIMARY KEY,
    "workoutDate" datetime NOT NULL,
    "notes" text
)
;
CREATE TABLE "track_exercise" (
    "id" integer NOT NULL PRIMARY KEY,
    "notes" text,
    "date_id" integer NOT NULL REFERENCES "track_workout" ("id"),
    "movement_id" varchar(32) NOT NULL REFERENCES "track_movement" ("movementId"),
    "progression_id" varchar(64) NOT NULL REFERENCES "track_progression" ("progressionId")
)
;
CREATE TABLE "track_set" (
    "id" integer NOT NULL PRIMARY KEY,
    "exercise_id" integer NOT NULL REFERENCES "track_exercise" ("id"),
    "reps" integer NOT NULL
)
;
COMMIT;

@author: chris
'''
import sqlite3
import os
from contextlib import closing

class UnknownMovement(KeyError):
    pass

class UnknownProgression(KeyError):
    pass

class UnknownExercise(KeyError):
    pass

class UnknownSet(KeyError):
    pass

class UnknownWorkout(KeyError):
    pass



class TrackerDB(object):
    '''
    Responsible for creating the database and for maintaining it 
    '''


    def __init__(self, path):
        '''
        Constructor
        '''
        self.path = path
    
    def __makeDatabase(self):
        '''
        Creates the actual tracker database and the associated tables 
        '''
        # The connection will be closed upon completion of the with block
        # thats what with does
        # the closing(...) makes the sqlite3.connect call withable
        with closing(sqlite3.connect(self.path)) as conn:
            try:                
                self.__makeMovements(conn)
                self.__makeProgressions(conn)
                self.__makeWorkout(conn)
                self.__makeExercise(conn)
                self.__makeSet(conn)
                conn.commit()
            except sqlite3.OperationalError:
                # do I really want to pass on this error 
                pass
        
    
    def __makeMovements(self,conn):
        '''
        Responsible for creating the Movement table of the tracker database
        '''
        conn.execute('''CREATE TABLE "track_movement" (
                    "movementId" varchar(32) NOT NULL PRIMARY KEY,
                    "movementName" varchar(32) NOT NULL,
                    "movementDesc" text NOT NULL)
                    ''')
    
    def __makeProgressions(self,conn):
        '''
        Responsible for creating the Progressions table of the tracker database
        '''
        conn.execute('''CREATE TABLE "track_progression" (
                    "movement_id" varchar(32) NOT NULL REFERENCES "track_movement" ("movementId"),
                    "difficulty" integer NOT NULL,
                    "progressionId" varchar(64) NOT NULL PRIMARY KEY,
                    "progressionName" varchar(64) NOT NULL,
                    "progressionDesc" text NOT NULL)
                    ''')
    
    def __makeWorkout(self,conn):
        conn.execute('''CREATE TABLE "track_workout" (
                    "id" integer NOT NULL PRIMARY KEY,
                    "workoutDate" datetime NOT NULL,
                    "notes" text)
                    ''')
    
    def __makeExercise(self,conn):
        conn.execute('''CREATE TABLE "track_exercise" (
                    "id" integer NOT NULL PRIMARY KEY,
                    "notes" text,
                    "date_id" integer NOT NULL REFERENCES "track_workout" ("id"),
                    "movement_id" varchar(32) NOT NULL REFERENCES "track_movement" ("movementId"),
                    "progression_id" varchar(64) NOT NULL REFERENCES "track_progression" ("progressionId"))
                    ''')
    
    def __makeSet(self,conn):
        conn.execute('''CREATE TABLE "track_set" (
                    "id" integer NOT NULL PRIMARY KEY,
                    "exercise_id" integer NOT NULL REFERENCES "track_exercise" ("id"),
                    "reps" integer NOT NULL)
                    ''')
    
    def createDatabase(self, force=False):
        '''
        create a new student absentee database
        if force = True and there is an existing database, 
            the existing database will be deleted and recreated
        If the database already exists, it does nothing
        If the database does not exist, one will be created
        '''
        
        #Case where force is true and the db exists
        if not force and not os.path.exists(self.path):
            self.__makeDatabase()
        elif not force and os.path.exists(self.path):
            #db already exists, no need to do anything
            return
        else:
            #this is the case where force = True
            
            #if the database already exists, delete it
            if os.path.exists(self.path):
                os.unlink(self.path)
                
            self.__makeDatabase()
            
    def addMovement(self,movementId, movementName, movementDesc):
        movement = movementId,movementName,movementDesc    
        with closing(sqlite3.connect(self.path)) as conn:
            conn.execute('INSERT INTO track_movement VALUES(?,?,?)',movement)
            conn.commit()

    def getMovements(self):
        with closing(sqlite3.connect(self.path)) as conn:
            movements = conn.execute('SELECT * FROM track_movement').fetchall()
            
        if not movements:
            raise UnknownMovement("No movements in database")         
           
        return movements
    
    def getMovement(self,movementName):
        with closing(sqlite3.connect(self.path)) as conn:
            movements = conn.execute('SELECT * FROM track_movement WHERE movementName=?',(movementName,)).fetchall()
            
        if not movements:
            raise UnknownMovement(movementName)
        
        return movements
                        
    def addProgression(self,movementName,difficulty,progressionId,progressionName,progressionDesc):        
        with closing(sqlite3.connect(self.path)) as conn:
            #first lookup movementName to get movementId
            movements = conn.execute('SELECT * FROM track_movement WHERE movementName=?',(movementName,)).fetchall()
            
            if not movements:
                raise UnknownMovement('addProgression: Movement Name, ' + movementName + ', was not found')
            
            movementId = (lambda t: t[0])(movements[0])
            
            progression = movementId,difficulty,progressionId,progressionName,progressionDesc
            conn.execute('INSERT INTO track_progression VALUES(?,?,?,?,?)',progression)
            conn.commit()
                 
    def getProgressions(self):
        with closing(sqlite3.connect(self.path)) as conn:
            progressions = conn.execute('SELECT * FROM track_progression').fetchall()
            
        if not progressions:
            raise UnknownProgression("Progression Table is empty")
        
        return progressions
        
    def getProgression(self,progressionName):
        with closing(sqlite3.connect(self.path)) as conn:
            progressions = conn.execute('SELECT * FROM track_progression WHERE progressionName=?',(progressionName,)).fetchall()
   
        if not progressions:
            raise UnknownProgression(progressionName)
        
        return progressions
    
    def addWorkout(self,date,notes):
        workout = date,notes
        with closing(sqlite3.connect(self.path)) as conn:
            conn.execute('INSERT INTO track_workout VALUES(NULL,?,?)',workout)
            conn.commit()
            
    def getWorkouts(self):
        with closing(sqlite3.connect(self.path)) as conn:
            workouts = conn.execute('SELECT * FROM track_workout').fetchall()
            
        if not workouts:
            raise UnknownWorkout('Workouts table is empty')
        
        return workouts
    
    def getWorkout(self,date):
        with closing(sqlite3.connect(self.path)) as conn:
            dates = conn.execute('SELECT * FROM track_workout WHERE workoutDate=?',(date,)).fetchall()
   
        if not dates:
            raise UnknownWorkout(date)
        
        return dates
               
        
    
    def addExercise(self):
        pass
    
    def addSet(self):
        pass

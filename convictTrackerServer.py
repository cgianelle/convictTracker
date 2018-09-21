'''

'''
 
import web
import json

db = web.database(dbn='sqlite',db='tracker')

urls = (
    '/addMovement','addMovement',  
)

class addMovement:
    def POST(self):
        i = web.input()
        if hasattr(i,'movement') and hasattr(i,'description'):
            print i
            id = i.movement.replace(' ','')
            movement = i.movement
            description = i.description
            db.insert('track_movement', movementid=id, movementName=movement, movementDesc=description)
            return 'Thank You'
        else:
            return 'Form not properly formatted'
        
if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
        
    
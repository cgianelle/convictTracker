'''
'''

import urllib
import urllib2
import cmd

class MovementCommandShell(cmd.Cmd):
    prompt = '>>> MCS# '
    def do_addMovement(self,line):
        self.movement = line
    
    def do_addDescription(self,line):
        self.description = line
    
    def emptyline(self):
        '''
        by default CMD will rerun the last command if an empty line is sent to the interpretter, here I am overiding
        this behavior so that it doesn't do that and behaves more like a bash shell
        '''
        pass
    
    def do_EOF(self,line):
        print ''
        print 'Good Bye'
        return True
    
    def getMovement(self):
        if hasattr(self,'movement') and hasattr(self,'description'):
            return self.movement, self.description
        else:
            return None


class ConvictTrackerCommandShell(cmd.Cmd): 
    prompt = 'CTSC# '
    def do_addMovement(self,line):
        mcs = MovementCommandShell()
        mcs.cmdloop()
        movement, desc = mcs.getMovement()
        url = self.base_url + '/addMovement'
        params = urllib.urlencode({
                'movement': movement,
                'description': desc
            })
        response = urllib2.urlopen(url,params).read()
        print response

    def do_setbaseurl(self,line):
        self.base_url = line 
        
    
    def emptyline(self):
        '''
        by default CMD will rerun the last command if an empty line is sent to the interpretter, here I am overiding
        this behavior so that it doesn't do that and behaves more like a bash shell
        '''
        pass
    
    def do_EOF(self,line):
        print ''
        print 'Good Bye'
        return True
    

if __name__ == '__main__':
    ConvictTrackerCommandShell().cmdloop()
     

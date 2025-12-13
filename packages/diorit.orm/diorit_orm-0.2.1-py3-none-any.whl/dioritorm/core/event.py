
class Event():
    def __init__(self):
        self.context = None


    def create(self):

        subClasses = Event.__subclasses__()
        for sub in subClasses:
            obj = sub()
            obj.context = self.context
            obj.onCreate()

    def save(self,node = None, connection = None):
        subClasses = Event.__subclasses__()
        for sub in subClasses:
            obj = sub()
            obj.context = self.context
            obj.onSave(node, connection)

    def onCreate(self):
        pass

    def onSave(self,node,connection = None):
        pass

class PluginEngine(object):
    def __init__(self):
        self.loadedPlugins = {}

        for lst in listsToBuild:
            self.__dict__[lst] = []

        for dct in dictsToBuild:
            self.__dict__[dct] = {}
            
        for plugin in reqPlugins:
            self.load(plugin)

    def load(self, plugin):
        print "Loading plugin:", plugin
        self.loadedPlugins[plugin] = __import__(plugin)
        
        for lst in listsToBuild:
            self.__dict__[lst].extend(self.loadedPlugins[plugin].__dict__[lst])

        for dct in dictsToBuild:
            self.__dict__[dct].update(self.loadedPlugins[plugin].__dict__[dct])
    
    def remove(self, plugin):
        pass

reqPlugins = ["mathematics"]
addPlugins = []
listsToBuild = ["containers", "parseOrder", "orderOfOperations"]
dictsToBuild = ["inputDict", "outputDict"]

if __name__ == '__main__':
    pe = PluginEngine()

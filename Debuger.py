class Debuger:
    def __init__(self, debInfo = "debug Info", buferLimit = 1000):
        self.debInfos = []
        self.buferLimit = buferLimit
        print(debInfo)
        
    def deb(self, debInfo = ""):
        if len(self.debInfos) >= self.buferLimit:
            self.debInfos = ["Bufer limit exceeded, cleared"]
            print("Bufer limit exceeded, cleared")
        self.debInfos.append(debInfo)
        print(debInfo)
        
    

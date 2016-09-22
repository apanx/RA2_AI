import plus
import AI

class Export(AI.SuperAI):
    "Export list describing robot"
    name = "Export"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        
    def Activate(self, active):
        if active:
                #"Print out all component id's and types for this robot."
	        output = file(self.botName + ".txt", "w")
	        for i in range(0, self.GetNumComponents()):
            		output.write(str(i))
            		output.write(" ")
            		output.write(str(self.GetComponentType(i)))
            		output.write("\n")
                output.close
                
        return AI.SuperAI.Activate(self, active)
        
    def Tick(self):
        # Do stupid stuff so that no one forgets they are running exporter
        self.Turn(100)
        return plus.AI.Tick(self)

AI.register(Export)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import *
import json
import os
import random

# .AlterDefinitions(root.ids.wordInput.text, root.ids.defInput.text)

currentSet = ""

def getCurrentSetID() -> str:
    global currentSet
    return currentSet

def setCurrentSetID(id : str) -> None:
    global currentSet
    currentSet = id


def retrieveSavedSets():
    files = os.listdir('./')
    sets = []
    for file in files:
        if file.endswith('.json'):
            sets.append(file)
    return sets

class WindowManager(ScreenManager):

    def saveSet(self, name, definitions):
        print(f"attempting to push name: {name} into {name}.json, definitions: {definitions}")
        with open(f"{name}.json", "w") as savefile:
            savefile.write(json.dumps({name:definitions}))

    def modfiyCSID(self, id : str):
        setCurrentSetID(id)

class SetsRow(GridLayout):
    print(getCurrentSetID())
    name = StringProperty('')

class MainMenu(Screen):
    pass

class SetsMenu(Screen):
    pass

class MakeNewSets(Screen):
    pass

class TeachSet(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    definitionText = StringProperty()

    def refreshDefinition(self):
        print("! Curred CSID: " + getCurrentSetID())
        with open(f"{getCurrentSetID()}.json", 'r') as file:
            definitions = json.load(file)
            #definitionText = f"{random.choice(definitions[getCurrentSetID()])['text'].split(":")[0]}"
            self.ids.definitionName.text = f"{random.choice(definitions[getCurrentSetID()])['text'].split(":")[0]}"

class SetsView(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ####################################################
        # Future me this is where data loading takes place #
        ###################################################3
        for set in retrieveSavedSets():
            print(set)
            self.data.append({"name": f"{set.replace('.json', '')}"})

    def refreshSets(self):
        print(retrieveSavedSets())

class DefinitionsRV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.my = App.get_running_app()
        self.data = []

    def AlterDefinitions(self, word, meaning):
        self.data.append({"text":f"{word}: {meaning}"})

kv = Builder.load_file("source.kv")

class studyHelper(App):
    DefinitionsRV = DefinitionsRV()
    def build(self):
        return kv
    
if __name__ == "__main__":
    studyHelper().run()
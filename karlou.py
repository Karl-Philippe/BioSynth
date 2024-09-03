class Person:
    def __init__(self, prenom):
        self.prenom = prenom
        self.state = "neutre"
        
    def bisous(self, person):
        person.state = "happy"
        
    def choubidoubidoudou(self):
        self.state = "blublu"

if __name__ == "__main__":
    karlou = Person(prenom="Karl")
    chloui = Person(prenom="Chloé")
    
    karlou.bisous(chloui)
    
    print(f"État de {chloui.prenom}: {chloui.state}")
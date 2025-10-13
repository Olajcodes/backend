# Creating a class named Pet
class Pet:
    """This takes information about the pet
    """
    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age

    # Function to display the class information
    def display_class_info(self):
        print(f"The Pet information is as follows:\nName\t\tSpecies\t\tAge\n{self.name}\t\t{self.species}\t\t{self.age}")
        
    # Function to celebrate the Pet's birthday
    def celebrate_birthday(self):
        print(f"\nCongratulations! Happy Birthday {self.name}. You are {self.age} years old.")
    
# Creating an object    
sample_pet = Pet("Cat", "Black", 3)

# Calling the functions
Pet.display_class_info(sample_pet)

Pet.celebrate_birthday(sample_pet)
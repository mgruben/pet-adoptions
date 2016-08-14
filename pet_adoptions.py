import random
import string

class AdoptionCenter(object):
    """
    The AdoptionCenter class stores the important information that a
    client would need to know about, such as the different numbers of
    species stored, the location, and the name. It also has a method to adopt a pet.
    """
    def __init__(self, name, species_types, location):
        assert type(name) == str, "'name' must be a string"
        self.name = name
        assert type(species_types) == dict, "'species_types' must be a dictionary"
        self.species_types = species_types
        assert type(location) == tuple, "'location' must be a tuple"
        assert len(location) == 2, "'location' must be 2 items long"
        for i in range(2):
            assert (type(location[i]) == int) or (type(location[i]) == float), "'location' must contain numbers"
        floating_location = (float(location[0]), float(location[1]))
        self.location = floating_location
    def get_number_of_species(self, animal):
        if animal in self.species_types:
            return self.species_types[animal]
        else:
            return 0
    def get_location(self):
        return self.location
    def get_species_count(self):
        return self.species_types.copy()
    def get_name(self):
        return self.name
    def adopt_pet(self, species):
        if species not in self.species_types:
            pass
        elif (self.species_types[species] == 1) or (self.species_types[species] == 0):
            del self.species_types[species]
        else:
            self.species_types[species] -= 1
    def __str__(self):
        return self.name+": "+str(self.location)+"; "+str(self.species_types)

class Adopter(object):
    """ 
    Adopters represent people interested in adopting a species.
    They have a desired species type that they want, and their score is
    simply the number of species that the shelter has of that species.
    """
    def __init__(self, name, desired_species):
        assert type(name) == str, "'name' must be a string"
        self.name = name
        assert type(desired_species) == str, "'desired_species' must be a string"
        self.desired_species = desired_species
    def get_name(self):
        return self.name
    def get_desired_species(self):
        return self.desired_species
    def get_score(self, adoption_center):
        num_desired = adoption_center.get_number_of_species(self.desired_species)
        return max(0.0,float(1 * num_desired))
    def __str__(self):
        return self.name + ", desires: " + self.desired_species 

class FlexibleAdopter(Adopter):
    """
    A FlexibleAdopter still has one type of species that they desire,
    but they are also alright with considering other types of species.
    considered_species is a list containing the other species the adopter will consider
    Their score should be 1x their desired species + .3x all of their desired species
    """
    def __init__(self, name, desired_species, considered_species):
        Adopter.__init__(self, name, desired_species)
        if type(considered_species) == str:
            considered_species = [considered_species]
        for item in considered_species:
            assert type(item) == str, "items in 'considered_species' must be strings"
        self.considered_species = considered_species
    def get_score(self, adoption_center):
        num_other = 0
        for species in self.considered_species:
            num_other += adoption_center.get_number_of_species(species)
        adopter_score = Adopter.get_score(self, adoption_center)
        return max(0.0,float(adopter_score + 0.3 * num_other))
    def __str__(self):
        result = super(FlexibleAdopter, self).__str__()
        result += ", would consider: "
        for s in self.considered_species:
            result += s + ", "
        return result[:-2]

class FearfulAdopter(Adopter):
    """
    A FearfulAdopter is afraid of a particular species of animal.
    If the adoption center has one or more of those animals in it, they will
    be a bit more reluctant to go there due to the presence of the feared species.
    Their score should be 1x number of desired species - .3x the number of feared species
    """
    def __init__(self, name, desired_species, feared_species):
        Adopter.__init__(self, name, desired_species)
        assert type(feared_species) == str, "'feared_species' must be a string"
        self.feared_species = feared_species
    def get_score(self, adoption_center):
        num_feared = adoption_center.get_number_of_species(self.feared_species)
        adopter_score = Adopter.get_score(self, adoption_center)
        return max(0.0,float(adopter_score - 0.3 * num_feared))
    def __str__(self):
        result = super(FearfulAdopter, self).__str__()
        result += ", but fears: " + self.feared_species
        return result

class AllergicAdopter(Adopter):
    """
    An AllergicAdopter is extremely allergic to a one or more species and cannot
    even be around it a little bit! If the adoption center contains one or more of
    these animals, they will not go there.
    Score should be 0 if the center contains any of the animals, or 1x number of desired animals if not
    """
    def __init__(self, name, desired_species, allergic_species):
        Adopter.__init__(self, name, desired_species)
        if type(allergic_species) == str:
            allergic_species = [allergic_species]
        for item in allergic_species:
            assert type(item) == str, "items in 'allergic_species' must be strings"
        self.allergic_species = allergic_species
    def get_score(self, adoption_center):
        species_count = adoption_center.get_species_count()
        for item in self.allergic_species:
            if item in species_count:
                return 0.0
        else:
            adopter_score = float(Adopter.get_score(self, adoption_center))
            return max(0.0,adopter_score)
    def __str__(self):
        result = super(AllergicAdopter, self).__str__()
        result += ", but is allergic to: "
        for s in self.allergic_species:
            result += s + ", "
        return result[:-2]
            

class MedicatedAllergicAdopter(AllergicAdopter):
    """
    A MedicatedAllergicAdopter is extremely allergic to a particular species
    However! They have a medicine of varying effectiveness, which will be given in a dictionary
    To calculate the score for a specific adoption center, we want to find what is the most allergy-inducing species that the adoption center has for the particular MedicatedAllergicAdopter. 
    To do this, first examine what species the AdoptionCenter has that the MedicatedAllergicAdopter is allergic to, then compare them to the medicine_effectiveness dictionary. 
    Take the lowest medicine_effectiveness found for these species, and multiply that value by the Adopter's calculate score method.
    """
    def __init__(self, name, desired_species, allergic_species, medicine_effectiveness):
        AllergicAdopter.__init__(self, name, desired_species, allergic_species)
        assert type(medicine_effectiveness) == dict, "'medicine_effectiveness' must be a dictionary"
        self.medicine_effectiveness = medicine_effectiveness
    def get_score(self, adoption_center):
        species_count = adoption_center.get_species_count()
        species_overlap = []
        for species in species_count:
            if species in self.medicine_effectiveness:
                species_overlap.append(species)
        lowest_medicine_effectiveness = 1
        for species in species_overlap:
            lowest_medicine_effectiveness = min(lowest_medicine_effectiveness, self.medicine_effectiveness[species])
        adopter_score = Adopter.get_score(self, adoption_center)
        return max(0.0,float(lowest_medicine_effectiveness * adopter_score))
    def __str__(self):
        result = super(MedicatedAllergicAdopter, self).__str__()
        result += ", but thankfully takes allergy medication for: "
        for m in self.medicine_effectiveness:
            result += m + " (" + str(self.medicine_effectiveness[m]*100) + "% effective), "
        return result[:-2]
        
        
class SluggishAdopter(Adopter):
    """
    A SluggishAdopter really dislikes travelling. The further away the
    AdoptionCenter is linearly, the less likely they will want to visit it.
    Since we are not sure the specific mood the SluggishAdopter will be in on a
    given day, we will asign their score with a random modifier depending on
    distance as a guess.
    Score should be
    If distance < 1 return 1 x number of desired species
    elif distance < 3 return random between (.7, .9) times number of desired species
    elif distance < 5. return random between (.5, .7 times number of desired species
    else return random between (.1, .5) times number of desired species
    """
    def __init__(self, name, desired_species, location):
        Adopter.__init__(self, name, desired_species)
        assert type(location) == tuple, "'location' must be a tuple"
        self.location = location
    def get_linear_distance(self, to_location):
        destination = to_location.get_location()
        d = ((destination[0]-self.location[0])**2+(destination[1]-self.location[1])**2)**(0.5)
        return d
    def get_score(self, adoption_center):
        d = self.get_linear_distance(adoption_center)
        adopter_score = max(0.0,Adopter.get_score(self, adoption_center))
        if d < 1:
            return float(adopter_score)
        elif d < 3:
            return random.uniform(0.7, 0.9) * adopter_score
        elif d < 5:
            return random.uniform(0.5, 0.7) * adopter_score
        elif d >= 5:
            return random.uniform(0.1, 0.5) * adopter_score
    def __str__(self):
        result = super(SluggishAdopter, self).__str__()
        result += ", and is located at " + str(self.location)
        return result


def get_ordered_adoption_center_list(adopter, list_of_adoption_centers):
    """
    The method returns a list of an organized adoption_center such that
    the scores for each AdoptionCenter to the Adopter will be ordered from
    highest score to lowest score.
    """
    unordered_list_of_adoption_center_instances = list_of_adoption_centers[:]
    unordered_list_of_scores = []
    for adoption_center in unordered_list_of_adoption_center_instances:
        unordered_list_of_scores.append(adopter.get_score(adoption_center))
    unordered_list_of_adoption_centers = []
    for item in unordered_list_of_adoption_center_instances:
        if type(item) == str:
            unordered_list_of_adoption_centers.append(item)
        else:
            unordered_list_of_adoption_centers.append(item.get_name())
    zipped_lists = zip(unordered_list_of_scores, unordered_list_of_adoption_centers)
    zipped_lists.sort(reverse=True)
    ordered_list_of_scores, ordered_list_of_adoption_centers = zip(*zipped_lists)
    return ordered_list_of_adoption_centers

def get_adopters_for_advertisement(adoption_center, list_of_adopters, n):
    """
    The function returns a list of the top n scoring Adopters from
    list_of_adopters (in numerical order of score)
    """
    if n < 0:
        n = 0
    unordered_list_of_adopter_instances = list_of_adopters[:]
    unordered_list_of_scores = []
    for adopter in unordered_list_of_adopter_instances:
        unordered_list_of_scores.append(adopter.get_score(adoption_center))
    unordered_list_of_adopters = []
    for person in unordered_list_of_adopter_instances:
        if type(person) == str:
            unordered_list_of_adopters.append(person)
        else:
            unordered_list_of_adopters.append(person.get_name())
    zipped_lists = zip(unordered_list_of_scores, unordered_list_of_adopters)
    zipped_lists.sort(reverse=True)
    ordered_list_of_scores, ordered_list_of_adopters = zip(*zipped_lists)
    return ordered_list_of_adopters[:n]

def test():
    
    Highlands = AdoptionCenter('Highlands', {'Dog':5,'Cat':1,'Wallaby':29,'Dingo':2, 'Sphinx':100}, (1,1))
    Lowlands = AdoptionCenter('Lowlands', {'Dog':1,'Cat':3,'Wallaby':9,'Dingo':20, 'Sphinx':10}, (3,3))
    Midlands = AdoptionCenter('Midlands', {'Dog':2,'Cat':100,'Wallaby':2,'Dingo':6, 'Sphinx':8}, (100, 100))
    Leftlands = AdoptionCenter('Leftlands', {'Dog':5,'Cat':6,'Wallaby':3,'Dingo':6, 'Sphinx':66}, (-50, 0))
    Rightlands = AdoptionCenter('Rightlands', {'Dog':8,'Cat':5,'Wallaby':7,'Dingo':4, 'Sphinx':121}, (50, 0))
    Uplands = AdoptionCenter('Uplands', {'Dog':2,'Cat':1,'Wallaby':7,'Dingo':5, 'Sphinx':12}, (0, 50))
    Downlands = AdoptionCenter('Downlands', {'Dog':1,'Cat':3,'Wallaby':4,'Dingo':5, 'Sphinx':13}, (0, -50))
    list_of_adoption_centers = [Highlands, Lowlands, Midlands, Leftlands, Rightlands, Uplands, Downlands]
    
    for ac in list_of_adoption_centers:
        print "Created " + str(ac)
    
    print ""

    Fan = FlexibleAdopter('Fan', 'Dog', 'Cat')
    Dan = FearfulAdopter('Dan', 'Dog', 'Wallaby')
    Allie = AllergicAdopter('Allie', 'Cat', ['Nunchuks', 'Fish', 'Wallaby'])
    Meddie = MedicatedAllergicAdopter('Meddie', 'Dog', ['Pineapple', 'Guava', 'Shark', 'Wallaby', 'Cat'], {'Wallaby':0.5, 'Cat':0.4})
    LessThanOneSal = SluggishAdopter('LessThanOneSal', 'Sphinx', (1, 1.9))
    Sal = SluggishAdopter('Sal', 'Sphinx', (2, 2))
    ThreeSal = SluggishAdopter('ThreeSal', 'Sphinx', (4, 1))
    FourSal = SluggishAdopter('FourSal', 'Sphinx', (5, 1))
    FiveSal = SluggishAdopter('FiveSal', 'Sphinx', (6, 1))
    SixSal = SluggishAdopter('SixSal', 'Sphinx', (7, 1))
    WayFarSal = SluggishAdopter('WayFarSal', 'Sphinx', (1000, 1000))
    list_of_adopters = [Fan, Dan, Allie, Meddie, LessThanOneSal, Sal, ThreeSal, FourSal, FiveSal, SixSal, WayFarSal]
    
    for ad in list_of_adopters:
        print "Created " + str(ad)
    
    print ""
    
    for ad in list_of_adopters:
        print "The best adoption centers for " + ad.name + " are, in descending order: "
        print get_ordered_adoption_center_list(ad, list_of_adoption_centers)
    
    print ""
    
    for ac in list_of_adoption_centers:
        print "The top 4 candidate adopters for " + ac.name + " are, in descending order: "
        print get_adopters_for_advertisement(ac,list_of_adopters, 4)

if __name__=="__main__":
    test()
'''
adopter = MedicatedAllergicAdopter("One", "Cat", ['Dog', 'Horse'], {"Dog": .5, "Horse": 0.2})
adopter2 = Adopter("Two", "Cat")
adopter3 = FlexibleAdopter("Three", "Horse", ["Lizard", "Cat"])
adopter4 = FearfulAdopter("Four","Cat","Dog")
adopter5 = SluggishAdopter("Five","Cat", (1,2))
adopter6 = AllergicAdopter("Six", "Cat", ["Dog"]) 

ac = AdoptionCenter("Place1", {"Mouse": 12, "Dog": 2}, (1,1))
ac2 = AdoptionCenter("Place2", {"Cat": 12, "Lizard": 2}, (3,5))
ac3 = AdoptionCenter("Place3", {"Horse": 25, "Dog": 9}, (-2,10))

# how to test get_adopters_for_advertisement
# get_adopters_for_advertisement(ac, [adopter, adopter2, adopter3, adopter4, adopter5, adopter6], 10)
# you can print the name and score of each item in the list returned

adopter4 = FearfulAdopter("Four","Cat","Dog")
adopter5 = SluggishAdopter("Five","Cat", (1,2))
adopter6 = AllergicAdopter("Six", "Lizard", ["Cat"]) 

ac = AdoptionCenter("Place1", {"Cat": 12, "Dog": 2}, (1,1))
ac2 = AdoptionCenter("Place2", {"Cat": 12, "Lizard": 2}, (3,5))
ac3 = AdoptionCenter("Place3", {"Cat": 40, "Dog": 4}, (-2,10))
ac4 = AdoptionCenter("Place4", {"Cat": 33, "Horse": 5}, (-3,0))
ac5 = AdoptionCenter("Place5", {"Cat": 45, "Lizard": 2}, (8,-2))
ac6 = AdoptionCenter("Place6", {"Cat": 23, "Dog": 7, "Horse": 5}, (-10,10))

# how to test get_ordered_adoption_center_list
# get_ordered_adoption_center_list(adopter4, [ac,ac2,ac3,ac4,ac5,ac6])                            
# you can print the name and score of each item in the list returned
'''

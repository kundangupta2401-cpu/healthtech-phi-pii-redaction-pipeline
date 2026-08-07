class Pseudonymizer:

    def __init__(self):
        self.mapping = {}
        self.person_count = 1
        self.org_count = 1
        self.location_count = 1

    def get_pseudonym(self, entity, entity_type):

        if entity in self.mapping:
            return self.mapping[entity]

        if entity_type == "PERSON":
            pseudonym = f"PATIENT_{self.person_count:03}"
            self.person_count += 1

        elif entity_type == "ORG":
            pseudonym = f"HOSPITAL_{self.org_count:03}"
            self.org_count += 1

        elif entity_type == "GPE":
            pseudonym = f"LOCATION_{self.location_count:03}"
            self.location_count += 1

        else:
            pseudonym = "[UNKNOWN]"

        self.mapping[entity] = pseudonym
        return pseudonym

if __name__ == "__main__":

    pseudonymizer = Pseudonymizer()

    print(pseudonymizer.get_pseudonym("Rahul Sharma", "PERSON"))
    print(pseudonymizer.get_pseudonym("Apollo Hospital", "ORG"))
    print(pseudonymizer.get_pseudonym("Delhi", "GPE"))
    print(pseudonymizer.get_pseudonym("Rahul Sharma", "PERSON"))
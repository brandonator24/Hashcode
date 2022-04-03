
# Practice Round - One Pizza - Hash Code 2022

class Client():
    def __init__(self, likes, dislikes):
        self.likes = likes
        self.dislikes = dislikes
    
    def is_pleased(self, toppings):
        for like in self.likes:
            if like not in toppings:
                return False
        for dislike in self.dislikes:
            if dislike in toppings:
                return False
        return True

class PizzaGenerator():
    def __init__(self, file_loc):
        self.clients = self.create_clients(file_loc)
        self.unique_toppings = self.get_unique_toppings()
        #print(self.unique_toppings)
        self.rated_toppings = self.rate_toppings(self.unique_toppings)
        print(file_loc)
        print("Conventional:", self.convert_toppings_to_output(self.get_optimum_toppings(self.rated_toppings)))
        print("Permutational:", self.convert_toppings_to_output(self.get_optimum_via_permutations(self.get_optimum_via_permutations([topping for topping in self.unique_toppings]))))
        print()        

    def get_optimum_via_permutations(self, available_toppings):
        import itertools
        best_perm = []
        pleased_clients = 0
        for i in range(1, len(available_toppings)):
            perms = list(itertools.permutations(available_toppings, i))
            for perm in perms:
                perm = list(perm)
                new_pleased_clients = self.get_number_of_pleased_clients(perm)
                if new_pleased_clients >= pleased_clients:
                    best_perm = perm
                    pleased_clients = new_pleased_clients
        return best_perm

    def convert_toppings_to_output(self, toppings):
        toppings_as_str = ""
        for topping in toppings:
            toppings_as_str += " " + topping
        return(f"{len(toppings)}{toppings_as_str}")

    def create_clients(self, file_loc):
        # open the file and convert into list.
        with open(file_loc) as input_file:
            input_lines = input_file.read().split("\n")
        number_of_clients = int(input_lines[0])
        clients = []
        # remove the amount of clients
        input_lines.pop(0)
        while len(input_lines) > 0:
            try:
                likes = input_lines[0].split(" ")[1:]
            except IndexError:
                likes = []
            try:
                dislikes = input_lines[1].split(" ")[1:]
            except IndexError:
                dislikes = []
            input_lines = input_lines[2:]
            clients.append(Client(likes, dislikes))
        return clients

    # Find all unique toppings
    def get_unique_toppings(self):
        unique_toppings = {}
        for client in self.clients:
            client_toppings = client.likes + client.dislikes
            for topping in client_toppings:
                if topping not in unique_toppings:
                    unique_toppings[topping] = 0
        #print(f"Unique Toppings: {unique_toppings}")
        return unique_toppings

    def rate_toppings(self, unique_toppings):
        for client in self.clients:
            for like in client.likes:
                unique_toppings[like] += 1
            for dislike in client.dislikes:
                unique_toppings[dislike] -= 1
        return unique_toppings

    def get_number_of_pleased_clients(self, toppings):
        pleased_clients = 0
        for client in self.clients:
            if client.is_pleased(toppings):
                pleased_clients += 1
        return pleased_clients

    def max_sub_arr(self, toppings_dict):
        #toppings dict
        toppings_used = []
        cur_max = 0
        max = -9999
        for topping_name in toppings_dict:
            cur_max += toppings_dict[topping_name]
            if (cur_max > max):
                max = cur_max
                toppings_used.append(topping_name)
        return toppings_used

    def get_optimum_toppings(self, toppings_dict):
        # get maximum pleasure of topping.
        max_val = toppings_dict[list(toppings_dict.keys())[0]]
        for topping in toppings_dict:
            current_val = toppings_dict[topping]
            # if is biggest yet.
            if max_val < current_val:
                max_val = current_val

        # find all toppings that are max.
        toppings = []
        for topping in toppings_dict:
            current_val = toppings_dict[topping]
            if current_val == max_val:
                toppings.append(topping)
        return toppings


if __name__ == "__main__":
    import os
    #for file_name in os.listdir("../inputs/"):
    #    PizzaGenerator(file_name)

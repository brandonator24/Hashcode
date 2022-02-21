
# Practice Round - One Pizza - Hash Code 2022

# alternate idea: somethin bout ascending order

class Client():
    def __init__(self, likes, dislikes):
        self.likes = likes
        self.dislikes = dislikes

class PizaGeneration():
    pass

def create_clients(file_loc):
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

clients = create_clients("e_elaborate.in.txt")


# Find all unique toppings
def get_unique_toppings():
    unique_toppings = {}
    for client in clients:
        client_toppings = client.likes + client.dislikes
        for topping in client_toppings:
            if topping not in unique_toppings:
                unique_toppings[topping] = 0
    print(f"Unique Toppings: {unique_toppings}")
    return unique_toppings

unique_toppings = get_unique_toppings()

def rate_toppings(unique_toppings):
    for client in clients:
        for like in client.likes:
            unique_toppings[like] += 1
        for dislike in client.dislikes:
            unique_toppings[dislike] -= 1
    return unique_toppings

def get_number_of_pleased_clients(toppings):
    pleased_clients = clients
    for client in clients:
        for like in client.likes:
            if like not in toppings:
                try:
                    pleased_clients.remove(client)
                except ValueError:
                    pass
        for dislike in client.dislikes:
            if dislike in toppings:
                try:
                    pleased_clients.remove(client)
                except ValueError:
                    pass
    return len(pleased_clients)

def max_sub_arr(toppings_dict):
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

def get_optimum_toppings(toppings_dict):
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

rated_toppings = rate_toppings(unique_toppings)
print(f"Rated Toppings: {rated_toppings}")

optimum_toppings = max_sub_arr(rated_toppings)

optimum_toppings2 = get_optimum_toppings(rated_toppings)

print(f"optimum_toppings from poser: {optimum_toppings2}")

#print(f"optimum_toppings from max_sub_arr: {optimum_toppings}")

toppings_as_str = ""
for topping in optimum_toppings2:
    toppings_as_str += " " + topping

print(f"{len(optimum_toppings2)}{toppings_as_str}")


if __name__ == "__main__":
    pass
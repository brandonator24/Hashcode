import pandas as pd
import numpy as np

def assembleData(file_name):
    dataframe = pd.read_csv(file_name)
    dfLikes = dataframe.iloc[dataframe.index%2==0]
    dfLikes.columns = ["temp"]
    dfLikes[["num toppings", "liked toppings"]] = dfLikes["temp"].str.split(" ",n=1,expand=True)
    dflikes = dfLikes.drop("temp", axis=1)
    dfLikes = dfLikes.reset_index(drop=True)
    #print(dfLikes)
    dfLiked_ing = dfLikes["liked toppings"].str.split(" ", expand = True)
    dfLiked_ing = dfLiked_ing.unstack().value_counts().to_frame()
    dfLiked_ing = dfLiked_ing.iloc[1: , :]
    dfLiked_ing = dfLiked_ing.set_axis(["like_score"], axis = 1, inplace = False)
    print(dfLiked_ing)
    
    print("\n")

    dfDislikes = dataframe.iloc[dataframe.index%2==1]
    dfDislikes.columns = ["temp"]
    dfDislikes[["num toppings", "disliked toppings"]] = dfDislikes["temp"].str.split(" ", n=1, expand = True)
    dfDislikes.drop("temp", axis = 1, inplace = True)
    dfDislikes.reset_index(drop=True, inplace=True)
    #print(dfDislikes)
    dfDisliked_ing = dfDislikes["disliked toppings"].str.split(" ", expand = True)
    dfDisliked_ing = dfDisliked_ing.unstack().value_counts().to_frame()
    dfDisliked_ing = dfDisliked_ing.iloc[1: , :]
    dfDisliked_ing = dfDisliked_ing.set_axis(["dislike_score"], axis = 1, inplace = False)
    dfDisliked_ing = dfDisliked_ing.drop()
    dfDisliked_ing = dfDisliked_ing["dislike_score"].apply(lambda x: x*-1)
    print(dfDisliked_ing)

    dfIngredients = pd.concat([dfLiked_ing, dfDisliked_ing], axis=1).fillna(0)
    dfIngredients["total_score"] = dfIngredients["like_score"] + dfIngredients["dislike_score"]
    dfIngredients["ingredient"] = dfIngredients.index
    print(dfIngredients)

    return dfIngredients

def chooseToppings(df):
    print(f"AAAAAAAAA: {type(df.iloc[5, 3])}")
    topping_list = []
    for i in range (1, len(df)):
        if(df.iloc[i, 2]) >-1:
            topping_list.append(df.iloc[i, 3])
    
    print(len(topping_list))
    return topping_list

def generateOutput(myList):
    myStr = ""
    for item in myList:
        myStr = myStr + " " + item
    
    output = str(len(myList)) + myStr
    with open("outputv2.txt", "w") as out_file:
        out_file.write(output)

if __name__ == "__main__":
    file_name = "e_elaborate.in.txt"
    df = assembleData(file_name)
    toppings = chooseToppings(df)
    generateOutput(toppings)


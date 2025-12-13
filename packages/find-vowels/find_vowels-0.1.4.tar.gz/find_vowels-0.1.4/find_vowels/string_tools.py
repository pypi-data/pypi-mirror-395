

def count_vowels(words:str) -> str:
    vowels_dict = {}
    for charecter in words:  #[ this is word]
        if charecter in ["a","i","o","u"]:
            if charecter in vowels_dict.keys():
                vowels_dict[charecter] += vowels_dict[charecter]
            else:
                vowels_dict[charecter] = 1
    return vowels_dict

# PRACTICAL 9A
# Fuzzy Ratios using FuzzyWuzzy

from fuzzywuzzy import fuzz, process

s1 = "I love fuzzysforfuzzys"
s2 = "I am loving fuzzysforfuzzys"

print("Fuzzy Ratio:", fuzz.ratio(s1, s2))
print("Partial Ratio:", fuzz.partial_ratio(s1, s2))
print("Token Sort Ratio:", fuzz.token_sort_ratio(s1, s2))
print("Token Set Ratio:", fuzz.token_set_ratio(s1, s2))
print("WRatio:", fuzz.WRatio(s1, s2))

query = "fuzzys for fuzzys"
choices = ["fuzzy for fuzzy", "fuzzy fuzzy", "g. for fuzzys"]

print("\nList of ratios:", process.extract(query, choices))
print("Best Match:", process.extractOne(query, choices))

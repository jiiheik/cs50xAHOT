# Text Input
t = input("Text: ")

# Number of letters
l = 0
for i in range(len(t)):
    if t[i].isalpha():
        l += 1

# Number of words
w = len(t.split())

# Number of sentences
s = 0
for i in range(len(t)):
    if t[i] == '!' or t[i] == '?' or t[i] == ".":
        s += 1

# Calculate index
result = ((0.0588 * (l / w)) * 100) - ((0.296 * (s / w)) * 100) - 15.8
r2 = round(result, 0)

if r2 < 1:
    print("Before Grade 1")
elif r2 > 16:
    print("Grade 16+")
else:
    print(f"Grade: {r2}")

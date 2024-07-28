import requests
from bs4 import BeautifulSoup
import pandas as pd

# Get user input
name = input("Enter the full name of a person to search for on Wikipedia: ")

# Format the name for the URL
formatted_name = name.replace(" ", "_")

# Build the URL and make the request
url = f'https://en.wikipedia.org/wiki/{formatted_name}'
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

# Print the page title
print(soup.title.text)
print()

# Find all labels and data in the infobox
all_labels = soup.find_all("th", class_="infobox-label")
all_data = soup.find_all("td", class_="infobox-data")

# Extract labels and data
labels = [label.text.strip() for label in all_labels]
labeldata = [data.text.strip() for data in all_data]

# Combine labels and data into a dictionary
dataset = dict(zip(labels, labeldata))
df = pd.DataFrame(list(dataset.items()), columns=["Label", "Data"])

#store data in excel
df.to_excel("wikiscrape_" + str(formatted_name) + ".xlsx", index=False)
print("All label info stored in 'wikiscrape_" + str(formatted_name) + ".xlsx'")

while(True):
    print("Choose a category: ")
    print()
    for label in all_labels:
        print(label.text.strip())
    print()
    question = str(input("Copy and paste the exact label for which you would like to learn more about (type quit to end): "))
    print()
    if question.lower() == 'quit':
        print("Thanks for using the program!")
        break

    else:
        if dataset.get(question) == None:
            print('Error! Unable to retrieve label data. Please try again.')
            print()
            continue
        else:
            print("Label Data: " + str(dataset.get(question)))
            print()
            continue

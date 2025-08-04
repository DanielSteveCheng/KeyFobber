import csv

# Open the CSV file
with open('TestFile.csv', 'r', newline='') as csvfile:
        # Create a csv.reader object
        csv_reader = csv.reader(csvfile)

        header = next(csv_reader)
        print(f"Header: {header}")

        users = []
        
        for row in csv_reader:
            users.append(row) # Each row is a list of strings

        print(users)
        print(users[0][0])
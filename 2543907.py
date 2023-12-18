import re

# Function to compute the score of a character in a word
def compute_character_score(letter, letter_index, lastletter, values):
    letter = letter.upper()

    # Return 0 for the first character of the word
    if letter_index == 0:
        return 0
    # Check if the letter is the last character and not 'E'
    elif lastletter:
        if letter == 'E':
            return 20
        else:
            return 5
    # Compute the weight for middle characters
    else:
        position_value = min(letter_index, 3)
        
        return position_value + values.get(letter, 0)

# Function to load letter scores from a file
def load_values(values_file):
    letter_scores = {}

    try:
        # Open the values file for reading
        with open(values_file, 'r') as file:
            # Iterate over each line in the file
            for line in file:
                # Split the line into parts based on whitespace
                parts = line.strip().split()
                
                # Check if there are exactly two parts
                if len(parts) == 2:
                    # Extract letter and score, then convert score to an integer
                    letter, score = parts
                    letter_scores[letter] = int(score)
    except FileNotFoundError:
        # Handle the case where the file is not found
        print(f"Error: File '{values_file}' not found.")
    except Exception as e:
        # Handle other exceptions that might occur during file reading
        print(f"Error while loading values: {e}")

    return letter_scores

# Function to filter and extract words from a line
def filtering_line(line1):
    line1 = ''.join(char for char in line1 if char != "'")
    line1 = re.sub(r'[^a-zA-Z\s]', '', line1)
    line1 = line1.upper()

    # Use re.findall to split the words
    words = re.findall(r'\b\w+\b', line1)
    return words

# Function to create abbreviations based on given rules
def create_abbreviations(treename_list, values):
    abbreviations_list = []

    for treename in treename_list:
        current_abbreviations = set()
        structured_treename = structure_treename(treename, 0)

        for i in range(1, len(structured_treename) - 1):
            for j in range(i, len(structured_treename) - 1):
                # Filter abbreviations based on length and alphabetic characters
                current_abbreviation = structured_treename[0] + structured_treename[i] + structured_treename[j + 1]
                if len(current_abbreviation) == 3 and current_abbreviation.isalpha():
                    # Calculate the score using the modified compute_character_score function
                    current_score = sum(
                        compute_character_score(letter, idx, idx == len(structured_treename) - 2, values)
                        for idx, letter in enumerate(current_abbreviation))
                    current_abbreviations.add((current_abbreviation.upper(), current_score))

        abbreviations_list.append(current_abbreviations)

    return abbreviations_list

# Function to structure the treename (currently a placeholder)
def structure_treename(treename, n):
    return treename

# Function to find the best abbreviations based on scores
def best_abbreviations(abbreviations):
    if not abbreviations:
        return set()

    # Sort the abbreviations by score in ascending order
    sorted_abbreviations = sorted(abbreviations, key=lambda x: x[1])
    
    # Find the minimum score
    min_score = sorted_abbreviations[0][1]

    # Use a set comprehension to get abbreviations with the minimum score
    min_score_abbreviations = {abbr for abbr, score in sorted_abbreviations if score == min_score}

    return min_score_abbreviations

# Main function
def main():
    file_path = r"C:\Users\mehul\OneDrive\Desktop\python assignment 12\trees.txt"
    values_file = r"C:\Users\mehul\OneDrive\Desktop\python assignment 12\values.txt"
    
    # Load values from the file
    values = load_values(values_file)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        treename_list = [line.strip() for line in file]

        # Generate abbreviations using the logic from generate_abbreviations
        abbreviations_list = create_abbreviations(treename_list, values)

        for i, line in enumerate(treename_list):
            # Print the line, list of abbreviations, and their scores
            print(line)
            final_abbreviations = best_abbreviations(abbreviations_list[i])
            
            # Print the best abbreviations
            if final_abbreviations:
                print(f"{' '.join(final_abbreviations)}")
            else:
                print("")  # Blank line for names without acceptable abbreviations
            print()

if __name__ == "__main__":
    main()

# File: ENEJI_2612928_PYTHON_ASSIGN.py  # Filename
# Author: Ali Patrick Eneji  # Author's name
# Purpose: Generate three-letter abbreviations for names following specific rules  # Brief purpose of the script

import re  # Import regex module for string pattern matching
from typing import Dict, List, Set, Tuple  # Import type hints for better code clarity

class AbbreviationGenerator:  # Class to encapsulate abbreviation generation logic
    def __init__(self):  # Constructor method
        # Hardcoded letter values as specified in the requirements  # Initializing letter value mapping
        self.letter_values = {
            'Q': 1, 'Z': 1,  # Value 1
            'J': 3, 'X': 3,  # Value 3
            'K': 6,          # Value 6
            'F': 7, 'H': 7, 'V': 7, 'W': 7, 'Y': 7,  # Value 7
            'B': 8, 'C': 8, 'M': 8, 'P': 8,  # Value 8
            'D': 9, 'G': 9,  # Value 9
            'L': 15, 'N': 15, 'R': 15, 'S': 15, 'T': 15,  # Value 15
            'O': 20, 'U': 20,  # Value 20
            'A': 25, 'I': 25,  # Value 25
            'E': 35  # Value 35
        }

    def _split_into_words(self, name: str) -> List[str]:  # Helper function to split names into words
        """Split name into words, handling special cases like possessives"""  # Docstring for method description
        # Remove apostrophes and convert to uppercase  # Clean name string
        name = name.upper()  # Convert name to uppercase
        
        # Handle possessives before splitting  # Remove possessive 's
        # Replace "'S " or "'S$" with a space or nothing
        name = re.sub(r"'S\s+", " ", name)  # Replace possessives ending with space
        name = re.sub(r"'S$", "", name)  # Replace possessives at end of name
        
        # Now remove any remaining apostrophes  # Clean remaining apostrophes
        name = name.replace("'", "")  # Remove stray apostrophes
        
        # Split on non-letter characters  # Split by delimiters
        words = re.split(r'[^A-Z]+', name)  # Split into list of words
        return [w for w in words if w]  # Remove empty strings  # Filter out empty strings

    def _get_letter_position_in_words(self, words: List[str], target_letter: str) -> List[tuple]:  # Helper to find letter positions
        """Find all positions of a letter in the words, returns list of (word_index, position, is_first, is_last)"""  # Docstring for method
        positions = []  # Initialize list to store positions
        for word_idx, word in enumerate(words):  # Loop through words
            for pos, letter in enumerate(word):  # Loop through letters in word
                if letter == target_letter:  # Check for matching letter
                    is_first = (pos == 0)  # Determine if it's the first letter
                    is_last = (pos == len(word) - 1)  # Determine if it's the last letter
                    positions.append((word_idx, pos, is_first, is_last))  # Append position data
        return positions  # Return positions list

    def _calculate_letter_score(self, letter: str, words: List[str], word_idx: int, pos_in_word: int, debug=False) -> int:  # Helper to calculate scores
        """Calculate score for a letter in a specific position"""  # Docstring for method
        word = words[word_idx]  # Get current word
        
        # Ignore possessive 's when determining last letter  # Handle possessive suffix
        actual_word = word.rstrip("S") if word.endswith("S") and len(word) > 1 else word  # Remove trailing 'S' if applicable
        
        # First letter of any word scores 0  # Special rule for first letter
        if pos_in_word == 0:  # Check if it's the first letter
            if debug:  # Debugging output
                print(f"  {letter}: First letter of word '{word}', score = 0")  # Debug message
            return 0  # Return score of 0
            
        # Last letter of real word (not counting possessive 's)  # Special rule for last letter
        if pos_in_word == len(actual_word) - 1:  # Check if it's the last letter
            score = 20 if letter == 'E' else 5  # Special rule for 'E'
            if debug:  # Debugging output
                print(f"  {letter}: Last letter of word '{actual_word}', score = {score} ({'E penalty' if letter == 'E' else 'regular'})")  # Debug message
            return score  # Return calculated score
            
        # Middle position  # Calculate score for middle position
        pos_value = 1 if pos_in_word == 1 else (2 if pos_in_word == 2 else 3)  # Position value based on index
        letter_value = self.letter_values.get(letter, 0)  # Fetch letter value
        score = pos_value + letter_value  # Total score calculation
        if debug:  # Debugging output
            print(f"  {letter}: Middle position {pos_in_word + 1} in '{word}', position value = {pos_value}, letter value = {letter_value}, total = {score}")  # Debug message
        return score  # Return total score

    def generate_abbreviations(self, name: str) -> List[Tuple[str, int]]:  # Method to generate abbreviations
        """Generate all possible valid abbreviations with their scores for a name"""  # Docstring for method
        words = self._split_into_words(name)  # Split name into words
        if not words:  # Check if there are no words
            return []  # Return empty list if no words are present

        first_letter = words[0][0]  # Get the first letter of the first word
        seen_abbrevs = {}  # Dictionary to track unique abbreviations and their lowest scores
        
        print(f"\nGenerating abbreviations for: {name}")  # Debug message
        
        # Build map of letter positions  # Create map of letter positions
        letter_positions = {}  # Initialize dictionary to store positions
        for word_idx, word in enumerate(words):  # Iterate over words
            for pos, letter in enumerate(word):  # Iterate over letters in word
                if letter not in letter_positions:  # Check if letter is not in dictionary
                    letter_positions[letter] = []  # Initialize list for this letter
                letter_positions[letter].append((word_idx, pos))  # Append position of letter
        
        # Get all possible second and third letters while maintaining order  # Generate combinations
        for letter2, positions2 in letter_positions.items():  # Iterate over second letters
            for word_idx2, pos2 in positions2:  # Iterate over positions of the second letter
                # Skip if this letter comes before the first letter in the original name
                if (word_idx2, pos2) <= (0, 0):  # Ensure order is maintained
                    continue  # Skip invalid combinations
                    
                for letter3, positions3 in letter_positions.items():  # Iterate over third letters
                    for word_idx3, pos3 in positions3:  # Iterate over positions of the third letter
                        # Skip if this letter doesn't come after the second letter
                        if (word_idx3, pos3) <= (word_idx2, pos2):  # Ensure order is maintained
                            continue  # Skip invalid combinations
                            
                        abbrev = first_letter + letter2 + letter3  # Create abbreviation
                        
                        # Skip if we've already found this abbreviation with a lower score
                        if abbrev in seen_abbrevs:  # Check if abbreviation exists
                            continue  # Skip duplicate abbreviations
                            
                        print(f"\nCalculating score for {abbrev}:")  # Debug message
                        print(f"  {first_letter}: First letter of name, score = 0")  # Debug message
                        
                        # Calculate scores for second and third letters  # Score calculation
                        score2 = self._calculate_letter_score(  # Score for second letter
                            letter2, words, word_idx2, pos2, debug=True)  # Pass parameters for calculation
                        score3 = self._calculate_letter_score(  # Score for third letter
                            letter3, words, word_idx3, pos3, debug=True)  # Pass parameters for calculation
                        
                        total_score = score2 + score3  # Calculate total score
                        print(f"Total score for {abbrev}: {total_score}")  # Debug message
                        
                        # Update seen_abbrevs only if this is a new minimum score
                        if abbrev not in seen_abbrevs or total_score < seen_abbrevs[abbrev]:  # Check for new minimum score
                            seen_abbrevs[abbrev] = total_score  # Update dictionary with abbreviation and score
        
        # Convert dictionary to list of tuples  # Format results
        return [(abbrev, score) for abbrev, score in seen_abbrevs.items()]  # Return list of abbreviations with scores

def main():  # Main function to run the program
    """Main function to process input file and generate abbreviations"""  # Docstring for main function
    generator = AbbreviationGenerator()  # Instantiate the generator
    
    # Get input filename  # Prompt user for input
    input_file = input("Enter input filename: ")  # Read input filename
    if not input_file.endswith('.txt'):  # Check file extension
        input_file += '.txt'  # Append .txt if missing
        
    output_file = f"eneji_{input_file.replace('.txt', '')}_abbrevs.txt"  # Define output filename
    
    try:  # Attempt to open input file
        with open(input_file, 'r') as f:  # Open input file in read mode
            names = [line.strip() for line in f if line.strip()]  # Read and clean lines
    except FileNotFoundError:  # Handle file not found error
        print(f"Error: Could not find input file {input_file}")  # Print error message
        return  # Exit the program

    # Generate all abbreviations  # Generate results
    name_abbrevs = {}  # Dictionary to store abbreviations by name
    all_abbrevs = set()  # Set to track all abbreviations
    
    # First pass: collect all abbreviations  # Process names
    for name in names:  # Iterate over names
        abbrevs = generator.generate_abbreviations(name)  # Generate abbreviations for name
        name_abbrevs[name] = abbrevs  # Store abbreviations in dictionary
        for abbrev, _ in abbrevs:  # Iterate over generated abbreviations
            if abbrev in all_abbrevs:  # Check for duplicates
                # Mark as duplicate  # Handle duplicates
                all_abbrevs.add(abbrev)  # Add abbreviation to set
            else:  # New abbreviation
                all_abbrevs.add(abbrev)  # Add to set
    
    # Write results  # Save results to file
    with open(output_file, 'w') as f:  # Open output file in write mode
        for name in names:  # Iterate over names
            f.write(f"{name}\n")  # Write name to file
            
            # Filter valid abbreviations (those not appearing in other names)  # Validate abbreviations
            valid_abbrevs = []  # List to store valid abbreviations
            for abbrev, score in name_abbrevs[name]:  # Iterate over abbreviations for the name
                appears_elsewhere = False  # Flag to check if abbreviation appears elsewhere
                for other_name in names:  # Check other names
                    if other_name != name:  # Ensure not comparing with the same name
                        if any(a[0] == abbrev for a in name_abbrevs[other_name]):  # Check for duplicates
                            appears_elsewhere = True  # Mark as appearing elsewhere
                            break  # Exit loop
                if not appears_elsewhere:  # If abbreviation is valid
                    valid_abbrevs.append((abbrev, score))  # Add to valid abbreviations
            
            if valid_abbrevs:  # Check if valid abbreviations exist
                # Find the minimum score among valid abbreviations  # Optimize results
                min_score = min(score for _, score in valid_abbrevs)  # Calculate minimum score
                # Only keep abbreviations with exactly the minimum score  # Filter abbreviations
                best_abbrevs = [abbrev for abbrev, score in valid_abbrevs if score == min_score]  # Find best abbreviations
                # Sort and remove duplicates  # Prepare for writing
                best_abbrevs = sorted(set(best_abbrevs))  # Sort and deduplicate
                f.write(f"{' '.join(best_abbrevs)}\n")  # Write abbreviations to file
            else:  # No valid abbreviations
                f.write("\n")  # Write empty line

if __name__ == "__main__":  # Entry point of the script
    main()  # Execute main function

# example of program that calculates the number of tweets cleaned
import os
import parse
import sys
import utility

# Checks string if contains unicode
# returns true if does, else false
def contain_unicode(text):
    # UNICODE CHECK
            # Attempt to decode into ASCII...
            try:
                text.decode('ascii')
                return False
            # If fails contains unicode
            except:
                return True

# Method that reads the tweets.txt file
# Creates an output text file, ft1.txt
# Creates a strings that contains each tweet without unicode characters and time stamp
# Prints number of posts that contained unicode
# Returns the complete output while writing it into the output text file
def clean_tweets(input, output):
    # Creates the output text file
    output_file = open(output,'w')

    # Creates JSON array out of line delimted JSON file
    json_input = utility.to_json_array(input)

    # Initialize unicode count variable
    unicode_count = 0

    # Iterate through all JSON Objects within the array
    for currentObj in json_input:
        if 'text' in currentObj:
            text = parse.parse_json(currentObj, 'text')
            created_at = parse.parse_json(currentObj, 'created_at')

            # UNICODE CHECK
            if contain_unicode(text) or contain_unicode(created_at):
                unicode_count+=1
                text = utility.clean_text(text)
                created_at = utility.clean_text(created_at)

            # Write JSON Object Post Output
            #print(text + ' (timestamp: ' + created_at + ')\n')
            output_file.write(text + ' (timestamp: ' + created_at + ')\n')

    # Writing aggregate unicode into output file and test string
    output_file.write(str(unicode_count) + ' tweet(s) contained unicode.')
    #print(str(unicode_count) + ' tweet(s) contained unicode.')

    # Close files
    output_file.close()
    print("\nTweet clean completed\nOutput in: " + output)

# Main method
def main(argv):
    # Initialization of base directory from excuted python script
    BASE_DIR = os.path.dirname(__file__)

    # Check for 3 arguments
    if len(sys.argv) != 3:
        print 'tweets_cleaned.py <input_file> <output_file>'
        sys.exit(2)

    # Runs program
    else:
        #clean_tweets(os.path.join(BASE_DIR,'../data-gen/tweets.txt'), os.path.join(BASE_DIR,'../tweet_output/ft1.txt'))
        clean_tweets(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main(sys.argv[1:])
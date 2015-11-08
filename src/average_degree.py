# example of program that calculates the average degree of hashtags
import debug
import parse
import os
import sys
import utility

# Creates the degree list out of the adjacency list
def create_degree_list(list):
    # Initialization of degree list
    list_degree = {}

    # Iterates through all of in nodes and initializes
    # degrees to zero
    for tag in list.keys():
        list_degree[tag] = 0

    # Iterates through all node connections and
    # increments the degree
    for tag in list:
        for i in list[tag]:
            list_degree[i['edge']]+=1

    return list_degree

# Creates an adjacency list of hashtags in each post
# and iterates through the list twice creating edges
# for each hashtag that appears within the same post
# Creates a dictionary who's keys represents nodes and
# values represent lists of edges from the key node
# {Node: [{edge: edge_value, timestamp: timestamp_value} {edge: edge_value, timestamp: timestamp_value}]}
def identify_hashtags(list, post, timestamp):
    # Calls utility node that creates list of hashtags
    # within a post
    matches = parse.parse_hashtag(post)

    # Only adds values if more than one hashtag
    if len(matches) > 1:
        # Iterates hashtags and appends it to the
        # adjacency list structure
        for hashtag in matches:
                # Initializes node if it doesn't
                # currently exists
                if hashtag not in list:
                    list[hashtag] = []

                # Iterates through list of hashtags a
                # second time and initializes edges
                # within list if they either don't exist
                # or are not equal to the parent node
                for inner_hashtag in matches:
                    # Initializing
                    if inner_hashtag not in list:
                        list[inner_hashtag] = []

                    # Check if should add
                    # Conditions:
                    # - If the child node is not equal to the parent node
                    # - If the child node does not already exist within the parent node
                    if not any(post['edge'] == inner_hashtag for post in list[hashtag]) and hashtag != inner_hashtag:
                        current_edge = {}
                        current_edge['edge'] = inner_hashtag
                        current_edge['timestamp'] = timestamp
                        list[hashtag].append(current_edge)

    return list

# Method that removes all outdated post within
# the adjacency list
def remove_outdated(list, threshold):
    for node in list.keys():
        # Transverses dictionary backwards and removes all
        # edges with time stamps before threshold;
        # additionally deletes all nodes that do not have
        # edges
        for i in xrange(len(list[node])-1, -1, -1):
            edge = list[node][i]
            if edge['timestamp'] < threshold:
                del list[node][i]
                if not list[node]:
                    del list[node]
    # Test if posts are deleted
    #print(str(count) + ' posts deleted\n------------------------------')
    return list

# Method that reads the tweets.txt file
# Creates an output text file, ft2.txt
# Grabs all text and created_at values
# Scrapes for # and identifies hashtags
# Creates adjacency list for all hashtags
def average_degree(input, output):
    # Creates the output text file
    output_file = open(output,'w')

    # String that stores all the content of the output.txt
    # Used for debugging purposes
    #test = ''

    # Creates JSON array out of line delimted JSON file
    json_input = utility.to_json_array(input)

    adjacency_list = {}
    previous_threshold_time = None

    # Iterates through all objects within JSON Array
    for current_obj in json_input:
        # Checks if text exists within json_input
        if 'text' in current_obj:
            # Creates list of texts and timestamps of posts
            text = parse.parse_json(current_obj,'text')
            created_at = parse.parse_json(current_obj,'created_at')

            # Cleans texts and timestamps and parses timestamps
            text = utility.clean_text(text)
            created_at = utility.clean_text(created_at)
            parsed_time = parse.parse_timestamps(created_at)

            # Calculates current post threshold time
            threshold_time = utility.minute_offset(parsed_time);

            # Initializes previous threshold time so it can be used
            # for comparison and skip redundant checks
            if previous_threshold_time is None:
                previous_threshold_time = threshold_time

            # Removes all edges in adjacency list below threshold time if
            # threshold time was changed and resets threshold time to latest
            # post's time
            if threshold_time != previous_threshold_time:
                adjacency_list = remove_outdated(adjacency_list, threshold_time)
            previous_threshold_time = threshold_time

            # Creates
            # {'text': timestamp} -> {Node: [{edge: , timestamp: } {edge: , timestamp: }]}
            # Creates adjacency from hashtag list created from the post
            adjacency_list = identify_hashtags(adjacency_list, text, parsed_time)

            # Writes adjacency list to text output and testing console
            #print(debug.debug_adjacency_list(adjacency_list))
            #test += debug.debug_adjacency_list(adjacency_list)
            #output_file.write(debug.debug_adjacency_list(adjacency_list))

            # Creates degree list and calculates average degrees
            degree_list = create_degree_list(adjacency_list)
            average_degree = utility.calculate_average(degree_list)

            # Adds degree list and average degrees to output file and
            # debug text
            #print(debug.debug_degree_list(degree_list))
            #print('Average degree = ' + debug.debug_degrees(degree_list) + str(average_degree))
            #output_file.write(debug.debug_degree_list(degree_list))
            #output_file.write('Average degree = ' + debug.debug_degrees(degree_list) + ' = ' + str(average_degree) + '\n')
            #print(str(average_degree))
            output_file.write(str(average_degree) + '\n')
            #test += debug.debug_degree_list(degree_list)
            #test += 'Average degree = ' + str(average_degree)+'\n\n'

    # Close files
    output_file.close()
    print("\nAverage degree completed\nOutput in: " + output)
    #print(test)

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
        #average_degree(os.path.join(BASE_DIR,'../data-gen/tweets.txt'), os.path.join(BASE_DIR,'../tweet_output/ft2.txt'))
        average_degree(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main(sys.argv[1:])
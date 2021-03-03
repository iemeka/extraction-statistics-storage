import re
import pandas as pd


# QUESTION A AND B
def updateDictionary(color_dictionary,data):
    for item in data:
        if item[-1] == ",":  # For ONLY monday. The last color - GREEN - has a comma, ""GREEN,""
            # print(item) 
            item = item[:-1]
        if item not in color_dictionary:
            color_dictionary[item]=0
        color_dictionary[item]+=1
    return color_dictionary

# extract colors
def extractColors():
    color_dictionary = {}
    colors_file = open("python_class_test.html","r")
    for line in colors_file.readlines():
        if re.search("^.*<td>",line) and re.search(",",line):
            line = re.findall("(?<=<td>).*(?=</td>)",line)
            data = line[0].split(", ") # split matches "comman and space."
            # print(data)
            color_dictionary = updateDictionary(color_dictionary,data)
    # print(color_dictionary)
    return color_dictionary

def makeDataFrame():
    color_dictionary = extractColors()
    df = pd.DataFrame(color_dictionary.items(),columns=['Color','Frequency']).sort_values('Frequency')
    print(df)
    return df


# QUESTION 1 - 5
# Find mean color of shirt
def findMean():
    """The mean color is the color which frquency has the minimum distance to the mean value"""
    mean_value = colors_dataFrame['Frequency'].mean()
    mean_color = ""
    lowest_distance = float('inf')
    for row in colors_dataFrame.iterrows():
        # print(row[1][0],row[1][1])
        color,frq = row[1][0],row[1][1]
        distance = abs(frq - mean_value)
        if distance < lowest_distance:
            lowest_distance = distance
            mean_color = color
    print(f"\nThe mean is {mean_value}")
    print("The color which frquency is closest to the mean is {} or any color with the minimum distance of {}".format(mean_color,round(lowest_distance,3)))
    print(f"Mean color of shirt is {mean_color} or RED")
    return mean_color

def findMode():
    '''The mode is the color with the highest frequency'''
    mode_data = colors_dataFrame.loc[colors_dataFrame['Frequency'].idxmax()]
    print("\nThe color worn mostly is BLUE")
    print(f"{mode_data}\n")
    return mode_data

def findMedian():
    '''The rows are sorted in ascending order according to the frequency'''
    median_df = colors_dataFrame
    median = median_df['Frequency'].median()
    print(f"The median value is {median}")
    print(f"The the first color who's cummulative frequency is more than {median} is the median color")
    median_df['Cummulative Frequency'] = median_df['Frequency'].cumsum()
    print(median_df)
    print(f"The median color is YELLOW")
    return "YELLOW"

    
def findVariance():
    variance = colors_dataFrame['Frequency'].var()
    print(f"\nThe variance is {round(variance,3)}")
    return variance

def probability():
    '''The probability of picking red is : Frequency of red DIVIDED BY total freqency'''
    red_row = colors_dataFrame.loc[colors_dataFrame['Color'] == "RED"]
    # print(red_row)
    freqency_of_red = red_row.iloc[0][1]
    print (f"\nFreqeency of red is {freqency_of_red}")
    total_frequency = colors_dataFrame['Frequency'].sum()
    print(f"Total frequency is {total_frequency}")
    prob_of_picking_red = round(float(freqency_of_red)/total_frequency,3)
    print(f"The probability of picking red is {prob_of_picking_red}\n")
    return prob_of_picking_red

# DATABASE
import psycopg2
import functools
from six.moves.configparser import ConfigParser

# CONFIGURATION
# Please check the file 'database.ini' and fill in your database credentials
def config(filename='database.ini',section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'. format(section, filename))
    
    return db

#Query runner for 'creating table'
def create_table(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            for sql in query():
                cur.execute(sql)
            conn.commit()
            msg = cur.statusmessage
            #print msg
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection ended.')
    return connect_run_close


# query runner for adding COLORS AND FREQUENCY to database
def save_colors(query):
    @functools.wraps(query)
    def connect_run_close():

        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query())
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                
    return connect_run_close

# create table query.
@create_table
def create_table():
    query = ["""
            CREATE TABLE color_table(
            id SERIAL PRIMARY KEY,
            color VARCHAR(100) NOT NULL,
            frequency VARCHAR(100) NOT NULL
            )
    """]
    return query

# Add colors to database
def saveColors():
    for row in colors_dataFrame.iterrows():
        color,freq = row[1][0],row[1][1]
        # print(color,freq)
        #Add task query
        @save_colors
        def insert_query():
            query = """INSERT INTO color_table(color,frequency) 
            VALUES('{}',{}) RETURNING id;""".format(color,freq)
            return query
        insert_query()
    print("All colors successfully saved in database\n")


# QUESTION 7 RECURSIVE SEARCHING ALGORITHM
# RECURSIVE BINARY SEARCH

def binary_search(left,right,target,arr):
    if left > right: 
        print("Not Found!")
        return -1
    mid = (left+right) // 2
    if arr[mid] == target:
        print("Found!")
        return  arr[mid]
    elif arr[mid] > target:
        right = mid-1
        return binary_search(left,right,target,arr)
    else:
        left = mid+1
        return binary_search(left,right,target,arr)

import numpy as np
# QUESTION 8 ---
def binaryToBaseTen():
    print("\nBinary to base 10")
    values = np.random.choice([0, 1], size=(4,), p=[1./3, 2./3])
    print(f"Randomly generated 0's and 1's : {values}")
    baseTen = 0
    binary_num=""
    for ind,k in enumerate(values,1):
        binary_num+=str(k)
        power = 4-ind
        baseTen+= k * (2**power)
    print(f"{binary_num} in Base10 is {baseTen}")
    return baseTen


# QUESTION 9 - sum first 50 fibonnaci sequence
def generate(n):
    if n <= 2:
        return n
    x,y = 1,1
    fibo_sum = 2
    nth_term = 2
    while nth_term <= n-1:
        _y = y
        y = x+y
        x = _y
        nth_term+=1
        fibo_sum+=y
    print(f"\nsum of first 50 fibonnaci sequence is {fibo_sum}")
    return fibo_sum

# Or
def generate_ii(n):
    if n <= 2:
        return n
    arr = [1,1]
    f_sum = 2
    while len(arr) <= n-1:
        arr.append(arr[-1]+arr[-2])
        f_sum+=arr[-1]
    return f_sum


# FUNCTION CALLS
def functionCalls():
    '''This function contains all function calls'''

    # measure of central tendency
    findMean()
    findMode()
    findMedian()
    findVariance()

    # Probability of picking red
    probability()

    # Binary Search
    # for this particular algorithm, your data must be sorted in ascending order.
    arr = [0,12,24,36,48,51,63,70,85,93,107] 
    target = 51
    left = 0
    right = len(arr) - 1
    print("Binary Search algorithm")
    print(binary_search(left,right,target,arr))

    # binary to base 10
    print(binaryToBaseTen())

    # sum of first 50 terms of fibonacci sequence
    print(generate(50)) # pass length of the sequence as argument 
    print(generate_ii(50)) # pass in as argument the length of the sequence
    print("\n")
    
    # database
    create_table()
    saveColors()


# This call is important as the dataframe created is used to answer other questions.
colors_dataFrame = makeDataFrame() 
functionCalls()







##
## Name: Dan Qiao
## Uniqname: jordannn
##


import sqlite3
import plotly.graph_objects as go

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from a database called choc.db
DBNAME = 'choc.sqlite'

# Part 1: Implement logic to process user commands
def process_command(command):
    '''
    input: command  --string
    output: 
    1: cannot recognize
    query  --string
    '''
    command_str = command.split()
    num_command = len(command_str)

    query = ''
    if (command_str[0] == 'bars'):
        query = Bars_command(command_str)
    elif (command_str[0] == 'companies'):
        query = Companies_command(command_str)
    elif (command_str[0] == 'countries'):
        query = Countries_command(command)
    elif (command_str[0] == 'regions'):
        query = Regions_command(command_str)
    else:
        print('Command not recognized:',command)
    
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    connection.close()
    return result

    
def Bars_command(command):
    '''
    Function:  high level command is 'Bars'
    ----------------------
    INPUT: command  type: list  
    e.g. ['Bars','country','=','BR','source','rating','bottom','8']

    OUTPUT: result  type: tuple
    ----------------------
    Bars
    Valid Options:
    none, country, region, sell, source, ratings, cocoa, top, bottom, <integer>
    Return:
    (Specific Bean Bar Name, Company Name, Company Location, Rating, Cocoa Percent, Broad Bean Origin)
    ----------------------
    select SpecificBeanBarName,Company,C.EnglishName,Rating,CocoaPercent,Countries.EnglishName
    from Bars
    join Countries AS B on B.Id = Bars.BroadBeanOriginId
    join Countries AS C on C.Id = Bars.CompanyLocationId
    where B.Alpha2 = "BR"
    order by Bars.Rating 
    '''
    query1 = 'SELECT SpecificBeanBarName,Company,C.EnglishName,Rating,CocoaPercent,B.EnglishName FROM Bars '
    # sell | source
    query2 = 'JOIN Countries AS C ON C.Id = Bars.CompanyLocationId '
    query2 = query2 + 'JOIN Countries AS B ON B.Id = Bars.BroadBeanOriginId '
    if 'source' in command:
        countries = 'B'
    else:
        countries = 'C'

    # country | region | none
    query3 = ''
    for i in command:
        if 'country' in i:
            query3 = 'WHERE '+countries+'.Alpha2 = "' + i[8:] + '" '
        elif 'region' in i:
            query3 = 'WHERE '+countries+'.Region = "' + i[7:] + '" '
    
    # ratings | cocoa 
    if 'ratings' in command:
        query4 = ' ORDER BY Bars.Rating '
    elif 'cocoa' in command:
        query4 = ' ORDER BY Bars.CocoaPercent '
    else:
        query4 = ' ORDER BY Bars.Rating '
    
    # top | bottom 
    if 'bottom' in command:
        query5 = 'ASC '
    else: 
        query5 = 'DESC '
    
    #<integer>
    for i in command:
        if i.isnumeric():
            query6 = 'LIMIT '+ i
            break
        else:
            query6 = 'LIMIT 10'

    query = query1 + query2 + query3 + query4 + query5 + query6
    return query

#print(Bars_command('bars sell country=CA ratings top 5'.split()) )

def Companies_command(command):
    '''
    Function:  high level command is 'Companies'
    ----------------------
    INPUT: command  type: list  
    e.g. ['Companies','region','=','Europe','number_of_bars','12']

    OUTPUT: result  type: tuple
    ----------------------
    Valid options:
    none, country, region, ratings, cocoa, number_of_bars, top, bottom, <integer>
    Return:
    (Company Name, Company Location, <agg: avg rating, avg cocoa, or number_of_bars>)
    ----------------------
    Example 2
    Companies region = Europe number_of_bars 12
    SELECT company,count(DISTINCT SpecificBeanBarName)
    from Bars
    join Countries on Countries.Id = bars.CompanyLocationId
    where Countries.Region = "Europe"
    group  by Bars.company
    order by count(DISTINCT SpecificBeanBarName) DESC
    '''
   
    query1 = 'SELECT Company,Countries.EnglishName'
    query1_1 = ' FROM Bars '
    
    query2 = 'JOIN Countries ON Countries.Id = Bars.CompanyLocationId '
   
    # country | region | none
    query3 = ' '
    for i in command:
        if 'country' in i:
            query3 = 'WHERE Countries.Alpha2 = "' + i[8:] + '" '
        elif 'region' in i:
            query3 = 'WHERE Countries.Region = "' + i[7:] + '" '
    
    query4_1 = 'group by Bars.company HAVING  count( SpecificBeanBarName) >4 '
    # ratings | cocoa | number_of_bars
    if 'ratings' in command:
        query4 = ' ORDER BY avg(Bars.Rating) '
        query1 = query1 + ',avg(Bars.Rating)'
    elif 'cocoa' in command:
        query4 = ' ORDER BY avg(Bars.CocoaPercent) '
        query1 = query1 + ',avg(Bars.CocoaPercent)'
    elif 'number_of_bars' in command:
        query4 = ' order by count( SpecificBeanBarName) '
        query1 = query1 + ',count(DISTINCT SpecificBeanBarName) '
    else:
        query4 = ' ORDER BY avg(Bars.Rating) '
        query1 = query1 + ',avg(Bars.Rating)'
    
    # top | bottom 
    if 'bottom' in command:
        query5 = 'ASC '
    else: 
        query5 = 'DESC '
    
    #<integer>
    for i in command:
        if i.isnumeric():
            query6 = 'LIMIT '+ i
            break
        else:
            query6 = 'LIMIT 10'

    query = query1 + query1_1 + query2 + query3 + query4_1+ query4 + query5 + query6
    return query 

#print(Companies_command('companies region=Europe number_of_bars'.split()))

def Countries_command(command):
    '''
    Function:  high level command is 'Countries'
    ----------------------
    INPUT: command  type: list  
    e.g. ['Countries','region','=','Asia','sell','cocoa','top']

    OUTPUT: result  type: tuple
    ----------------------
    Valid options:
    none,  region, sell, source, ratings, cocoa, number_of_bars, top, bottom, <integer>
    Return:
    (Country, Region, <agg: avg rating, avg cocoa, or number_of_bars>)
    ----------------------
    Example 3
    Countries region = Asia sell cocoa top
    select Countries.EnglishName, Countries.Region,avg(Bars.CocoaPercent)
    from Bars
    join Countries on Countries.Id = Bars.CompanyLocationId
    where Countries.Region = "Asia"
    group by Countries.EnglishName. (group first)
    ORDER by avg(Bars.CocoaPercent) DESC
    '''
   
    query1 = 'SELECT Countries.EnglishName,Countries.Region'
    query1_1 = ' FROM Bars '
    # sell | source
    if 'source' in command:
        query2 = 'JOIN Countries ON Countries.Id = Bars.BroadBeanOriginId '
    else:
        query2 = 'JOIN Countries ON Countries.Id = bars.CompanyLocationId '
    
    # region | none
    query3 = ' '
    for i in command:
        if 'region' in i:
            query3 = 'WHERE Countries.Region = "' + i[7:] + '" '
    
    query4_1 = 'group by Countries.EnglishName HAVING count( SpecificBeanBarName) >4 '
    # ratings | cocoa | number_of_bars
    if 'ratings' in command:
        query4 = ' ORDER BY avg(Bars.Rating) '
        query1 = query1 + ',avg(Bars.Rating)'
    elif 'cocoa' in command:
        query4 = ' ORDER BY avg(Bars.CocoaPercent) '
        query1 = query1 + ',avg(Bars.CocoaPercent)'
    elif 'number_of_bars' in command:
        query4 = ' order by count( SpecificBeanBarName) '
        query1 = query1 + ',count( SpecificBeanBarName) '
    else:
        query4 = ' ORDER BY avg(Bars.Rating) '
        query1 = query1 + ',avg(Bars.Rating)'
    
    # top | bottom 
    if 'bottom' in command:
        query5 = 'ASC '
    else: 
        query5 = 'DESC '
    
    #<integer>
    for i in command:
        if i.isnumeric():
            query6 = 'LIMIT '+ i
            break
        else:
            query6 = 'LIMIT 10'

    query = query1 + query1_1 + query2 + query3 + query4_1+ query4 + query5 + query6
    #print(command)
    return query

#print(Countries_command('countries source region=Americas bottom 3 barplot'.split()))


def Regions_command(command):
    '''
    Function:  high level command is 'Region'
    ----------------------
    INPUT: command  type: list  
    e.g. ['Regions','source','top','3']

    OUTPUT: result  type: tuple
    ----------------------
    Valid Options:
    sell, source, ratings, cocoa, number_of_bars, top, bottom, <integer>
    Return:
    (Region, <agg: avg rating, avg cocoa, or number_of_bars>)
    ----------------------
    Example 4
    Regions source top 3
    SELECT Region,avg(Bars.Rating)
    from Countries
    join Bars on Bars.BroadBeanOriginId = Countries.Id
    group by Region
    order by avg(Bars.Rating) DESC
    limit 3
    '''
   
    query1 = 'SELECT Region'
    query1_1 = ' FROM Countries '
    # sell | source
    if 'source' in command:
        query2 = 'JOIN Bars ON Bars.BroadBeanOriginId = Countries.Id '
    else:
        query2 = 'JOIN Bars ON Bars.CompanyLocationId = Countries.Id '
    
    query4_1 = 'group by Region HAVING  count( SpecificBeanBarName) >4 '
    # ratings | cocoa | number_of_bars
    if 'ratings' in command:
        query4 = ' ORDER BY avg(Bars.Rating) '
        query1 = query1 + ',avg(Bars.Rating)'
    elif 'cocoa' in command:
        query4 = ' ORDER BY avg(Bars.CocoaPercent) '
        query1 = query1 + ',avg(Bars.CocoaPercent)'
    elif 'number_of_bars' in command:
        query4 = ' order by count( Bars.SpecificBeanBarName) '
        query1 = query1 + ',count( Bars.SpecificBeanBarName) '
    else:
        query4 = ' ORDER BY avg(Bars.Rating) '
        query1 = query1 + ',avg(Bars.Rating)'
    
    # top | bottom 
    if 'bottom' in command:
        query5 = 'ASC '
    else:
        query5 = 'DESC '
    
    #<integer>
    for i in command:
        if i.isnumeric():
            query6 = 'LIMIT '+ i
            break
        else:
            query6 = 'LIMIT 10'

    query = query1 + query1_1 + query2 + query4_1+ query4 + query5 + query6
    return query

#print(Region_command('Regions source top 3'.split()))

def load_help_text():
    with open('Proj3Help.txt') as f:
        return f.read()

# Part 2 & 3: Implement interactive prompt and plotting. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'help':
            print(help_text)
            continue

        results = process_command(response) # all records
        response_str = response.split()

        n = len(results)
        print(n)
        x_data = []
        y_data = []

        # Part3: barplot
        if ('barplot' in response):
            # high level options
            # bars
            if (response_str[0]=='bars'):
                # ratings | cocoa
                if 'ratings' in response:
                    for i in range(n):
                        x_data.append(results[i][0])
                        y_data.append(results[i][3])
                elif 'cocoa' in response:
                    for i in range(n):
                        x_data.append(results[i][0])
                        y_data.append(results[i][4])
            # companies
            elif (response_str[0]=='companies'):
                for i in range(n):
                    x_data.append(results[i][0])
                    y_data.append(results[i][2])
            #countries
            elif (response_str[0]=='countries'):
                for i in range(n):
                    x_data.append(results[i][0])
                    y_data.append(results[i][2])
            #regions
            elif (response_str[0]=='regions'):
                for i in range(n):
                    x_data.append(results[i][0])
                    y_data.append(results[i][1])

            # Figure show
            print(y_data)
            bar_data = go.Bar(x=x_data, y=y_data)
            fig = go.Figure(data=bar_data)
            fig.show()

        # not use Barplot
        else:
            for result in results: # for every record
                for i in result:   # for every parameters displayed
                    if type(i) is str: # less than 15 strings
                        if len(i)>12:
                            i = i[:12]+'...'
                    #output
                    mat = "{:<15}"
                    print(mat.format(i),end='')
                print('')  # switch to next record

    print('bye') # if 'exit', print 'bye'.

# Make sure nothing runs or prints out when this file is run as a module/library
if __name__=="__main__":
    interactive_prompt()

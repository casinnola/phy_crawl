import html5lib, os, glob
from bs4 import BeautifulSoup

dir_path = 'html_files'
results_path = 'html_files/modified/'

# Set a counter for each physician. This won't necessarily be their id, just a unique counter for each record here.
temp_id = 0

# Iterate through all html files in the directory
for file_name in glob.glob(os.path.join(dir_path, "*.html")):

    my_data = (file_name)
    soup = BeautifulSoup(open(my_data, "r").read(), 'html5lib')
    
    #print (temp_id)
    # Iterate through all img tags with the specific id value
    for i in soup.find_all('img', id='ctl00_ContentPlaceHolder2_ctl00_imgPhysician'):
        #in each iteration, i is the entire img tag, so calling it's src attribute will find the source value (the URL)
        photo_url = 'http://www.chnola.org' + i['src']
        
        ############
        # This conditional was to ignore the "thumnophoto.jpg".
        # I'm taking it out, but there does need to be some way of flagging those who don't have photos.
        ###
        #headshot_url = i['src']
        #if headshot_url == '/Physicians/images/thumbnophoto.jpg':
            #headshot_url = None
            #photo_url = None
        # This part can probably be simplified
        #if headshot_url is not None:
            #photo_url = 'http://www.chnola.org' + headshot_url
        #else:
            #print ('Photo url: No photo url')
        # End of conditional
        ############    
    
    
    for i in soup.find_all('h2', class_='physicians_moduleSubtitle2'):
        # Because the contents of this h2 tag contain more than just a single string, you need to call it using the stripped_strings generator. 
        for string in i.stripped_strings:
            name = string
                        
    for i in soup.find_all('div', class_='physicians_floatleft'):
        for string in i.stripped_strings:
            contact_info = string
            # NOTE: I know this isn't the way these lists should be done. This just plops everything into a string and outputs it without
            # regard for creating pairs of contentType & content (i.e., Phone Number = xxx, Fax Number = yyy, etc.
            
    list_spec = []
    
    for i in soup.find_all('div', id='divSpecialties'):
        for string in i.stripped_strings:
            # Check to see if the variable 'specialties' already exists. If it does, that means the loop has already run once and is adding > 1 value,
            #  so append a comma plus this value
            #if 'specialties' in locals():
                #specialties += '\n' + string
            #else:
                #specialties = string
            list_spec.append(string)

    
    
        #NOTE TO SELF: you have to recycle this repetitive stuff into functions. Figure out the actions that happen in every loop, or are repeated in different loops.
        
        
    # Write this physician's data into an html file. Alternatively, you can move the write function out of the loop altogether and create one aggregate file,
    # but that would require learning how to populate tuples with all of the collected data, accounting for the fact that some physicians will have more
    # and some less.
    
    results_file = os.path.splitext(results_path)[0] + 'record-' + str(temp_id) + '.html'
    # LOOK AT ME! All those time I got the error Can't convert 'int' object to str implicitly... DUH, you have to convert an int
    # to a string by using str(int)
    
    with open(results_file, 'w') as html_file:
        
        html_file.write ('<html>\n\n<body>\n\n')
        html_file.write ('<h2>ID # ' + str(temp_id) + '</h2>\n')
        html_file.write ('<h1>')
        html_file.write (name + '</h1>\n')
        if photo_url is not None:
            html_file.write ('<div style=\"display: block;\">\n\t<img src=\"' + photo_url + '\">\n</div>\n')
        html_file.write ('<h3>Contact info:</h3><pre>' + contact_info + '</pre>')
        html_file.write ('<h3>Specialties</h3>\n<ul>\n')
        # Iterate through the list of specialties, printing each one in a <li>
        # NOTE: this is going to be how you create the CSV file. Pay attention to what you did here.
        for i in list_spec:
            html_file.write ('\t<li>' + i)
            html_file.write ('</li>\n')
        html_file.write ('</ul>\n\n')
        html_file.write ('</body>\n\n</html>')
        
        
            
    # The last thing in the loop is to increment the temp_phys_id index by 1.
    temp_id += 1
    
    # TO DO: use regex to process the first & last names into separate variables,
    # decide on what format you want the data to be in to make it easier to upload to MySQL
    
    #Do you want to learn Python/MySQL? Or just use this Python script to process the data, then use PHP/MySQL to run the database?
#Font Book, standard font faces and sizes   
def FontBook(size = "medium", face = "standard"):
    
    FONT_SIZES = {'small': '10px', 'medium': '16px', 'large': '20px'}
    FONT_FACE = {'standard': 'sans-serif'}

    if (size in FONT_SIZES.keys()):
        fs = FONT_SIZES[size]
    else:
        fs = "{0}px".format(size)
    

    if (face in FONT_FACE.keys()):
        ff = FONT_FACE[face]
    else:
        ff = face
    
    fontval = "{0} {1}".format(fs, ff)
    return fontval



#Define specific colors by name here

#ColorBook.py
def ColorBook(value):
    colorBook = {}

    
    #Colors by color name
    colorBook['FMBlue'] = '#19354c'
    colorBook['BrightRed'] = '#ff2222'
    colorBook['Green'] = '#068c35'
    colorBook['Orange'] = 'Orange'

    #Colors by TFS State
    colorBook['Impediment'] = '#ff2222' #BrightRed
    colorBook['Committed'] = '#068c35' #Green
    colorBook['Backlog'] = '#c0c0c0' #Gray
    colorBook['Backlog 8.3.1'] = '#f0f0f0' #Light Gray
    colorBook['Demo to Product Owner'] = '#19354c' #FMBlue


    #Colors by TFS Severity
    colorBook['Critical'] = '#ff2222' #BrightRed
    colorBook['High'] = 'Orange' #Orange
    colorBook['Medium'] = '#068c35' #Green
    colorBook['Low'] = '#19354c' #FMBlue

    #Colors by Series Name
    colorBook['Customer Facing'] = '#ff2222' #BrightRed
    colorBook['All Others'] = 'Orange' 

    

    if (value in colorBook.keys()):
        return colorBook[value]
    else:
        return value # Color not in color book
    

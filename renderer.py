from bs4 import BeautifulSoup

f = file("example.svg", "r")


html_doc = f.read();
soup = BeautifulSoup(html_doc, 'html.parser')

for tag in soup.find_all():
    n = tag.name
    if(n == "polyline"):
        print "Poly"
    elif(n =="path"):
        print "Path"
    elif(n =="rect"):
        print "Rect"
        print int(tag['x']) + int(tag['y'])

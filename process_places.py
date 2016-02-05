"""
Process the lines of the places of intrest.
"""
def process(raw):
    places = []
    #Line by line processing
    for line in raw:
        entry = {}
        line = line.rstrip()
        #if there is a blank line
        if len(line) == 0:
            continue

        pieces = line.split(':')

        if len(pieces) == 2:
            entry['name'] = pieces[0]
            latlng = pieces[1].split(' ')
            try:
                entry['lat'] = float(latlng[0])
                entry['lng'] = float(latlng[1])
            except ValueError:
                print(latlng[0] + " " + latlng[1])
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) +
                "Split into |{}|".format("|".join(pieces)))

        places.append(entry)

    return places

"""
simple testing
"""
def main():
    f = open("data/places.txt")
    parsed = process(f)
    print(parsed)

if __name__ == "__main__":
    main()


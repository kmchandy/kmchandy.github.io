import sys

def make_module_from_parts(header, overlay, footer, links, body, module_name):
    
    with open(module_name, 'w') as outfile:

        outfile.write('<title>' + module_name + '</title>')
        outfile.write("\n")

        with open(header) as infile:
            outfile.write(infile.read())
        outfile.write("\n \n")

        outfile.write("<!-- Start Sidebar----------> \n \n")
        with open(links) as infile:
            list_of_links = infile.read().splitlines()

            for link_and_name in list_of_links:
                link, name = link_and_name.split('#')
                outfile.write(
                    '<a class="w3-bar-item w3-button w3-hover-black "')
                outfile.write("\n")
                outfile.write(
                    'href=' + '"' + link + '"' + ' > ' + '\n')
                outfile.write(name + "\n")
                outfile.write("</a>")
                outfile.write("\n")
        outfile.write("\n")
        outfile.write("</nav>")
        outfile.write("\n")
        outfile.write("<!-- End Sidebar---------->")
        outfile.write("\n \n")

        with open(overlay) as infile:
            outfile.write(infile.read())
        outfile.write("\n")

        with open(body) as infile:
            outfile.write(infile.read())
        outfile.write("\n")

        with open(footer) as infile:
            outfile.write(infile.read())
        outfile.write("\n")
    return

def make_module(frame, contents):
    print('frame ', frame)
    print('contents ', contents)
    with open(frame) as infile:
        header, overlay, footer = infile.read().split()
    with open(contents) as infile:
        links, body, module_name = infile.read().split()
    make_module_from_parts(
        header, overlay, footer, links, body, module_name)
    


if __name__ == "__main__":
    header, links, overlay, body, footer, module_name = sys.argv[1:]
    make_module_from_parts(header, links, overlay, body, footer, module_name)

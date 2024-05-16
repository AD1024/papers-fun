import pybtex.database
import json
import os
from pybtex.database import BibliographyData, Entry

with open('config.json') as fd:
    configs = json.load(fd)

# Adapted from https://github.com/m-niemeyer/m-niemeyer.github.io
def generate_person_html(persons, connection=" and "):
    s = ""
    for p in persons:
        string_part_i = ""
        for name_part_i in p.get_part('first') + p.get_part('last'): 
            if string_part_i != "":
                string_part_i += " "
            string_part_i += name_part_i
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s

def build_readme():
    with open(os.path.join('papers-fun', 'README.md'), 'w') as fd_readme:
        fd_readme.write('# Papers by fields\n\n')
        for field_config in configs:
            bibtex_file = field_config['bibtex']
            bib_data = pybtex.database.parse_file(bibtex_file)
            if len(bib_data.entries) == 0:
                continue
            field_name = field_config['field']
            print(f'Rendering {field_name}...')
            md_file = field_config['file']
            fp = os.path.join('papers-fun', md_file)
            fd_readme.write(f'- [{field_name}]({md_file})\n\n')
            with open(fp, 'w') as fd:
                fd.write(f'# {field_name}\n\n')
                fd.write(f'Go Back to [Catalog](README.md)\n\n')
                fd.write('(Sorted by year)\n\n')
                for key, entry in sorted(bib_data.entries.items(), key=lambda x: int(x[1].fields['year']), reverse=True):
                    # fd.write(f'- [{entry.fields["title"]}]({entry.fields["url"]}) ({entry.fields["year"]})\n')
                    cite = "<pre><code>"
                    cite += BibliographyData({key: entry}).to_string('bibtex')
                    # cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'])}" + "}, \n"
                    # for entr in ['title', 'year']:
                    #     cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
                    cite += """</pre></code>"""
                    fd.write(f"<details>"
                            f'<summary><a href="{entry.fields["url"]}">{entry.fields["title"]}</a> ({entry.fields["year"]})</summary>'
                            '<br>'
                            f'{cite}'
                            '</details>')

if __name__ == '__main__':
    build_readme()
    print('Done!')
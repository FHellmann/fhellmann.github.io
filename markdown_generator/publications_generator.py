import os

from scholarly import scholarly

# Retrieve the author's data, fill-in, and print
# Get an iterator for the author results
search_query = scholarly.search_author('Fabio Hellmann')
my_profile = list(filter(lambda author: author['scholar_id'] == '-WjvWTkAAAAJ', search_query))[0]
my_profile = scholarly.fill(my_profile)
# Take a closer look at the first publication
publications = [scholarly.fill(publication) for publication in my_profile['publications']]

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    "′": "'",
    "…": "...",
    "“": "''",
    "”": "''",
    "é": "e",
}


def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c, c) for c in text)


for idx, item in enumerate(publications):
    bib = item['bib']
    print(bib.keys())
    pub_title = bib['title']
    print(f'{idx + 1}: {pub_title}')
    cites_id = item['cites_id'][0] if 'cites_id' in item else idx + 1
    pub_year = bib['pub_year']
    authors = bib['author'].split(' and ')
    pub_date = f'{pub_year}-01-01'
    pub_abstract = bib['abstract']
    pub_conference = bib['conference'] if 'conference' in bib else bib['journal']
    pub_url = item['pub_url']
    publisher = f'{bib["publisher"]}, ' if "publisher" in bib else ""
    num_citations = item['num_citations']
    first_author_firstname = authors[0].split(' ')[0]
    first_author_lastname = authors[0].split(' ')[-1]
    citation = f'{first_author_lastname}, {first_author_firstname} et al. "{pub_title}." {pub_conference}. {publisher}{pub_year}'
    print(citation)
    md_filename = f"{pub_year}-{cites_id}.md"
    html_filename = f"{pub_year}-{cites_id}"

    ## YAML variables
    md = f"---\ntitle: \"{pub_title}\"\n"
    md += "collection: publications"
    md += f"\npermalink: /publication/{html_filename}"
    if len(str(pub_abstract)) > 5:
        md += f"\nabstract: \"{html_escape('.'.join(pub_abstract.split('.')[:4]))}\""
    md += f"\ndate: {pub_date}"
    md += f"\nvenue: '{html_escape(pub_conference)}'"
    if len(str(pub_url)) > 5:
        md += f"\npaperurl: '{pub_url}'"
    md += f"\ncitation: '{citation}'"
    md += "\n---"

    ## Markdown description for individual page
    if len(str(pub_abstract)) > 5:
        md += f"\n{html_escape(pub_abstract)}\n"
    if len(str(pub_url)) > 5:
        md += f"\n[Download paper here]({pub_url})\n"
    md += "\nRecommended citation: " + citation

    md_filename = os.path.basename(md_filename)
    with open("../_publications/" + md_filename, 'w') as f:
        f.write(md)

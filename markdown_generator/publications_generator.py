import os

from scholarly import scholarly

# Retrieve the author's data, fill-in, and print
# Get an iterator for the author results
search_query = scholarly.search_author('Fabio Hellmann')
my_profile = list(filter(lambda author: author['scholar_id'] == '-WjvWTkAAAAJ', search_query))[0]
my_profile = scholarly.fill(my_profile)
# Take a closer look at the first publication
publications = [scholarly.fill(publication) for publication in my_profile['publications']]
[print(f'{idx + 1}: {item["bib"]["title"]}') for idx, item in enumerate(publications)]

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
    pub_abstract = bib['abstract']
    pub_conference = bib['conference'] if 'conference' in bib else bib['journal']
    pub_url = item['pub_url']
    num_citations = item['num_citations']
    md_filename = f"{pub_year}-01-01-{cites_id}.md"
    html_filename = f"{pub_year}-01-01-{cites_id}"

    ## YAML variables
    md = f"---\ntitle: \"{pub_title}\"\n"
    md += "collection: publications"
    md += f"\npermalink: /publication/{html_filename}"
    if len(str(pub_abstract)) > 5:
        md += f"\nabstract: \"{html_escape(pub_abstract)}\""
    md += f"\ndate: {pub_year}"
    md += f"\nvenue: '{html_escape(pub_conference)}'"
    if len(str(pub_url)) > 5:
        md += f"\npaperurl: '{pub_url}'"
    md += f"\ncitation: '{num_citations}'"
    md += "\n---"

    ## Markdown description for individual page
    if len(str(pub_abstract)) > 5:
        md += f"\n{html_escape(pub_abstract)}\n"
    if len(str(pub_url)) > 5:
        md += f"\n[Download paper here]({pub_url})\n"

    # md += "\nRecommended citation: " + item.citation
    md_filename = os.path.basename(md_filename)
    print(md)
    with open("../_publications/" + md_filename, 'w') as f:
        f.write(md)

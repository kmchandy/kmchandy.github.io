"""
Test matching using sentence transformers.

"""
import requests
import string
import re
import json
import numpy as np
import pickle
import pprint
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup
from HTML_text import HTML_text_string


# Constants
model = SentenceTransformer('all-MiniLM-L6-v2')

website = 'https://kmchandy.github.io/'
table_of_contents_page = 'table_of_contents.html'
table_of_contents_url = website + table_of_contents_page

# Name of the file in which embeddings for sections are stored.
section_embeddings_file = 'section_embeddings_file.pkl'

# Name of the file in which texts for sections are stored.
section_texts_file = 'section_texts_file.json'

# NUM_PAGES is thenumber of pages for which embeddings are calculated.
NUM_PAGES = 2

# question is matched against sections in the text.
question = "What is an epoch?"



def get_html_soup_from_url(url: str):
  """Get page at url in Beautifulsoup form.

  """
  try:
    response_from_url = requests.get(url)
  except:
    # Error occurred. Skip this url
    # response_from_url.raise_for_status():
    return None
  html_soup_from_url = response_from_url.text
  return BeautifulSoup(html_soup_from_url, 'html.parser')


def matching_score(doc_0, doc_1):
    """
    Returns
    -------
    ndarray:
       similarity of encodings of doc_0 and doc_1
    """
    
    # 1. Specify model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 2. Calculate embeddings
    embeddings = model.encode([doc_0, doc_1])

    # 3. Calculate embedding similarities
    return model.similarity(embeddings, embeddings)


def get_embeddings_for_sections_in_webpage(url):
    """
    Partitions webpage into parts where each part
    is the text between <div id='SECTION'> to the matching
    </div>. A part is called a section.
    The function computes a model embedding for each section.

    Returns
    -------
    list 
         each element of list is a model embedding for a section.
    """
    #embeddings_for_sections = []
    page_soup = get_html_soup_from_url(url)
    
    # sections_soup is a list of <div id='SECTION'>
    # to matching </div>
    sections_soup = page_soup.find_all(id="SECTION")

    embeddings_for_sections = [
        model.encode(section_soup.text) for section_soup in sections_soup]



def get_page_url_list(table_of_contents_url):
    """gets list of page urls from table_of_contents_url

    Parameters
    ----------
    table_of_contents_url: url
       The url of the table of contents of the course
       The table of contents has a list of urls of 
       pages.

    Returns
    -------
    list
       A list of urls of pages in the table of contents.
    """
    table_of_contents_soup = get_html_soup_from_url(table_of_contents_url)

    # Each page has an anchor <a href=url>page name</a>
    # page_soup_list is a list starting with all anchors 'a'
    page_soup_list = table_of_contents_soup.find_all('a')

    # page_url_list is list of urls of pages in table_of_contents.
    # A page url is the url relative to the url of the website.
    # Each page url in table_of_contents_url is separated by 'href'
    # Each page url ends with .html, and starts with a letter.
    # Skip a link such as <a href="./cross_reference.html"> which
    #   starts with .
    page_url_list = []
    for page_soup in page_soup_list:
        page_url = page_soup['href']
        if page_url.endswith('html') and page_url[0].isalpha():
            page_url_list.append(website + page_url)
    return page_url_list
    

def get_sections_embedding_dict():
    """Creates json file containing embedding of each section.
    
    Notes
    -----
    The content of the course is listed in table_of_contents_url.
    table_of_contents_url is a url that has a list of page urls.
    Each page has a set of chunks. Chunks may overlap. We call
    chunks SECTIONS.
    A section is identified by <div id=SECTION>.
    Each section has an anchor <a name=section_name>, and each
    section has a url.
    This function determines the model embedding for each section
    and stores the embedding in sections_embedding_dict.
    The key of sections_embedding_dict is the section url
    and the value is the embedding.

    """
    # Get the list of page urls from  table of contents url
    page_url_list = get_page_url_list(table_of_contents_url)

    # Each page url has one or more sections.
    # The section url is page url + # + section name 
    # sections_embedding_dict[section_url] is
    # the embedding for the section with this section_url.
    # sections_text_dict[section_url] is
    # the text of the section with this section_url.
    sections_embedding_dict = dict()
    sections_text_dict = dict()

    # Limit the number of pages analyzed to NUM_PAGES.
    # count is used for that purpose.
    count = 0

    # Go through each page in table of contents.
    for page_url in page_url_list:

        # page_soup is the page in BeautifulSoup form.
        page_soup = get_html_soup_from_url(page_url)
        
        # If page url is not available then skip rest of loop.
        if not page_soup: continue

        # Each section is identified by a <div id="SECTION'>
        # sections_soup_list is list of sections on this page
        # in soup form.
        sections_soup_list = page_soup.find_all(id="SECTION")

        # count is used for debugging.
        # Stop after NUM_PAGES have been read.
        count += 1
        if count > NUM_PAGES:
            break

        # Go through each section on this page.
        for section_soup in sections_soup_list:
            
            # Each section has anchor <a name=section_name>
            section_name = section_soup.a['name']
            section_notes = section_soup.notes
            # print(f'section_notes is {section_notes}')
             
            # section_url is the pointer to the section
            section_url = page_url + '#' + section_name
             
            # Convert soup to plain text
            section_text = (section_soup.text)
             
            # Compute the embedding for this section.
            # The embedding is an ndarray.
            embedding_for_section_ndarray = model.encode(section_text)
            
            # Put the embedding and text for this section into dicts.
            #sections_embedding_dict[section_url] = embedding_for_section_list
            sections_embedding_dict[section_url] = embedding_for_section_ndarray
            sections_text_dict[section_url] = section_text
            
        # Finished putting embeddings and text for sections on this page into
        # sections_embedding_dict and sections_text_dict.

    # Finished going through pages in table of contents.
    
    # Clear files of embeddings and section texts.
    open(section_embeddings_file, 'w').close()
    open(section_texts_file, 'w').close()

    np.save(section_embeddings_file, sections_embedding_dict)
    # Store section embeddings in file
    with open(section_embeddings_file, 'wb') as file:
        pickle.dump(sections_embedding_dict, file)
    
    # Store section texts in file
    with open(section_texts_file, 'w') as f:
        json.dump(sections_text_dict, f)
               
        

def get_sections_that_match_query(question: str) -> str:
    """ Returns text by appending sections that best match the question
    
    Parameters
    ----------
    question: str
      The question that is matched against sections.

    Returns
    -------
       str
         The sections with similarity of at least MIN_SECTION_SIMILARITY
         are appended together in order, starting with highest similarity.
         The appending of sections stops after the number of characters in
         the appended text exceeds MAX_TEXT_LENGTH.
         The appended text is returned.
    """
    
    MIN_SECTION_SIMILARITY = 0.3
    MAX_TEXT_LENGTH = 2000

    # Get dict of section embeddings from the file.
    # A key of sections_embedding_dict is a section url
    # and the correspnding value is the embedding of that
    # section.
    with open(section_embeddings_file, 'rb') as file:
        sections_embedding_dict = pickle.load(file)

    # Get dict of section text from the file.
    # A key of sections_text_dict is a section url
    # and the correspnding value is the text of that
    # section.
    with open(section_texts_file, 'r') as text_file:
        sections_text_dict = json.load(text_file)

    # questions_embedding is the embedding of the question.
    model = SentenceTransformer('all-MiniLM-L6-v2')
    question_embedding = model.encode(question)

    # Create sections_similarity_dict where key of the dict
    # is a section url and the value is the similarity of the
    # section and the question.
    # Note: model.similarity returns a list of lists.
    # similarity[0][0] is a number.
    sections_similarity_dict = dict()
    for key_value in sections_embedding_dict.items():
        section_url, section_embedding = key_value
        similarity = model.similarity(question_embedding, section_embedding)
        sections_similarity_dict[section_url] = similarity[0][0]

    # sorted_sections_similarity_dict is a dict of
    # section_url: similarity sorted in decreasing similarity.
    sorted_sections_similarity_dict = {
        kv[0]: kv[1] for kv in
        sorted(sections_similarity_dict.items(),
                   key = lambda x: (-x[1], x[0]))}

    # text_length is the total length of the text of appended sections.
    text_length = 0
    # The function returns the text string: sections_with_high_similarity.
    sections_with_high_similarity=[]
    
    for key_value in sorted_sections_similarity_dict.items():
        section_url, section_similarity = key_value
        print(f'section is {section_url}, similarity is {section_similarity}')
        section_text = sections_text_dict[section_url]
        text_length += len(section_text)
        if section_similarity < MIN_SECTION_SIMILARITY: break
        sections_with_high_similarity.append(section_text)
        if text_length > MAX_TEXT_LENGTH: break

    print('passing text to LLM')
    pprint.pp(sections_with_high_similarity)

    
    

    

        

    

        


if __name__ == '__main__':
    get_sections_embedding_dict()
    get_sections_that_match_query(question="what is a channel?")
    """
    print (HTML_text_string)
    soup = BeautifulSoup(HTML_text_string, 'html.parser')
    sections_soup = soup.find_all(attrs={"id": "SECTION"})
    for section_soup in sections_soup:
        print(section_soup.get_text())
        print(section_soup.prettify(formatter="html"))
        print(section_soup['class'])
        print(section_soup.a['name'])

    
    #  Get embeddings for sections in the specified webpage.
    website = 'https://kmchandy.github.io/'
    chapter = 'ChannelSnapshots/'
    page = 'LogicalClocks.html'
    page_url = website + chapter + page
    test(page_url)
    #page_url = \
      #'https://kmchandy.github.io/DISTRIBUTED_SYSTEM_MODELS/BasicsStates.html'
    embeddings_for_sections =  \
      get_embeddings_for_sections_in_webpage(page_url)
    # Embedding for questions
    question = "can two steps have the same epoch?"
    embedding_for_question = model.encode(question)
    # Get similarity scores between question and each section
    print (f'question is {question}')
    for embedding_for_section in embeddings_for_sections:
        similarities = model.similarity(
            embedding_for_question, embedding_for_section)
        print (f'similarity is {similarities[0,0]:.2f}')
    """

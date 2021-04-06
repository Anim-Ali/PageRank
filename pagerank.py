import os
import random
import re
import sys
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #corpus =  {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    # list of links the page has
    page_list = corpus.get(page)
    no_of_pages = len(page_list)
    total_pages = len(corpus)
    prob_dict = {}
    # evenly set probability of choosing a page at random among all N possible pages
    random_prob = (1 - damping_factor) / total_pages
    # if there are no links in page, the page has links to all pages
    if no_of_pages == 0:
        for each_page in corpus:
            prob_dict[each_page] = (1/total_pages)
    else:
        for each_page in corpus:
            # if page is in the page list, calculate the probability
            if each_page in page_list:
                prob_dict[each_page] = ((damping_factor/no_of_pages) + random_prob)
            # else set probability to random probability
            else:
                prob_dict[each_page] = random_prob
    # return probability dictionary
    return prob_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # dictionary to store pagerank values
    pagerank_dict = {}
    # assign each page a rank of 1/N
    for each_page in corpus:
        pagerank_dict[each_page] = 1 / len(corpus)
    # select first sample page randomly
    page = random.choice(list(corpus.keys()))
    # loop to generate all samples
    for i in range(n):
        # call transition_model to get sample
        sample = transition_model(corpus, page, damping_factor)
        # for each page in sample dictionary
        for each_page in sample:
            # add probability of sample dict to the same page in pagerank dictionary
            pagerank_dict[each_page] += sample.get(each_page)
            # select next  page randomly
            if random.random() <= sample.get(each_page):
                page = each_page
    # normalize probability values
    for each_page in pagerank_dict:
        pagerank_dict[each_page] = pagerank_dict.get(each_page)/n
    # return pagerank dictionary
    return pagerank_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # dictionary to store PageRank values
    pagerank_dict = {}
    total_pages = len(corpus)

    # assign each page a rank of 1/N
    for each_page in corpus:
        pagerank_dict[each_page] = 1/total_pages

    # evenly set probability of choosing a page at random among all N possible pages
    randomProb = 1-damping_factor/total_pages

    # variable to calculate changes in rankvalue
    accuracy = 0.005

    # while change in rankvalue is less than 0.001
    while accuracy > 0.001:

        accuracy = -math.inf
        for each_page in pagerank_dict:

            # set of all pages that link to 'each_page'
            i_set = set()

            # get pages that has a link to 'each_page'
            for link_page in corpus:
                link_set = corpus.get(link_page)

                if each_page in link_set:
                    i_set.add(link_page)

                # if page has no links it has links to all pages
                if len(link_set) == 0:
                    i_set.add(link_page)

            summation = 0
            # loop through all pages that have a link to 'each_page'
            for every_page in i_set:

                # if 'every_page' has no outgoing links, divide prob by total pages
                if len(corpus.get(every_page)) == 0:
                    summation += pagerank_dict.get(every_page) / total_pages
                    # pass

                # else, divide prob by no of outgoing links
                else:
                    summation += pagerank_dict.get(every_page) / len(corpus.get(every_page))

            # calculate new page rank
            newPagerank = randomProb + (damping_factor * summation)

            # check accuracy
            accuracy = max(accuracy, abs(pagerank_dict[each_page] - newPagerank))

            # add new pagereank to dictionary
            pagerank_dict[each_page] = newPagerank

    # normalize the probability values, so that all values add upto 1
    dict_sum = 0

    for page in pagerank_dict:
        dict_sum += pagerank_dict.get(page)

    for page in pagerank_dict:
        pagerank_dict[page] = pagerank_dict.get(page) / dict_sum

    # return pagerank dictionary
    return pagerank_dict


if __name__ == "__main__":
    main()

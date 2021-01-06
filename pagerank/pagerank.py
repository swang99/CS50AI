import os
import random
import math
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    total_prob = 0
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
        total_prob += ranks[page]
    print("Sum of the probabilities: ", round(total_prob, 4))
    ranks = iterate_pagerank(corpus, DAMPING)
    total_prob = 0
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
        total_prob += ranks[page]
    print("Sum of the probabilities: ", round(total_prob, 4))


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
    distribution = {} 
    links = len(corpus[page])
    pgs = len(corpus)

    if links != 0:
        for pg in corpus:
            distribution[pg] = (1-damping_factor) / pgs 
        for pg in corpus[page]:  
            distribution[pg] += damping_factor / links
    else:
        for pg in corpus:
            distribution[pg] = 1/pgs
    
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    """
    sample_pr = {} 
    # add keys and placeholder weightings into dict
    for item in corpus:
        sample_pr[item] = 0
    # pick random first page
    page = random.choice(list(corpus)) 
    # update weightings
    for i in range(1, n+1):
        previous_sample = transition_model(corpus, page, damping_factor)  
        for page in sample_pr: 
            sample_pr[page] = (((i-1) * sample_pr[page]) + previous_sample[page]) / i
        page = random.choices(list(sample_pr.keys()), list(sample_pr.values()), k=1)[0]
    return sample_pr


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    iterate_pr = {}  # before iteration
    new_iterate_pr = {}  # after iteration
    close_enough = False  # before and after values close enough?
    N = len(corpus) 
    
    # add keys and initial PageRank 1/N
    for item in corpus:
        iterate_pr[item] = 1 / N

     # iterate through PageRank formula
    while close_enough == False:
        for page in iterate_pr:
            summation = float(0)
            for item in corpus:
                # If page has links, add summation in formula
                if page in corpus[item]:
                    summation += iterate_pr[item] / len(corpus[item])
                # If page has no links, link to any page
                if not corpus[item]:
                    summation += iterate_pr[item] / len(corpus)

            new_iterate_pr[page] = ((1 - damping_factor) / N) + damping_factor * summation

        close_enough = True
    
    # checking whether the difference before / after iteration is close enough
        for page in iterate_pr: 
            if not math.isclose(new_iterate_pr[page], iterate_pr[page], abs_tol=0.001):
                close_enough = False
            iterate_pr[page] = new_iterate_pr[page]

    return iterate_pr


if __name__ == "__main__":
    main()
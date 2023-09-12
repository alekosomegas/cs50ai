import os
import random
import re
import sys

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
    probability_distribution = {k: (1-damping_factor) * 1/len(corpus) for k in corpus}
    for link in corpus[page]:
        probability_distribution[link] += 1/len(corpus[page]) * damping_factor
    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = {k: 0 for k in corpus}
    starting_page = random.choice(list(corpus.keys()))
    for i in range(n):
        model = transition_model(corpus, starting_page, damping_factor)
        # choose one as random based on percentages for the next iteration
        starting_page = random.choices(
            [page for page in model.keys()],
            weights=[v for v in model.values()])[0]
        samples[starting_page] += 1
    return {k: v/n for (k, v) in samples.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = {k: 1/len(corpus) for k in corpus}
    page_refs = {k: [] for k in corpus}
    min_dif = 0.001

    for page in corpus:
        for ref, links in corpus.items():
            if ref == page:
                continue
            if page in links:
                page_refs[page].append(ref)

    while page_refs:
        for page, refs in page_refs.copy().items():
            prev = page_ranks[page]
            new = (1-damping_factor) / len(corpus) + damping_factor * sum([page_ranks[x] / len(corpus[x]) for x in refs])
            page_ranks[page] = new
            if abs(new - prev) < min_dif:
                page_refs.__delitem__(page)

    return page_ranks


if __name__ == "__main__":
    main()

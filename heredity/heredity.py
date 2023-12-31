import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    # # Check for proper usage
    # if len(sys.argv) != 2:
    #     sys.exit("Usage: python heredity.py data.csv")
    # people = load_data(sys.argv[1])

    people = load_data("data/family0.csv")

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    p = 1
    p_gene = None
    for person in people.values():
        num_of_genes = get_num_of_genes(person, one_gene, two_genes)
        print("PERSON: ", person, "   ", "NUM OF GENES: ", num_of_genes, "\n")

        if person["mother"] and person["father"]:
            num_of_genes_mother = get_num_of_genes(people.get(person["mother"]), one_gene, two_genes)
            num_of_genes_father = get_num_of_genes(people.get(person["father"]), one_gene, two_genes)

            print("NUM GENES MOTHER: ", num_of_genes_mother, "NUM GENES FATHER: ", num_of_genes_father, "\n")
            if num_of_genes == 0:
                p_gene = (1 - prop_inherit(num_of_genes_mother)) * (1 - prop_inherit(num_of_genes_father))
            elif num_of_genes == 1:
                p_gene = prop_inherit(num_of_genes_mother) * (1 - prop_inherit(num_of_genes_father)) + \
                    prop_inherit(num_of_genes_father) * (1 - prop_inherit(num_of_genes_mother))
            elif num_of_genes == 2:
                p_gene = prop_inherit(num_of_genes_mother) * prop_inherit(num_of_genes_father)

            print("PROB GENE: ", p_gene, "\n")
        else:
            p_gene = PROBS["gene"][num_of_genes]
            print("NO PARENT gene: ", p_gene)

        has_trait = False
        if person["name"] in have_trait:
            has_trait = True

        p_trait = PROBS["trait"][num_of_genes][has_trait]
        print("  trait: ", p_trait)

        p *= p_gene * p_trait

    print("FINAL P: ", p, "\n")
    return p


def prop_inherit(parent_num):
    c = 1 if parent_num == 0 else -1
    print("PROB OF INHERITANCE: ", parent_num / 2 + c * PROBS["mutation"], "\n")
    return parent_num / 2 + c * PROBS["mutation"]


def get_num_of_genes(person, one_gene, two_genes):
    num_of_genes = 0
    if person.get('name') in one_gene:
        num_of_genes = 1
    if person['name'] in two_genes:
        num_of_genes = 2
    return num_of_genes


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        total = 0
        for gene in probabilities[person]["gene"]:
            total += probabilities[person]["gene"][gene]
        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] = probabilities[person]["gene"][gene] / total

        total = 0
        for trait in probabilities[person]["trait"]:
            total += probabilities[person]["trait"][trait]
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] = probabilities[person]["trait"][trait] / total


if __name__ == "__main__":
    main()

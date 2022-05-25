from disjoint_set import DisjointSets


def main():

    djs = DisjointSets(size=60, path_compression=True)
    for ii in range(0, 60):
        djs.make_set(ii)

    for ii in range(0, 30):
        djs.union(ii, 2*ii)
    for ii in range(0, 20):
        djs.union(ii, 3*ii)
    for ii in range(0, 12):
        djs.union(ii, 5*ii)

    for ii in range(0, 60):
        djs.find(ii)

    max_rank = max(djs.rank)
    print(f"Max rank {max_rank}")


if __name__ == "__main__":
    main()

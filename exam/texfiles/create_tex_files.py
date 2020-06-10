import os



topicNumbers = list(range(9, 18))
topicTitles = [
              "Algorithms for percolation systems",
              "Percolation on small lattices",
              "Cluster number density in 1-d percolation",
              "Cluster size in 1-d percolation",
              r"Measurement and behavior of $P(p, L)$ and $\Pi(p, L)$",
              "The cluster number density",
              r"Finite size scaling of $\Pi(p, L)$",
              "Effective percolation threshold",
              "Subsets of the spanning cluster"
              ]

for i, num in enumerate(topicNumbers):
    filename = f"topic{topicNumbers[i]}.tex"
    outfile = open(filename, "w")
    outfile.write(r"\newpage" + "\n")
    outfile.write(r"\section{Topic " + str(topicNumbers[i]) + ": " + topicTitles[i] + "}\label{sec:" + "topic" + str(topicNumbers[i]) + "}")
    outfile.close()

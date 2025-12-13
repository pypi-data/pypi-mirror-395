"""
Title: Structural Polarization and Segregation Measures
Author: Onur Tuncay Bal
Date Created: 02.12.2024
Date Last Updated: 05.12.2025


Notes
-----

If you are using please cite the corresponding paper.


"""

from typing import List, Tuple, Set, Any, Dict, Union, Hashable
import numpy as np 
import warnings
import random

class Measurer:
    """
    A utility class for handling graph-based measurements with community structure.

    This class stores an edge list representation of a graph together with a node
    membership mapping and performs optional safety checks to ensure data consistency
    at initialization.

    Parameters
    ----------
    edgelist : List[Tuple[Hashable, Hashable]]
        A list of edges where each edge is represented as a tuple
        (source_node, target_node).
    membership : Dict[Hashable, Hashable]
        A dictionary mapping each node ID to its corresponding community or group ID.
    directed : bool, optional (default=True)
        If True, the graph is treated as directed; otherwise it is treated as undirected.
    safe_create : bool, optional (default=True)
        If True, perform consistency checks between the edgelist and the membership
        dictionary during initialization.

    Raises
    ------
    TypeError
        If any of the inputs are not of the expected types.
    ValueError
        If the consistency checks fail (e.g., missing membership for nodes in the edgelist).
    """

    def __init__(
        self,
        edgelist: List[Tuple],
        membership: Dict,
        directed: bool = True,
        safe_create: bool = True,
    ) -> None:

        if not isinstance(edgelist, list):
            raise TypeError("edgelist must be a list of (u, v) tuples.")

        if not all(isinstance(e, tuple) and len(e) == 2 for e in edgelist):
            raise TypeError(
                "Each element of edgelist must be a tuple of length 2: (source, target)."
            )

        if not isinstance(membership, dict):
            raise TypeError("membership must be a dictionary mapping node -> group.")

        if not isinstance(directed, bool):
            raise TypeError("directed must be a boolean.")

        if not isinstance(safe_create, bool):
            raise TypeError("safe_create must be a boolean.")


        self.edgelist: List[Tuple[Hashable, Hashable]] = edgelist.copy()
        self.membership: Dict[Hashable, Hashable] = membership.copy()
        self.directed: bool = directed
        self.safe_create: bool = safe_create


        if self.safe_create:
            nodes_in_edges = set()
            for u, v in self.edgelist:
                nodes_in_edges.add(u)
                nodes_in_edges.add(v)

            nodes_in_membership = set(self.membership.keys())

            missing = nodes_in_edges - nodes_in_membership
            if missing:
                raise ValueError(
                    f"The following nodes appear in the edgelist but are missing "
                    f"from the membership dictionary: {missing}"
                )
            
            unused = nodes_in_membership - nodes_in_edges
            if unused:
                raise ValueError(
                    f"The following nodes appear in the membership dictionary but "
                    f"do not occur in the edgelist: {unused}"
                )
            


        self.nodes = sorted({u for e in self.edgelist for u in e})
        self.n = len(self.nodes)
        self.m = len(self.edgelist)


    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"n={self.n}, "
            f"m={self.m}, "
            f"directed={self.directed}, "
            f"safe_create={self.safe_create}"
            f")"
        )
    
    def __identify_high_degree_nodes(
        self,
        partition_a: List[Any],
        partition_b: List[Any],
        influencer_count: float,
    ) -> Tuple[List[Any], List[Any]]:
        """
        Identify nodes with highest degrees from each partition.

        This is an internal helper for the a few functions.
        It is not part of the public API.
        """

        if not partition_a or not partition_b or influencer_count < 0:
            raise ValueError(
                "Invalid input: partitions must be non-empty and "
                "influencer_count must be non-negative."
            )


        degrees: Dict[Any, int] = {node: 0 for node in self.nodes}
        for u, v in self.edgelist:
            degrees[u] += 1
            degrees[v] += 1  

        degrees_a = {node: degrees[node] for node in partition_a}
        degrees_b = {node: degrees[node] for node in partition_b}

        count_a = count_b = influencer_count
        if influencer_count < 1:
            count_a = max(1, int(influencer_count * len(partition_a)))
            count_b = max(1, int(influencer_count * len(partition_b)))

        top_nodes_a = sorted(
            degrees_a.items(), key=lambda x: (-x[1], x[0])
        )[: int(count_a)]
        top_nodes_b = sorted(
            degrees_b.items(), key=lambda x: (-x[1], x[0])
        )[: int(count_b)]

        return [node for node, _ in top_nodes_a], [node for node, _ in top_nodes_b]

    def __detect_the_boundary_nodes(
        self,
    ) -> Tuple[List, List, List[Tuple]]:
        """
        Detect boundary nodes and edges between communities.
        This is not a part of public API
        Returns
        -------
        boundary_nodes : List
            Nodes that are on the community boundary.
        boundary_node_membership : List
            Community labels corresponding to ``boundary_nodes``.
        boundary_edges : List[Tuple]
            Edges that run across communities (endpoints in different groups).
        """


        boundary_edges: List[Tuple] = []
        for u, v in self.edgelist:
            if self.membership[u] != self.membership[v]:
                boundary_edges.append((u, v))


        boundary_node_candidates: Set = set()
        for u, v in boundary_edges:
            boundary_node_candidates.add(u)
            boundary_node_candidates.add(v)


        neighbors: Dict[Any, Set] = {node: set() for node in self.nodes}
        for u, v in self.edgelist:
            neighbors[u].add(v)
            neighbors[v].add(u)

        boundary_nodes_set: Set = set()
        for candidate in boundary_node_candidates:
            for nb in neighbors.get(candidate, []):
                if nb not in boundary_node_candidates:
                    boundary_nodes_set.add(candidate)
                    break

        boundary_nodes: List = list(boundary_nodes_set)
        boundary_node_membership: List = [self.membership[node] for node in boundary_nodes]

        return boundary_nodes, boundary_node_membership, boundary_edges


    def boundary_connectivity(self, verbose: bool = False) -> float:
        """
        Compute the boundary connectivity score.

        This measure evaluates, for each boundary node, how strongly it is
        connected to nodes outside the boundary (di) relative to:
        - nodes outside the boundary (di), and
        - other boundary nodes in *different* communities (db).

        The final score is centered by subtracting 0.5 and then averaged
        across all boundary nodes.

        Parameters
        ----------
        verbose : bool, optional (default=False)
            If True, print a summary of boundary and non-boundary nodes.

        Returns
        -------
        float
            Boundary connectivity score.
        """

        boundary_nodes, boundary_node_memberships, boundary_edges = (
            self.__detect_the_boundary_nodes()
        )

        if not boundary_nodes:
            return 0.0


        neighbors: Dict[Any, Set] = {node: set() for node in self.nodes}
        for u, v in self.edgelist:
            neighbors[u].add(v)
            neighbors[v].add(u)

        boundary_nodes_set: Set = set(boundary_nodes)
        scores: List[float] = []


        non_boundary_nodes: List = [
            node for node in self.nodes if node not in boundary_nodes_set
        ]

        for boundary_node in boundary_nodes:
            node_neighbors = neighbors.get(boundary_node, set())

            di = [nb for nb in node_neighbors if nb not in boundary_nodes_set]

            db = [
                nb
                for nb in node_neighbors
                if nb in boundary_nodes_set
                and self.membership[nb] != self.membership[boundary_node]
            ]

            score = (len(di) + 0.0001) / ((len(di) + len(db)) + 0.0001)
            scores.append(score)

        if verbose:
            print(
                f"Summary --- \n"
                f" Boundary Nodes:\n{boundary_nodes}\n"
                f" Non_Boundary_Nodes:\n{non_boundary_nodes}"
            )

        scores = [s - 0.5 for s in scores]
        return sum(scores) / len(scores)



    def freeman_segregation(self) -> float:
        """
        Calculate Freeman's Segregation Index.

        This uses the original formulation for two groups. The measure compares
        the proportion of between-group ties in the observed graph to the
        expected proportion under a random graph on the same node set where
        each dyad is equally likely.

        Interpretation
        --------------
        - ≈ 1  : extremely segregated (much fewer between-group ties than random)
        - ≈ 0  : segregation comparable to a random graph
        - < 0  : integration (more between-group ties than random)

        Notes
        -----
        Freeman's original measure is defined for undirected networks with
        exactly two groups. Here, if the embedded network is directed, the same
        formula is applied to the directed edge set and a warning is issued.

        References
        ----------
        Freeman, L. C. (1978). "On measuring systematic integration."
        Bojanowski, M., & Corten, R. (2014). "Measuring Segregation in Social Networks."
        """

        if self.directed:
            warnings.warn(
                "Freeman's segregation index is defined for undirected networks; "
                "the embedded network is directed, so the measure is applied to "
                "the directed edge set.",
                UserWarning,
                stacklevel=2,
            )

        n = self.n
        if n < 2:
            raise ValueError("Freeman's segregation index is undefined for n < 2.")


        node_index = {node: i for i, node in enumerate(self.nodes)}

        adj = np.zeros((n, n), dtype=int)
        for u, v in self.edgelist:
            i = node_index[u]
            j = node_index[v]
            adj[i, j] += 1
            if not self.directed:
                adj[j, i] += 1


        membership_arr = np.array([self.membership[node] for node in self.nodes])
        groups = np.unique(membership_arr)

        if groups.size != 2:
            raise ValueError(
                "Freeman's segregation index is defined for exactly two groups. "
                f"Found {groups.size} groups: {groups.tolist()}"
            )

        g0, g1 = groups[0], groups[1]

        group0_nodes = (membership_arr == g0)
        group1_nodes = (membership_arr == g1)

        n0 = group0_nodes.sum()
        n1 = group1_nodes.sum()

        if n0 == 0 or n1 == 0:
            raise ValueError(
                "Freeman's segregation index is undefined when one of the groups has size 0."
            )


        internal0 = adj[np.ix_(group0_nodes, group0_nodes)].sum() # Iner edges running within groups.
        internal1 = adj[np.ix_(group1_nodes, group1_nodes)].sum()

        total_connections = adj.sum()
        if total_connections == 0:
            raise ValueError(
                "Freeman's segregation index is undefined for graphs with no edges."
            )


        external_connections = total_connections - (internal0 + internal1) # I wonder if there is a faster way above 

        p = external_connections / total_connections
        
        number_of_possible_ties = n * (n - 1) # We normalize it with 2 for undirected below, for directed this already is working.
        pi = (2 * n0 * n1) / number_of_possible_ties # This is the number of ties that we would expect by chance

        if pi == 0:
            raise ValueError(
                "Freeman's segregation index is undefined when the expected "
                "proportion of external ties is zero (degenerate group sizes)."
            )

        return 1.0 - (p / pi)

    def segregation_matrix_index(
        self,
        individual_groups: bool = False,
    ) -> Union[Tuple[float, float], float]:
        """
        Fershtman's Segregation Matrix Index.

        This index is applicable to both directed and undirected graphs and is
        computed for two groups. In the original formulation, it returns a
        separate index for each group; optionally, their mean can be returned.

        Parameters
        ----------
        individual_groups : bool, optional (default=False)
            If True, return the segregation index for each group separately
            as a tuple (smi_group_a, smi_group_b).
            If False, return the mean of the two group indices.

        Raises
        ------
        ValueError
            If the graph does not have exactly two groups or if group sizes
            are too small for the index to be defined.

        Notes
        -----
        Original calculation returns a value for each group separately. If
        ``individual_groups`` is False, the function returns the mean of the
        two group indices.

        References
        ----------
        Fershtman (1997), "Cohesive Group Detection in a Social Network by
        the Segregation Matrix Index."
        """

        n = self.n
        if n < 2:
            raise ValueError(
                "Segregation Matrix Index is undefined for graphs with fewer than 2 nodes."
            )


        node_index = {node: i for i, node in enumerate(self.nodes)}


        adj = np.zeros((n, n), dtype=float)
        for u, v in self.edgelist:
            i = node_index[u]
            j = node_index[v]
            adj[i, j] += 1.0
            if not self.directed:
                adj[j, i] += 1.0

        membership_arr = np.array([self.membership[node] for node in self.nodes])
        groups = np.unique(membership_arr)

        if groups.size != 2:
            raise ValueError(
                "Segregation Matrix Index is defined for exactly two groups. "
                f"Found {groups.size} groups: {groups.tolist()}."
            )

        g_a, g_b = groups[0], groups[1]
        groupa_nodes = (membership_arr == g_a)
        groupb_nodes = (membership_arr == g_b)

        size_a = groupa_nodes.sum()
        size_b = groupb_nodes.sum()

        if size_a < 2 or size_b < 2:
            raise ValueError(
                "Segregation Matrix Index is undefined when any group has size < 2."
            )


        x_aa = adj[np.ix_(groupa_nodes, groupa_nodes)].sum()
        d_aa = x_aa / (size_a * (size_a - 1))

        x_bb = adj[np.ix_(groupb_nodes, groupb_nodes)].sum()
        d_bb = x_bb / (size_b * (size_b - 1))

        external_edges = adj[np.ix_(groupa_nodes, groupb_nodes)].sum()
        d_ab = external_edges / (size_a * size_b)

        if d_ab == 0:
            raise ValueError(
                "Segregation Matrix Index is undefined when there are no "
                "between-group ties (d_ab = 0)."
            )

        # Relative densities
        r_a = d_aa / d_ab
        r_b = d_bb / d_ab

        smi_a = (r_a - 1.0) / (r_a + 1.0)
        smi_b = (r_b - 1.0) / (r_b + 1.0)

        if individual_groups:
            return smi_a, smi_b
        return (smi_a + smi_b) / 2.0

    def krackhardt_ei(self, negative: bool = True) -> float:
        """
        Calculate Krackhardt's EI ratio with the network and membership embedded
        in the object.

        Parameters
        ----------
        negative : bool, optional (default=True)
            If False, return the original version of the EI index:
            values closer to 1 then indicate higher segregation (i.e. more
            internal than external ties).

        Returns
        -------
        float
            EI index (or its original version if ``negative=False``).

        Notes
        -----
        The EI index is defined as

            EI = (EL - IL) / (EL + IL),

        where:
        - EL is the number of external links (between different groups),
        - IL is the number of internal links (within the same group).

        EI approaches:
        - -1 when almost all ties are internal (strong segregation),
        -  0 when internal and external ties are balanced,
        -  1 when almost all ties are external (integration).
        
        If ``negative=True``, the returned value is ``-EI``, so higher values
        indicate more segregation. Please consider this while applying this
        measure.

        Reference
        ---------
        Krackhardt, D., & Stern, R. N. (1988). "Informal networks and
        organizational crises: An experimental simulation."
        """

        n = self.n
        if n == 0:
            raise ValueError("Krackhardt's EI index is undefined for an empty graph.")


        node_index = {node: i for i, node in enumerate(self.nodes)}


        adj = np.zeros((n, n), dtype=float)
        for u, v in self.edgelist:
            i = node_index[u]
            j = node_index[v]
            adj[i, j] += 1.0
            if not self.directed:
                adj[j, i] += 1.0


        membership_arr = np.array([self.membership[node] for node in self.nodes])


        same_group = membership_arr[:, None] == membership_arr[None, :]

        np.fill_diagonal(same_group, False)

        diff_group = ~same_group

        # Internal and external links
        internal_links = adj[same_group].sum()
        external_links = adj[diff_group].sum()

        denom = internal_links + external_links
        if denom == 0:
            raise ValueError(
                "Krackhardt's EI index is undefined when there are no ties in the graph."
            )

        ei = (external_links - internal_links) / denom
        if negative:
            ei = -ei

        return float(ei)

    def modularity_score(self) -> float:

        """
        Compute Newman–Girvan modularity score based on the membership
        embedded in the object (binary partition).

        This mirrors the behavior of:
            nx.community.modularity(G, [partition_a, partition_b])
        for an undirected simple graph with a binary partition.

        Returns
        -------
        float
            Modularity score, in [-0.5, 1].
 
        """


        if self.directed:
            warnings.warn(
                "modularity_score treats the graph as an undirected simple graph "
                "for the purpose of modularity",
                UserWarning,
                stacklevel=2,
            )

        n = self.n
        if n < 2:
            return 0.0


        node_index = {node: i for i, node in enumerate(self.nodes)}


        adj = np.zeros((n, n), dtype=float)
        for u, v in self.edgelist:
            i = node_index[u]
            j = node_index[v]
            if i == j:

                continue
            adj[i, j] = 1.0
            adj[j, i] = 1.0

        twom = adj.sum()
        if twom == 0:

            return 0.0

        degrees = adj.sum(axis=1)

        membership_arr = np.array([self.membership[node] for node in self.nodes])
        groups = np.unique(membership_arr)

        if groups.size != 2:
            raise ValueError(
                "modularity_score is currently implemented for a binary partition. "
                f"Found {groups.size} groups: {groups.tolist()}."
            )

        Q = 0.0
        for i in range(n):
            for j in range(n):
                if membership_arr[i] == membership_arr[j]:
                    Q += adj[i, j] - (degrees[i] * degrees[j] / twom)

        Q /= twom 
        return float(Q)

    def log_moodys_odds_ratio(self) -> float:
        """
        Calculate the log Moody's odds-ratio (Moody's ORWG) based on dyads.

        This follows the logic of `netseg::orwg()` for an undirected network:
        we consider unordered dyads (i < j) and compare the odds of a dyad
        being connected if it is within-group vs between-group.

        The 2×2 table is:

                        tie present    tie absent
            within        m_within1      m_within0
            between       m_between1     m_between0

        and we return:

            log( OR ) where
            OR = (m_within1 * m_between0) / (m_within0 * m_between1)

        Raises
        ------
        ValueError
            If the network is directed.
            If fewer than two groups are present.
            If the odds-ratio is undefined (some cells zero or negative).

        References
        ----------
        Moody (2001); Bojanowski & Corten (2014); netseg::orwg()
        """

        if self.directed:
            raise ValueError("Moody's odds-ratio (orwg) is defined for undirected networks.")

        n = self.n
        if n < 2:
            raise ValueError("Moody's odds-ratio is undefined for n < 2.")


        node_index = {node: i for i, node in enumerate(self.nodes)}

        adj = np.zeros((n, n), dtype=int)
        for u, v in self.edgelist:
            i = node_index[u]
            j = node_index[v]
            if i == j:
                continue  
            adj[i, j] = 1
            adj[j, i] = 1

        membership_arr = np.array([self.membership[node] for node in self.nodes])
        groups = np.unique(membership_arr)

        if groups.size < 2:
            raise ValueError(
                f"Moody's odds-ratio requires at least two groups; found {groups.size}."
            )


        m_within1 = 0  # within-group, tie present
        m_within0 = 0  # within-group, tie absent
        m_between1 = 0  # between-group, tie present
        m_between0 = 0  # between-group, tie absent

        for i in range(n):
            gi = membership_arr[i]
            for j in range(i + 1, n):
                gj = membership_arr[j]
                tie_present = adj[i, j] == 1

                if gi == gj:
                    if tie_present:
                        m_within1 += 1
                    else:
                        m_within0 += 1
                else:
                    if tie_present:
                        m_between1 += 1
                    else:
                        m_between0 += 1

        num = m_within1 * m_between0
        den = m_within0 * m_between1

        if num <= 0 or den <= 0:
            raise ValueError(
                "Moody's odds-ratio is undefined: some cells in the within/between "
                "× present/absent table are zero or negative."
            )

        return float(np.log(num / den))
    
    def random_walk_controversy(
        self,
        influencer_ratio: float,
        simulation_count: int,
        walks_per_simulation: int,
    ) -> float:
        """
        Compute polarization using the Random Walk Controversy (RWC) method.

        Parameters
        ----------
        influencer_ratio : float
            Fraction or count of nodes to mark as influencers in each partition.
            If < 1, treated as a fraction of partition size.
            If >= 1, treated as an absolute count.
        simulation_count : int
            Number of independent simulations to run.
        walks_per_simulation : int
            Number of random walks per simulation.

        Returns
        -------
        float
            Average Random Walk Controversy score across all simulations.

        Raises
        ------
        ValueError
            If the graph is directed.
            If the partition is not binary or one side is empty.
        """

        if self.directed:
            raise ValueError(
                "Random Walk Controversy is currently implemented for undirected graphs."
            )

        # Binary partition: membership == 0 vs membership == 1
        partition_a = [node for node in self.nodes if self.membership[node] == 0]
        partition_b = [node for node in self.nodes if self.membership[node] == 1]

        if not partition_a or not partition_b:
            raise ValueError(
                "RWC requires a binary partition with non-empty groups labelled 0 and 1."
            )

        influencers_a, influencers_b = self.__identify_high_degree_nodes(
            partition_a=partition_a,
            partition_b=partition_b,
            influencer_count=influencer_ratio,
        )

        influencers_a_set = set(influencers_a)
        influencers_b_set = set(influencers_b)


        neighbor_cache: Dict[Any, List[Any]] = {node: [] for node in self.nodes}
        for u, v in self.edgelist:
            neighbor_cache[u].append(v)
            neighbor_cache[v].append(u)  # undirected

        controversy_sum = 0
        partition_choices = (partition_a, partition_b)

        for _ in range(simulation_count):
            ll = rr = lr = rl = 0

            for _ in range(walks_per_simulation):
                side_idx = random.randint(0, 1)
                start_node = random.choice(partition_choices[side_idx])

                current = start_node
                while True:
                    neighbors = neighbor_cache.get(current, [])
                    if not neighbors:
                        raise ValueError(
                            f"Encountered isolated node '{current}' during random walk. The graph might not be connected."
                        )

                    next_node = random.choice(neighbors)

                    if next_node in influencers_a_set:
                        if side_idx == 0:
                            ll += 1
                        else:
                            rl += 1
                        break
                    elif next_node in influencers_b_set:
                        if side_idx == 0:
                            lr += 1
                        else:
                            rr += 1
                        break

                    current = next_node

            left_total = ll + rl
            right_total = lr + rr

            if left_total == 0:
                left_total = 1
            if right_total == 0:
                right_total = 1

            prob_ll = ll / left_total
            prob_rl = rl / left_total
            prob_lr = lr / right_total
            prob_rr = rr / right_total

            controversy_sum += prob_ll * prob_rr - prob_rl * prob_lr

        return controversy_sum / simulation_count

    def betweenness_controversy_js(self) -> float:
        """
        Compute Betweenness Centrality Controversy using Jensen–Shannon distance.

        This is a variant of Betweenness Centrality Controversy (BCC), where
        the original formulation uses Kullback–Leibler (KL) divergence between
        the edge-betweenness distributions of inter-group and intra-group edges.
        Here we instead use Jensen–Shannon distance, which is:

        - symmetric,
        - bounded (in [0, 1] with SciPy's implementation),
        - and numerically more stable than raw KL.

        Notes
        -----
        - Requires `igraph` for efficient edge betweenness computation.
        - Requires `scipy` for `scipy.spatial.distance.jensenshannon`.
        Both dependencies are imported lazily.

        Returns
        -------
        float
            Jensen–Shannon distance between inter- and intra-group
            edge-betweenness distributions.

        Raises
        ------
        ImportError
            If `igraph` or `scipy` are not installed when this method is called.
        ValueError
            If there are no inter-group or no intra-group edges, or if
            histogram construction fails (e.g., zero mass in one distribution).
        """


        try:
            import igraph as ig
        except ImportError as exc:
            raise ImportError(
                "betweenness_controversy_js requires the 'igraph' package for "
                "fast edge-betweenness computation. Please install python-igraph."
            ) from exc

        try:
            from scipy.spatial.distance import jensenshannon
        except ImportError as exc:
            raise ImportError(
                "betweenness_controversy_js requires SciPy "
                "(scipy.spatial.distance.jensenshannon). "
                "Please install scipy to use this measure."
            ) from exc


        n = self.n
        if n == 0:
            raise ValueError("Cannot compute BCC-JS on an empty graph.")

        node_index = {node: i for i, node in enumerate(self.nodes)}


        g = ig.Graph(directed=self.directed)
        g.add_vertices(n)
        ig_edges = [(node_index[u], node_index[v]) for (u, v) in self.edgelist]
        g.add_edges(ig_edges)

        membership_vec = [self.membership[node] for node in self.nodes]


        edge_btwns = g.edge_betweenness()
        ig_edgelist = g.get_edgelist()

        inter_edge_btws = []
        intra_edge_btws = []


        for idx, (u_id, v_id) in enumerate(ig_edgelist):
            if membership_vec[u_id] != membership_vec[v_id]:
                inter_edge_btws.append(edge_btwns[idx])
            else:
                intra_edge_btws.append(edge_btwns[idx])

        if not inter_edge_btws or not intra_edge_btws:
            raise ValueError(
                "Cannot compute BCC-JS: need at least one inter-group and one "
                "intra-group edge."
            )

        a = np.array(inter_edge_btws, dtype=float)
        b = np.array(intra_edge_btws, dtype=float)


        bins = np.histogram_bin_edges(np.hstack([a, b]), bins="auto")

        hist_a, _ = np.histogram(a, bins=bins, density=True)
        hist_b, _ = np.histogram(b, bins=bins, density=True)

        if hist_a.sum() == 0 or hist_b.sum() == 0:
            raise ValueError(
                "Cannot compute BCC-JS: one of the histograms has zero total mass."
            )

        hist_a /= hist_a.sum()
        hist_b /= hist_b.sum()

        jsd = jensenshannon(hist_a, hist_b)  
        return float(jsd)

    def dipole_polarization(
        self,
        influencer_ratio: float,
        max_iterations: int = 500,
        tolerance: float = 1e-5,
    ) -> float:
        """
        Computes Dipole Polarization index through polarity diffusion from
        influential nodes.

        Identifies influential nodes in each partition, assigns them polar
        values, and diffuses these values through the network until convergence.

        Parameters
        ----------
        influencer_ratio : float
            Fraction or count of nodes to mark as influencers.
        max_iterations : int, optional
            Maximum number of diffusion iterations (default: 500).
        tolerance : float, optional
            Convergence threshold for polarity changes (default: 1e-5).

        Returns
        -------
        float
            Dipole Polarization score in range [0, 1].
        """

        if self.directed:
            raise ValueError("Dipole polarization is defined for undirected networks.")


        partition_a = [node for node in self.nodes if self.membership[node] == 0]
        partition_b = [node for node in self.nodes if self.membership[node] == 1]

        if not partition_a or not partition_b:
            raise ValueError(
                "Dipole polarization requires two non-empty groups labelled 0 and 1."
            )


        influencers_a, influencers_b = self.__identify_high_degree_nodes(
            partition_a=partition_a,
            partition_b=partition_b,
            influencer_count=influencer_ratio,
        )


        node_list = list(self.nodes)
        node_indices = {node: idx for idx, node in enumerate(node_list)}

        polarities = np.zeros(len(node_list), dtype=float)

        for node in influencers_a:
            polarities[node_indices[node]] = -1.0
        for node in influencers_b:
            polarities[node_indices[node]] = 1.0

        influencer_set = set(influencers_a) | set(influencers_b)

        listener_indices = [
            node_indices[node]
            for node in node_list
            if node not in influencer_set
        ]


        neighbor_indices: Dict[int, List[int]] = {node_indices[node]: [] for node in node_list}
        for u, v in self.edgelist:
            iu = node_indices[u]
            iv = node_indices[v]
            neighbor_indices[iu].append(iv)
            neighbor_indices[iv].append(iu)

        influencer_a_indices = [node_indices[node] for node in influencers_a]
        influencer_b_indices = [node_indices[node] for node in influencers_b]

        new_polarities = polarities.copy()
        iterations = 0


        while iterations < max_iterations:
            
            for idx in listener_indices:
                neighbors = neighbor_indices[idx]
                total = sum(polarities[n] for n in neighbors) + polarities[idx]
                count = len(neighbors) + 1
                new_polarities[idx] = total / count

            
            for idx in influencer_a_indices:
                new_polarities[idx] = -1.0
            for idx in influencer_b_indices:
                new_polarities[idx] = 1.0


            if np.all(np.abs(polarities - new_polarities) <= tolerance):
                break

            polarities = new_polarities.copy()
            iterations += 1


        positive_mask = new_polarities > 0
        negative_mask = new_polarities < 0

        num_positive = np.sum(positive_mask)
        num_nodes = len(node_list)

        size_asymmetry = abs(2 * num_positive - num_nodes) / num_nodes

        mean_positive = (
            np.mean(new_polarities[positive_mask]) if num_positive > 0 else 0.0
        )
        mean_negative = (
            np.mean(new_polarities[negative_mask])
            if np.sum(negative_mask) > 0
            else 0.0
        )

        polarity_distance = abs(mean_positive - mean_negative) / 2.0

        return (1.0 - size_asymmetry) * polarity_distance


    def _benchmark(self):
        """
        Not for importing just to compare the measures with the previous implementations.
        But also can be used computing all polarization metrics at once ;)
        """

        results = {}

        results["RWC"] = self.random_walk_controversy(influencer_ratio=5,
                                                      simulation_count= 100,
                                                      walks_per_simulation=100)
        results["EI"] = self.krackhardt_ei()
        results["BCC"] = self.betweenness_controversy_js()
        results["BP"] = self.boundary_connectivity()
        results["DP"] = self.dipole_polarization(5)
        results['Q'] = self.modularity_score()
        results["SEG"] = self.segregation_matrix_index()
        results['FreemanSeg'] = self.freeman_segregation()
        results['log-Moodys'] = self.log_moodys_odds_ratio()


        return results


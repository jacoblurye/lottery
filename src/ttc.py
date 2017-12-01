"""Implements a variant of the Top Trading-Cycles algorithm.
"""

class TTC:
    """
        Run TTC on a list of students.
    """

    def __init__(self, students):
        self.students = students

    def run(self):
        """
            Do TTC.
        """
        # Initialize top preference graph
        graph = self._build_graph()

        while graph:
            
            # Find a cycle
            cycle = TTC._find_cycle(graph)

            # Trade along the cycle
            TTC._trade_on_cycle(cycle)

            # Build graph again
            graph = self._build_graph()


    def _build_graph(self):
        """
            Construct a top-preference graph of students.
        """
        graph = {}

        for student in self.students:
            tradable_courses = student.get_tradable_courses()
            # If the student has no tradable courses, they exit the market
            if not tradable_courses:
                continue


        return graph
    
    @staticmethod
    def _find_cycle(graph):
        """
            Using Tarjan's algorithm for finding Strongly Connected Components,
            find and return all trading cycles of student slots.
            With reference to: https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
        """

        ######### Helper
        def strongconnect(node, index, indexes, lowlinks, S, graph):
            indexes[node] = index
            lowlinks[node] = index
            index += 1
            S.append(node)

            children = graph[node]
            for child in children:
                if child not in indexes:
                    strongconnect(child, index, indexes, lowlinks, S, graph)
                    lowlinks[node] = min(lowlinks[node], lowlinks[child])
                elif child in S:
                    lowlinks[node] = min(lowlinks[node], indexes[child])

            if lowlinks[node] == indexes[node]:
                SCC = [node]
                nxt = S.pop()
                while nxt != node:
                    SCC.append(nxt)
                    nxt = S.pop()
                return SCC
        ######### End Helper

        # Bookkeeping
        S = []
        index = 0
        indexes = {}
        lowlinks = {}

        SCCs = []
        for student in graph.iterkeys():
            if student not in indexes:
                SCC = strongconnect(student, index, indexes, lowlinks, S, graph)
                SCCs.append(SCC)

        return SCCs


    @staticmethod
    def _find_cycle_old(graph):
        """
            Using Floyd's cycle detection algorithm, find and return a trading cycle of student slots.
            With reference to: https://en.wikipedia.org/wiki/Cycle_detection#Computer_representation
        """
        ### Begin Floyd
        initial = graph.itervalues().next()
        slow = graph[initial]
        fast = graph[slow]

        # Detect cycle
        while slow != fast:
            slow = graph[slow]
            fast = graph[graph[fast]]

        # Find cycle root node
        slow = initial
        while slow != fast:
            slow = graph[slow]
            fast = graph[fast]
        ### End Floyd

        # Collect the cycle
        cycle = [slow]
        slow = graph[slow]
        while slow != cycle[0]:
            cycle.append(slow)
            slow = graph[slow]
        
        return cycle

    @staticmethod
    def _trade_on_cycle(cycle):
        """
            Execute course spot trades along a given cycle.
        """
        l = len(cycle)
        # Trade course spots "backwards" along the cycle
        for i in xrange(l):
            recipient, _ = cycle[i]
            trader, new_spot = cycle[(i + 1) % l]

            # Make the trade
            recipient.offer_spot(new_spot)
            trader.remove_spot(new_spot)

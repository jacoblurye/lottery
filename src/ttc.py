"""Implements a variant of the Top Trading-Cycles algorithm.
"""
from copy import deepcopy
from random import choice
from collections import defaultdict

class TTC:
    """
        Run TTC on a list of students.
    """

    def __init__(self, students):

        # clear student enrollments
        for student in students:
            student.offered_courses.update(student.enrolled_courses)
            student.enrolled_courses.clear()

        self.students = students
        self.top_prefs = {}
        self.tradable_courses = {}
        self.orig_students = deepcopy(students)
        self.orig_util = sum([s.get_studycard_value() for s in students])

    def run(self):
        """
            Do TTC.
        """
        # Initialize top preference graph
        print "Building graph"
        graph = self._build_graph()

        while len(graph) > 1:

            # Find cycles
            print "Finding cycles"
            cycles = TTC._find_cycles(graph)

            # If there are no cycles, end TTC
            if not cycles:
                break

            # Trade along the cycles
            print "Trading along cycles"
            for cycle in cycles:
                self._trade_on_cycle(cycle)

            for student in self.students:
               student.get_studycard_destructive()

            # Build graph again
            for student in self.students:
                if student.has_room():
                    student.init_trading()

            print "Rebuilding graph"
            graph = self._build_graph()

        if self.orig_util > sum([s.get_studycard_value() for s in self.students]):
            self.students = self.orig_students


    def _build_graph(self):
        """
            Construct a top-preference graph of students.
        """
        graph = {}

        nodes = []
        for student in self.students:
            # Enroll in most preferable courses
            student._update_preferences()
            # If student has courses to trade and room in their studycard,
            # they enter this TTC round
            if student.has_room() and student.offered_courses:
                nodes.append(student)

        # Point students at other students who have their top choice course
        for student in nodes:
            children = [
                s for s in nodes
                if student.top_preference() in s.offered_courses
                and s != student
            ]
            if children:
                graph[student] = children
            else:
                for k, v in graph.iteritems():
                    if student in v:
                        v.remove(student)
                    graph[k] = v
                nodes.remove(student)

        # Make sure there are no students pointing at students who were removed above
        for student in nodes:
            try:
                sanitized_children = [
                    c for c in graph[student]
                    if c in graph
                    and student.top_preference() in c.offered_courses
                ]
                graph[student] = sanitized_children
            except KeyError:
                student.get_studycard_destructive()

        return graph

    def _most_preferable_achievable(self, student):
        """
            Get the most preferable course for a student that other students have.
        """
        self.top_prefs[student] = student.top_preference()

    
    @staticmethod
    def _find_cycles(graph):
        """
            Using Tarjan's algorithm for finding Strongly Connected Components,
            find and return all trading cycles of student slots.
            With reference to: https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
        """
        # Bookkeeping
        stack = []
        index = 0
        indexes = {}
        lowlinks = {}

        sccs = []
        for student in graph.iterkeys():
            if student not in indexes:
                scc = TTC._strongconnect(student, index, indexes, lowlinks, stack, graph)
                sccs.append(scc)

        print "Found ", len(sccs), " SCCs!"

        # Convert SCCs to cycles
        cycles = []
        for scc in sccs:
            if len(scc) > 1:
                cycle = TTC._scc_to_cycle_johnson(graph, scc)
            else:
                cycle = scc
            cycles.append(cycle)
        
        # Return cycles of length > 1 (since those self-loops are automatically resolved)
        out_cycles = []
        for cycle in cycles:
            if len(cycle) > 1:
                out_cycles.append(cycle)
        return out_cycles

    @staticmethod
    def _strongconnect(node, index, indexes, lowlinks, stack, graph):
        """
            Tarjan's helper function.
            With reference to: https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
        """
        indexes[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)

        if node not in graph:
            return

        children = graph[node]
        for child in children:
            if child not in indexes:
                TTC._strongconnect(child, index, indexes, lowlinks, stack, graph)
                lowlinks[node] = min(lowlinks[node], lowlinks[child])
            elif child in stack:
                lowlinks[node] = min(lowlinks[node], indexes[child])

        # If we're at an SCC root, build the SCC
        if lowlinks[node] == indexes[node]:
            SCC = [node]
            nxt = stack.pop()
            while nxt != node:
                SCC.append(nxt)
                nxt = stack.pop()
            return SCC

    @staticmethod
    def _scc_to_cycle_johnson(graph, scc):
        """
            Find all cycles in an SCC using Johnson's algorithm.
        """

        def unblock(node, block_set, block_map):
            if node not in block_set:
                return
            block_set.remove(node)
            for child in block_map[node]:
                unblock(child, block_set, block_map)
            del block_map[node]


        def findCycles(subgraph, root, curr, block_set=set(), block_map=defaultdict(set), stack=[]):
            stack.append(curr)
            block_set.add(curr)
            found_cycle = False
                        
            cycles = []
            for child in subgraph[curr]:
                # We found a cycle
                if child == root:
                    cycle = stack[::-1]
                    stack.pop()
                    cycles.append(cycle)
                    found_cycle = True 
                elif child not in block_set:
                    child_cycles = findCycles(subgraph, root, child, block_set, block_map, stack[:])
                    cycles.extend(child_cycles)
                    found_cycle = found_cycle or len(child_cycles)

            if found_cycle:
                unblock(curr, block_set, block_map)
            else:
                for child in subgraph[curr]:
                    block_map[child].add(curr)

            stack.pop()
            return cycles

        all_cycles = []
        while scc:
            subgraph = {}
            for node in scc:
                try:
                    subgraph[node] = [c for c in graph[node] if c in scc]
                except KeyError:
                    pass

            root = scc.pop()

            new_cycles = findCycles(graph, root, root)
            all_cycles.extend(new_cycles)

        # Randomly choose one of the longest cycles:
        if all_cycles:
            max_len = max([len(c) for c in all_cycles])
            max_cycs = [c for c in all_cycles if len(c) == max_len]
            return choice(max_cycs)

        return []


    def _trade_on_cycle(self, cycle):
        """
            Execute course spot trades along a given cycle.
        """

        l = len(cycle)

        # To conduct trades, we step backwards through the cycle
        cycle.reverse()

        # Trade course spots along the cycle
        for i in xrange(l):
            recipient = cycle[i]
            trader = cycle[(i + 1) % l]

            # Make the trade
            recipient.offer_spot(recipient.top_preference())
            trader.remove_spot(recipient.top_preference())

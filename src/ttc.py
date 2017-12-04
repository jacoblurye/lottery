"""Implements a variant of the Top Trading-Cycles algorithm.
"""

from tqdm import tqdm

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

    def run(self):
        """
            Do TTC.
        """

        for student in self.students:
            student.init_trading()

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

            # Enroll etc.
            # for student in self.students:
            #     print student, ":"
            #     print student.offered_courses, student.enrolled_courses
            #     student.get_studycard_destructive()
            #     print student.offered_courses, student.enrolled_courses
            #     print

            # Build graph again
            print "Rebuilding graph"
            graph = self._build_graph()


    def _build_graph(self):
        """
            Construct a top-preference graph of students.
        """
        graph = {}

        # Lock in students' top preferences
        nodes = []
        for student in self.students:
            student._update_preferences()
            if student.has_room() and student.offered_courses:
                nodes.append(student)

        # Point students at other students who have their top choice course
        for student in nodes:
            # print student, " has top pref ", student.top_preference()
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
                        # print "A"
                        v.remove(student)
                    graph[k] = v
                nodes.remove(student)

        # print graph
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
            cycle = TTC._scc_to_cycle_johnson(graph, scc)
            cycles.append(cycle)
        
        # Return cycles of length > 1 (since those self-loops are automatically resolved)
        return [c for c in cycles if len(c) > 1]
    
    @staticmethod
    def _scc_to_cycle(graph, scc):
        """
            Given a strongly connected component, return the longest cycle over that component.
        """
        scc_set = set(scc)
        get_children = lambda node: [c for c in graph[node] if c in scc_set]
        is_cycle = lambda path: path[0] in get_children(path[-1])


        ###### BEGIN HELPER
        # With reference to: https://stackoverflow.com/questions/29320556/finding-longest-path-in-a-graph
        def dfs(root, seen=[], path=None):
            if path is None:
                path = [root]
            
            seen.append(root)

            paths = []
            # print graph
            children = get_children(root)
            for child in children:
                if child not in seen:
                    new_path = path + [child]
                    paths.append(new_path)
                    paths.extend(dfs(child, seen[:], new_path))
            cycles = [p for p in paths if is_cycle(p)]
            print len(cycles)
            return cycles

        ###### END HELPER

        # Collect all paths from root to dest
        print "Finding all paths"
        cycles = dfs(graph.items()[0][0])
        print "Done"

        # Return the longest path
        if cycles:
            # Randomly choose between longest cycles
            # cycles = [p for p in paths if is_cycle(p)]
            max_len = max([len(c) for c in cycles])
            max_cycles = [c for c in cycles if len(c) == max_len]
            return choice(max_cycles)
        
        return []

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

            return cycles

        all_cycles = []
        while scc:
            subgraph = {}
            for node in scc:
                subgraph[node] = [c for c in graph[node] if c in scc]

            root = scc.pop()
            
            new_cycles = findCycles(subgraph, root, root)
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

        # cycle.reverse()

        # Trade course spots "backwards" along the cycle
        for i in xrange(l):
            recipient = cycle[i]
            trader = cycle[(i + 1) % l]

            slot = max(trader.offered_courses, key=recipient.preference_dict.get)
            
            # Make the trade
            recipient.offer_spot(slot)
            trader.remove_spot(slot)

            #print old_sc, recipient.get_studycard_destructive(), recipient.get_studycard_value()

"""Implements a variant of the Top Trading-Cycles algorithm.
"""

from tqdm import tqdm

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

    def run(self):
        """
            Do TTC.
        """
        # Initialize top preference graph
        print "Building graph"
        graph = self._build_graph()

        while graph:
            
            # Find cycles
            print "Finding cycles"
            cycles = TTC._find_cycles(graph)

            # If there are no cycles, end TTC
            if not cycles:
                break

            # Trade along the cycles
            print "Trading along cycles"
            for cycle in cycles:
                TTC._trade_on_cycle(cycle)

            # Build graph again
            print "Rebuilding graph"
            graph = self._build_graph()


    def _build_graph(self):
        """
            Construct a top-preference graph of students.
        """
        graph = {}

        # Build up list of student-course pairs
        # (A pair exists if student was allocated a spot in that course)
        student_course_list = []
        for student in self.students:
            tradable_courses = student.get_tradable_courses()

            # If the student has no tradable courses, they exit the market
            if not tradable_courses:
                continue

            for course in tradable_courses:
                student_course_list.append((student, course))
        
        # Point student-course pairs at pairs with their top (achievable) preference course
        for student_course in student_course_list:
            top_pref = student_course[0].top_preference()
            children = [s_c for s_c in student_course_list if s_c[1] == top_pref and s_c[0] != student_course[0]]
            graph[(student_course)] = children

        return graph
    
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
            print "Finding longest cycle"
            cycle = TTC._scc_to_cycle(graph, scc)
            print "Done."
            cycles.append(cycle)
        
        # Return cycles of length > 1 (since those self-loops are automatically resolved)
        return [c for c in cycles if len(c) > 1]

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
    def _scc_to_cycle(graph, scc):
        """
            Given a strongly connected component, return the longest cycle over that component.
        """
        scc_set = set(scc)
        get_children = lambda node: [c for c in graph[node] if c in scc_set]

        ###### BEGIN HELPER
        def get_all_paths(root, dest, path):
            # Add current root to path
            path.append(root)

            # We've reached the end of a path
            if root == dest:
                return path
            else:
                paths = []
                # Get all child paths
                for child in get_children(root):
                    if child not in path:
                        res = get_all_paths(child, dest, path)
                        if res:
                            paths.append(res)
                return paths
        ###### END HELPER

        # Collect all paths from root to dest
        paths = []
        root = scc[0]
        for dest in tqdm(scc[1:]):
            paths += get_all_paths(root, dest, [])
        
        # Return the longest path
        if paths:
            return max(paths, key=len)
        return []

    
    @staticmethod
    def _trade_on_cycle(cycle):
        """
            Execute course spot trades along a given cycle.
        """
        l = len(cycle)
        # Trade course spots "backwards" along the cycle
        for i in xrange(l):
            recipient, old_spot = cycle[i]
            trader, new_spot = cycle[(i + 1) % l]

            print (recipient, old_spot.subject + " " + str(old_spot.number)), " for ", (trader, new_spot.subject + " " + str(new_spot.number))

            # Make the trade
            recipient.offer_spot(new_spot)
            trader.remove_spot(new_spot)

            recipient.get_studycard_destructive()

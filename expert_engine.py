"""
expert_engine.py
================
Symbolic Reasoning Layer — The "Truth Engine"
Hybrid Expert-LLM Tutor for Accurate Self-Learning Support in Computer Science
Author: Arise Steven Samuel

Architecture Role:
    This module implements Layer 3 of the Hybrid Architecture described in Chapter 3.
    It uses the Experta library (Python port of CLIPS) which internally uses the
    Rete Algorithm for highly efficient pattern-matching against the knowledge base.

    Design Philosophy (Constraint-Based Modelling):
    Rather than enumerating every possible correct answer, this engine defines the
    CONSTRAINTS that every correct answer must satisfy. The engine validates a query
    against these constraints and returns verified ground-truth facts.

Domain:
    Python Programming
        - Variables & Data Types
        - Control Flow
        - Functions
        - Object-Oriented Programming (OOP)

    Data Structures
        - Arrays / Lists
        - Stacks
        - Queues
        - Linked Lists
        - Binary Trees & Binary Search Trees (BST)
        - Hash Tables

    Algorithms
        - Sorting Algorithms (Bubble, Merge, Quick Sort)
        - Searching Algorithms (Linear Search, Binary Search)
        - Big-O Notation & Complexity Analysis
        - Graph Theory & Graph Algorithms (BFS, DFS)

    Theory of Computation
        - Automata Theory (DFA, NFA, Finite Automata)

Fact Categories per topic:
    - definition   : what the concept is
    - property     : key characteristics and rules
    - step         : how it works / core logic
    - error        : common student mistakes and misconceptions
    - use_case     : when and why to use it
"""

# -----------------------------------------------------------------------------
# Python 3.10+ compatibility patch for experta
# experta uses collections.Callable which was removed in Python 3.10.
# This patch restores it before experta is imported.
# -----------------------------------------------------------------------------
import collections
import collections.abc

if not hasattr(collections, "Callable"):
    collections.Callable = collections.abc.Callable
if not hasattr(collections, "Mapping"):
    collections.Mapping = collections.abc.Mapping
if not hasattr(collections, "MutableMapping"):
    collections.MutableMapping = collections.abc.MutableMapping
if not hasattr(collections, "Iterable"):
    collections.Iterable = collections.abc.Iterable
if not hasattr(collections, "Iterator"):
    collections.Iterator = collections.abc.Iterator

from experta import *


# =============================================================================
# FACT DEFINITIONS
# =============================================================================

class TopicQuery(Fact):
    """
    Fired by the orchestrator when a student asks about a topic.
    Fields:
        name (str) : normalised topic name, e.g. 'functions'
    """
    pass


class TopicFact(Fact):
    """
    Asserted BY the engine's rules as verified ground truth.

    Fields:
        topic       (str) : topic name
        category    (str) : 'definition' | 'property' | 'step' |
                            'error' | 'use_case'
        rule_id     (str) : unique rule identifier for the UI trace panel
        description (str) : the verified, human-readable fact string
        priority    (int) : display order in Expert System Trace (lower = first)
    """
    pass


# =============================================================================
# KNOWLEDGE ENGINE
# =============================================================================

class CSKnowledgeEngine(KnowledgeEngine):

    # =========================================================================
    # PYTHON PROGRAMMING
    # =========================================================================

    # -------------------------------------------------------------------------
    # VARIABLES & DATA TYPES
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="variables"))
    def variables_definition(self):
        self.declare(TopicFact(
            topic="variables",
            category="definition",
            rule_id="VAR-DEF-01",
            description=(
                "DEFINITION — A variable in Python is a named reference (label) "
                "that points to an object stored in memory. Python is dynamically "
                "typed: a variable does not have a fixed type and can be reassigned "
                "to an object of a different type at any point."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="variables"))
    def variables_data_types(self):
        self.declare(TopicFact(
            topic="variables",
            category="property",
            rule_id="VAR-PROP-01",
            description=(
                "CORE DATA TYPES — "
                "int: whole numbers (e.g. x = 5). "
                "float: decimal numbers (e.g. x = 3.14). "
                "str: text, enclosed in single or double quotes (e.g. x = 'hello'). "
                "bool: True or False only — note the capital first letter. "
                "NoneType: represents the absence of a value (None). "
                "Use type(variable) to inspect the type of any variable at runtime."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="variables"))
    def variables_naming_rules(self):
        self.declare(TopicFact(
            topic="variables",
            category="property",
            rule_id="VAR-PROP-02",
            description=(
                "NAMING RULES (HARD CONSTRAINTS) — "
                "Variable names MUST start with a letter or underscore (_). "
                "They CANNOT start with a number. "
                "They CANNOT contain spaces or special characters (use underscores). "
                "They are case-sensitive: 'name', 'Name', and 'NAME' are three "
                "different variables. "
                "Reserved keywords (e.g. if, for, while, class) CANNOT be used as "
                "variable names."
            ),
            priority=3
        ))

    @Rule(TopicQuery(name="variables"))
    def variables_errors(self):
        self.declare(TopicFact(
            topic="variables",
            category="error",
            rule_id="VAR-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. Using a variable before assigning it causes a NameError. "
                "2. Confusing assignment (=) with equality comparison (==). "
                "   x = 5 assigns the value 5 to x. "
                "   x == 5 checks whether x is equal to 5 (returns True or False). "
                "3. Assuming integer division works like other languages: "
                "   in Python 3, 7 / 2 = 3.5 (float). Use 7 // 2 = 3 for integer division. "
                "4. Misspelling a variable name — Python is case-sensitive and will "
                "   raise a NameError rather than silently using the wrong variable."
            ),
            priority=4
        ))

    # -------------------------------------------------------------------------
    # CONTROL FLOW
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="control_flow"))
    def control_flow_definition(self):
        self.declare(TopicFact(
            topic="control_flow",
            category="definition",
            rule_id="CF-DEF-01",
            description=(
                "DEFINITION — Control flow refers to the order in which individual "
                "statements, instructions, or function calls are executed. "
                "Python provides three core control flow structures: "
                "conditional statements (if/elif/else), loops (for, while), "
                "and loop control keywords (break, continue, pass)."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="control_flow"))
    def control_flow_properties(self):
        self.declare(TopicFact(
            topic="control_flow",
            category="property",
            rule_id="CF-PROP-01",
            description=(
                "KEY RULES — "
                "INDENTATION IS SYNTAX: Python uses indentation (4 spaces standard) "
                "to define code blocks. Inconsistent indentation causes an "
                "IndentationError or silent logic errors. "
                "if/elif/else: only one branch executes per evaluation. "
                "for loop: iterates over a sequence (list, range, string, etc.). "
                "while loop: repeats as long as a condition is True — requires a "
                "termination condition to avoid an infinite loop. "
                "break: exits the loop immediately. "
                "continue: skips the rest of the current iteration and moves to the next."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="control_flow"))
    def control_flow_errors(self):
        self.declare(TopicFact(
            topic="control_flow",
            category="error",
            rule_id="CF-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. Off-by-one errors: range(n) produces 0 to n-1, NOT 0 to n. "
                "2. Infinite while loops: forgetting to update the loop variable "
                "   inside the loop body. "
                "3. Using = instead of == inside an if condition. "
                "4. Misunderstanding elif: once one branch is True, all remaining "
                "   elif and else branches are skipped entirely. "
                "5. Indentation errors: mixing tabs and spaces causes "
                "   TabError in Python 3."
            ),
            priority=3
        ))

    # -------------------------------------------------------------------------
    # FUNCTIONS
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="functions"))
    def functions_definition(self):
        self.declare(TopicFact(
            topic="functions",
            category="definition",
            rule_id="FN-DEF-01",
            description=(
                "DEFINITION — A function is a named, reusable block of code defined "
                "with the 'def' keyword. It optionally accepts parameters (inputs) "
                "and optionally returns a value using the 'return' statement. "
                "A function is defined once and can be called (invoked) multiple times."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="functions"))
    def functions_properties(self):
        self.declare(TopicFact(
            topic="functions",
            category="property",
            rule_id="FN-PROP-01",
            description=(
                "KEY RULES — "
                "SCOPE: Variables defined inside a function are LOCAL — they do not "
                "exist outside the function. Variables defined outside are GLOBAL. "
                "RETURN vs PRINT: 'return' sends a value back to the caller and ends "
                "the function. 'print' only displays to the console — it does NOT "
                "produce a usable value. A function without a return statement "
                "implicitly returns None. "
                "DEFAULT PARAMETERS: Parameters can have default values "
                "(e.g. def greet(name='Student')). "
                "They must always be placed AFTER non-default parameters."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="functions"))
    def functions_recursion(self):
        self.declare(TopicFact(
            topic="functions",
            category="property",
            rule_id="FN-PROP-02",
            description=(
                "RECURSION — A function that calls itself. "
                "HARD CONSTRAINT: Every recursive function MUST have a base case — "
                "a condition that stops the recursion. Without a base case, the "
                "function calls itself infinitely and raises a RecursionError "
                "(stack overflow). "
                "The base case is checked FIRST before the recursive call."
            ),
            priority=3
        ))

    @Rule(TopicQuery(name="functions"))
    def functions_errors(self):
        self.declare(TopicFact(
            topic="functions",
            category="error",
            rule_id="FN-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. Confusing return and print: storing the result of a function "
                "   that uses print instead of return gives None. "
                "2. Mutable default arguments: using a list or dict as a default "
                "   parameter (e.g. def fn(x=[])). The default is created ONCE and "
                "   shared across all calls — causes unexpected persistent state. "
                "   Use None as default and create the list inside the function. "
                "3. Calling a function before defining it in the same script. "
                "4. Forgetting parentheses when calling a function: "
                "   'my_function' references the function object; "
                "   'my_function()' actually calls it. "
                "5. Missing base case in recursion — causes RecursionError."
            ),
            priority=4
        ))

    # -------------------------------------------------------------------------
    # OBJECT-ORIENTED PROGRAMMING (OOP)
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="oop"))
    def oop_definition(self):
        self.declare(TopicFact(
            topic="oop",
            category="definition",
            rule_id="OOP-DEF-01",
            description=(
                "DEFINITION — Object-Oriented Programming (OOP) is a programming "
                "paradigm that organises code around objects — instances of classes. "
                "A class is a blueprint that defines attributes (data) and methods "
                "(behaviour). An object is a specific instance created from that blueprint. "
                "The four pillars of OOP are: Encapsulation, Inheritance, "
                "Polymorphism, and Abstraction."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="oop"))
    def oop_class_structure(self):
        self.declare(TopicFact(
            topic="oop",
            category="property",
            rule_id="OOP-PROP-01",
            description=(
                "CLASS STRUCTURE RULES — "
                "__init__: the constructor method, called automatically when an "
                "object is created. It initialises the object's attributes. "
                "self: refers to the current instance of the class. It MUST be the "
                "first parameter of every instance method. Python passes it automatically — "
                "you do not pass it manually when calling the method. "
                "Instance variables (self.x) belong to a specific object. "
                "Class variables are defined outside __init__ and shared across "
                "ALL instances of the class."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="oop"))
    def oop_inheritance(self):
        self.declare(TopicFact(
            topic="oop",
            category="property",
            rule_id="OOP-PROP-02",
            description=(
                "INHERITANCE — A child class inherits all attributes and methods "
                "of its parent class. Defined as: class Child(Parent). "
                "super().__init__() must be called in the child's __init__ to "
                "properly initialise the parent class attributes. "
                "METHOD OVERRIDING: A child class can redefine a method from the "
                "parent class. Python uses the child's version when called on "
                "a child instance (polymorphism)."
            ),
            priority=3
        ))

    @Rule(TopicQuery(name="oop"))
    def oop_errors(self):
        self.declare(TopicFact(
            topic="oop",
            category="error",
            rule_id="OOP-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. Forgetting 'self' as the first parameter in an instance method "
                "   causes a TypeError when the method is called. "
                "2. Confusing class variables and instance variables: modifying a "
                "   mutable class variable (e.g. a list) via one instance affects "
                "   ALL instances. "
                "3. Forgetting to call super().__init__() in a child class — the "
                "   parent's attributes are not initialised, causing AttributeError. "
                "4. Calling a method without parentheses returns the method object, "
                "   not the result. "
                "5. Confusing __init__ (initialiser) with __new__ (object creator) — "
                "   students almost always want __init__."
            ),
            priority=4
        ))

    # =========================================================================
    # DATA STRUCTURES
    # =========================================================================

    # -------------------------------------------------------------------------
    # ARRAYS / LISTS
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="lists"))
    def lists_definition(self):
        self.declare(TopicFact(
            topic="lists",
            category="definition",
            rule_id="LST-DEF-01",
            description=(
                "DEFINITION — A Python list is an ordered, mutable, dynamic array "
                "that can hold elements of mixed types. Lists are zero-indexed: "
                "the first element is at index 0, the last at index n-1 (or index -1). "
                "Lists are the Python equivalent of dynamic arrays in other languages."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="lists"))
    def lists_properties(self):
        self.declare(TopicFact(
            topic="lists",
            category="property",
            rule_id="LST-PROP-01",
            description=(
                "KEY OPERATIONS & COMPLEXITY — "
                "Access by index: O(1). "
                "Append to end (list.append): O(1) amortised. "
                "Insert at arbitrary position (list.insert): O(n) — shifts elements. "
                "Delete by index (del list[i]): O(n) — shifts elements. "
                "Search (in operator): O(n) — scans sequentially. "
                "Length (len): O(1). "
                "Slicing list[a:b]: O(b-a) — creates a new list."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="lists"))
    def lists_errors(self):
        self.declare(TopicFact(
            topic="lists",
            category="error",
            rule_id="LST-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. IndexError: accessing list[n] when the valid range is 0 to n-1. "
                "2. Shallow copy confusion: b = a does NOT copy the list — both "
                "   variables point to the same object. Use b = a.copy() or b = a[:]. "
                "3. Modifying a list while iterating over it — causes skipped elements "
                "   or unexpected behaviour. Iterate over a copy instead. "
                "4. Confusing list.append(x) (adds one item) with "
                "   list.extend([x, y]) (adds multiple items). "
                "5. Off-by-one in slicing: list[0:3] returns indices 0, 1, 2 — "
                "   the end index is exclusive."
            ),
            priority=3
        ))

    # -------------------------------------------------------------------------
    # STACKS
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="stacks"))
    def stacks_definition(self):
        self.declare(TopicFact(
            topic="stacks",
            category="definition",
            rule_id="STK-DEF-01",
            description=(
                "DEFINITION — A Stack is a linear data structure that follows the "
                "Last In, First Out (LIFO) principle: the last element added is the "
                "first element removed. Think of it as a stack of plates — you can "
                "only add or remove from the top."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="stacks"))
    def stacks_operations(self):
        self.declare(TopicFact(
            topic="stacks",
            category="step",
            rule_id="STK-STEP-01",
            description=(
                "CORE OPERATIONS — "
                "push(item): adds an item to the top of the stack. "
                "pop(): removes and returns the top item. "
                "peek() / top(): returns the top item WITHOUT removing it. "
                "is_empty(): returns True if the stack has no elements. "
                "In Python, a list implements a stack natively: "
                "push = list.append(item), pop = list.pop(). Both are O(1)."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="stacks"))
    def stacks_use_case(self):
        self.declare(TopicFact(
            topic="stacks",
            category="use_case",
            rule_id="STK-USE-01",
            description=(
                "USE CASES — "
                "Function call management (the call stack in any program). "
                "Undo/redo functionality in editors. "
                "Balanced parentheses / bracket checking. "
                "Depth-First Search (DFS) in graphs and trees. "
                "Expression evaluation and syntax parsing."
            ),
            priority=3
        ))

    @Rule(TopicQuery(name="stacks"))
    def stacks_errors(self):
        self.declare(TopicFact(
            topic="stacks",
            category="error",
            rule_id="STK-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. Stack underflow: calling pop() on an empty stack raises an "
                "   IndexError. Always check is_empty() before popping. "
                "2. Confusing LIFO (Stack) with FIFO (Queue) — they are opposites. "
                "3. Using list.pop(0) — this removes from the FRONT (index 0), "
                "   making it a Queue operation, NOT a Stack pop. "
                "   A Stack pop is always list.pop() with no argument (removes from end). "
                "4. Forgetting that peek() should not modify the stack."
            ),
            priority=4
        ))

    # -------------------------------------------------------------------------
    # QUEUES
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="queues"))
    def queues_definition(self):
        self.declare(TopicFact(
            topic="queues",
            category="definition",
            rule_id="QUE-DEF-01",
            description=(
                "DEFINITION — A Queue is a linear data structure that follows the "
                "First In, First Out (FIFO) principle: the first element added is the "
                "first element removed. Think of it as a real-world queue (line) — "
                "the person who arrives first is served first."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="queues"))
    def queues_operations(self):
        self.declare(TopicFact(
            topic="queues",
            category="step",
            rule_id="QUE-STEP-01",
            description=(
                "CORE OPERATIONS — "
                "enqueue(item): adds an item to the REAR of the queue. "
                "dequeue(): removes and returns the item from the FRONT. "
                "peek(): returns the front item without removing it. "
                "is_empty(): returns True if the queue has no elements. "
                "IMPLEMENTATION: Use collections.deque in Python — NOT a plain list. "
                "deque.append(item) enqueues to the right (rear). "
                "deque.popleft() dequeues from the left (front). Both are O(1). "
                "Using list.pop(0) for dequeue is O(n) — avoid it."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="queues"))
    def queues_errors(self):
        self.declare(TopicFact(
            topic="queues",
            category="error",
            rule_id="QUE-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. Implementing a queue with a plain list and using pop(0) — "
                "   this is O(n) and inefficient. Use collections.deque. "
                "2. Confusing enqueue (add to rear) with push (add to top of stack). "
                "3. Queue underflow: calling dequeue() on an empty queue. "
                "   Always check is_empty() first. "
                "4. Confusing FIFO (Queue) with LIFO (Stack)."
            ),
            priority=3
        ))

    # -------------------------------------------------------------------------
    # LINKED LISTS
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="linked_lists"))
    def linked_lists_definition(self):
        self.declare(TopicFact(
            topic="linked_lists",
            category="definition",
            rule_id="LL-DEF-01",
            description=(
                "DEFINITION — A Linked List is a linear data structure where each "
                "element (node) stores a value and a pointer (reference) to the next "
                "node in the sequence. Unlike arrays, nodes are NOT stored in "
                "contiguous memory — they are linked via pointers. "
                "The list is accessed via the HEAD node (first node). "
                "The last node's pointer is None (marks the end of the list)."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="linked_lists"))
    def linked_lists_properties(self):
        self.declare(TopicFact(
            topic="linked_lists",
            category="property",
            rule_id="LL-PROP-01",
            description=(
                "KEY OPERATIONS & COMPLEXITY — "
                "Access by index: O(n) — must traverse from head. "
                "Search: O(n). "
                "Insert at head: O(1). "
                "Insert at tail (with tail pointer): O(1). "
                "Insert at arbitrary position: O(n) to traverse, O(1) to insert. "
                "Delete node (given the node): O(1). "
                "Delete by value: O(n) to find, O(1) to remove. "
                "No random access — unlike arrays, you cannot do list[i] in O(1)."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="linked_lists"))
    def linked_lists_errors(self):
        self.declare(TopicFact(
            topic="linked_lists",
            category="error",
            rule_id="LL-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. Losing the HEAD reference: if head is overwritten without saving "
                "   the rest of the list, the entire list becomes inaccessible (memory leak). "
                "2. Not handling the None pointer at the tail — causes AttributeError "
                "   when traversing past the last node (e.g. current.next.next on tail). "
                "3. Forgetting to update pointers on both sides during insertion or "
                "   deletion — leaves the list in a broken, inconsistent state. "
                "4. Confusing singly linked list (one pointer: next) with doubly "
                "   linked list (two pointers: next and prev). "
                "5. Infinite loop during traversal: failing to advance the current "
                "   pointer (current = current.next) inside the loop."
            ),
            priority=3
        ))

    # -------------------------------------------------------------------------
    # BINARY TREES & BINARY SEARCH TREES
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="trees"))
    def trees_definition(self):
        self.declare(TopicFact(
            topic="trees",
            category="definition",
            rule_id="TR-DEF-01",
            description=(
                "DEFINITION — A Tree is a hierarchical, non-linear data structure "
                "consisting of nodes connected by edges. "
                "A Binary Tree is a tree where each node has AT MOST two children: "
                "a left child and a right child. "
                "A Binary Search Tree (BST) is a Binary Tree with an ordering property: "
                "for every node N, all values in N's LEFT subtree are LESS THAN N's value, "
                "and all values in N's RIGHT subtree are GREATER THAN N's value."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="trees"))
    def trees_traversals(self):
        self.declare(TopicFact(
            topic="trees",
            category="step",
            rule_id="TR-STEP-01",
            description=(
                "TREE TRAVERSALS — "
                "In-order (Left → Root → Right): visits nodes in ascending sorted "
                "order for a BST. "
                "Pre-order (Root → Left → Right): used to copy or serialise a tree. "
                "Post-order (Left → Right → Root): used to delete a tree or evaluate "
                "expression trees. "
                "Level-order (Breadth-First): visits nodes level by level using a Queue."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="trees"))
    def trees_complexity(self):
        self.declare(TopicFact(
            topic="trees",
            category="property",
            rule_id="TR-PROP-01",
            description=(
                "BST COMPLEXITY — "
                "Search, Insert, Delete: O(log n) average case for a balanced BST. "
                "WORST CASE: O(n) for a degenerate (skewed) BST — occurs when nodes "
                "are inserted in sorted order, producing a structure equivalent to a "
                "linked list. "
                "A balanced BST (e.g. AVL Tree, Red-Black Tree) guarantees O(log n) "
                "in all cases by self-balancing after insertions and deletions."
            ),
            priority=3
        ))

    @Rule(TopicQuery(name="trees"))
    def trees_errors(self):
        self.declare(TopicFact(
            topic="trees",
            category="error",
            rule_id="TR-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. Confusing a Binary Tree (structural definition: max 2 children) "
                "   with a BST (structural + ordering constraint). Not all Binary "
                "   Trees are BSTs. "
                "2. Assuming BST search is always O(log n) — it degrades to O(n) "
                "   on an unbalanced tree. "
                "3. Incorrect BST insertion: inserting a duplicate without a defined "
                "   policy (allow left, allow right, or discard) breaks the invariant. "
                "4. Forgetting to handle the None case in recursive traversal — "
                "   causes AttributeError when reaching a leaf node's child. "
                "5. Confusing in-order, pre-order, and post-order traversals — "
                "   only in-order gives sorted output for a BST."
            ),
            priority=4
        ))

    # -------------------------------------------------------------------------
    # HASH TABLES
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="hash_tables"))
    def hash_tables_definition(self):
        self.declare(TopicFact(
            topic="hash_tables",
            category="definition",
            rule_id="HT-DEF-01",
            description=(
                "DEFINITION — A Hash Table (Hash Map) is a data structure that maps "
                "keys to values using a hash function. The hash function converts a "
                "key into an integer index, which determines where the value is stored "
                "in an underlying array. In Python, the built-in dict is implemented "
                "as a hash table."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="hash_tables"))
    def hash_tables_properties(self):
        self.declare(TopicFact(
            topic="hash_tables",
            category="property",
            rule_id="HT-PROP-01",
            description=(
                "KEY PROPERTIES & COMPLEXITY — "
                "Insert, Search, Delete: O(1) average case. "
                "WORST CASE: O(n) when many keys hash to the same index (collision). "
                "COLLISION: occurs when two different keys produce the same hash index. "
                "Resolved by chaining (each slot holds a linked list of colliding entries) "
                "or open addressing (probe for the next available slot). "
                "Python dicts use open addressing with a compact hash table. "
                "Keys MUST be hashable (immutable): strings, integers, tuples are valid. "
                "Lists and dicts CANNOT be used as keys — they are mutable."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="hash_tables"))
    def hash_tables_errors(self):
        self.declare(TopicFact(
            topic="hash_tables",
            category="error",
            rule_id="HT-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. Using a mutable type (list, dict) as a dictionary key raises "
                "   TypeError: unhashable type. "
                "2. Assuming dictionary order is random — since Python 3.7, dicts "
                "   maintain insertion order. This is a language guarantee. "
                "3. KeyError: accessing a key that does not exist. "
                "   Use dict.get(key, default) to safely retrieve with a fallback. "
                "4. Confusing dict[key] (raises KeyError if missing) with "
                "   dict.get(key) (returns None if missing). "
                "5. Assuming O(1) is always guaranteed — worst-case O(n) exists "
                "   under heavy hash collisions."
            ),
            priority=3
        ))

    # =========================================================================
    # ALGORITHMS
    # =========================================================================

    # -------------------------------------------------------------------------
    # SORTING ALGORITHMS
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="sorting"))
    def sorting_definition(self):
        self.declare(TopicFact(
            topic="sorting",
            category="definition",
            rule_id="SORT-DEF-01",
            description=(
                "DEFINITION — Sorting is the process of arranging elements in a "
                "defined order (typically ascending or descending). "
                "Three fundamental sorting algorithms are: "
                "Bubble Sort (simple, O(n²)), "
                "Merge Sort (divide and conquer, O(n log n)), and "
                "Quick Sort (divide and conquer, O(n log n) average, O(n²) worst case). "
                "The choice of algorithm depends on dataset size, memory constraints, "
                "and whether stability is required."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="sorting"))
    def sorting_bubble(self):
        self.declare(TopicFact(
            topic="sorting",
            category="step",
            rule_id="SORT-STEP-01",
            description=(
                "BUBBLE SORT — "
                "Repeatedly compares adjacent pairs and swaps them if out of order. "
                "After each full pass, the largest unsorted element bubbles to its "
                "correct position at the end. "
                "TIME: Best O(n) with early-exit optimisation (already sorted). "
                "Average & Worst: O(n²). SPACE: O(1) in-place. "
                "STABILITY: Stable — equal elements preserve their original order. "
                "OPTIMISATION: Use a 'swapped' flag — if no swap occurs in a full "
                "pass, the array is already sorted and the algorithm terminates early."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="sorting"))
    def sorting_merge(self):
        self.declare(TopicFact(
            topic="sorting",
            category="step",
            rule_id="SORT-STEP-02",
            description=(
                "MERGE SORT — "
                "Divide and Conquer: recursively splits the array into halves until "
                "each subarray has one element, then merges them back in sorted order. "
                "TIME: O(n log n) in ALL cases — best, average, and worst. "
                "SPACE: O(n) — requires auxiliary arrays during the merge step. "
                "STABILITY: Stable — equal elements preserve their original order. "
                "BEST USE: Large datasets, external sorting, when stability is required."
            ),
            priority=3
        ))

    @Rule(TopicQuery(name="sorting"))
    def sorting_quick(self):
        self.declare(TopicFact(
            topic="sorting",
            category="step",
            rule_id="SORT-STEP-03",
            description=(
                "QUICK SORT — "
                "Divide and Conquer: selects a pivot, partitions the array so elements "
                "less than the pivot go left and greater go right, then recurses. "
                "TIME: Best & Average O(n log n). WORST CASE: O(n²) — occurs when "
                "the pivot is always the smallest or largest element (e.g. sorted input "
                "with naive first-element pivot). "
                "SPACE: O(log n) average for the call stack. "
                "STABILITY: NOT stable in standard form. "
                "MITIGATION: Use random pivot or median-of-three pivot selection "
                "to avoid worst-case degradation."
            ),
            priority=4
        ))

    @Rule(TopicQuery(name="sorting"))
    def sorting_errors(self):
        self.declare(TopicFact(
            topic="sorting",
            category="error",
            rule_id="SORT-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. Assuming Quick Sort is always O(n log n) — it degrades to O(n²) "
                "   on sorted or reverse-sorted input with naive pivot selection. "
                "2. Confusing Merge Sort space complexity — it requires O(n) auxiliary "
                "   space, unlike in-place sorts like Bubble Sort. "
                "3. Assuming Bubble Sort is always O(n²) — with the swapped flag "
                "   optimisation it achieves O(n) on already-sorted input. "
                "4. Confusing stability: Merge Sort is stable; Quick Sort is not. "
                "5. Using Bubble Sort on large datasets — O(n²) is impractical for n > 1000."
            ),
            priority=5
        ))

    # -------------------------------------------------------------------------
    # SEARCHING ALGORITHMS
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="searching"))
    def searching_definition(self):
        self.declare(TopicFact(
            topic="searching",
            category="definition",
            rule_id="SRCH-DEF-01",
            description=(
                "DEFINITION — Searching is the process of locating a specific element "
                "within a data structure. The two fundamental searching algorithms are: "
                "Linear Search: scans every element sequentially — works on any array. "
                "Binary Search: repeatedly halves the search space — requires a SORTED "
                "array. The choice between them depends entirely on whether the data "
                "is sorted."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="searching"))
    def searching_linear(self):
        self.declare(TopicFact(
            topic="searching",
            category="step",
            rule_id="SRCH-STEP-01",
            description=(
                "LINEAR SEARCH — "
                "Iterates through every element from index 0 to n-1. "
                "At each index i, compare array[i] to the target. "
                "If array[i] == target: return i (found). "
                "If the loop completes without a match: return -1 (not found). "
                "TIME: Best O(1) — target is first element. Average & Worst O(n). "
                "SPACE: O(1). No preprocessing required. "
                "SUITABLE FOR: Unsorted data, small datasets, single searches."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="searching"))
    def searching_binary(self):
        self.declare(TopicFact(
            topic="searching",
            category="step",
            rule_id="SRCH-STEP-02",
            description=(
                "BINARY SEARCH — "
                "HARD PREREQUISITE: The array MUST be sorted before Binary Search "
                "is applied. Applying it to an unsorted array produces undefined behaviour. "
                "ALGORITHM: Initialise low=0, high=n-1. While low <= high: "
                "compute mid = (low + high) // 2. "
                "If array[mid] == target: return mid. "
                "If array[mid] < target: set low = mid + 1 (discard left half). "
                "If array[mid] > target: set high = mid - 1 (discard right half). "
                "If loop exits: return -1 (not found). "
                "TIME: Best O(1). Average & Worst O(log n). SPACE: O(1) iterative."
            ),
            priority=3
        ))

    @Rule(TopicQuery(name="searching"))
    def searching_errors(self):
        self.declare(TopicFact(
            topic="searching",
            category="error",
            rule_id="SRCH-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. Applying Binary Search to an unsorted array — produces incorrect "
                "   results without raising an error, making this a silent bug. "
                "2. Assuming Binary Search is always O(1) — it is O(log n). "
                "3. Integer overflow in mid calculation: use mid = low + (high - low) // 2 "
                "   instead of (low + high) // 2 in languages with fixed integer sizes. "
                "   Python integers do not overflow, but the pattern is good practice. "
                "4. Off-by-one in boundary conditions: using low < high instead of "
                "   low <= high causes the algorithm to miss the last element."
            ),
            priority=4
        ))

    # -------------------------------------------------------------------------
    # BIG-O NOTATION & COMPLEXITY ANALYSIS
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="big_o"))
    def big_o_definition(self):
        self.declare(TopicFact(
            topic="big_o",
            category="definition",
            rule_id="BGO-DEF-01",
            description=(
                "DEFINITION — Big-O notation describes the upper bound of an "
                "algorithm's time or space requirements as a function of input size n. "
                "It characterises worst-case growth rate, ignoring constants and "
                "lower-order terms. "
                "Common classes (fastest to slowest): "
                "O(1) — Constant. O(log n) — Logarithmic. O(n) — Linear. "
                "O(n log n) — Linearithmic. O(n²) — Quadratic. "
                "O(2ⁿ) — Exponential. O(n!) — Factorial."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="big_o"))
    def big_o_properties(self):
        self.declare(TopicFact(
            topic="big_o",
            category="property",
            rule_id="BGO-PROP-01",
            description=(
                "KEY RULES — "
                "DROP CONSTANTS: O(2n) simplifies to O(n). "
                "DROP LOWER-ORDER TERMS: O(n² + n) simplifies to O(n²). "
                "WORST CASE: Big-O describes the worst case unless stated otherwise. "
                "SPACE COMPLEXITY: Big-O also applies to memory usage — "
                "an algorithm that creates an auxiliary array of size n has O(n) space. "
                "BEST / AVERAGE / WORST: An algorithm may have different complexities "
                "for each case. Quick Sort is O(n log n) average but O(n²) worst case."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="big_o"))
    def big_o_examples(self):
        self.declare(TopicFact(
            topic="big_o",
            category="use_case",
            rule_id="BGO-USE-01",
            description=(
                "COMMON ALGORITHM COMPLEXITIES — "
                "O(1): array index access, hash table lookup (average). "
                "O(log n): Binary Search, balanced BST operations. "
                "O(n): Linear Search, single array traversal. "
                "O(n log n): Merge Sort, Quick Sort (average), Heap Sort. "
                "O(n²): Bubble Sort, Selection Sort, Insertion Sort (worst case). "
                "O(2ⁿ): naive recursive Fibonacci, brute-force subset enumeration. "
                "RULE OF THUMB: For n = 1,000,000 — O(n log n) is fast; "
                "O(n²) is too slow for real-time applications."
            ),
            priority=3
        ))

    @Rule(TopicQuery(name="big_o"))
    def big_o_errors(self):
        self.declare(TopicFact(
            topic="big_o",
            category="error",
            rule_id="BGO-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. Confusing best-case with worst-case: Binary Search is O(1) best "
                "   case but O(log n) worst case — stating O(1) without qualification "
                "   is incorrect. "
                "2. Not dropping constants: O(3n) is NOT a valid Big-O class — "
                "   simplify to O(n). "
                "3. Confusing time complexity with space complexity — an algorithm "
                "   can be O(n) time but O(1) space (e.g. Linear Search). "
                "4. Assuming nested loops always mean O(n²) — only true if both "
                "   loops iterate n times. A loop running log n times inside an "
                "   n-loop gives O(n log n)."
            ),
            priority=4
        ))

    # -------------------------------------------------------------------------
    # GRAPH THEORY & ALGORITHMS
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="graphs"))
    def graphs_definition(self):
        self.declare(TopicFact(
            topic="graphs",
            category="definition",
            rule_id="GRP-DEF-01",
            description=(
                "DEFINITION — A Graph is a non-linear data structure consisting of "
                "a set of vertices (nodes) connected by edges. "
                "DIRECTED graph: edges have a direction (A → B does not imply B → A). "
                "UNDIRECTED graph: edges have no direction (A — B implies both directions). "
                "WEIGHTED graph: each edge carries a numerical value (weight/cost). "
                "UNWEIGHTED graph: all edges are equal. "
                "A graph with no cycles is called a DAG (Directed Acyclic Graph). "
                "Trees are a special case of graphs — connected, undirected, with no cycles."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="graphs"))
    def graphs_representation(self):
        self.declare(TopicFact(
            topic="graphs",
            category="property",
            rule_id="GRP-PROP-01",
            description=(
                "GRAPH REPRESENTATION — "
                "ADJACENCY MATRIX: a 2D array where matrix[i][j] = 1 if an edge "
                "exists between vertex i and vertex j. Space: O(V²). "
                "Best for dense graphs (many edges). "
                "ADJACENCY LIST: each vertex stores a list of its neighbours. "
                "Space: O(V + E) where V = vertices, E = edges. "
                "Best for sparse graphs (few edges). "
                "In Python, an adjacency list is typically implemented as a "
                "dictionary of lists: graph = {node: [neighbours]}."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="graphs"))
    def graphs_traversals(self):
        self.declare(TopicFact(
            topic="graphs",
            category="step",
            rule_id="GRP-STEP-01",
            description=(
                "GRAPH TRAVERSALS — "
                "BFS (Breadth-First Search): explores all neighbours at the current "
                "depth before moving deeper. Uses a QUEUE. "
                "Time: O(V + E). Finds shortest path in unweighted graphs. "
                "DFS (Depth-First Search): explores as far as possible along each "
                "branch before backtracking. Uses a STACK (or recursion). "
                "Time: O(V + E). Used for cycle detection, topological sorting, "
                "and connected component identification. "
                "VISITED SET: Both BFS and DFS require a visited set to avoid "
                "processing the same node twice in graphs with cycles."
            ),
            priority=3
        ))

    @Rule(TopicQuery(name="graphs"))
    def graphs_errors(self):
        self.declare(TopicFact(
            topic="graphs",
            category="error",
            rule_id="GRP-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. Forgetting the visited set in BFS/DFS — causes infinite loops "
                "   in graphs with cycles. "
                "2. Confusing BFS and DFS data structures: BFS uses a Queue (FIFO); "
                "   DFS uses a Stack (LIFO) or recursion. "
                "3. Assuming BFS finds the shortest path in weighted graphs — "
                "   BFS only guarantees shortest path in UNWEIGHTED graphs. "
                "   Use Dijkstra's algorithm for weighted graphs. "
                "4. Confusing trees with graphs: all trees are graphs, but not all "
                "   graphs are trees. Trees have no cycles and are fully connected."
            ),
            priority=4
        ))

    # =========================================================================
    # THEORY OF COMPUTATION
    # =========================================================================

    # -------------------------------------------------------------------------
    # AUTOMATA THEORY
    # -------------------------------------------------------------------------

    @Rule(TopicQuery(name="automata"))
    def automata_definition(self):
        self.declare(TopicFact(
            topic="automata",
            category="definition",
            rule_id="AUT-DEF-01",
            description=(
                "DEFINITION — Automata Theory is the study of abstract computational "
                "machines (automata) and the problems they can solve. "
                "A Finite Automaton (FA) is the simplest model — a machine with a "
                "finite number of states that reads an input string one symbol at a time "
                "and either accepts or rejects it. "
                "Two types exist: "
                "DFA (Deterministic Finite Automaton): for each state and input symbol, "
                "exactly ONE transition is defined. "
                "NFA (Non-deterministic Finite Automaton): for each state and input symbol, "
                "ZERO or MORE transitions may exist, including epsilon (ε) transitions "
                "that consume no input."
            ),
            priority=1
        ))

    @Rule(TopicQuery(name="automata"))
    def automata_dfa(self):
        self.declare(TopicFact(
            topic="automata",
            category="property",
            rule_id="AUT-PROP-01",
            description=(
                "DFA — FORMAL DEFINITION: A DFA is a 5-tuple (Q, Σ, δ, q₀, F) where: "
                "Q = finite set of states. "
                "Σ = finite input alphabet. "
                "δ: Q × Σ → Q = transition function (maps state + symbol → next state). "
                "q₀ ∈ Q = initial (start) state. "
                "F ⊆ Q = set of accept (final) states. "
                "A DFA accepts a string if, after reading all input symbols starting "
                "from q₀, the machine ends in a state that belongs to F. "
                "A DFA rejects a string if it ends in a non-accept state or if no "
                "valid transition exists for a given symbol."
            ),
            priority=2
        ))

    @Rule(TopicQuery(name="automata"))
    def automata_nfa(self):
        self.declare(TopicFact(
            topic="automata",
            category="property",
            rule_id="AUT-PROP-02",
            description=(
                "NFA — KEY PROPERTIES: "
                "An NFA is also a 5-tuple (Q, Σ, δ, q₀, F) but the transition "
                "function is δ: Q × (Σ ∪ {ε}) → P(Q), mapping to a POWER SET of states. "
                "An NFA accepts a string if AT LEAST ONE possible computation path "
                "ends in an accept state. "
                "EQUIVALENCE: Every NFA can be converted to an equivalent DFA using "
                "the subset construction algorithm. DFAs and NFAs recognise exactly "
                "the same class of languages — the Regular Languages. "
                "EPSILON TRANSITIONS (ε): Allow the machine to change state without "
                "consuming any input symbol."
            ),
            priority=3
        ))

    @Rule(TopicQuery(name="automata"))
    def automata_languages(self):
        self.declare(TopicFact(
            topic="automata",
            category="use_case",
            rule_id="AUT-USE-01",
            description=(
                "REGULAR LANGUAGES & APPLICATIONS — "
                "Finite Automata recognise Regular Languages — the simplest class "
                "in the Chomsky Hierarchy. "
                "Regular Languages can also be described by Regular Expressions. "
                "REAL-WORLD APPLICATIONS: "
                "Lexical analysis in compilers (tokenising source code). "
                "Pattern matching and text search (grep, regex engines). "
                "Network protocol design (validating packet formats). "
                "Vending machines and traffic light controllers (simple state machines). "
                "LIMITATION: Finite Automata cannot recognise context-free languages "
                "such as balanced parentheses — a Pushdown Automaton is required for that."
            ),
            priority=4
        ))

    @Rule(TopicQuery(name="automata"))
    def automata_errors(self):
        self.declare(TopicFact(
            topic="automata",
            category="error",
            rule_id="AUT-ERR-01",
            description=(
                "COMMON STUDENT ERRORS — "
                "1. Confusing DFA and NFA power: both recognise exactly the same set "
                "   of languages (Regular Languages). NFA is NOT more powerful than DFA — "
                "   it is only more concise to construct. "
                "2. Assuming an NFA rejects if any path fails — an NFA ACCEPTS if "
                "   at least one computation path reaches an accept state. "
                "3. Forgetting that ε-transitions in an NFA consume no input — "
                "   the machine changes state without reading a symbol. "
                "4. Confusing the start state with an accept state — a state can be "
                "   both the start state and an accept state simultaneously, but it "
                "   is not automatically an accept state just because it is the start. "
                "5. Applying Finite Automata to non-regular languages — FA cannot "
                "   count unbounded repetitions (e.g. aⁿbⁿ requires a Pushdown Automaton)."
            ),
            priority=5
        ))


# =============================================================================
# PUBLIC INTERFACE
# =============================================================================

TOPIC_ALIASES: dict[str, str] = {
    # Variables & Data Types
    "variables":                    "variables",
    "variable":                     "variables",
    "data types":                   "variables",
    "data type":                    "variables",
    "datatypes":                    "variables",
    "types":                        "variables",

    # Control Flow
    "control flow":                 "control_flow",
    "control_flow":                 "control_flow",
    "if else":                      "control_flow",
    "if statement":                 "control_flow",
    "loops":                        "control_flow",
    "for loop":                     "control_flow",
    "while loop":                   "control_flow",
    "conditionals":                 "control_flow",

    # Functions
    "functions":                    "functions",
    "function":                     "functions",
    "recursion":                    "functions",
    "recursive":                    "functions",
    "def":                          "functions",

    # OOP
    "oop":                          "oop",
    "object oriented":              "oop",
    "object-oriented":              "oop",
    "classes":                      "oop",
    "class":                        "oop",
    "inheritance":                  "oop",
    "objects":                      "oop",
    "polymorphism":                 "oop",
    "encapsulation":                "oop",

    # Lists / Arrays
    "lists":                        "lists",
    "list":                         "lists",
    "arrays":                       "lists",
    "array":                        "lists",

    # Stacks
    "stacks":                       "stacks",
    "stack":                        "stacks",

    # Queues
    "queues":                       "queues",
    "queue":                        "queues",

    # Linked Lists
    "linked lists":                 "linked_lists",
    "linked list":                  "linked_lists",
    "linked_lists":                 "linked_lists",
    "linked_list":                  "linked_lists",
    "singly linked list":           "linked_lists",
    "doubly linked list":           "linked_lists",

    # Trees
    "trees":                        "trees",
    "tree":                         "trees",
    "binary tree":                  "trees",
    "binary search tree":           "trees",
    "bst":                          "trees",
    "avl tree":                     "trees",
    "avl":                          "trees",

    # Hash Tables
    "hash tables":                  "hash_tables",
    "hash table":                   "hash_tables",
    "hash_tables":                  "hash_tables",
    "hash map":                     "hash_tables",
    "hashmap":                      "hash_tables",
    "dictionary":                   "hash_tables",
    "dictionaries":                 "hash_tables",
    "dict":                         "hash_tables",

    # Sorting
    "sorting":                      "sorting",
    "sorting algorithms":           "sorting",
    "bubble sort":                  "sorting",
    "merge sort":                   "sorting",
    "quick sort":                   "sorting",
    "bubblesort":                   "sorting",
    "mergesort":                    "sorting",
    "quicksort":                    "sorting",

    # Searching
    "searching":                    "searching",
    "searching algorithms":         "searching",
    "linear search":                "searching",
    "binary search":                "searching",
    "search":                       "searching",

    # Big-O
    "big o":                        "big_o",
    "big-o":                        "big_o",
    "big_o":                        "big_o",
    "time complexity":              "big_o",
    "space complexity":             "big_o",
    "complexity":                   "big_o",
    "complexity analysis":          "big_o",
    "asymptotic":                   "big_o",
    "asymptotic notation":          "big_o",

    # Graphs
    "graphs":                       "graphs",
    "graph":                        "graphs",
    "graph theory":                 "graphs",
    "bfs":                          "graphs",
    "dfs":                          "graphs",
    "breadth first search":         "graphs",
    "depth first search":           "graphs",
    "breadth-first search":         "graphs",
    "depth-first search":           "graphs",
    "directed graph":               "graphs",
    "undirected graph":             "graphs",

    # Automata Theory
    "automata":                     "automata",
    "automata theory":              "automata",
    "finite automata":              "automata",
    "finite automaton":             "automata",
    "dfa":                          "automata",
    "nfa":                          "automata",
    "deterministic finite automaton": "automata",
    "non-deterministic finite automaton": "automata",
    "nondeterministic finite automaton": "automata",
    "state machine":                "automata",
    "finite state machine":         "automata",
    "fsm":                          "automata",
    "regular language":             "automata",
    "regular languages":            "automata",
    "epsilon transition":           "automata",
}

SUPPORTED_TOPICS: list[str] = sorted(set(TOPIC_ALIASES.values()))


def get_expert_facts(topic_name: str) -> dict:
    """
    Primary public interface for the orchestrator.

    Normalises the topic name, fires the Rete engine, collects all
    TopicFact assertions, and returns them as a structured dictionary.

    Args:
        topic_name (str): Raw topic name from the user query.

    Returns:
        dict with keys:
            "success"       (bool)  : True if topic is in the knowledge base.
            "topic"         (str)   : Canonical topic name.
            "facts"         (list)  : List of fact dicts, sorted by priority.
            "facts_string"  (str)   : Pre-formatted string for LLM prompt injection.
            "error"         (str)   : Error message if success is False.
    """
    normalised = topic_name.strip().lower()
    canonical = TOPIC_ALIASES.get(normalised)

    if canonical is None:
        return {
            "success": False,
            "topic":   topic_name,
            "facts":   [],
            "facts_string": "",
            "error": (
                f"Topic '{topic_name}' is not in the knowledge base. "
                f"Supported topics: {', '.join(SUPPORTED_TOPICS)}."
            )
        }

    # Fresh engine instance per query — stateless, thread-safe
    engine = CSKnowledgeEngine()
    engine.reset()
    engine.declare(TopicQuery(name=canonical))
    engine.run()

    # Harvest all asserted TopicFact instances
    raw_facts = [
        fact for fact in engine.facts.values()
        if isinstance(fact, TopicFact)
    ]

    raw_facts.sort(key=lambda f: f["priority"])

    facts_list = [
        {
            "rule_id":     fact["rule_id"],
            "category":    fact["category"],
            "description": fact["description"],
            "priority":    fact["priority"],
        }
        for fact in raw_facts
    ]

    # Formatted string injected into the LLM prompt
    lines = [f"=== VERIFIED FACTS FOR: {canonical.replace('_', ' ').upper()} ==="]
    for f in facts_list:
        lines.append(f"\n[{f['rule_id']}] ({f['category'].upper()})")
        lines.append(f["description"])
    facts_string = "\n".join(lines)

    return {
        "success":      True,
        "topic":        canonical,
        "facts":        facts_list,
        "facts_string": facts_string,
        "error":        None,
    }


# =============================================================================
# STANDALONE TEST — run `python expert_engine.py` to verify the engine
# =============================================================================

if __name__ == "__main__":
    test_topics = [
        "variables",
        "control flow",
        "functions",
        "oop",
        "lists",
        "stacks",
        "queues",
        "linked list",
        "binary search tree",
        "dictionary",
        "sorting",
        "binary search",
        "big o",
        "graphs",
        "automata theory",
        "dfa",
        "heap sort",        # Not in KB — tests graceful error handling
    ]

    for topic in test_topics:
        print("\n" + "=" * 70)
        result = get_expert_facts(topic)
        if result["success"]:
            print(result["facts_string"])
        else:
            print(f"[ENGINE] {result['error']}")
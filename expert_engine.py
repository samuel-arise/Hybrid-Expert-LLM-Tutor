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
    This minimises space/time complexity as described in Section 3.2, Point 3.

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
import compat
import collections
import collections.abc

if not hasattr(collections, "Callable"):
    collections.Callable = collections.abc.Callable

from experta import (
    KnowledgeEngine,
    Fact,
    Rule,
)
from typing import Optional


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
    """
    Rule-Based Expert System for Python Programming and Data Structures tutoring.

    Constraint-Based Modelling approach:
        Rules encode the PROPERTIES that define a topic's correctness,
        not an exhaustive decision tree. This keeps the knowledge base
        maintainable and extensible.
    """

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


# =============================================================================
# PUBLIC INTERFACE
# =============================================================================

TOPIC_ALIASES: dict[str, str] = {
    # Variables & Data Types
    "variables":                "variables",
    "variable":                 "variables",
    "data types":               "variables",
    "data type":                "variables",
    "datatypes":                "variables",
    "types":                    "variables",

    # Control Flow
    "control flow":             "control_flow",
    "control_flow":             "control_flow",
    "if else":                  "control_flow",
    "if statement":             "control_flow",
    "loops":                    "control_flow",
    "for loop":                 "control_flow",
    "while loop":               "control_flow",
    "conditionals":             "control_flow",

    # Functions
    "functions":                "functions",
    "function":                 "functions",
    "recursion":                "functions",
    "recursive":                "functions",
    "def":                      "functions",

    # OOP
    "oop":                      "oop",
    "object oriented":          "oop",
    "object-oriented":          "oop",
    "classes":                  "oop",
    "class":                    "oop",
    "inheritance":              "oop",
    "objects":                  "oop",

    # Lists / Arrays
    "lists":                    "lists",
    "list":                     "lists",
    "arrays":                   "lists",
    "array":                    "lists",

    # Stacks
    "stacks":                   "stacks",
    "stack":                    "stacks",

    # Queues
    "queues":                   "queues",
    "queue":                    "queues",

    # Linked Lists
    "linked lists":             "linked_lists",
    "linked list":              "linked_lists",
    "linked_lists":             "linked_lists",
    "linked_list":              "linked_lists",
    "singly linked list":       "linked_lists",
    "doubly linked list":       "linked_lists",

    # Trees
    "trees":                    "trees",
    "tree":                     "trees",
    "binary tree":              "trees",
    "binary search tree":       "trees",
    "bst":                      "trees",

    # Hash Tables
    "hash tables":              "hash_tables",
    "hash table":               "hash_tables",
    "hash_tables":              "hash_tables",
    "hash map":                 "hash_tables",
    "hashmap":                  "hash_tables",
    "dictionary":               "hash_tables",
    "dictionaries":             "hash_tables",
    "dict":                     "hash_tables",
}

SUPPORTED_TOPICS: list[str] = sorted(set(TOPIC_ALIASES.values()))


def get_expert_facts(topic_name: str) -> dict:
    """
    Primary public interface for the orchestrator.

    Normalises the topic name, fires the Rete engine, collects all
    TopicFact assertions, and returns them as a structured dictionary.

    Args:
        topic_name (str): Raw topic name from the user query
                          (e.g., "Binary Search Tree", "oop", "linked list").

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
        "sorting",       # Not in KB — tests graceful error handling
    ]

    for topic in test_topics:
        print("\n" + "=" * 70)
        result = get_expert_facts(topic)
        if result["success"]:
            print(result["facts_string"])
        else:
            print(f"[ENGINE] {result['error']}")
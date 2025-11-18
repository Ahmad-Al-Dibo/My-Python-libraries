# Implementation of a simplified "Logic Theory Machine" style theorem prover in Python.
# - Syntax supported: 
#     variables: alphanumeric starting with letter, e.g. A, p, q1
#     unary: ~  (not)
#     binary: & (and), | (or), -> (implies), <-> (iff)
# - Approach: parse formulas, convert to CNF (classical steps), represent clauses as frozensets of literals,
#   and run a heuristic resolution search that prefers short clauses (smallest combined size) and enforces a beam limit.
# - This is a practical, compact, and readable implementation intended to be close in spirit to the LT
#   (heuristic-driven search for proofs) but using modern CNF & resolution machinery.
# - Example: proves (A -> C) from axioms (A -> B) and (B -> C).
#
# You can edit the `axioms` and `goal` at the bottom and re-run this cell to try other theorems.

import re
from collections import deque, defaultdict
from itertools import combinations
import math
import time

# -------------------------- Parser --------------------------
token_spec = [
    ("SKIP", r"[ \t\n]+"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("NOT", r"~"),
    ("IFF", r"<->"),
    ("IMPL", r"->"),
    ("AND", r"&"),
    ("OR", r"\|"),
    ("VAR", r"[A-Za-z][A-Za-z0-9_]*"),
]

token_regex = re.compile("|".join("(?P<%s>%s)" % pair for pair in token_spec))

class Token:
    def __init__(self, kind, val):
        self.kind = kind
        self.val = val
    def __repr__(self):
        return f"Token({self.kind},{self.val})"

def tokenize(s):
    pos = 0
    tokens = []
    while pos < len(s):
        m = token_regex.match(s, pos)
        if not m:
            raise SyntaxError(f"Unexpected char at pos {pos}: {s[pos:pos+10]!r}")
        kind = m.lastgroup
        if kind != "SKIP":
            tokens.append(Token(kind, m.group(0)))
        pos = m.end()
    return tokens

# Grammar (recursive descent)
# Expr := IffExpr
# IffExpr := ImplExpr ( "<->" ImplExpr )*
# ImplExpr := OrExpr ( "->" OrExpr )*
# OrExpr := AndExpr ( "|" AndExpr )*
# AndExpr := NotExpr ( "&" NotExpr )*
# NotExpr := "~" NotExpr | Atom
# Atom := VAR | "(" Expr ")"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else Token("EOF","")
    def accept(self, kind):
        if self.peek().kind == kind:
            t = self.peek()
            self.i += 1
            return t
        return None
    def expect(self, kind):
        t = self.accept(kind)
        if not t:
            raise SyntaxError(f"Expected {kind} at token {self.peek()}")
        return t

    def parse(self):
        node = self.parse_iff()
        if self.peek().kind != "EOF":
            raise SyntaxError("Extra input after end")
        return node

    def parse_iff(self):
        left = self.parse_impl()
        while self.accept("IFF"):
            right = self.parse_impl()
            left = ("<->", left, right)
        return left

    def parse_impl(self):
        left = self.parse_or()
        while self.accept("IMPL"):
            right = self.parse_or()
            left = ("->", left, right)
        return left

    def parse_or(self):
        left = self.parse_and()
        while self.accept("OR"):
            right = self.parse_and()
            left = ("|", left, right)
        return left

    def parse_and(self):
        left = self.parse_not()
        while self.accept("AND"):
            right = self.parse_not()
            left = ("&", left, right)
        return left

    def parse_not(self):
        if self.accept("NOT"):
            operand = self.parse_not()
            return ("~", operand)
        else:
            return self.parse_atom()

    def parse_atom(self):
        t = self.peek()
        if self.accept("LPAREN"):
            node = self.parse_iff()
            self.expect("RPAREN")
            return node
        elif t.kind == "VAR":
            self.i += 1
            return ("var", t.val)
        else:
            raise SyntaxError(f"Unexpected token {t} in parse_atom")

def parse_formula(s):
    tokens = tokenize(s)
    p = Parser(tokens)
    return p.parse()

# ------------------- Formula transformations (to CNF) -------------------

def eliminate_iff(node):
    if not isinstance(node, tuple):
        return node
    op = node[0]
    if op == "<->":
        A = eliminate_iff(node[1])
        B = eliminate_iff(node[2])
        # (A <-> B) => (A -> B) & (B -> A)
        return ("&", ("->", A, B), ("->", B, A))
    else:
        return tuple([op] + [eliminate_iff(child) for child in node[1:]])

def eliminate_impl(node):
    if not isinstance(node, tuple):
        return node
    op = node[0]
    if op == "->":
        A = eliminate_impl(node[1])
        B = eliminate_impl(node[2])
        # (A -> B) => (~A | B)
        return ("|", ("~", A), B)
    else:
        return tuple([op] + [eliminate_impl(child) for child in node[1:]])

def push_not(node):
    # move NOT inwards using De Morgan, produce nodes with ~ only on variables
    if not isinstance(node, tuple):
        return node
    op = node[0]
    if op == "~":
        inner = node[1]
        if inner[0] == "~":
            return push_not(inner[1])
        if inner[0] == "&":
            return ("|", push_not(("~", inner[1])), push_not(("~", inner[2])))
        if inner[0] == "|":
            return ("&", push_not(("~", inner[1])), push_not(("~", inner[2])))
        if inner[0] == "var":
            return node  # ~ var
        # if nested implication forms exist, they should have been removed
        return ("~", push_not(inner))
    elif op in ("&","|"):
        return (op, push_not(node[1]), push_not(node[2]))
    else:
        # var or other
        return tuple([op] + [push_not(child) for child in node[1:]])

def distribute_or_over_and(node):
    # transform (A | (B & C)) => (A | B) & (A | C)
    if not isinstance(node, tuple):
        return node
    op = node[0]
    if op == "|":
        A = distribute_or_over_and(node[1])
        B = distribute_or_over_and(node[2])
        if isinstance(A, tuple) and A[0] == "&":
            # (A1 & A2) | B  => (A1 | B) & (A2 | B)
            return ("&", distribute_or_over_and(("|", A[1], B)), distribute_or_over_and(("|", A[2], B)))
        if isinstance(B, tuple) and B[0] == "&":
            # A | (B1 & B2) => (A | B1) & (A | B2)
            return ("&", distribute_or_over_and(("|", A, B[1])), distribute_or_over_and(("|", A, B[2])))
        return ("|", A, B)
    elif op in ("&",):
        return ("&", distribute_or_over_and(node[1]), distribute_or_over_and(node[2]))
    else:
        return node

def to_cnf(node):
    # Convert to CNF step by step
    node = eliminate_iff(node)
    node = eliminate_impl(node)
    node = push_not(node)
    node = distribute_or_over_and(node)
    return node

# ------------------------- Clause utils -------------------------
# Represent literal as (name, sign) where sign is True for positive, False for negated.
def literal_to_tuple(lit):
    # lit is either ("var", name) or ("~", ("var", name))
    if isinstance(lit, tuple) and lit[0] == "~":
        v = lit[1]
        if v[0] != "var":
            raise ValueError("Expected var under not")
        return (v[1], False)
    elif isinstance(lit, tuple) and lit[0] == "var":
        return (lit[1], True)
    else:
        raise ValueError("Can't convert literal: " + str(lit))

def cnf_to_clauses(node):
    # CNF is conjunction of disjunctions of literals
    if not isinstance(node, tuple):
        # single var or single ~var
        return [frozenset([literal_to_tuple(node)])]
    if node[0] == "&":
        left = cnf_to_clauses(node[1])
        right = cnf_to_clauses(node[2])
        return left + right
    if node[0] == "|":
        # gather all literals of this clause (flatten nested ORs)
        lits = []
        stack = [node]
        while stack:
            cur = stack.pop()
            if isinstance(cur, tuple) and cur[0] == "|":
                stack.append(cur[2])
                stack.append(cur[1])
            else:
                lits.append(literal_to_tuple(cur))
        # remove duplicates
        return [frozenset(lits)]
    if node[0] == "~" or node[0] == "var":
        return [frozenset([literal_to_tuple(node)])]
    raise ValueError("Unknown CNF node: " + str(node))

# ------------------------- Resolution with heuristics -------------------------

def complementary(l1, l2):
    # l1 and l2 are (name, sign)
    return l1[0] == l2[0] and l1[1] != l2[1]

def resolve(c1, c2):
    # return set of resolvents (as frozensets). Standard resolution: pick a literal in c1 that complements one in c2.
    resolvents = set()
    for l1 in c1:
        for l2 in c2:
            if complementary(l1,l2):
                new_clause = set(c1.union(c2))
                new_clause.discard(l1)
                new_clause.discard(l2)
                resolvents.add(frozenset(new_clause))
    return resolvents

def heuristic_score_clause(clause):
    # simple heuristic: shorter clauses are preferable; also penalize clauses with many distinct variables.
    return len(clause) + 0.1 * len({lit[0] for lit in clause})

def find_proof_by_resolution(axioms_clauses, goal_clause, max_steps=20000, beam=200, timeout=10.0):
    """
    axioms_clauses: list of frozenset(literals)
    goal_clause: frozenset(literals) representing the clause(s) of the theorem to refute (we add its negation)
    This function tries to prove that axioms |= goal by adding neg(goal) and deriving empty clause.
    Returns proof object with status and trace of derived clauses (parent pointers).
    """
    start_time = time.time()
    # Knowledge base (set of clauses)
    clauses = set(axioms_clauses)
    # Add negation of goal: goal may be multiple clauses; for propositional theorem proving,
    # we add the negation of the formula, but here for convenient usage we accept a single clause goal
    # and add each literal of goal negated as separate unit clauses? Simpler: add negation of goal as clause(s).
    # If goal is a single literal clause, negation is unit clause with opposite literal.
    negated = []
    # If goal clause is empty, trivial
    if len(goal_clause) == 0:
        return {"proved": True, "steps": 0, "trace": [], "message":"Goal is empty clause"}
    # Add negation of entire goal clause: for theorem T, add clause(s) representing ~T.
    # For typical usage, caller should pass CNF of ~goal already as clauses; here we negate by turning each
    # literal in the goal clause into its negation and adding them as unit clauses (equivalent to negating a disjunction).
    for lit in goal_clause:
        negated.append(frozenset([(lit[0], not lit[1])]))
    for nc in negated:
        clauses.add(nc)

    # prepare parent map for proof reconstruction: clause -> (parent1, parent2)
    parents = {}
    derived = set()
    # index for quick lookup and heuristic selection
    clause_list = list(clauses)
    # Maintain a frontier priority structure: pairs to consider, prioritized by sum of clause heuristic sizes
    # We'll generate resolvents incrementally and enforce beam size
    new_queue = deque()
    # precompute all pairs
    for (i,c1), (j,c2) in combinations(list(enumerate(clause_list)),2):
        new_queue.append((c1,c2))
    steps = 0

    # Use a best-first ordering by sorting occasionally by total heuristic
    while new_queue and steps < max_steps:
        if time.time() - start_time > timeout:
            return {"proved": False, "steps": steps, "trace": parents, "message":"timeout"}
        # Heuristic selection: pick best pair among a sample up to beam
        sample = []
        sample_size = min(len(new_queue), beam)
        for _ in range(sample_size):
            sample.append(new_queue.popleft())
        # score pairs
        sample.sort(key=lambda pair: heuristic_score_clause(pair[0]) + heuristic_score_clause(pair[1]))
        # push back non-selected
        for pair in sample[1:]:
            new_queue.append(pair)
        c1,c2 = sample[0]
        steps += 1
        resolvents = resolve(c1,c2)
        for r in resolvents:
            if r not in clauses:
                parents[r] = (c1,c2)
                if len(r) == 0:
                    # derived empty clause -> proof found
                    return {"proved": True, "steps": steps, "trace": parents, "empty_clause": r, "message":"proved"}
                # add new resolvent and enqueue new pairs with existing clauses
                clauses.add(r)
                for c in list(clauses):
                    if c is r: continue
                    new_queue.append((r,c))
        # occasionally trim queue to beam size to keep heuristic behavior
        if len(new_queue) > beam * 10:
            # keep best portion according to heuristic for pairs
            items = list(new_queue)
            items.sort(key=lambda pair: heuristic_score_clause(pair[0]) + heuristic_score_clause(pair[1]))
            new_queue = deque(items[:beam*5])
    return {"proved": False, "steps": steps, "trace": parents, "message":"max_steps_reached"}

# ------------------------- Utility helpers -------------------------

def formula_to_cnf_clauses(formula_str):
    parsed = parse_formula(formula_str)
    cnf = to_cnf(parsed)
    clauses = cnf_to_clauses(cnf)
    # normalize clause literal order
    normed = []
    for c in clauses:
        normed.append(frozenset(sorted(c)))
    return normed

def pretty_clause(c):
    if not c:
        return "⊥ (empty)"
    lits = []
    for v,s in sorted(c):
        lits.append((("" if s else "~") + v))
    return "(" + " ∨ ".join(lits) + ")"

def reconstruct_proof(trace, empty_clause):
    # trace: clause -> (p1,p2)
    proof_order = []
    visited = set()
    def dfs(cl):
        if cl in visited: return
        visited.add(cl)
        parents = trace.get(cl)
        if parents:
            dfs(parents[0])
            dfs(parents[1])
        proof_order.append(cl)
    dfs(empty_clause)
    return proof_order

# ------------------------- Example / Test -------------------------
if __name__ == "__main__":
    # Example: from (A -> B) and (B -> C) prove (A -> C).
    axioms = ["(A -> B)", "(B -> C)"]
    goal = "(A -> C)"
    print("Axioms:", axioms)
    print("Goal:", goal)
    # convert to CNF clauses
    ax_clauses = []
    for a in axioms:
        ax_clauses.extend(formula_to_cnf_clauses(a))
    goal_clauses = formula_to_cnf_clauses(goal)
    print("Axiom clauses:")
    for c in ax_clauses:
        print(" ", pretty_clause(c))
    print("Goal clauses (CNF of goal):")
    for c in goal_clauses:
        print(" ", pretty_clause(c))
    # For our resolution function, we will treat `goal_clause` as the first (and only) clause of goal CNF
    # and add its negation. For complex goals, you can pass all clauses or wrap them with parentheses.
    # We'll try to prove by adding negated goal unit clauses.
    result = find_proof_by_resolution(ax_clauses, goal_clauses[0], max_steps=10000, beam=500, timeout=5.0)
    print("\nResult:", result["message"], "steps:", result["steps"])
    if result["proved"]:
        empty_clause = result.get("empty_clause", frozenset())
        proof_order = reconstruct_proof(result["trace"], empty_clause)
        print("Proof (derived clauses in order):")
        for cl in proof_order:
            print("  ", pretty_clause(cl))
    else:
        print("No proof found within limits.")

# End of implementation cell. You can copy this module to a .py file or run in an interactive Python session.


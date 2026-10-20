import os
from typing import List, Union, Dict, Set, Tuple, Optional
from collections import defaultdict
from graphviz import Digraph

class Token:
    def __init__(self, type_: str, value: str):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"

def tokenize(regex: str) -> List[Token]:
    tokens = []
    i = 0

    while i < len(regex):
        char = regex[i]

        if char in ('*', '|', '(', ')', '+'):
            tokens.append(Token(char, char))
            i += 1
        elif char.isalnum():
            tokens.append(Token('CHAR', char))
            i += 1
        else:
            raise ValueError(f"Unexpected character: {char}")

    return tokens

class ASTNode:
    pass

class CharNode(ASTNode):
    def __init__(self, value: str):
        self.value = value

class ConcatNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

class UnionNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

class StarNode(ASTNode):
    def __init__(self, child: ASTNode):
        self.child = child

class PlusNode(ASTNode):
    def __init__(self, child: ASTNode):
        self.child = child

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Optional[Token]:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, type_: str) -> Token:
        token = self.current_token()
        if token and token.type == type_:
            self.pos += 1
            return token
        raise ValueError(f"Expected token type {type_}, but got {token}")

    # =====
    def parse(self) -> ASTNode:
        node = self.parse_union()

        if self.current_token() is not None:
            raise ValueError(
                f"Unexpected token: {self.current_token()}"
            )

        # return self.parse_union()
        return node
    # =====

    def parse_union(self) -> ASTNode:
        left = self.parse_concat()

        while self.current_token() and self.current_token().type == '|':
            self.eat('|')
            right = self.parse_concat()
            left = UnionNode(left, right)

        return left

    def parse_concat(self) -> ASTNode:
        left = self.parse_star()

        while self.current_token() and self.current_token().type not in ('|', ')'):
            right = self.parse_star()
            left = ConcatNode(left, right)

        return left

    def parse_star(self) -> ASTNode:
        node = self.parse_base()

        while self.current_token() and self.current_token().type in ('*', '+'):
            if self.current_token().type == '*':
                self.eat('*')
                node = StarNode(node)
            elif self.current_token().type == '+':
                self.eat('+')
                node = PlusNode(node)

        return node

    def parse_base(self) -> ASTNode:
        token = self.current_token()

        # =====
        if token is None:
            raise ValueError(
                "Expected a character or an opening parenthesis."
            )
        # =====

        if token.type == 'CHAR':
            self.eat('CHAR')
            return CharNode(token.value)
        elif token.type == '(':
            self.eat('(')
            node = self.parse_union()
            self.eat(')')
            return node
        raise ValueError(f"Unexpected token: {token}")

class NFA:
    def __init__(self, start_state: int, accept_state: int, transitions: Dict[int, Dict[Optional[str], Set[int]]]):
        self.start_state = start_state
        self.accept_state = accept_state
        self.transitions = transitions

    def add_transition(self, from_state: int, symbol: Optional[str], to_state: int):
        if from_state not in self.transitions:
            self.transitions[from_state] = defaultdict(set)
        self.transitions[from_state][symbol].add(to_state)

class NFAConstructor:
    def __init__(self):
        self.state_count = 0

    def new_state(self) -> int:
        state = self.state_count
        self.state_count += 1
        return state

    def char_to_nfa(self, node: CharNode) -> NFA:
        start = self.new_state()
        accept = self.new_state()
        nfa = NFA(start, accept, defaultdict(lambda: defaultdict(set)))
        nfa.add_transition(start, node.value, accept)
        return nfa

    def concat_to_nfa(self, node: ConcatNode) -> NFA:
        left_nfa = self.build_nfa(node.left)
        right_nfa = self.build_nfa(node.right)
        left_nfa.add_transition(left_nfa.accept_state, None, right_nfa.start_state)
        return NFA(left_nfa.start_state, right_nfa.accept_state, {**left_nfa.transitions, **right_nfa.transitions})

    def union_to_nfa(self, node: UnionNode) -> NFA:
        left_nfa = self.build_nfa(node.left)
        right_nfa = self.build_nfa(node.right)
        start = self.new_state()
        accept = self.new_state()
        nfa = NFA(start, accept, {**left_nfa.transitions, **right_nfa.transitions})
        nfa.add_transition(start, None, left_nfa.start_state)
        nfa.add_transition(start, None, right_nfa.start_state)
        nfa.add_transition(left_nfa.accept_state, None, accept)
        nfa.add_transition(right_nfa.accept_state, None, accept)
        return nfa

    def star_to_nfa(self, node: StarNode) -> NFA:
        inner_nfa = self.build_nfa(node.child)
        start = self.new_state()
        accept = self.new_state()
        nfa = NFA(start, accept, {**inner_nfa.transitions})
        nfa.add_transition(start, None, inner_nfa.start_state)
        nfa.add_transition(start, None, accept)
        nfa.add_transition(inner_nfa.accept_state, None, inner_nfa.start_state)
        nfa.add_transition(inner_nfa.accept_state, None, accept)
        return nfa

    def build_nfa(self, node: ASTNode) -> NFA:
        if isinstance(node, CharNode):
            return self.char_to_nfa(node)
        elif isinstance(node, ConcatNode):
            return self.concat_to_nfa(node)
        elif isinstance(node, UnionNode):
            return self.union_to_nfa(node)
        elif isinstance(node, StarNode):
            return self.star_to_nfa(node)
        # =====
        elif isinstance(node, PlusNode):
            # return self.star_to_nfa(ConcatNode(node.child, StarNode(node.child)))
            return self.concat_to_nfa(ConcatNode(node.child, StarNode(node.child)))
        # =====
        else:
            raise ValueError("Unknown AST Node type")

def visualize_nfa(nfa: NFA, filename: str = 'nfa_graph'):
    dot = Digraph(comment="NFA", format="png")

    dot.node("start", shape="point")
    dot.edge("start", str(nfa.start_state))

# =====
    # for state in nfa.transitions:
    #     if state == nfa.accept_state:
    #         dot.node(str(state), shape="doublecircle", label=f"{state} (Accept)")
    #     else:
    #         dot.node(str(state), shape="circle", label=str(state))

    states = {
        nfa.start_state,
        nfa.accept_state,
        *nfa.transitions.keys(),
    }

    for transitions in nfa.transitions.values():
        for targets in transitions.values():
            states.update(targets)

    for state in sorted(states):
        if state == nfa.accept_state:
            dot.node(str(state), shape="doublecircle", label=f"{state} (Accept)")
        else:
            dot.node(str(state), shape="circle", label=str(state))
# =====

    for from_state, transitions in nfa.transitions.items():
        for symbol, to_states in transitions.items():
            for to_state in to_states:
                label = "ε" if symbol is None else symbol
                dot.edge(str(from_state), str(to_state), label=label)

    # dot.render(filename, directory=os.path.dirname(filename), view=False)
    rendered_path = dot.render(filename, directory=os.path.dirname(filename), view=False)

    # Delete the .gv file if it exists
    gv_file = f"{filename}"
    if os.path.exists(gv_file):
        os.remove(gv_file)

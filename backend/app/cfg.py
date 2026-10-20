#!/usr/bin/env python3
# cfg_to_pda_slide.py – PDA that renders & behaves exactly like Example-3 slide
# ----------------------------------------------------------
#  Grammar file (stdin or pipe):
#      S
#      a,b
#      S -> a S b | ε
# ----------------------------------------------------------

import sys
import itertools
# =====
import time
# =====
from collections import defaultdict, deque
from graphviz import Digraph

EPS   = 'ε'    # epsilon for input & stack actions
BOT   = '$'    # bottom-of-stack marker

Q1, Q2, Q3, QF = 'q1', 'q2', 'q3', 'qf'   # state names used in logic
# ----------------------------------------------------------
#  1. read grammar
# ----------------------------------------------------------
def read_grammar(text: str):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if len(lines) < 3:
        raise ValueError("Need start symbol, terminals, and at least one rule.")
    start = lines[0]
    terms = set(lines[1].split(','))
    prods = defaultdict(list)           # {A: list of RHS (list[str])}
    for ln in lines[2:]:
        ln = ln.replace('→', '->')
        h, rhs = map(str.strip, ln.split('->'))
        for alt in rhs.split('|'):
            alt = alt.strip()
            if alt in {'', 'ε', 'λ'}:
                prods[h].append([])      # empty production
            else:
                prods[h].append(alt.split())
    return start, terms, prods
# ----------------------------------------------------------
#  2. PDA construction (allow pop = EPS meaning "pop nothing")
#     delta[q][(inp, pop)] = set( (next, pushStr) )
# ----------------------------------------------------------
def build_pda(start, terms, prods):
    d = defaultdict(lambda: defaultdict(set))
    push = lambda q,a,pop,qn,strg: d[q][(a,pop)].add((qn,strg))

    # initial chain: q1 ─ε,ε→$→ q2 ─ε,ε→S→ q3
    push(Q1, EPS, EPS, Q2, BOT)
    push(Q2, EPS, EPS, Q3, start)

    # =====
    # One counter shared by all production rules.
    h_id = itertools.count(start=4)
    # =====

    # variable expansions inside q3
    for A, rhss in prods.items():
        for rhs in rhss:
            if not rhs:                        # A -> ε
                push(Q3, EPS, A, Q3, '')
            else:
                rev = rhs[::-1]                # push rightmost first
                # first edge: pop A, push last symbol
                last, rest = rev[0], rev[1:]
                h_curr = Q3
                # =====
                # h_id = itertools.count(start=4)
                # =====
                h_next = f'q{next(h_id)}'
                push(h_curr, EPS, A, h_next, last)
                # middle edges for remaining symbols (if any)
                for sym in rest:
                    h_curr, h_next = h_next, f'q{next(h_id)}'
                    push(h_curr, EPS, EPS, h_next, sym)
                # final edge back to q3
                push(h_next, EPS, EPS, Q3, '')

    # terminal self-loops
    for a in terms:
        push(Q3, a, a, Q3, '')

    # accept
    push(Q3, EPS, BOT, QF, '')
    return d
# ----------------------------------------------------------
#  3. δ table pretty print
# ----------------------------------------------------------
def print_delta(delta):
    print('\nδ transition table')
    print(f'{"from":<5} {"in":<2} {"pop":<3} → {"to":<5} {"push"}')
    print('-'*30)
    for q in delta:
        for (a,pop), tgts in delta[q].items():
            for qn,push in tgts:
                a = a or EPS
                pop = pop or EPS
                push = push or EPS
                print(f'{q:<5} {a:<2} {pop:<3} → {qn:<5} {push}')

# ----------------------------------------------------------
#  4. Graphviz drawing (slide style)
# ----------------------------------------------------------
# =====
# def draw(delta, fname='pda_graph'):
def draw(delta, fname='pda_graph', view=True):
# =====
    dot = Digraph('PDA', format='png')
    dot.attr(rankdir='LR', nodesep='0.9', ranksep='0.7', splines='polyline',
             fontname='Helvetica', fontsize='12')
    dot.attr('node', shape='circle', style='filled', fillcolor='#ffffff',
             color='#8e8e8e', width='0.8')

    # numbering visible nodes 1,2,3,4,...
    mapping = {Q1:'1', Q2:'2', Q3:'3', QF:'4'}
    helper_counter = itertools.count(start=5)
    visible = {Q1,Q2,Q3,QF}

    # discover helper states
    for q in delta:
        for (a,pop),tgts in delta[q].items():
            for qn,_ in tgts:
                if qn not in mapping:
                    mapping[qn] = str(next(helper_counter))
                    visible.add(qn)

    # draw nodes
    dot.node('entry', shape='point', color='black')
    for q in visible:
        shape = 'doublecircle' if q==QF else 'circle'
        # =====
        # dot.node(mapping[q], label=mapping[q], shape=shape)
        dot.node(mapping[q], label=q, shape=shape)
        # =====

    # entry edge
    dot.edge('entry', mapping[Q1], arrowhead='none')

    # edges
    def lbl(a,pop,push):
        return f'{a or EPS}, {pop or EPS} → {push or EPS}'
    for q in delta:
        for (a,pop),tgts in delta[q].items():
            for qn,push in tgts:
                tail, head = mapping[q], mapping[qn]
                attrs={}
                if q==qn and a==pop and push=='' and a in {c for c in 'abcdefghijklmnopqrstuvwxyz'}:
                    attrs=dict(tailport='s',headport='w',loop='left')
                dot.edge(tail, head, label=lbl(a,pop,push), **attrs)

    # =====
    # dot.render(fname, view=True)
    return dot.render(fname, view=view)
    # =====

# ----------------------------------------------------------
#  5. membership tester (supports pop = EPS)
# ----------------------------------------------------------

# =====
# def accepts(delta, w):
def accepts(delta, w, max_configs=50000, timeout=3.0):
    # Node = tuple                       # (pos, q, stack)
    start_node = (0, Q1, ())           # empty stack
    q = deque([start_node])
    seen = {start_node}

    deadline = time.monotonic() + timeout

    # while q:
    while q:
        if time.monotonic() > deadline:
            raise RuntimeError(
                "Search time limit reached. "
                "The result is inconclusive."
            )
# =====

        pos,qc,stack = q.popleft()
        sym = w[pos] if pos<len(w) else None
        top = stack[-1] if stack else None

        for a,pop in [(EPS,EPS), (sym,None)]:
            if a is None: continue
            for (ia,ip),tgts in delta[qc].items():
                if ia==a and (ip==EPS or (stack and ip==top)):
                    for qn,push in tgts:
                        new_pos = pos + (0 if a==EPS else 1)
                        new_stack = list(stack)
                        if ip!=EPS:
                            new_stack.pop()
                        if push:
                            # =====
                            # new_stack.extend(push[::-1])
                            new_stack.append(push)
                            # =====
                        node = (new_pos, qn, tuple(new_stack))
                        if node in seen or new_pos>len(w): continue
                        if qn==QF and new_pos==len(w) and not new_stack:
                            return True

                        # =====
                        if len(seen) >= max_configs:
                            raise RuntimeError(
                                "Search configuration limit reached. "
                                "The result is inconclusive."
                            )
                        # =====

                        seen.add(node)
                        q.append(node)
    return False
# ----------------------------------------------------------
#  6. driver
# ----------------------------------------------------------
if __name__ == "__main__":
    print("Paste your CFG (blank line to end):")
    txt=[]
    while True:
        try: line=input()
        except EOFError: break
        if not line.strip(): break
        txt.append(line)
    try:
        start,terms,prods = read_grammar('\n'.join(txt))
    except ValueError as e:
        print("Error:",e); sys.exit(1)

    delta = build_pda(start,terms,prods)
    print_delta(delta)
    print("\nRendering PDA to pda_graph.png …")
    draw(delta)

    # quick tester
    while True:
        # try:
        #     s = input("\nTest string (blank = quit): ")
        try:
            s = input("\nTest string (ε = empty string, blank = quit): ")

        except (EOFError,KeyboardInterrupt):
            break

        if s == "":
            break

        # =====
        if s == EPS:
            s = ""
        # =====

        # =====
        # print("✔ accepted" if accepts(delta,s) else "✘ rejected")
        try:
            accepted = accepts(delta, s)
            print("✔ accepted" if accepted else "✘ rejected")
        except RuntimeError as error:
            print(f"? Inconclusive: {error}")
        # =====

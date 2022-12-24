import string

from fnf import FNFMaker

opps = {
    "a": "x := x + y",
    "b": "y := y + 2z",
    "c": "x := 3x + z",
    "d": "z := y − z"
}


def dependence_fun(c1, c2):
    l1, r1 = opps[c1].split(":=")
    l2, r2 = opps[c2].split(":=")
    l1 = [c for c in l1 if c in string.ascii_letters]
    r1 = [c for c in r1 if c in string.ascii_letters]
    l2 = [c for c in l2 if c in string.ascii_letters]
    r2 = [c for c in r2 if c in string.ascii_letters]

    return any([c in r2 for c in l1]) or any([c in r1 for c in l2])


word = "baadcb"

if __name__ == '__main__':
    maker = FNFMaker(
        alphabet=list(opps),
        dependence_fun=dependence_fun
    )
    print("Dependencies:\n", maker.get_dependencies())

    G = maker.build_graph(word)
    maker.draw_graph(G, word)
    fnf = maker.getFNF(G, word)

    print("FNF:\n", fnf)

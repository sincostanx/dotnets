# Inspired by
# https://tgmstat.wordpress.com/2013/06/12/draw-neural-network-diagrams-graphviz/

# UPDATE HISTORY
# April, 2018 - 2to3 - Madhavun Candadai

# Add options to customize output via command line (for IRP)

import argparse

def generate(args):
    layers = args.layer_dim
    
    layers_str = ["\"Input (0)\""] + [f"\"Hidden ({i+1})\"" for i in range(len(layers) - 2)] + [f"\"Output ({len(layers) - 1})\""]
    layers_col = ["none"] + ["none"] * (len(layers) - 2) + ["none"]
    layers_fill = [args.color] + [args.hidden_color] * (len(layers) - 2) + [args.color]
    
    font = "Hilda 10"
    
    print("digraph G {")
    print("\tfontname = \"{}\"".format(font))
    print("\trankdir=LR")
    print("\tsplines=line")
    print("\tnodesep=.08;")
    print("\tranksep=1;")
    print("\tedge [color=black, arrowsize=.5];")
    print("\tnode [fixedsize=true,label=\"\",style=filled," + \
        "color=none,fillcolor=gray,shape=circle]\n")
    
    # Clusters
    for i in range(0, len(layers)):
        print(("\tsubgraph cluster_{} {{".format(i)))
        print(("\t\tcolor={};".format(layers_col[i])))
        print(("\t\tnode [style=filled, color=white, penwidth={},"
              "fillcolor={} shape=circle];".format(
                  args.penwidth,
                  layers_fill[i])))
    
        print(("\t\t"), end=' ')
    
        for a in range(layers[i]):
            print("l{}{} ".format(i + 1, a), end=' ')
    
        print(";")
        print(("\t\tlabel = {};".format(layers_str[i])))
    
        print("\t}\n")
    
    # Nodes
    for i in range(1, len(layers)):
        for a in range(layers[i - 1]):
            for b in range(layers[i]):
                print("\tl{}{} -> l{}{}".format(i, a, i + 1, b))
    
    print("}")

def convert_arg_line_to_args(arg_line):
    for arg in arg_line.split():
        if not arg.strip(): continue
        yield str(arg)

if __name__ == "__main__":
    # color options available at https://graphviz.org/doc/info/colors.html
    parser = argparse.ArgumentParser(
        description="Option for MLP generation",
        fromfile_prefix_chars="@",
        conflict_handler="resolve",
    )
    parser.add_argument("--color", "--color", default="black", type=str, help="color for input and output")
    parser.add_argument("--hidden-color", "--hidden_color", default="gray", type=str, help="color for neurons in hidden layers")
    parser.add_argument("--penwidth", default=15, type=int, help="Penwidth for neuron nodes")
    parser.add_argument("--layer-dim", "--layer_dim", nargs="*", type=int, default=[3, 5, 5, 5, 2])
    parser.convert_arg_line_to_args = convert_arg_line_to_args
    args = parser.parse_args()
    generate(args)


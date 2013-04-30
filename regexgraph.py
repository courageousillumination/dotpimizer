import pydot

epsilon = '<&#949;>'

class Token:
    def __init__(self):
        return None
    def add_to_graph(self, graph):
        return None

class OrOp(Token):
    def __init__(self, groups):
        self.groups = groups
        
    def add_to_graph(self, graph, state, parent = None):
        end_nodes = []
        state+=1
        graph.add_node(pydot.Node(str(state)))
        graph.add_edge(pydot.Edge(str(parent), str(state), label=epsilon))
        parent = state
        for group in self.groups:
            state = group.add_to_graph(graph, state, parent)
            end_nodes.append(state)
       #Create an end node and link everything back to that
        state+=1
        graph.add_node(pydot.Node(str(state)))
        for node in end_nodes:
            graph.add_edge(pydot.Edge(str(node), str(state), label=epsilon))
        return state
        
class LiteralExpression(Token):
    def __init__(self, chars):
        self.chars = chars
    
    def add_to_graph(self, graph, state, parent = None):
        state += 1
        graph.add_node(pydot.Node(str(state)))
        graph.add_edge(pydot.Edge(str(parent), str(state), label=self.chars))
           
        return state
        
class RegexToken(Token):
    def __init__(self, tokens):
        self.tokens = tokens
        
    def add_to_graph(self, graph, state, parent = None):
        for token in self.tokens:
            state = token.add_to_graph(graph, state, parent)
            parent = str(state)
        return state 
        
class StarToken(Token):
    def __init__(self, token):
        self.token = token
        
    def add_to_graph(self, graph, state, parent = None):
        print parent
        state = self.token.add_to_graph(graph, state, parent)
        #Add the end node
        state += 1
        graph.add_node(pydot.Node(str(state)))
        
        graph.add_edge(pydot.Edge(str(parent), str(state-1), label=epsilon))
        graph.add_edge(pydot.Edge(str(state-1), str(parent), label=epsilon))
        graph.add_edge(pydot.Edge(str(state-1), str(state), label=epsilon))
        
        return state
        
class PlusToken(Token):
    def __init__(self, token):
        self.token = token
        
    def add_to_graph(self, graph, state, parent = None):
        state = self.token.add_to_graph(graph, state, parent)
        #Add the end node
        state += 1
        graph.add_node(pydot.Node(str(state)))
        
        graph.add_edge(pydot.Edge(str(state-1), str(parent), label=epsilon))
        graph.add_edge(pydot.Edge(str(state-1), str(state), label=epsilon))
        
        return state
        
class ParenToken(Token):
    def __init__(self, token):
        self.token = token
    
    def add_to_graph(self, graph, state, parent = None):
        return self.token.add_to_graph(graph,state,parent)
        
def tokenize(regex):
    #Return any tokens that get passed in here
    if isinstance(regex, Token):
        return regex
    #If this is an operator just return
    if regex == "|" or regex == "*" or regex == "+":
        return regex
    #First, loop over and break into outer most parenthesis
    paren_counter = 0
    broken = []
    paren_string = ""
    for char in regex:
        if char == "(":
            if paren_counter == 0:
                if paren_string != "":
                    broken.append(paren_string)
                paren_string = ""
            else:
                paren_string += char    
            paren_counter += 1
        elif char == ")":
            paren_counter -= 1
            if paren_counter == 0:
                broken.append(ParenToken(tokenize(paren_string)))
                paren_string = ""
            else:
                paren_string += char
        #Get special chars in the outmost layer
        elif (char == "|" or char == "*" or char == "+") and paren_counter == 0:
            if(paren_string != ""):
                broken.append(paren_string)
            broken.append(char)  
            paren_string = ""
        else:
            paren_string += char
            
    if paren_string != "":
        broken.append(paren_string)
    if len(broken) == 1:
        or_split = regex.split('|')
        if len(or_split) != 1:
            result = OrOp([tokenize(x) for x in or_split])
        else:
            #Just deal with literal
            result = LiteralExpression(regex)
        return result
            
    else:
        tokens =  [tokenize(x) for x in broken]
        print tokens
        #Apply the * and +
        for index, token in enumerate(tokens):
            #If it's a literal expression, just get the previous character
            if token == "*" or token == "+":
                if isinstance(token, LiteralExpression):
                    previous_token = LiteralExpression(token.chars[-1])
                    token.chars = token.chars[:-1]
                else:
                    previous_token = tokens[index - 1]
                    index = index - 1 
                if token == "*":
                    tokens[index] = StarToken(previous_token)
                elif token == "+":
                    tokens[index] = PlusToken(previous_token)
        #Remove all the stars that are left
        tokens = [x for x in tokens if x != "*" and x != "+" 
                  and not (isinstance(x, LiteralExpression) and x.chars == "")]
        #Then we can apply ors
        if "|" in tokens:
            tokens = [OrOp([x for x in tokens if x != "|"])]
        
        return RegexToken(tokens)

def regex_to_graph(regex, graph_name = "regex_graph"):
    """
    Convert a regular expression to a pydot
    graph object. Requires correct parentheses
    """
    graph = pydot.Dot(graph_name, graph_type='digraph')
    graph.add_node(pydot.Node('0'))
    state = 0
    
    regex_token = tokenize(regex)
    
    regex_token.add_to_graph(graph, state, "0")
        
    return graph

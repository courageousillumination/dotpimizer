import pydot

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
        graph.add_edge(pydot.Edge(str(parent), str(state), label="epsilon"))
        parent = state
        print parent
        for group in self.groups:
            state = group.add_to_graph(graph, state, parent)
            end_nodes.append(state)
       #Create an end node and link everything back to that
        state+=1
        graph.add_node(pydot.Node(str(state)))
        for node in end_nodes:
            graph.add_edge(pydot.Edge(str(node), str(state), label="epsilon"))
        return state
        
class LiteralExpression(Token):
    def __init__(self, chars):
        self.chars = chars
    
    def add_to_graph(self, graph, state, parent = None):
        
        #Add the link to the parent
        for char in self.chars:
            state+=1
            graph.add_node(pydot.Node(str(state)))
            graph.add_edge(pydot.Edge(str(parent), str(state), label=char))
            parent = state
            
        return state
        
class RegexToken(Token):
    def __init__(self, tokens):
        self.tokens = tokens
        
    def add_to_graph(self, graph, state, parent = None):
        for token in self.tokens:
            state = token.add_to_graph(graph, state, parent)
            parent = str(state)
          
        return state          
def tokenize(regex):
    #If this is an operator just return
    if regex == "|":
        return regex
    if "(" in regex:
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
                    broken.append(paren_string)
                    paren_string = ""
                else:
                    paren_string += char
            #Get or in the outmost layer
            elif char == "|" and paren_counter == 0:
                broken.append(paren_string)
                broken.append(char)  
                paren_string = ""
            else:
                paren_string += char
            
        if paren_string != "":
            broken.append(paren_string)
        tokens =  [tokenize(x) for x in broken]
        #Then we can apply ors
        print tokens
        if "|" in tokens:
            tokens = [OrOp([x for x in tokens if x != "|"])]
            print tokens
        return RegexToken(tokens)
    else:
        #In this case we have a pretty simple regex
        #Split on or cause that binds hella loose
        or_split = regex.split('|')
        if len(or_split) != 1:
            result = OrOp([tokenize(x) for x in or_split])
        #Otherwise actually tokenize
        else:
            #Just deal with literal
            result = LiteralExpression(regex)
        #In the case where there are no parentheisi we can deal with this eaiser    
    """if "(" in regex:
        tokens = []
        paren_counter = 0
        paren_expression = ""
        for char in regex:
            if char == '(':
                if paren_counter == 0:
                    if paren_expression != "":
                        tokens.append(tokenize(paren_expression))
                        print paren_expression
                        paren_expression = ""
                else:
                    paren_expression += char 
                paren_counter += 1
            elif char == ')':
                paren_counter -= 1
                if paren_counter == 0:
                    tokens.append(tokenize(paren_expression))
                    print paren_expression
                    paren_expression = ""
                else:
                    paren_expression += char
            else:
                paren_expression += char
        if paren_expression != "":
            tokens.append(tokenize(paren_expression))
        
        result = RegexToken(tokens)
    else:
        #Otherwise we do some other stuff
        #Split on or cause that binds hella loose
        or_split = regex.split('|')
        if len(or_split) != 1:
            result = OrOp([tokenize(x) for x in or_split])
        #Otherwise actually tokenize
        else:
            #Just deal with literal
            result = LiteralExpression(regex)"""
    return result

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

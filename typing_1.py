from typing import Dict, List, Union,Optional
import json
from graphviz import Digraph
from datetime import date, timedelta
import numpy as np

class Activity:
    def __init__(self, id:int, name: str, duration: int, predecessors_indices: List[int]):
        self.id=id
        self.name = name
        self.duration = duration
        self.predecessors_indices = predecessors_indices


class NodeState:
    def __init__(self, name: str, emerging_arrows: List[Union['ArrowTask', 'DashedArrow']], terminating_arrows: List[Union['ArrowTask', 'DashedArrow']]):
        self.name = name
        self.emerging_arrows = emerging_arrows
        self.terminating_arrows=terminating_arrows


class ArrowTask:
    def __init__(self, activity_name: str, duration: int, destination_node: NodeState,starting_node: NodeState,early_start,early_finish,late_start,late_finish):
        self.activity_name = activity_name
        self.duration = duration
        self.destination_node = destination_node
        self.starting_node=starting_node
        self.early_start=early_start
        self.early_finish=early_finish
        self.late_start=late_start
        self.late_finish=late_finish


class DashedArrow:
    def __init__(self, destination_node: NodeState,starting_node: NodeState,early_start,early_finish,late_start,late_finish):
        self.destination_node = destination_node
        self.starting_node=starting_node
        self.early_start=early_start
        self.early_finish=early_finish
        self.late_start=late_start
        self.late_finish=late_finish


def get_aoa_data_structure(activity_data: List[Activity]) -> NodeState:
    # states: Dict[str, NodeState] = {}
    # start_node = NodeState('start', [],[])
    # states['[]'] = start_node
    # ending_nodes: List[NodeState] = [start_node]

    # dict_forward: Dict[NodeState,int]={}
    # dict_backward:Dict[NodeState,int]={}

    # dict_backward[start_node]=0

    # for index, activity in enumerate(activity_data):
    #     state_key = json.dumps(activity.predecessors_indices)
    #     state = states.get(state_key)
        
    #     if not state:
    #         state = NodeState(state_key, [],[])
    #         states[state_key] = state
    #         for predecessor_index in activity.predecessors_indices:
    #             temp = states.get(f'[{predecessor_index}]')
    #             if temp and len(temp.emerging_arrows) == 0:
    #                 ending_nodes = [node for node in ending_nodes if node != temp]
    #             if temp:
    #                 new_dummy=DashedArrow(state,temp,None,None,None,None)
    #                 temp.emerging_arrows.append(new_dummy)
    #                 state.terminating_arrows.append(new_dummy)
    #                 if dict_forward.get(temp) is None:
    #                     dict_forward[temp]=1
    #                 else:
    #                     dict_forward[temp]=dict_forward[temp]+1
    #                 if dict_backward.get(state) is None:
    #                     dict_backward[state]=1
    #                 else:
    #                     dict_backward[state]=dict_backward[state]+1
                    
        
    #     dest_node = NodeState(f'[{index}]', [],[])
    #     ending_nodes.append(dest_node)
    #     states[f'[{index}]'] = dest_node
        
    #     if len(state.emerging_arrows) == 0:
    #         ending_nodes = [node for node in ending_nodes if node != state]
        
    #     new_activity=ArrowTask(activity.name, activity.duration, dest_node,state,None,None,None,None)
    #     state.emerging_arrows.append(new_activity)
    #     dest_node.terminating_arrows.append(new_activity)
    #     if dict_forward.get(state) is None:
    #         dict_forward[state]=1
    #     else:
    #         dict_forward[state]=dict_forward[state]+1
    #     if dict_backward.get(dest_node) is None:
    #         dict_backward[dest_node]=1
    #     else:
    #         dict_backward[dest_node]=dict_backward[dest_node]+1
    
    # finish_node = NodeState('finish', [],[])
    # for ending_node in ending_nodes:
    #     creat=DashedArrow(finish_node,ending_node,None,None,None,None)
    #     ending_node.emerging_arrows.append(creat)
    #     finish_node.terminating_arrows.append(creat)
    #     if dict_forward.get(ending_node) is None:
    #         dict_forward[ending_node]=1
    #     else:
    #         dict_forward[ending_node]=dict_forward[ending_node]+1
    #     if dict_backward.get(finish_node) is None:
    #         dict_backward[finish_node]=1
    #     else:
    #         dict_backward[finish_node]=dict_backward[finish_node]+1
    
    # dict_forward[finish_node]=0
    
    # return start_node,dict_forward,dict_backward

    states: Dict[str, NodeState] = {}
    start_node = NodeState('start', [],[])
    states['[]'] = start_node
    ending_nodes: List[NodeState] = [start_node]

    dict_forward: Dict[NodeState,int]={}
    dict_backward:Dict[NodeState,int]={}

    dict_backward[start_node]=0

    for index, activity in enumerate(activity_data):
        state_key = json.dumps(activity.predecessors_indices)
        state = states.get(state_key)
        
        if not state:
            state = NodeState(state_key, [],[])
            states[state_key] = state
            for predecessor_index in activity.predecessors_indices:
                temp = states.get(f'[{predecessor_index}]')
                if temp and len(temp.emerging_arrows) == 0:
                    ending_nodes = [node for node in ending_nodes if node != temp]
                if temp:
                    new_dummy=DashedArrow(state,temp,None,None,None,None)
                    temp.emerging_arrows.append(new_dummy)
                    state.terminating_arrows.append(new_dummy)
                    if dict_forward.get(temp) is None:
                        dict_forward[temp]=1
                    else:
                        dict_forward[temp]=dict_forward[temp]+1
                    if dict_backward.get(state) is None:
                        dict_backward[state]=1
                    else:
                        dict_backward[state]=dict_backward[state]+1
                    
        dest_node = NodeState(f'[{index}]', [],[])
        ending_nodes.append(dest_node)
        states[f'[{index}]'] = dest_node
        
        if len(state.emerging_arrows) == 0:
            ending_nodes = [node for node in ending_nodes if node != state]
        
        new_activity=ArrowTask(activity.name, activity.duration, dest_node,state,None,None,None,None)
        state.emerging_arrows.append(new_activity)
        dest_node.terminating_arrows.append(new_activity)
        if dict_forward.get(state) is None:
            dict_forward[state]=1
        else:
            dict_forward[state]=dict_forward[state]+1
        if dict_backward.get(dest_node) is None:
            dict_backward[dest_node]=1
        else:
            dict_backward[dest_node]=dict_backward[dest_node]+1
    
    finish_node = NodeState('finish', [],[])
    for ending_node in ending_nodes:
        creat=DashedArrow(finish_node,ending_node,None,None,None,None)
        ending_node.emerging_arrows.append(creat)
        finish_node.terminating_arrows.append(creat)
        if dict_forward.get(ending_node) is None:
            dict_forward[ending_node]=1
        else:
            dict_forward[ending_node]=dict_forward[ending_node]+1
        if dict_backward.get(finish_node) is None:
            dict_backward[finish_node]=1
        else:
            dict_backward[finish_node]=dict_backward[finish_node]+1
    
    dict_forward[finish_node]=0
    node = start_node
    nodes = list(dict_forward.keys())
    node_indices = {node: i for i, node in enumerate(nodes)}
    
    # Initialize an empty adjacency matrix
    size = len(nodes)
    adjacency_matrix = np.zeros((size, size), dtype=int)
    
    # Fill the adjacency matrix
    def visit(node: NodeState):
        node_index = node_indices[node]
        for arrow in node.emerging_arrows:
            dest_index = node_indices[arrow.destination_node]
            if isinstance(arrow, ArrowTask):
                adjacency_matrix[node_index, dest_index] = 1
            elif isinstance(arrow, DashedArrow):
                adjacency_matrix[node_index, dest_index] = 2
            visit(arrow.destination_node)
    
    visit(start_node)
    
    a1 = []
    a2 = []
    a3 = []
    n = len(adjacency_matrix)

    def get_indexes(lst, element):
      return [index for index, value in enumerate(lst) if value == element]
    
    for j in range(n-1):
            q = get_indexes(list(adjacency_matrix[:,j]), 2)
            if len(q)!= 0:
                a7 = False
                for i in range(len(q)):
                    
                    if 1 not in adjacency_matrix[q[i], :]:
                        if  a7 == False: 
                          a1.append([q[i], j])
                          a7 = True
                          for e in range(len(q)):
                            if e!=i:
                                a2.append([q[e], j])
                                a3.append([q[e], q[i]])

    def find_key(d, target_value):
      for key, value in d.items():
        if value == target_value:
            return key
        
    def find_arrow(node1: NodeState, node2: NodeState) -> Optional[Union[ArrowTask, DashedArrow]]:
        for arrow in node1.emerging_arrows:
          if arrow.destination_node == node2:
            return arrow
          
    def check_arrow(node1: NodeState, node2: NodeState) -> Optional[Union[ArrowTask, DashedArrow]]:
        for arrow in node1.emerging_arrows:
          if arrow.destination_node == node2:
            return True
        return False
    
    for i in range(len(a2)):
        node1 = find_key(node_indices, a2[i][0])
        node2= find_key(node_indices, a2[i][1])
        arrow = find_arrow(node1, node2)
        node1.emerging_arrows.remove(arrow)
        node2.terminating_arrows.remove(arrow)
        if dict_forward.get(node1) == 1:
            dict_forward[node1] = None
        else:
            dict_forward[node1] -= 1
    
        if dict_backward.get(node2) == 1:
            dict_backward[node2] = None
        else:
            dict_backward[node2] -= 1

    for i in range(len(a3)):
        node1 = find_key(node_indices, a3[i][0])
        node2= find_key(node_indices, a3[i][1])
        arrow = DashedArrow(node2, node1, None, None, None, None)
        node1.emerging_arrows.append(arrow)
        node2.terminating_arrows.append(arrow)
        if dict_forward.get(node1) is None:
            dict_forward[node1] = 1
        else:
            dict_forward[node1] += 1
    
       # Increment dict_backward for node2
        if dict_backward.get(node2) is None:
            dict_backward[node2] = 1
        else:
            dict_backward[node2] += 1

    def w1(n):
      for a in n:
        if a.name == "finish":
            return a
        
    for i in range(len(a1)):
        node1 = find_key(node_indices, a1[i][0])
        node2= find_key(node_indices, a1[i][1])
        emerging_arrow = find_arrow(node1, node2)
        terminating_arrow = node2.emerging_arrows[0]
        destination_node=terminating_arrow.destination_node
        new_arrow = ArrowTask(
                    activity_name=terminating_arrow.activity_name,
                    duration=terminating_arrow.duration,
                    starting_node=node1,
                    destination_node=terminating_arrow.destination_node,
                    early_start=terminating_arrow.early_start,
                    early_finish=terminating_arrow.early_finish,
                    late_start=terminating_arrow.late_start,
                    late_finish=terminating_arrow.late_finish
                )

        node1.emerging_arrows.append(new_arrow)
        node1.emerging_arrows.remove(emerging_arrow)
                
        new_arrow.destination_node.terminating_arrows.append(new_arrow)
        new_arrow.destination_node.terminating_arrows.remove(terminating_arrow)

        if node2 in dict_forward:
            del dict_forward[node2]
        if node2 in dict_backward:
            del dict_backward[node2]

    visited = set()

    def visit(node: NodeState):
        if node in visited:
            return
        visited.add(node)
        # Check conditions for single emerging and terminating arrows
        if len(node.emerging_arrows) == 1 and len(node.terminating_arrows) == 1:
          emerging_arrow = node.emerging_arrows[0]
          terminating_arrow = node.terminating_arrows[0]
          if emerging_arrow.destination_node ==w1(node_indices) :
          
            # Get the single emerging and terminating arrows

            # Create a new ArrowTask connecting the start of the emerging_arrow to the end of the terminating_arrow
              if isinstance(emerging_arrow, DashedArrow) and isinstance(terminating_arrow, ArrowTask):
                new_arrow = ArrowTask(
                    activity_name=terminating_arrow.activity_name,
                    duration=terminating_arrow.duration,
                    starting_node=terminating_arrow.starting_node,
                    destination_node=emerging_arrow.destination_node,
                    early_start=terminating_arrow.early_start,
                    early_finish=terminating_arrow.early_finish,
                    late_start=terminating_arrow.late_start,
                    late_finish=terminating_arrow.late_finish
                )

                # Update the links to point to the new ArrowTask
                new_arrow.starting_node.emerging_arrows.append(new_arrow)
                new_arrow.starting_node.emerging_arrows.remove(terminating_arrow)
                
                new_arrow.destination_node.terminating_arrows.append(new_arrow)
                new_arrow.destination_node.terminating_arrows.remove(emerging_arrow)

                # Remove the current node from the graph
                if node in dict_forward:
                    del dict_forward[node]
                if node in dict_backward:
                    del dict_backward[node]
            
          elif len(node.emerging_arrows) == 1 and len(node.terminating_arrows) == 1 :
          
            # Get the single emerging and terminating arrows
            if (check_arrow(terminating_arrow.starting_node, emerging_arrow.destination_node) ==False):

            # Create a new ArrowTask connecting the start of the emerging_arrow to the end of the terminating_arrow
              if isinstance(emerging_arrow, DashedArrow) and isinstance(terminating_arrow, ArrowTask):
                new_arrow = ArrowTask(
                    activity_name=terminating_arrow.activity_name,
                    duration=terminating_arrow.duration,
                    starting_node=terminating_arrow.starting_node,
                    destination_node=emerging_arrow.destination_node,
                    early_start=terminating_arrow.early_start,
                    early_finish=terminating_arrow.early_finish,
                    late_start=terminating_arrow.late_start,
                    late_finish=terminating_arrow.late_finish
                )

                # Update the links to point to the new ArrowTask
                new_arrow.starting_node.emerging_arrows.append(new_arrow)
                new_arrow.starting_node.emerging_arrows.remove(terminating_arrow)
                
                new_arrow.destination_node.terminating_arrows.append(new_arrow)
                new_arrow.destination_node.terminating_arrows.remove(emerging_arrow)

                # Remove the current node from the graph
                if node in dict_forward:
                    del dict_forward[node]
                if node in dict_backward:
                    del dict_backward[node]

        for arrow in node.emerging_arrows[:]:
            visit(arrow.destination_node)

    visit(start_node)
    return start_node,dict_forward,dict_backward


def visualize_aoa(start_node: NodeState) -> Digraph:
    dot = Digraph(comment='Activity-on-Arrow (AOA) Network')
    dot.attr(rankdir='LR')
    visited = set()

    def visit(node: NodeState):
        if node.name in visited:
            return
        visited.add(node.name)

        for arrow in node.emerging_arrows:
            if isinstance(arrow, ArrowTask):
                # Add edge with taillabel for start dates and headlabel for finish dates
                dot.edge(
                    node.name, arrow.destination_node.name,
                    label=f'{arrow.activity_name} ({arrow.duration})',
                    taillabel=f' ES: {arrow.early_start}\n  LS: {arrow.late_start}',  # Early start and late start dates near tail
                    headlabel=f'EF: {arrow.early_finish}\nLF: {arrow.late_finish}',  # Early finish and late finish dates near head
                    fontsize='15',  # Decrease the font size of the labels
                    minlen='8',  # Increase the minimum length of the edge
                    labelfontsize='12',  # Font size for the tail and head labels
                    labeldistance='5',  # Distance for the tail and head labels
                    labelfloat='false',  # Ensure the label is not floating
                    labelangle='0'  # Keep angle 0 for the labels
                )
            elif isinstance(arrow, DashedArrow):
                dot.edge(node.name, arrow.destination_node.name, style='dashed',
                    taillabel=f' ES: {arrow.early_start}\n  LS: {arrow.late_start}',  # Early start and late start dates near tail
                    headlabel=f'EF: {arrow.early_finish}\nLF:{arrow.late_finish}',  # Early finish and late finish dates near head
                    fontsize='10',  # Decrease the font size of the labels
                    minlen='9',  # Increase the minimum length of the edge
                    labelfontsize='12',  # Font size for the tail and head labels
                    labeldistance='5',  # Distance for the tail and head labels
                    labelfloat='false',  # Ensure the label is not floating
                    labelangle='0'  # Keep angle 0 for the labels
                    )

            visit(arrow.destination_node)

    visit(start_node)
    return dot

def visualize_aoa2(start_node: NodeState) -> Digraph:
    dot = Digraph(comment='Activity-on-Arrow (AOA) Network')
    dot.attr(rankdir='LR')
    visited = set()

    def visit(node: NodeState):
        if node.name in visited:
            return
        visited.add(node.name)

        for arrow in node.emerging_arrows:
            if isinstance(arrow, ArrowTask):
                dot.edge(node.name, arrow.destination_node.name, label=f'{arrow.activity_name} ({arrow.duration})')
            elif isinstance(arrow, DashedArrow):
                dot.edge(node.name, arrow.destination_node.name, style='dashed')

            visit(arrow.destination_node)

    visit(start_node)
    return dot

def find_longest_path(start_node: NodeState) -> List[NodeState]:
    def dfs(node: NodeState, current_path: List[NodeState], current_duration: int) -> None:
        nonlocal longest_duration, longest_path

        if not node.emerging_arrows:
            if current_duration > longest_duration:
                longest_duration = current_duration
                longest_path = current_path[:]
            return

        for arrow in node.emerging_arrows:
            if isinstance(arrow, ArrowTask):
                dfs(arrow.destination_node, current_path + [arrow.destination_node], current_duration + arrow.duration)
            else:
                dfs(arrow.destination_node, current_path + [arrow.destination_node], current_duration)

    longest_duration = 0
    longest_path = []
    dfs(start_node, [start_node], 0)
    return longest_path,longest_duration

def critical_path_both(start_node: NodeState, longest_path: Optional[List[NodeState]] = None) -> Digraph:
    dot = Digraph(comment='Critical Path Activity-on-Arrow (AOA) Network')
    dot.attr(rankdir='LR')
    visited = set()
    longest_path_set = set(node.name for node in longest_path) if longest_path else set()

    def visit(node: NodeState):
        if node.name in visited:
            return
        visited.add(node.name)

        for arrow in node.emerging_arrows:
            color = 'red' if arrow.destination_node.name in longest_path_set else 'black'
            style = 'bold' if arrow.destination_node.name in longest_path_set else 'solid'
            if isinstance(arrow, ArrowTask):
                dot.edge(node.name, arrow.destination_node.name, label=f'{arrow.activity_name} ({arrow.duration})', color=color, style=style)
            elif isinstance(arrow, DashedArrow):
                dot.edge(node.name, arrow.destination_node.name, style='dashed')

            visit(arrow.destination_node)

    visit(start_node)
    return dot

def critical_path_both2(start_node: NodeState, longest_path: Optional[List[NodeState]] = None) -> Digraph:
    dot = Digraph(comment='Critical Path Activity-on-Arrow (AOA) Network')
    dot.attr(rankdir='LR')
    visited = set()
    longest_path_set = set(node.name for node in longest_path) if longest_path else set()

    def visit(node: NodeState):
        if node.name in visited:
            return
        visited.add(node.name)

        for arrow in node.emerging_arrows:
            color = 'red' if arrow.destination_node.name in longest_path_set else 'black'
            style = 'bold' if arrow.destination_node.name in longest_path_set else 'solid'
            if isinstance(arrow, ArrowTask):
                # Add edge with taillabel for start dates and headlabel for finish dates
                dot.edge(
                    node.name, arrow.destination_node.name,
                    color=color,
                    style=style,
                    label=f'{arrow.activity_name} ({arrow.duration})',
                    taillabel=f' ES: {arrow.early_start}\n  LS: {arrow.late_start}',  # Early start and late start dates near tail
                    headlabel=f'EF: {arrow.early_finish}\nLF: {arrow.late_finish}',  # Early finish and late finish dates near head
                    fontsize='15',  # Decrease the font size of the labels
                    minlen='8',  # Increase the minimum length of the edge
                    labelfontsize='12',  # Font size for the tail and head labels
                    labeldistance='5',  # Distance for the tail and head labels
                    labelfloat='false',  # Ensure the label is not floating
                    labelangle='0'  # Keep angle 0 for the labels
                )
            elif isinstance(arrow, DashedArrow):
                dot.edge(node.name, arrow.destination_node.name, style='dashed',
                    taillabel=f' ES: {arrow.early_start}\n  LS: {arrow.late_start}',  # Early start and late start dates near tail
                    headlabel=f'EF: {arrow.early_finish}\nLF:{arrow.late_finish}',  # Early finish and late finish dates near head
                    fontsize='10',  # Decrease the font size of the labels
                    minlen='9',  # Increase the minimum length of the edge
                    labelfontsize='12',  # Font size for the tail and head labels
                    labeldistance='5',  # Distance for the tail and head labels
                    labelfloat='false',  # Ensure the label is not floating
                    labelangle='0'  # Keep angle 0 for the labels
                    )

            visit(arrow.destination_node)

    visit(start_node)
    return dot


# Example usage with sample data
# activity_data = [
#     Activity(id=1,name='e', duration=1, predecessors_indices=[]),
#     Activity(id=1,name='r', duration=2, predecessors_indices=[0]),
#     Activity(id=1,name='t', duration=3, predecessors_indices=[0]),
#     Activity(id=1,name='y', duration=4, predecessors_indices=[1])
#     # Activity(id=1,name='E', duration=5, predecessors_indices=[1]),
#     # Activity(id=1,name='F', duration=4, predecessors_indices=[3, 4]),
#     # Activity(id=1,name='G', duration=6, predecessors_indices=[2, 4]),
#     # Activity(id=1,name='H', duration=6, predecessors_indices=[3, 6]),
#     # Activity(id=1,name='I', duration=2, predecessors_indices=[5]),
#     # Activity(id=1,name='J', duration=3, predecessors_indices=[5, 7])
# ]

# start_node,forward,backward = get_aoa_data_structure(activity_data)
# dot = visualize_aoa(start_node)

# # print(forward[start_node])
# for key,val in forward.items():
#     print(key.name,"->",val)

# for key,val in backward.items():
#     print(key.name,"->",val)
# # print(backward[finish_node])
# # # Render the graph to a file and view it
# dot.render('aoa_network2', format='png')

# start_date = date(2024, 4, 10)
# end_date = date(2024, 5, 6)

# timeline_dot = create_timeline(start_date, end_date)
# timeline_dot.render('timeline', format='png', cleanup=True)


from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, List, Dict
from math import log2
from learning.util import Algorithm, AlgorithmRegistry

Example = Dict[str, Any]
Examples = List[Example]

from logging import getLogger

logger = getLogger(__name__)


@dataclass(frozen=True)
class AttrLogicExpression(ABC):
    """
    Abstract base class representing a logic expression.
    """
    ...

    @abstractmethod
    def __call__(self, *args, **kwargs):
        ...


@dataclass(frozen=True)
class Conjunction(AttrLogicExpression):
    """
    A configuration of attribute names and the values the attributes should take for this conjunction to evaluate
    to true.

    `attribute_confs` is a map from attribute names to their values.
    """
    attribute_confs: Dict[str, Any]

    def __post_init__(self):
        assert 'target' not in self.attribute_confs, "Nice try, but 'target' cannot be part of the hypothesis."

    def __call__(self, example: Example):
        """
        Evaluates whether the conjunction applies to an example or not. Returns true if it does, false otherwise.


        Args:
            example: Example to check if the conjunction applies.

        Returns:
            True if the values of *all* attributes mentioned in the conjunction and appearing in example are equal,
            false otherwise.


        """
        return all(self.attribute_confs[k] == example[k] for k in set(self.attribute_confs).intersection(example))

    def __repr__(self):
        return " AND ".join(f"{k} = {v}" for k, v in self.attribute_confs.items())


@dataclass(frozen=True)
class Disjunction(AttrLogicExpression):
    """
    Disjunction of conjunctions.
    """
    conjunctions: List[Conjunction]

    def __call__(self, example: Example):
        """
        Evaluates whether the disjunction applies to a given example.

        Args:
            example: Example to check if the disjunction applies.

        Returns: True if any of its conjunctions returns true, and false if none evaluates to true.

        """
        return any(c(example) for c in self.conjunctions)

    def __repr__(self):
        return " " + "\nOR\n ".join(f"{v}" for v in self.conjunctions)


class Tree(ABC):
    """
    This is an abstract base class representing a leaf or a node in a tree.
    """
    ...


@dataclass
class Leaf(Tree):
    """
    This is a leaf in the tree. It's value is the (binary) classification, either True or False.
    """
    target: bool


@dataclass
class Node(Tree):
    """
    This is a node in the tree. It contains the attribute `attr_name` which the node is splitting on and a dictionary
    `branches` that represents the children of the node and maps from attribute values to their corresponding subtrees.
    """
    attr_name: str
    branches: Dict[Any, Tree] = field(default_factory=dict)


def same_target(examples: Examples) -> bool:
    """
    This function checks whether the examples all have the same target.

    Args:
        examples: Observations to check

    Returns: Whether the examples all have the same target.
    """
    if not examples:
        return True
    target_value = examples[0]['target']
    for example in examples[1:]:
        if example['target'] != target_value:
            return False
    return True



def plurality_value(examples: Examples) -> bool:
    """
    This function returns whether there are more positively or negatively classified examples in the dataset.
    Args:
        examples: Examples to check.

    Returns: True if more examples classified as positive, False otherwise.

    """
    if not examples:
        return None
    targets = [example['target'] for example in examples]
    return max(set(targets), key=targets.count)
    


def binary_entropy(examples: Examples) -> float:
    """
    Calculates the binary (shannon) entropy of a dataset regarding its classification.
    Args:
        examples: Dataset to calculate the shannon entropy.

    Returns: The shannon entropy of the classification of the dataset.

    """
    print(examples)
    if len(examples) == 0:
        return 0.0

    num_pos = sum(1 for example in examples if example['target'] == True)
    num_neg = sum(1 for example in examples if example['target'] == False)
    total = len(examples)

    if num_pos == 0 or num_neg == 0:
        return 0.0

    p_pos = num_pos / total
    p_neg = num_neg / total

    entropy = -p_pos * log2(p_pos) - p_neg * log2(p_neg)

    return entropy
    


def to_logic_expression(tree: Tree) -> AttrLogicExpression:
    """
    Converts a Decision tree to its equivalent logic expression.
    Args:
        tree: Tree to convert.

    Returns: The corresponding logic expression consisting of attribute values, conjunctions and disjunctions.

    """
    paths = defaultdict(list)
    
    def dfs(node, path):
        if not node:
            return
        if isinstance(node, Leaf):
            paths[node.target].append(path)
            return
        attr = node.attr_name
        for val, child in node.branches.items():
            dfs(child, path + [(attr, val)])
            
    dfs(tree, [])
    
    disjunctions = []
    for label, conjunctions in paths.items():
        conjunctions = [Conjunction([attr_val_pair for attr_val_pair in c]) for c in sorted(conjunctions, key=lambda x: [x[i][0] for i in range(len(x))])]
        disjunctions.append(Disjunction(conjunctions))
    
    return disjunctions
    
    raise NotImplementedError()
    


@AlgorithmRegistry.register("dtl")
class DecisionTreeLearner(Algorithm):
    """
    This is the decision tree learning algorithm.
    """

    def find_hypothesis(self) -> AttrLogicExpression:
        tree = self.decision_tree_learning(examples=self.dataset.examples, attributes=self.dataset.attributes,
                                           parent_examples=[])
        return to_logic_expression(tree)

    def decision_tree_learning(self, examples: Examples, attributes: List[str], parent_examples: Examples) -> Tree:
        """
        This is the main function that learns a decision tree given a list of example and attributes.
        Args:
            examples: The training dataset to induce the tree from.
            attributes: Attributes of the examples.
            parent_examples: Examples from previous step.

        Returns: A decision tree induced from the given dataset.
        """

    def get_most_important_attribute(self, attributes: List[str], examples: Examples) -> str:
        """
        Returns the most important attribute according to the information gain measure.
        Args:
            attributes: The attributes to choose the most important attribute from.
            examples: Dataset from which the most important attribute is to be inferred.

        Returns: The most informative attribute according to the dataset.

        """

        information_gains = {attr: self.information_gain(examples, attr) for attr in attributes}
        return max(information_gains, key=information_gains.get)


    def information_gain(self, examples: Examples, attribute: str) -> float:
        """
        This method calculates the information gain (as presented in the lecture)
        of an attribute according to given observations.

        Args:
            examples: Dataset to infer the information gain from.
            attribute: Attribute to infer the information gain for.

        Returns: The information gain of the given attribute according to the given observations.

        """
        total_entropy = binary_entropy(examples)
        attribute_values = set([e[attribute] for e in examples])
        subset_entropies = []
        for value in attribute_values:
            subset = [e for e in examples if e[attribute] == value]
            subset_entropy = binary_entropy(subset)
            subset_weight = len(subset) / len(examples)
            subset_entropies.append(subset_weight * subset_entropy)
        return total_entropy - sum(subset_entropies)


@AlgorithmRegistry.register("your-algo-name")
class MyDecisionTreeLearner(DecisionTreeLearner):
    ...

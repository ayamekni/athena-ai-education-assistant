"""
Static Quiz Generator Service
Generates fake quiz data in the format expected by the frontend
"""

import uuid
from typing import List, Dict
from datetime import datetime


class QuizQuestion:
    def __init__(
        self,
        question_id: int,
        question_text: str,
        options: List[str],
        correct_answer: str,
        explanation: str,
        difficulty: str,
    ):
        self.question_id = question_id
        self.question_text = question_text
        self.options = options
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.difficulty = difficulty

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "question_text": self.question_text,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "difficulty": self.difficulty,
        }


class QuizResponse:
    def __init__(
        self,
        quiz_id: str,
        topic: str,
        num_questions: int,
        questions: List[QuizQuestion],
        context_used: str = "Static Data Generator",
    ):
        self.quiz_id = quiz_id
        self.topic = topic
        self.num_questions = num_questions
        self.questions = questions
        self.context_used = context_used
        self.formatted_display = self._generate_formatted_display()

    def _generate_formatted_display(self) -> str:
        """Generate a formatted string representation of the quiz"""
        display = f"# {self.topic} Quiz\n\n"
        display += f"**Total Questions:** {self.num_questions}\n\n"

        for q in self.questions:
            display += f"**{q.question_id}. {q.question_text}**\n"
            display += f"*Difficulty: {q.difficulty}*\n\n"
            for i, option in enumerate(q.options):
                display += f"   {chr(65 + i)}) {option}\n"
            display += f"\n**Correct Answer:** {q.correct_answer}\n"
            display += f"**Explanation:** {q.explanation}\n\n"
            display += "---\n\n"

        return display

    def to_dict(self):
        return {
            "quiz_id": self.quiz_id,
            "topic": self.topic,
            "num_questions": self.num_questions,
            "questions": [q.to_dict() for q in self.questions],
            "formatted_display": self.formatted_display,
            "context_used": self.context_used,
        }


# ==================== PYTHON QUIZZES ====================
PYTHON_QUIZZES = {
    "easy": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What is the output of print(type([]))?",
                options=[
                    "<class 'list'>",
                    "<class 'array'>",
                    "<class 'collection'>",
                    "<class 'tuple'>",
                ],
                correct_answer="<class 'list'>",
                explanation="The type() function returns the class of an object. An empty bracket [] creates a list, so type([]) returns <class 'list'>.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=2,
                question_text="Which of the following is NOT a Python data type?",
                options=["int", "string", "float", "list"],
                correct_answer="string",
                explanation="Python has 'str' (string) as a data type, not 'string'. The other three are valid data types.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What does len('Python') return?",
                options=["5", "6", "7", "Error"],
                correct_answer="6",
                explanation="The len() function returns the number of characters in a string. 'Python' has 6 characters: P-y-t-h-o-n.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=4,
                question_text="How do you create a comment in Python?",
                options=["# comment", "// comment", "/* comment */", "-- comment"],
                correct_answer="# comment",
                explanation="Python uses the hash symbol (#) to denote a single-line comment.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is the result of 5 // 2 in Python?",
                options=["2.5", "2", "3", "Error"],
                correct_answer="2",
                explanation="The // operator performs floor division, which divides and rounds down to the nearest integer. 5 // 2 = 2.",
                difficulty="easy",
            ),
        ],
        [
            QuizQuestion(
                question_id=1,
                question_text="What keyword is used to create a function in Python?",
                options=["function", "def", "define", "func"],
                correct_answer="def",
                explanation="Python uses the 'def' keyword to define a function.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=2,
                question_text="Which of the following creates a dictionary?",
                options=["{}", "[]", "()", "set()"],
                correct_answer="{}",
                explanation="An empty dictionary is created using curly braces {}. [] creates a list, () creates a tuple, and set() creates a set.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What does the range(5) function produce?",
                options=[
                    "[0, 1, 2, 3, 4, 5]",
                    "[1, 2, 3, 4, 5]",
                    "[0, 1, 2, 3, 4]",
                    "(0, 1, 2, 3, 4)",
                ],
                correct_answer="[0, 1, 2, 3, 4]",
                explanation="range(5) produces numbers from 0 to 4 (not including 5). When converted to a list, it becomes [0, 1, 2, 3, 4].",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=4,
                question_text="How do you access the last item in a list named 'items'?",
                options=["items[last]", "items[-1]", "items[len(items)]", "items.last()"],
                correct_answer="items[-1]",
                explanation="In Python, negative indexing starts from the end of the list. -1 refers to the last item.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is the correct syntax for a for loop?",
                options=[
                    "for i = 0; i < 5; i++",
                    "for (i in range(5))",
                    "for i in range(5):",
                    "for i < 5:",
                ],
                correct_answer="for i in range(5):",
                explanation="Python uses the syntax 'for variable in iterable:' for loops, with a colon at the end.",
                difficulty="easy",
            ),
        ],
    ],
    "medium": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What is the difference between a list and a tuple in Python?",
                options=[
                    "Lists are immutable, tuples are mutable",
                    "Lists are mutable, tuples are immutable",
                    "There is no difference",
                    "Tuples are slower than lists",
                ],
                correct_answer="Lists are mutable, tuples are immutable",
                explanation="Lists can be modified after creation (mutable), while tuples cannot be changed once created (immutable).",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=2,
                question_text="What does the *args parameter allow in a function?",
                options=[
                    "Named keyword arguments",
                    "Variable number of positional arguments",
                    "Default arguments",
                    "Arguments with asterisks",
                ],
                correct_answer="Variable number of positional arguments",
                explanation="*args allows a function to accept a variable number of non-keyword arguments.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=3,
                question_text="Which method removes and returns the last item from a list?",
                options=["remove()", "delete()", "pop()", "discard()"],
                correct_answer="pop()",
                explanation="The pop() method removes and returns the last item from a list. remove() removes by value, not by position.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What is a lambda function in Python?",
                options=[
                    "A function that returns a lambda value",
                    "An anonymous function with a single expression",
                    "A function defined in a library",
                    "A deprecated function",
                ],
                correct_answer="An anonymous function with a single expression",
                explanation="Lambda functions are anonymous functions defined with the lambda keyword that can have any number of arguments but only one expression.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What does list comprehension do?",
                options=[
                    "Compresses a list",
                    "Creates a new list by applying an expression to each item",
                    "Compares two lists",
                    "Organizes list elements",
                ],
                correct_answer="Creates a new list by applying an expression to each item",
                explanation="List comprehension is a concise way to create a new list by applying a function to every item in an iterable.",
                difficulty="medium",
            ),
        ],
        [
            QuizQuestion(
                question_id=1,
                question_text="What is the output of 'hello'.upper()?",
                options=["'HELLO'", "'Hello'", "'HELLO", "Error"],
                correct_answer="'HELLO'",
                explanation="The upper() method returns a string in uppercase. 'hello'.upper() returns 'HELLO'.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=2,
                question_text="How do you check if a key exists in a dictionary?",
                options=[
                    "if dict.key:",
                    "if key in dict:",
                    "if dict.has_key(key):",
                    "if key == dict:",
                ],
                correct_answer="if key in dict:",
                explanation="The 'in' operator checks if a key exists in a dictionary.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What is the purpose of the __init__ method in a class?",
                options=[
                    "Initialize imports",
                    "Initialize the class object (constructor)",
                    "Initialize the module",
                    "Initialize global variables",
                ],
                correct_answer="Initialize the class object (constructor)",
                explanation="The __init__ method is a constructor that initializes a new instance of a class.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What does the zip() function do?",
                options=[
                    "Compresses files",
                    "Combines multiple iterables element-wise",
                    "Sorts elements",
                    "Filters elements",
                ],
                correct_answer="Combines multiple iterables element-wise",
                explanation="zip() takes multiple iterables and combines them element-wise, returning an iterator of tuples.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is the difference between == and is?",
                options=[
                    "No difference",
                    "== checks value, is checks identity/reference",
                    "is checks value, == checks identity",
                    "is is deprecated",
                ],
                correct_answer="== checks value, is checks identity/reference",
                explanation="== compares values, while 'is' checks if two variables refer to the same object in memory.",
                difficulty="medium",
            ),
        ],
    ],
    "hard": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What is the time complexity of searching in a dictionary?",
                options=["O(n)", "O(log n)", "O(1)", "O(n log n)"],
                correct_answer="O(1)",
                explanation="Dictionary lookups are O(1) average case because they use hash tables for fast key access.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=2,
                question_text="What is a generator in Python?",
                options=[
                    "A function that generates random numbers",
                    "A function that returns a sequence of values one at a time using yield",
                    "A tool for creating lists",
                    "A library for data generation",
                ],
                correct_answer="A function that returns a sequence of values one at a time using yield",
                explanation="A generator is a function that uses 'yield' to return values one at a time, creating an iterator that is memory efficient.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What is the purpose of the @property decorator?",
                options=[
                    "Declare a class property",
                    "Make a method work like an attribute",
                    "Create a private variable",
                    "Define a static method",
                ],
                correct_answer="Make a method work like an attribute",
                explanation="@property allows you to access a method like an attribute without calling it as a function.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What is monkey patching?",
                options=[
                    "Fixing bugs in a program",
                    "Dynamically modifying or extending code at runtime",
                    "Patching security vulnerabilities",
                    "Optimizing code performance",
                ],
                correct_answer="Dynamically modifying or extending code at runtime",
                explanation="Monkey patching is the technique of modifying or extending classes and functions at runtime.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What does the GIL (Global Interpreter Lock) prevent?",
                options=[
                    "Code from running",
                    "Multiple threads from executing Python bytecode simultaneously",
                    "Imports from working",
                    "Object creation",
                ],
                correct_answer="Multiple threads from executing Python bytecode simultaneously",
                explanation="The GIL ensures that only one thread executes Python bytecode at a time, even on multi-core processors.",
                difficulty="hard",
            ),
        ],
    ],
}

# ==================== MACHINE LEARNING QUIZZES ====================
MACHINE_LEARNING_QUIZZES = {
    "easy": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What is supervised learning?",
                options=[
                    "Learning without any labels",
                    "Learning with labeled training data",
                    "Learning by watching humans",
                    "Learning from supervisors",
                ],
                correct_answer="Learning with labeled training data",
                explanation="Supervised learning uses labeled training data where the target output is known.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=2,
                question_text="What is the main goal of regression?",
                options=[
                    "Classify data into categories",
                    "Predict continuous values",
                    "Find patterns in data",
                    "Reduce dimensions",
                ],
                correct_answer="Predict continuous values",
                explanation="Regression is used to predict continuous values, like price or temperature.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What is a decision tree?",
                options=[
                    "A tree in a forest",
                    "A flowchart of decisions for classification",
                    "A data structure for storage",
                    "A type of neural network",
                ],
                correct_answer="A flowchart of decisions for classification",
                explanation="A decision tree is a flowchart-like model that makes decisions based on feature values.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What does SVM stand for?",
                options=[
                    "Support Vector Machine",
                    "Supervised Vector Model",
                    "Statistical Vector Method",
                    "Support Validation Model",
                ],
                correct_answer="Support Vector Machine",
                explanation="SVM (Support Vector Machine) is a supervised learning algorithm used for classification and regression.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is a feature in machine learning?",
                options=[
                    "A characteristic or property of the data",
                    "A machine learning library",
                    "A type of algorithm",
                    "A neural network layer",
                ],
                correct_answer="A characteristic or property of the data",
                explanation="Features are the input variables or characteristics used to make predictions.",
                difficulty="easy",
            ),
        ],
    ],
    "medium": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What is overfitting in machine learning?",
                options=[
                    "Using too much data",
                    "Model learning noise instead of pattern, performing well on training but poorly on test data",
                    "Training for too short",
                    "Using too many features",
                ],
                correct_answer="Model learning noise instead of pattern, performing well on training but poorly on test data",
                explanation="Overfitting occurs when a model memorizes training data including noise, leading to poor generalization.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=2,
                question_text="What is cross-validation used for?",
                options=[
                    "Validating data format",
                    "Assessing model performance on different data splits",
                    "Validating input data",
                    "Comparing models",
                ],
                correct_answer="Assessing model performance on different data splits",
                explanation="Cross-validation evaluates model performance by training and testing on different subsets of data.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What does accuracy measure?",
                options=[
                    "Speed of prediction",
                    "Percentage of correct predictions",
                    "Memory usage",
                    "Training time",
                ],
                correct_answer="Percentage of correct predictions",
                explanation="Accuracy is the ratio of correct predictions to total predictions.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What is regularization in machine learning?",
                options=[
                    "Regular model training",
                    "Technique to prevent overfitting by penalizing complex models",
                    "Training on regular intervals",
                    "Data standardization",
                ],
                correct_answer="Technique to prevent overfitting by penalizing complex models",
                explanation="Regularization adds penalties to complex models to prevent overfitting.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is the difference between L1 and L2 regularization?",
                options=[
                    "No difference",
                    "L1 uses absolute values, L2 uses squared values",
                    "L1 is for regression, L2 is for classification",
                    "L1 is faster than L2",
                ],
                correct_answer="L1 uses absolute values, L2 uses squared values",
                explanation="L1 (Lasso) uses sum of absolute values, L2 (Ridge) uses sum of squared values for penalties.",
                difficulty="medium",
            ),
        ],
    ],
    "hard": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What is the curse of dimensionality?",
                options=[
                    "Problems with high-dimensional data due to sparsity and distance metrics becoming less meaningful",
                    "A curse word in coding",
                    "Too many algorithms",
                    "Complexity of algorithms",
                ],
                correct_answer="Problems with high-dimensional data due to sparsity and distance metrics becoming less meaningful",
                explanation="As dimensions increase, data becomes sparse and distance metrics become less meaningful, affecting model performance.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=2,
                question_text="What is the purpose of gradient descent?",
                options=[
                    "Descending from mountains",
                    "Finding the minimum of a cost function by updating parameters",
                    "Sorting data in descending order",
                    "Calculating gradients",
                ],
                correct_answer="Finding the minimum of a cost function by updating parameters",
                explanation="Gradient descent is an optimization algorithm that finds the minimum of a cost function by iteratively updating parameters.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What is ensemble learning?",
                options=[
                    "Learning from an ensemble of data",
                    "Combining multiple models to make better predictions",
                    "A single large model",
                    "Training multiple times",
                ],
                correct_answer="Combining multiple models to make better predictions",
                explanation="Ensemble learning combines predictions from multiple models to improve overall performance.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What is the purpose of PCA (Principal Component Analysis)?",
                options=[
                    "Data analysis and visualization",
                    "Dimensionality reduction while preserving variance",
                    "Data cleaning",
                    "Feature scaling",
                ],
                correct_answer="Dimensionality reduction while preserving variance",
                explanation="PCA reduces dimensionality by finding principal components that capture maximum variance in data.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is a hyperparameter in machine learning?",
                options=[
                    "Parameter learned by the model",
                    "A parameter set before training, not learned from data",
                    "A very important parameter",
                    "A parameter of a hyperplane",
                ],
                correct_answer="A parameter set before training, not learned from data",
                explanation="Hyperparameters are parameters set before training (like learning rate, regularization strength) that are not learned from data.",
                difficulty="hard",
            ),
        ],
    ],
}

# ==================== DEEP LEARNING QUIZZES ====================
DEEP_LEARNING_QUIZZES = {
    "easy": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What is a neural network?",
                options=[
                    "A network of computers",
                    "A computational model inspired by biological neurons",
                    "A type of internet network",
                    "A network protocol",
                ],
                correct_answer="A computational model inspired by biological neurons",
                explanation="Neural networks are computational models inspired by how biological neurons work in the brain.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=2,
                question_text="What is a neuron in a neural network?",
                options=[
                    "A computer processor",
                    "A basic computing unit with weights and biases",
                    "A type of algorithm",
                    "A data point",
                ],
                correct_answer="A basic computing unit with weights and biases",
                explanation="A neuron is a basic computing unit that takes inputs, applies weights and biases, and produces an output.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What is an activation function?",
                options=[
                    "A function that activates neurons",
                    "A function that introduces non-linearity to the network",
                    "A function that activates the computer",
                    "A type of loss function",
                ],
                correct_answer="A function that introduces non-linearity to the network",
                explanation="Activation functions introduce non-linearity, allowing networks to learn complex patterns.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What does a convolutional layer do?",
                options=[
                    "Converts data format",
                    "Applies filters to extract features from input",
                    "Combines data",
                    "Normalizes data",
                ],
                correct_answer="Applies filters to extract features from input",
                explanation="Convolutional layers apply learnable filters to extract spatial features from input data.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is backpropagation?",
                options=[
                    "Going back in data",
                    "Algorithm to compute gradients and update weights",
                    "Reversing a process",
                    "Going backwards through layers",
                ],
                correct_answer="Algorithm to compute gradients and update weights",
                explanation="Backpropagation is an algorithm that computes gradients of the loss function with respect to weights and updates them.",
                difficulty="easy",
            ),
        ],
    ],
    "medium": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What is a CNN (Convolutional Neural Network)?",
                options=[
                    "A news network",
                    "A network with convolutional layers for processing grid-like data",
                    "A type of algorithm",
                    "A computer network",
                ],
                correct_answer="A network with convolutional layers for processing grid-like data",
                explanation="CNNs are networks with convolutional layers designed for processing images and other grid-like data.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=2,
                question_text="What does a pooling layer do?",
                options=[
                    "Combines data from multiple sources",
                    "Reduces spatial dimensions and highlights important features",
                    "Pools data together",
                    "Normalizes data",
                ],
                correct_answer="Reduces spatial dimensions and highlights important features",
                explanation="Pooling layers reduce spatial dimensions and retain the most important features.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What is a batch size in neural networks?",
                options=[
                    "The total amount of data",
                    "Number of samples processed before updating weights",
                    "Size of each batch file",
                    "Number of epochs",
                ],
                correct_answer="Number of samples processed before updating weights",
                explanation="Batch size is the number of samples processed in one forward-backward pass before updating weights.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What is dropout in neural networks?",
                options=[
                    "Dropping out of training",
                    "Technique to prevent overfitting by randomly disabling neurons",
                    "Removing data",
                    "Stopping training",
                ],
                correct_answer="Technique to prevent overfitting by randomly disabling neurons",
                explanation="Dropout randomly disables neurons during training to prevent co-adaptation and reduce overfitting.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is an RNN (Recurrent Neural Network)?",
                options=[
                    "A network that runs multiple times",
                    "Network with connections forming cycles for sequence processing",
                    "A network that repeats data",
                    "A random neural network",
                ],
                correct_answer="Network with connections forming cycles for sequence processing",
                explanation="RNNs have recurrent connections that allow them to process sequences and maintain memory.",
                difficulty="medium",
            ),
        ],
    ],
    "hard": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What is vanishing gradient problem?",
                options=[
                    "Gradients becoming too large",
                    "Gradients becoming too small, preventing weight updates in deep networks",
                    "Disappearing data",
                    "Convergence issues",
                ],
                correct_answer="Gradients becoming too small, preventing weight updates in deep networks",
                explanation="Vanishing gradient problem occurs when gradients become very small, making weight updates ineffective in deep networks.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=2,
                question_text="What is a LSTM (Long Short-Term Memory) cell?",
                options=[
                    "A long storage memory",
                    "RNN variant with gates to control information flow and handle long-term dependencies",
                    "A type of RAM",
                    "A storage device",
                ],
                correct_answer="RNN variant with gates to control information flow and handle long-term dependencies",
                explanation="LSTM cells have gates (forget, input, output) that control information flow, solving the vanishing gradient problem.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What is batch normalization?",
                options=[
                    "Normalizing batch data",
                    "Normalizing layer inputs to improve training stability",
                    "Organizing batches",
                    "Batch processing",
                ],
                correct_answer="Normalizing layer inputs to improve training stability",
                explanation="Batch normalization normalizes layer inputs during training, improving training speed and stability.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What is a residual connection (skip connection)?",
                options=[
                    "Leftover connections",
                    "Direct connection that allows gradients to skip layers",
                    "A type of layer",
                    "Backup connection",
                ],
                correct_answer="Direct connection that allows gradients to skip layers",
                explanation="Residual connections allow gradients to bypass layers, enabling very deep networks (ResNets).",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is the purpose of an attention mechanism?",
                options=[
                    "Making the network pay attention",
                    "Allowing model to focus on relevant parts of input",
                    "Monitoring training",
                    "Storing attention data",
                ],
                correct_answer="Allowing model to focus on relevant parts of input",
                explanation="Attention mechanisms allow models to dynamically focus on relevant parts of the input during processing.",
                difficulty="hard",
            ),
        ],
    ],
}

# ==================== NLP QUIZZES ====================
NLP_QUIZZES = {
    "easy": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What does NLP stand for?",
                options=[
                    "Network Language Processing",
                    "Natural Language Processing",
                    "Neural Learning Protocol",
                    "Numerical Language Program",
                ],
                correct_answer="Natural Language Processing",
                explanation="NLP (Natural Language Processing) is the field of AI that focuses on understanding and processing human language.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=2,
                question_text="What is tokenization in NLP?",
                options=[
                    "Converting tokens to words",
                    "Breaking text into words, phrases, or sentences",
                    "Encrypting text",
                    "Token generation",
                ],
                correct_answer="Breaking text into words, phrases, or sentences",
                explanation="Tokenization is the process of breaking text into smaller units like words or sentences.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What is stemming in NLP?",
                options=[
                    "Creating stems for plants",
                    "Reducing words to their root form",
                    "Organizing text",
                    "Text analysis",
                ],
                correct_answer="Reducing words to their root form",
                explanation="Stemming reduces words to their root form (e.g., 'running' -> 'run') to normalize text.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What is a stop word in NLP?",
                options=[
                    "A word that stops the program",
                    "Common words with little semantic value (like 'the', 'is')",
                    "A type of word",
                    "Important words",
                ],
                correct_answer="Common words with little semantic value (like 'the', 'is')",
                explanation="Stop words are common words that typically don't carry important meaning and are often filtered out.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is word embedding?",
                options=[
                    "Embedding words in sentences",
                    "Representing words as vectors in a continuous space",
                    "Embedding documents",
                    "Text storage",
                ],
                correct_answer="Representing words as vectors in a continuous space",
                explanation="Word embeddings represent words as dense vectors in a continuous space, capturing semantic relationships.",
                difficulty="easy",
            ),
        ],
    ],
    "medium": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What is lemmatization?",
                options=[
                    "Identifying words similar to lemmas",
                    "Reducing words to their dictionary form using grammatical rules",
                    "Removing lemmas",
                    "Text filtering",
                ],
                correct_answer="Reducing words to their dictionary form using grammatical rules",
                explanation="Lemmatization reduces words to their lemma (base form) using grammatical analysis.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=2,
                question_text="What is a bag of words model?",
                options=[
                    "A collection of word bags",
                    "Represents text by word frequencies, ignoring order",
                    "A storage method",
                    "A type of embedding",
                ],
                correct_answer="Represents text by word frequencies, ignoring order",
                explanation="Bag of words model represents text by counting word frequencies while ignoring word order.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What is TF-IDF?",
                options=[
                    "Text Frequency-Important Document Format",
                    "Term Frequency-Inverse Document Frequency, weighting scheme for text",
                    "A type of database",
                    "Text file format",
                ],
                correct_answer="Term Frequency-Inverse Document Frequency, weighting scheme for text",
                explanation="TF-IDF weights words based on their frequency in a document and rarity across documents.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What is named entity recognition (NER)?",
                options=[
                    "Recognizing entity names",
                    "Identifying and classifying named entities (persons, locations, etc.)",
                    "Naming entities",
                    "Entity recognition system",
                ],
                correct_answer="Identifying and classifying named entities (persons, locations, etc.)",
                explanation="NER identifies and classifies named entities like names, locations, and organizations in text.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is sentiment analysis?",
                options=[
                    "Analyzing emotions of people",
                    "Determining the sentiment or emotion expressed in text",
                    "Analyzing sentence structure",
                    "Text complexity analysis",
                ],
                correct_answer="Determining the sentiment or emotion expressed in text",
                explanation="Sentiment analysis determines whether text expresses positive, negative, or neutral sentiment.",
                difficulty="medium",
            ),
        ],
    ],
    "hard": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What is a Transformer in NLP?",
                options=[
                    "A device that transforms electricity",
                    "Architecture using self-attention for parallel processing of sequences",
                    "A type of embedding",
                    "A text converter",
                ],
                correct_answer="Architecture using self-attention for parallel processing of sequences",
                explanation="Transformers use self-attention mechanisms to process sequences in parallel, enabling models like BERT and GPT.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=2,
                question_text="What is BERT in NLP?",
                options=[
                    "A person's name",
                    "Bidirectional Encoder Representations from Transformers for contextual word embeddings",
                    "A text encoding method",
                    "A type of algorithm",
                ],
                correct_answer="Bidirectional Encoder Representations from Transformers for contextual word embeddings",
                explanation="BERT uses bidirectional transformers to create contextual word embeddings, pre-trained on large corpora.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What is self-attention?",
                options=[
                    "Attention to oneself",
                    "Mechanism allowing each element to interact with all other elements in sequence",
                    "A type of attention span",
                    "Attention to self-data",
                ],
                correct_answer="Mechanism allowing each element to interact with all other elements in sequence",
                explanation="Self-attention allows each position to attend to all other positions, computing relevance weights.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What is machine translation?",
                options=[
                    "Translating machine language",
                    "Automatically translating text from one language to another using ML",
                    "Moving machines",
                    "Language conversion",
                ],
                correct_answer="Automatically translating text from one language to another using ML",
                explanation="Machine translation uses neural networks to automatically translate text between languages.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is a language model?",
                options=[
                    "A model of language structure",
                    "Statistical model predicting probability of word sequences",
                    "A template for language",
                    "A language framework",
                ],
                correct_answer="Statistical model predicting probability of word sequences",
                explanation="Language models predict the probability of word sequences, used in text generation and completion.",
                difficulty="hard",
            ),
        ],
    ],
}

# ==================== COMPUTER VISION QUIZZES ====================
COMPUTER_VISION_QUIZZES = {
    "easy": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What is computer vision?",
                options=[
                    "Vision of computers",
                    "Field of AI that enables computers to interpret visual information",
                    "Computer graphics",
                    "Image storage",
                ],
                correct_answer="Field of AI that enables computers to interpret visual information",
                explanation="Computer vision is the field that focuses on enabling computers to understand and interpret visual data from images and videos.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=2,
                question_text="What is an image in computer vision?",
                options=[
                    "A visual representation",
                    "A 2D array of pixel values",
                    "A graphic",
                    "A picture file",
                ],
                correct_answer="A 2D array of pixel values",
                explanation="In computer vision, an image is represented as a 2D array of pixel values (grayscale) or multiple channels (color).",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What is a pixel?",
                options=[
                    "A small picture",
                    "The smallest unit of an image",
                    "A picture element",
                    "Both B and C",
                ],
                correct_answer="Both B and C",
                explanation="A pixel (picture element) is the smallest unit of an image, representing color or intensity at that location.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What is image classification?",
                options=[
                    "Organizing images into folders",
                    "Assigning labels or categories to images",
                    "Grouping similar images",
                    "Categorizing image types",
                ],
                correct_answer="Assigning labels or categories to images",
                explanation="Image classification assigns predefined labels or categories to images based on their visual content.",
                difficulty="easy",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is object detection?",
                options=[
                    "Detecting objects in real world",
                    "Identifying and locating objects within images",
                    "Detecting object materials",
                    "Object recognition",
                ],
                correct_answer="Identifying and locating objects within images",
                explanation="Object detection identifies and locates multiple objects within an image, typically using bounding boxes.",
                difficulty="easy",
            ),
        ],
    ],
    "medium": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What is image segmentation?",
                options=[
                    "Dividing images into parts",
                    "Partitioning image into pixel-level regions with labels",
                    "Cutting images",
                    "Image separation",
                ],
                correct_answer="Partitioning image into pixel-level regions with labels",
                explanation="Image segmentation divides an image into multiple regions or pixel groups with assigned labels.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=2,
                question_text="What is the difference between semantic and instance segmentation?",
                options=[
                    "No difference",
                    "Semantic: class labels, Instance: individual object labels",
                    "Instance: class labels, Semantic: individual object labels",
                    "Semantic is faster",
                ],
                correct_answer="Semantic: class labels, Instance: individual object labels",
                explanation="Semantic segmentation assigns class labels to pixels. Instance segmentation distinguishes individual objects of the same class.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What is an edge in image processing?",
                options=[
                    "The border of an image",
                    "Boundary between regions with different intensities",
                    "A sharp line",
                    "Part of image",
                ],
                correct_answer="Boundary between regions with different intensities",
                explanation="Edges are boundaries between regions with different intensity or color values in an image.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What is feature extraction in computer vision?",
                options=[
                    "Extracting features from data",
                    "Process of identifying and extracting relevant visual characteristics from images",
                    "Feature removal",
                    "Data extraction",
                ],
                correct_answer="Process of identifying and extracting relevant visual characteristics from images",
                explanation="Feature extraction identifies important visual characteristics like edges, textures, and colors from images.",
                difficulty="medium",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is a convolutional filter/kernel?",
                options=[
                    "A filtering device",
                    "Small matrix applied to image for feature extraction",
                    "A type of image",
                    "Data filter",
                ],
                correct_answer="Small matrix applied to image for feature extraction",
                explanation="A convolutional kernel is a small matrix that slides over an image to extract features through convolution operation.",
                difficulty="medium",
            ),
        ],
    ],
    "hard": [
        [
            QuizQuestion(
                question_id=1,
                question_text="What is the purpose of non-maximum suppression (NMS)?",
                options=[
                    "Suppressing non-maximum values",
                    "Removing overlapping bounding boxes, keeping highest confidence detections",
                    "Suppressing noise",
                    "Box optimization",
                ],
                correct_answer="Removing overlapping bounding boxes, keeping highest confidence detections",
                explanation="NMS removes overlapping bounding boxes, keeping the ones with highest confidence scores.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=2,
                question_text="What is Intersection over Union (IoU)?",
                options=[
                    "Intersection of unique elements",
                    "Ratio of intersection to union of two bounding boxes",
                    "A type of algorithm",
                    "Data union measure",
                ],
                correct_answer="Ratio of intersection to union of two bounding boxes",
                explanation="IoU measures overlap between predicted and ground truth bounding boxes: intersection/union.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=3,
                question_text="What is YOLO in object detection?",
                options=[
                    "You Only Learn Once",
                    "You Only Look Once - real-time object detection",
                    "A type of network",
                    "A detection method",
                ],
                correct_answer="You Only Look Once - real-time object detection",
                explanation="YOLO is a real-time object detection system that predicts bounding boxes and class probabilities in one pass.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=4,
                question_text="What is ROI pooling?",
                options=[
                    "Pooling regions of interest",
                    "Extracting fixed-size features from variable-size regions of interest",
                    "Region optimization",
                    "Feature pooling",
                ],
                correct_answer="Extracting fixed-size features from variable-size regions of interest",
                explanation="ROI pooling extracts fixed-size feature maps from variable-size regions of interest in an image.",
                difficulty="hard",
            ),
            QuizQuestion(
                question_id=5,
                question_text="What is pose estimation?",
                options=[
                    "Estimating pose of people",
                    "Detecting and localizing key points on human or object bodies",
                    "Position estimation",
                    "Spatial positioning",
                ],
                correct_answer="Detecting and localizing key points on human or object bodies",
                explanation="Pose estimation detects and localizes key body joints/points to determine body pose or shape.",
                difficulty="hard",
            ),
        ],
    ],
}

QUIZ_DATA_BY_TOPIC = {
    "python": PYTHON_QUIZZES,
    "machine learning": MACHINE_LEARNING_QUIZZES,
    "deep learning": DEEP_LEARNING_QUIZZES,
    "nlp": NLP_QUIZZES,
    "natural language processing": NLP_QUIZZES,
    "computer vision": COMPUTER_VISION_QUIZZES,
}


def generate_quiz(topic: str, num_questions: int = 10, difficulty: str = "mixed") -> QuizResponse:
    """
    Generate a quiz response for a given topic
    
    Args:
        topic: The quiz topic (python, machine learning, deep learning, nlp, computer vision)
        num_questions: Number of questions in the quiz (default 10)
        difficulty: Difficulty level (easy, medium, hard, mixed)
    
    Returns:
        QuizResponse object ready to be serialized to JSON
    """
    topic_lower = topic.lower()
    
    # Find the matching quiz data
    quiz_data = None
    matched_topic = None
    
    for key in QUIZ_DATA_BY_TOPIC.keys():
        if key in topic_lower or topic_lower in key:
            quiz_data = QUIZ_DATA_BY_TOPIC[key]
            matched_topic = key
            break
    
    if not quiz_data:
        raise ValueError(f"No quiz data available for topic: {topic}")
    
    # Get questions based on difficulty
    selected_questions = []
    
    if difficulty == "mixed":
        # Get a mix of difficulties
        for diff_level in ["easy", "medium", "hard"]:
            if diff_level in quiz_data and quiz_data[diff_level]:
                # Get first available question set for this difficulty
                question_set = quiz_data[diff_level][0]
                # Distribute questions across difficulties
                questions_per_difficulty = num_questions // 3
                selected_questions.extend(question_set[:questions_per_difficulty])
    else:
        # Get questions from specific difficulty
        if difficulty in quiz_data and quiz_data[difficulty]:
            question_set = quiz_data[difficulty][0]
            selected_questions = question_set[:num_questions]
    
    # Ensure we have enough questions
    if len(selected_questions) < num_questions:
        # Fill with any available questions
        for diff_level in ["easy", "medium", "hard"]:
            if len(selected_questions) >= num_questions:
                break
            if diff_level in quiz_data and quiz_data[diff_level]:
                for qs in quiz_data[diff_level]:
                    for q in qs:
                        if len(selected_questions) >= num_questions:
                            break
                        if q not in selected_questions:
                            selected_questions.append(q)
    
    # Take only the requested number
    selected_questions = selected_questions[:num_questions]
    
    # Re-index questions
    for idx, q in enumerate(selected_questions, 1):
        q.question_id = idx
    
    # Create quiz response
    quiz_id = str(uuid.uuid4())
    quiz = QuizResponse(
        quiz_id=quiz_id,
        topic=topic,
        num_questions=num_questions,
        questions=selected_questions,
        context_used=f"Static Quiz Generator - {matched_topic or topic}"
    )
    
    return quiz

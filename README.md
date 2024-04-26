**README for CKY Parsing Project**

**Introduction:**
This project implements the CKY algorithm for Context-Free Grammar (CFG) and Probabilistic Context-Free Grammar (PCFG) parsing. It involves parsing sentences based on a given grammar and producing parse trees. The main goal is to understand and implement the CKY algorithm, retrieve parse trees, and evaluate the parser's performance.

**Project Components:**
1. **Files:**
    - `cky.py`: Contains the implementation of the CKY parser class and methods.
    - `evaluate_parser.py`: Script to evaluate the parser against a test set.
    - `grammar.py`: Contains the class `Pcfg` representing a PCFG grammar and methods to read and verify grammar files.
    - `atis3.pcfg`: File containing the PCFG grammar rules.
    - `atis3_test.ptb`: Test corpus containing sentences for evaluation.

2. **Data Files:** - NOTE: data files not included for copyright reasons
    - `atis3.pcfg`: Contains the PCFG grammar rules extracted from the ATIS subsection of the Penn Treebank.
    - `atis3_test.ptb`: Test corpus containing sentences for evaluating the parser.

**Project Tasks:**
1. **Part 1 - Reading the Grammar and Getting Started:**
    - Verifying that the given grammar is a valid PCFG in Chomsky Normal Form.
    - Checking grammar format and print confirmation if valid, otherwise print an error message.

2. **Part 2 - Membership Checking with CKY:**
    - Implementation the `is_in_language` method in `CkyParser` class to check if a sentence is in the language of the grammar using the CKY algorithm.
    - Testing the method with different sentences and grammar.

3. **Part 3 - Parsing with Backpointers:**
    - Extending the parser to retrieve the most probable parse for the input sentence using PCFG probabilities.
    - Implementing the `parse_with_backpointers` method in `CkyParser` class to construct parse and probability tables during parsing.

4. **Part 4 - Retrieving a Parse Tree:**
    - Writing the `get_tree` function to reconstruct a parse tree from the backpointer table returned by `parse_with_backpointers`.
    - Testing the function with different sentences and grammar.

5. **Part 5 - Evaluating the Parser :**
    - Using the provided script `evaluate_parser.py` to evaluate the parser against the test corpus.
    - Comparing predicted trees with target trees using precision, recall, and F-score metrics.

**Usage:**
1. Clone the repository or download the project files.
2. Ensure Python 3 is installed on your system.
3. Run `evaluate_parser.py` with the PCFG grammar file (`atis3.pcfg`) and test corpus file (`atis3_test.ptb`) as arguments.
    ```bash
    python evaluate_parser.py atis3.pcfg atis3_test.ptb
    ```
4. Check the evaluation results for coverage and average F-scores.


**References:**
- Penn Treebank
- ATIS (Air Travel Information Services)
- CKY Algorithm
- Probabilistic Context-Free Grammar (PCFG)


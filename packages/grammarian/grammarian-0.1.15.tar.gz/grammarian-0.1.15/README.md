
# Grammarian

Grammarian is a Python package that allows you to easily check the correctness of English words, and also suggests "what the author (potentially) meant" if the word is not correct. 




## Authors

- [@hiko667](https://github.com/hiko667)


## Deployment

To deploy this package, while being in the same dir as it run 

```bash
pip install .

```


## Usage/Examples

To import grammarian package run
```python
from grammarian import Grammarian

```

Grammarian is a python class. You run 

```python
g = Grammarian()

```
to create an instance of it. Constructor is meant to be empty. To check grammar of any english word run:

```python
g.check_grammar("apple")

```
check_grammar returns an GrammarianCheck class instance. If the word you have given is correct, GrammarianCheck.is_correct will be True, and GrammarianCheck.suggestions will be None. If the word is incorrect, GrammarianCheck.is_correct will be False, and GrammarianCheck.suggestions will be a list of 10 suggested words (in str). Run:
```python
str(g.check_grammar("appleq"))

```
to return a str in format of:
```python
return ' '.join(self.suggestions)
```
or in terminal:
```bash
apple appled apples apelet apoplex appale appel appet appl apply
```

## Feedback

If you have any feedback, please reach out to me on github. All feedback will be apriciated



# Grammarian

Grammarian is a Python package that allows you to easily check the correctness of English words, and also suggests "what the author (potentially) meant" if the word is not correct. 




## Authors

- [@hiko667](https://github.com/hiko667)


## Deployment

To deploy this package, you just need to run following commnd in your terminal:

```bash
pip install grammarian

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
check_grammar returns an GrammarianCheck class instance. If the word you have given is correct, GrammarianCheck.is_correct will be True, and GrammarianCheck.suggestions will be None. If the word is incorrect, GrammarianCheck.is_correct will be False, and GrammarianCheck.suggestions will be a list of 5 suggested words (in str). Run:
```python
str(g.check_grammar("appleq"))

```
to return a str in format of:
```python
return ' '.join(self.suggestions)
```
to acces all of the words on their own run:
```python
g.check_grammar("appleq")[i]
```
where 'i' variable is by deafault between 0-5. For "appleq" it returns:
```bash
apple appled apples apelet apoplex 
```
as mentioned, i is "by deafult" no higher than 5. Since grammarian 0.1.20 you can set the number of returned elements. If you set the size variable to zero or less, code will just return if its correct.
```python
g.check_grammar("appleq", 10)
```


## Feedback

If you have any feedback, please reach out to me on github. All feedback will be apriciated


# SquidgyTesty

SquidgyTest is a prompt testing framework for LLM prompt templates. 

# Prompt Template and Test Format

Prompts are defined in text files and are templated to accept parameters.

Here is an example of book_author.txt:
```
The author of the book {book_title} is
```

Tests are defined in YAML files:
```
tests:
  book_author:
    prompt_file: ./book_author.txt
    params:
      title: Twenty Thousand Leagues Under the Sea
    assertions:
      equalTo: Jules Verne
```

You can also append data to a prompt, which is very useful when emulating chat bots:
```
tests:
  book_author:
    prompt_file: ./book_author.txt
    prompt_append: Jules Verne and he was born in the year
    params:
      title: Twenty Thousand Leagues Under the Sea
    assertions:
      equalTo: 1828
```
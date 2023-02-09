# SquidgyTesty

SquidgyTest is a prompt testing framework for LLM prompt templates. It features:
* Define prompts tests in YAML files
* Prompts can be defined in templated text files so they are callable from SquidgyTesty and your app
* Caches outputs from LLMs across prompt runs
* Supported assertions:
    * Equal To
    * Similar To: uses embeddings and a cosine similarity score to determine passing
    * More coming as needed...
* Supports GPT3
    * Other LLM contributions welcome!
* MIT License

# Why Prompt Testing?
This project came out of necessity from managing 50+ prompts for [Squidgies](https://squidgies.app), a
language learning app based on LLMs. During development we found:
* It is very easy to introduce typos into prompts which create undesired results
* Prompts have a wide number of expected outputs depending on the input
* Prompts need to be verified against new model versions 
* Prompt writers and testers are often separate than the application developer. SquidgyTesty allows collaboration between them.

# Installing
To install:
```
$ pip install git+https://github.com/squidgyai/squidgy-testy
```

# Getting Started

We're going to create a project of the following structure:

```
/example
/example/book_author.txt
/example/tests/test_book_author.yaml
```

Before you can create a test, you need to create a prompt to tests. 
Prompts are defined in text files and accept basic templated parameters. 
To create your first prompt, create a file called book_author.txt:
```
The author of the book {book_title} is
```

Tests are defined in YAML files and go in the "tests" directory. Let's create one called "test-book_author.yaml":
```
tests:
  book_author:
    prompt_file: ./book_author.txt
    params:
      book_title: Twenty Thousand Leagues Under the Sea
    stop: ['.']
    assertions:
      - equalTo: Jules Verne
```

To run all the tests:
```
$ pip install git+https://github.com/squidgyai/squidgy-testy
$ cd example
$ python -m squidgy_testy --directory ./example
Running tests...
test_book_author:
* book_author: 
  * equalTo: FAILED 
    * Diff:
      - Jules Verne      
      + Jules Verne.
```

As you can see our first test failed. We can see that there was an extra period. To fix this, we can add a "stop" to our test so that GPT3 knows when to stop.
```
tests:
  book_author:
    ....
    stop: ['.']
```

Now run all the tests again:
```
Running tests...
test_book_author:
* book_author:
  * equalTo: ✓ (cached)
```

You'll notice, not only did your test pass, but SquidgyTesty cached the results from the previous run and used them to run your test.
This makes your test run faster, and reduces costs.
These results are stored in the .squidgy_testy directory in your project.

## Extending Prompts
You can also append data to a prompt, which is very useful when emulating chat bots:
```
tests:
  book_author_year:
    prompt_file: ./book_author.txt
    prompt_append: Jules Verne and he was born in the year
    params:
      title: Twenty Thousand Leagues Under the Sea
    stop: ['.']
    assertions:
      - equalTo: 1828
```

## Similar To
You can also use the similarTo assertion to validate that the result is roughly what you expect.

```
tests:
  book_author_similarity:
    prompt_file: ./book_author.txt
    params:
      title: Twenty Thousand Leagues Under the Sea
    assertions:
    - similarTo: 
        value: Julesy Verney
        threshold: 0.8
```

Underneath the covers, it uses OpenAI to create embeddings for the actual result from GPT-3 and the expected result.
It then uses cosine similarity to compares these two and see if the similarity is above the expected value.

# Questions, Ideas and Contributions
Ask questions or get involved by joining the [Squidiges discord](https://discord.gg/A3nSQEQZ6f).

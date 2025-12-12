# How to contribute  to MAFw

> Anyone can cook (*Gusteau*)

> Not everyone can become a great artist, but a great artist can come from anywhere (*A. Ego*) 

## Have you got a brilliant idea or just hit a bug?

MAFw is open for you to contribute with new code, fresh ideas, exciting tools and bug fixes. 

The best way is to use the [issue feature](https://code.europa.eu/kada/mafw/-/issues) on our Gitlab repository and 
post there your ideas, possibly including a merge request with your own code.

### Before starting coding

We tried to produce a high quality code, and for this we have adopted four rules:

1. **Lint your code.** Following a strict convention in variable naming or fixing the maximum length of the 
  lines is not just a whim, but makes your code more readable and easier to be adopted by the user community. 
  Scientists tend to be more keen on substantial things and neglect what they think it is just *appearance*, but in 
  our experience we have seen great advantages when everybody is sticking to a well-defined set of rules.   
2. **Always add the documentation.** This is particularly relevant for scientists who develop hundreds of code 
  snippets, and they tend to forget what scripts are about. Writing proper documentation is a two-fold task: you 
  need to document your classes and methods (API documentation) to explain how to use them, but also include in the 
  so-called general documentation a paragraph mentioning the rationale behind this new development.
3. **Be pedantic.** Python is very flexible when it comes to typing and we all appreciate this, but static typing (even though not enforced at run time) can be very useful in preventing bugs. MAFw provides static typing for all its components, and it uses [mypy](https://mypy-lang.org/) as a type-checker.
4. **Do not forget about testing!** Always provide a good set of unit tests for your code. We know that coverage is 
  just a number and does not guarantee that your code is bug-free, but we are aiming at nearly 100% coverage, so 
  help us in keeping this target. A unit test should verify that in an isolated environment, your code is doing what it is supposed to be doing. You can achieve this with a   clever use of Mock classes and patches. MAFw is a rather complex ecosystem where many different actors are
  operating with great synergy to bring you with the desired output. For this reason, please consider also an 
  integration test, where you show how your code is exchanging information with the other parts. Have a look at the 
  existing test suite to get inspired.   
 
## Get ready for coding

### Use hatch as development helper

You are not left alone in following all these rules, we have set up tools to help you! 

[Hatch](http://hatch.pypa.io/latest/) is a brilliant piece of code that is not just used to build python packages, but 
it helps developers to deal with everyday tasks. Have a look at their website to get a glance of all possibilities.

We strongly recommend to install hatch via [pipx](https://pipx.pypa.io/stable/), so that the hatch executable is 
available systemwide even if installed in a separated environment.

### Get the source code

The next step is to clone the MAFw repository locally on your development PC. You can do it either by forking the 
original repository, or using directly the original repository. You can get instructions on our [Gitlab page](https://code.europa.eu/kada/mafw).

### Create the development environment

Once you have your copy of MAFw on disk, just open a terminal (windows or linux), navigate to the directory with the 
repository (this is the path containing the pyproject.toml file) and type:

`hatch shell dev.py3.13`

This simple command will create a separate virtual environment installing MAFw in development mode along with all 
the required dependencies and login into this shell. 

If you do not have python 3.13 on your system, hatch will take care of downloading and installing it.

### Have pre-commit installed

MAFw developers adopted [pre-commit](https://pre-commit.com/) to automatically lint and check the code during the change committing. This is 
assuring that all the code that is checked in is following the adopted convention. Type this command from your 
development shell to have this tool setup.

`pre-commit install`

This will assure that all code reaching the repository is lint and checked.

## During coding

### Committing your changes

Git is a great tool, so please use it efficiently. Always provide a meaningful commit message following the so-called [conventional commit](https://www.conventionalcommits.org/) scheme.
Start the commit message with the correct commit type, followed by the optional scope and by the summary. Add all the rest in the message body. 

Here is an example:

`
refactor: fix typing annotation

resolve mypy warnings.

Signed-off-by: BULGHERONI Antonio <antonio.bulgheroni@ec.europa.eu>
`

In this way, the [CHANGELOG.md](https://code.europa.eu/kada/mafw/-/blob/main/CHANGELOG.md) file will be automatically generated when merging the commits. 

### Documentation

During coding, please do not forget to follow also rules 2, 3 and 4. I have the feeling that writing the 
documentation while coding is somehow very efficient. You might think it is a waste of time, but it helps you and 
others to better understand the code and its role.

Once you are done with writing the documentation, you can generate the HTML pages using the following command.

From your development environment:

`hatch run doc`

or from outside the development environment:

`hatch run dev.py3.13:doc`

Check that the HTML output reflects the content of your API and general documentation and be sure to correct all 
errors and warnings that may appear during the generation process.

### Static type checking

To perform static type checking, MAFw adopted mypy. Hatch is also helpful in this respect. 

`hatch run types:check`

This will run mypy and will take care of installing the required type stubs, if missing. 

### Testing

As already mentioned, add a comprehensive test suite for your code. Put the test code in a separate file inside the 
tests subfolder (have a look at an existing file to see the recommended structure).

You can run one, multiple or the whole test suite using hatch commands.

`hatch test tests/test_my_module.py` for single test modules

`hatch test` for the whole test suite.

Adding the `-a` flag will cause hatch to perform the test suite over all python versions included in the test matrix.
It is quite lengthy, but it needs to be done at least once before pushing your changes to the repository.

To generate coverage data, you need to add `-c` and then you can convert the tabular output in a more confortable HTML report with the following command:

`hatch run hatch-test.py3.13:cov-html`

# Are you stuck with a problem and have no idea on how to fix it? 

It happens sometimes and it is very frustrating. Again, the best way is to get in touch with the developers via [Gitlab](https://code.europa.eu/kada/mafw/-/issues).
from ollama import chat


class CoderAgent:
  PROBLEM_DEFINITION_MODEL = "qwen2.5-coder:14b"
  PROBLEM_DEFINITION_PROMPT = """\
  You are an AI problem generalizer and given a long text that explains the problem.
  1. Read it carefully and understand the problem.
  2. Write a concise problem definition without any unnecessary details and stupid themes.
  4. If there are any examples, make sure to include them in the problem definition verbatim.
  5. If there are any edge cases, make sure to include them in the problem definition verbatim.
  6. If there are any assumptions, make sure to include them in the problem definition verbatim.
  7. If there are any clarifications, make sure to include them in the problem definition verbatim.
  8. Do not include any code examples or implementation details in the problem definition.
  9. If there is Part 2, drop all the details about Part 1 and focus on Part 2.

  Only return the problem definition that is necessary to solve the problem.
  - Do not reformat the example input or output.
  """

  INPUT_FORMAT_MODEL = "qwen2.5-coder:14b"
  INPUT_FORMAT_PROMPT = """\
  You are given a long text that explains the problem. The text contains the input format.
  1. Read it carefully and understand the input format.
  2. Write a concise format definition so that the final solution can be implemented and can return the correct result.
  3. If there are any examples, make sure to include them VERBATIM, EXACTLY AS WRITTEN in the input format. Do not trim or modify them.

  Only return the input format that is necessary to solve the problem.
  - Do not reformat the example input or output.
  """

  CODE_MODEL = "qwen2.5-coder:14b"
  CODE_PROMPT = """\
  You are given a problem definition and input format. Write a Python script that solves the problem.
  1. Write a script that takes an input file name as an argument and reads the input from the file.
  ```python
  with open(sys.argv[1]) as f:
    # Read the input from the file
    content = f.read()
    # ... solve the problem ...
    print(result)
  ```
  2. Make sure the function is correct and efficient.
  3. If there is Part 2, drop all the details about Part 1 and focus on Part 2.

  Only return code that is necessary to solve the problem.
  - Do not include any unnecessary code or comments. 
  - Do not include any explanation or justification.
  - Do not include markdown or any other formatting.
  - Do not read from `sys.stdin` nor call `input()`.
  - Print the result to the standard output using `print()` (Do not write it to a file.)
  - Do not start with any non-Python text like "Here's a Python script that solves the problem"
  """

  def solve(self, problem, input_data):
    problem_def = self.generate_problem_definition(problem)
    print('======== Problem Definition ==========\n', problem_def)
    input_format = self.generate_input_format(problem, input_data.split('\n')[:15])
    print('======== Input Format ================\n', input_format)
    code = self.generate_code(problem_def, input_format)
    print('======== Code ========================\n', code)
    return code

  def generate_problem_definition(self, problem):
    res = chat(
      model=self.PROBLEM_DEFINITION_MODEL,
      options={
        'temperature': 0.2,
      },
      messages=[
        {"role": "system", "content": self.PROBLEM_DEFINITION_PROMPT},
        {"role": "user", "content": problem},
      ]
    )
    return res['message']['content']

  def generate_input_format(self, problem, first_lines):
    res = chat(
      model=self.INPUT_FORMAT_MODEL,
      options={
        'temperature': 0.1,
      },
      messages=[
        {"role": "system", "content": self.INPUT_FORMAT_PROMPT},
        {"role": "user", "content": problem + '\n\nHere is the first lines of the given input file:\n' + '\n'.join(first_lines) + '\n...\n'},
      ]
    )
    return res['message']['content']

  def generate_code(self, problem_def, input_format):
    res = chat(
      model=self.CODE_MODEL,
      options={
        'temperature': 0.2,
      },
      messages=[
        {"role": "system", "content": self.CODE_PROMPT},
        {"role": "user", "content": 'Problem Definition: ' + problem_def + '\nInput Format: ' + input_format},
      ]
    )
    code =res['message']['content']
    return code.replace('```python', '').replace('```', '').strip()

from aoc2024.agent import CoderAgent
import sys
import os


if len(sys.argv) == 3:
    with open(sys.argv[1]) as f, \
        open(sys.argv[2]) as ff:
        problem = f.read()
        input_data = ff.read()

        code = CoderAgent().solve(problem, input_data)

        problem_name = os.path.basename(sys.argv[1]).split('.')[0]
        solution_path = f'solutions/{problem_name}.py'
        with open(solution_path, 'w') as f:
            f.write(code)

        print('======== Solution ===================\n')
        os.system(f'python {solution_path} {sys.argv[2]}')

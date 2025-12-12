import os
import re
import subprocess
import tempfile
from textwrap import dedent, indent


def update_file(path, env_overrides=None, run_path=None):
    with open(path) as handle:
        content = handle.read()

    env = os.environ.copy()
    env['WHATNEXT_TODAY'] = '2025-12-25'
    env['WHATNEXT_EDITOR'] = 'true'
    if env_overrides:
        env.update(env_overrides)

    pattern = re.compile(
        r"""
            ^ ([ \t]*)  ```bash\n       # capture the indent
            ( \1 \(computer\)% .*? )    # capture the command and output
            ^ \1        ```
        """,
        re.MULTILINE | re.DOTALL | re.VERBOSE
    )

    sections = []
    last_end = 0
    for match in pattern.finditer(content):
        sections.append(content[last_end:match.start()])
        lines = dedent(match.group(2)).split('\n')
        result = []

        index = 0
        while index < len(lines):
            line = lines[index]

            # examples can feature multiple commands
            if line.startswith('(computer)%'):
                command = line[len('(computer)%'):].strip()

                result.append(line)

                actual_command = command
                if run_path:
                    actual_command = f'{command} {run_path}'

                proc = subprocess.run(
                    actual_command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    env=env,
                )
                if proc.returncode != 0:
                    raise RuntimeError(f'{actual_command!r} failed: {proc.stderr}')
                output = proc.stdout.rstrip('\n')

                if run_path:
                    run_path_basename = os.path.basename(run_path)
                    output = re.sub(
                        r'[^\n]*' + re.escape(run_path_basename),
                        path,
                        output
                    )

                for output_line in output.split('\n'):
                    result.append(output_line)

                index += 1
                while index < len(lines):
                    if lines[index].startswith('(computer)%'):
                        result.append('')
                        break
                    index += 1
                continue

            result.append(line)
            index += 1

        block = '```bash\n' + '\n'.join(result).rstrip('\n') + '\n```'
        sections.append(indent(block, match.group(1)))
        last_end = match.end()

    sections.append(content[last_end:])
    updated = ''.join(sections)

    if updated != content:
        with open(path, 'w') as handle:
            handle.write(updated)
        print(f'Updated {path}')


def main():
    # replace samples in README using itself
    with open('README.md') as handle:
        content = handle.read()
    match = re.search(r'```markdown\n(.*?)```', content, re.DOTALL)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp:
        temp.write(f'# What next?\n\n{match.group(1)}')
        temp.flush()
        update_file('README.md', run_path=temp.name)
    os.unlink(temp.name)

    # replace samples in usage using ./example
    update_file(
        'docs/usage.md', {
            'WHATNEXT_CONFIG': '.whatnext.all',
            'WHATNEXT_DIR': 'example',
        }
    )


if __name__ == '__main__':
    main()

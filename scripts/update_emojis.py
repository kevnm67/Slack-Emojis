#!/usr/bin/env python3
import argparse
import os


def get_emoji_list():
    # Get a sorted list of emojis found in the Emojis directory
    path = os.path.join(os.path.dirname(__file__), '../Emojis')
    files = os.listdir(path)

    return sorted(files)


def generate_readme(table):
    # Regerate the README.md file with the updated emoji table
    readme_path = os.path.join(os.path.dirname(__file__), '../README.md')

    with open(readme_path, 'r') as file:
        current_readme = file.read()

    emoji_heading = '## Emojis\n\n'
    next_heading = '## Attribution'
    head = current_readme.split(emoji_heading)[0]
    tail = current_readme.split(next_heading)[1]

    replacement = emoji_heading
    replacement += table + '\n\n'
    replacement += next_heading
    updated_readme = head + replacement + tail

    return updated_readme

def generate_table(emojis = get_emoji_list()):
    table = []
    table.append("| Emoji              | Image                               |")
    table.append("| ------------------ | ----------------------------------- |")

    for emoji in get_emoji_list():
        name = emoji.split('.')[0]
        entry = "| {} | ![{}](./Emojis/{}) |".format(name, name, emoji)
        table.append(entry)

    return "\n".join(table)

def main(dry_run):
    readme = generate_readme(generate_table())
    readme_path = os.path.join(os.path.dirname(__file__), '../README.md')
    
    if dry_run:
        print(readme)
    else:
        with open(readme_path, 'w') as file:
            file.write(readme)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--dry-run', 
                        help='Print updated readme to console',
                        action='store_true', 
                        default=False)

    args = parser.parse_args()

    main(dry_run=args.dry_run)
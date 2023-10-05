import datetime
import json
import sys

def read_issue_content(path):
    with open(path, 'r') as f:
        return json.load(f)

def split_file(path):
    # das template hat einen header das mit '---' beginnt und endet
    # der rest ist der content
    with open(path, 'r') as f:
        content = f.read()
        header = content.split('---')[1]
        content = content.split('---')[2]

    return header, content

def replace_title(content, new_title):
    content_lines = content.split('\n')
    for i, line in enumerate(content_lines):
        if '{short title of solved problem and solution}' in line:
            content_lines[i] = content_lines[i].replace('{short title of solved problem and solution}', new_title)
    # join header_lines to one string separated by \n
    content = '\n'.join(content_lines)
    return content

def replace_field(header, prefix, new_value):
    header_lines = header.split('\n')
    for i, line in enumerate(header_lines):
        if line.startswith(prefix):
            header_lines[i] = prefix + ' ' + new_value
    # join header_lines to one string separated by \n
    header = '\n'.join(header_lines)
    return header

def replace_date(header, new_date=None):
    # new_date is empty, the get the current date (YYYY-MM-DD)
    if not new_date:
        new_date = datetime.datetime.now().strftime('%Y-%m-%d')
    return replace_field(header, 'date:', new_date)

def replace_status(header, new_status):
    return replace_field(header, 'status:', new_status)

def remove_no_response(issue_data):
    for key in issue_data:
        if issue_data[key] == '_No response_':
            issue_data[key] = ''
    return issue_data


issue_data = read_issue_content(f'{sys.argv[1]}.json')
remove_no_response(issue_data)
adr_template_filename = sys.argv[2]
document_name = issue_data['Document Filename']

# get the diretory of adr_filename path
adr_dir = adr_template_filename.split('/')
adr_dir = '/'.join(adr_dir[:-1])


issue_data['Id'] = sys.argv[1]
issue_data['Date'] = datetime.datetime.now().strftime('%Y-%m-%d')


header, content = split_file(adr_template_filename)
header = replace_status(header, issue_data['Status'])
header = replace_date(header, issue_data['Date'])
content = replace_title(content, issue_data['ADR Title'])

# write header and content back to file
with open(f"{adr_dir}/{document_name}.md", 'x') as f:
    f.write('---')
    f.write(header)
    f.write('---\n')
    f.write(content)


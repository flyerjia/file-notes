## file-notes
file-notes can add note information to the file. It works with Python 3.6+.

## Installation
```
pip install file-notes
```

## Usage
Command
```
fn [-l|-al|-a|-u|-d] [file_or_dir] [note]
```
Show all file information
```
fn -l
```
Show all file information including hidden files
```
fn -al
```
Add a note to a file
```
fn -a file_or_dir_name 'note'
```
Update a file's note
```
fn -u file_or_dir_name 'new note'
```
Delete a file's note
```
fn -d file_or_dir_name
```
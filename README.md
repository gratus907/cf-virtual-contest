# cf-virtual-contest

## Features 
- Automaticallly try fetching new contests 
- Filter out contest if any of participants have attempted any of the problems
  - Solved after contest (practice) is considered
  - Solved on another division of same round is considered 
  - Solved in gym contest / mashup is **NOT** considered

## Todo
- Div 1/2 choice
- Full list of problems
- Recommendation (by problem rating)
- Run this on server? IDK
- `fetch_contests` should recieve cmd arguments

## Usage
```bash
$ python3 main.py
Input user name (A, B, C):
NAME_1 NAME_2 NAME_3
```

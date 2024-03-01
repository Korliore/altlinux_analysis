#!/bin/bash

show_help() {
  echo "Usage: ./get_stat [OPTIONS]"
  echo "Options:"
  echo "  -br1, --branch_1 <branch_name>  Set a name for Branch_1 (required)"
  echo "  -br2, --branch_2 <branch_name>  Set a name for Branch_2 (required)"
  echo "  -s, --save_on_file <path_to_file>              Save the result to a file"
  echo "  -h, --help                      Show this message and shut down"
}

while [[ "$#" -gt 0 ]]; do
  case $1 in
    -br1|--branch_1) Branch_1="$2"; shift;;
    -br2|--branch_2) Branch_2="$2"; shift;;
    -s|--save_on_file) 
        if [[ -z "$2" ]]; then
            echo "Error: The value for the -s option is not specified."
            exit 1
            show_help
        fi
        Save_on_file="$2"; shift;;
    -h|--help) show_help; exit 0;;
    *) echo "Unknown parameter: $1"; exit 1;;
  esac
  shift
done

if [[ -z $Branch_1 || -z $Branch_2 ]]; then
  show_help
  exit 1
fi

python3 main.py $Branch_1 $Branch_2 $Save_on_file

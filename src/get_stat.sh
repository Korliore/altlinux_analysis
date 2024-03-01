#!/bin/bash

show_help() {
  echo "Использование: ./get_stat [ОПЦИИ]"
  echo "Опции:"
  echo "  -br1, --branch_1 <branch_name>  Установить имя для Branch_1 (обязательно)"
  echo "  -br2, --branch_2 <branch_name>  Установить имя для Branch_2 (обязательно)"
  echo "  -s, --save_on_file <path_to_file>              Сохранить результат в файл"
  echo "  -h, --help                      Показать это сообщение и завершить работу"
}

while [[ "$#" -gt 0 ]]; do
  case $1 in
    -br1|--branch_1) Branch_1="$2"; shift;;
    -br2|--branch_2) Branch_2="$2"; shift;;
    -s|--save_on_file) 
        if [[ -z "$2" ]]; then
            echo "Ошибка: значение для опции -s не указано."
            exit 1
            show_help
        fi
        Save_on_file="$2"; shift;;
    -h|--help) show_help; exit 0;;
    *) echo "Неизвестный параметр: $1"; exit 1;;
  esac
  shift
done

if [[ -z $Branch_1 || -z $Branch_2 ]]; then
  show_help
  exit 1
fi

python3 main.py $Branch_1 $Branch_2 $Save_on_file

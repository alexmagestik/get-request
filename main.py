#!/usr/bin/env python3
import sys

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Dummy:
        def __getattr__(self, name):
            return ""
    Fore = Style = Dummy()

from http_client import get
from country_info import get_country_info


def print_header(text: str):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
    print(f"{text}")
    print(f"{'=' * 70}{Style.RESET_ALL}")


def print_success(text: str):
    print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")


def print_error(text: str):
    print(f"{Fore.RED}{text}{Style.RESET_ALL}")


def print_info(text: str):
    print(f"{Fore.YELLOW}{text}{Style.RESET_ALL}")


def format_json_pretty(data):
    import json
    return json.dumps(data, indent=2, ensure_ascii=False)


def format_number(num):
    try:
        num_f = float(num)
        if num_f.is_integer():
            return f"{int(num_f):,}".replace(",", " ")
        return f"{num_f}".replace(",", " ")
    except Exception:
        return str(num)


def format_country_russian(country_data):
    lines = []
    names = country_data.get('names', {}) or {}
    official = names.get('official') or (country_data.get('name') or {}).get('official')
    common = names.get('common') or (country_data.get('name') or {}).get('common')
    if official:
        lines.append(f"{Fore.YELLOW}Официальное название:{Style.RESET_ALL} {official}")
    if common:
        lines.append(f"{Fore.YELLOW}Общее название:{Style.RESET_ALL} {common}")

    capitals = country_data.get('capitals') or []
    if capitals:
        cap = capitals[0]
        cap_name = cap.get('name') if isinstance(cap, dict) else cap
        if cap_name:
            lines.append(f"{Fore.YELLOW}Столица:{Style.RESET_ALL} {cap_name}")

    region = country_data.get('region')
    subregion = country_data.get('subregion')
    if region and subregion:
        lines.append(f"{Fore.YELLOW}Регион:{Style.RESET_ALL} {region}, {subregion}")
    elif region:
        lines.append(f"{Fore.YELLOW}Регион:{Style.RESET_ALL} {region}")

    languages = country_data.get('languages') or []
    lang_names = []
    for lang in languages:
        if isinstance(lang, dict):
            name = lang.get('name') or lang.get('native_name')
            if name:
                lang_names.append(name)
        elif isinstance(lang, str):
            lang_names.append(lang)
    if lang_names:
        lines.append(f"{Fore.YELLOW}Языки:{Style.RESET_ALL} {', '.join(lang_names)}")

    currencies = country_data.get('currencies') or []
    curr_list = []
    for cur in currencies:
        if isinstance(cur, dict):
            code = cur.get('code', '')
            name = cur.get('name', '')
            symbol = cur.get('symbol', '')
            if code and name and symbol:
                curr_list.append(f"{code} ({name}, символ: {symbol})")
            elif code and name:
                curr_list.append(f"{code} ({name})")
            elif code:
                curr_list.append(code)
        elif isinstance(cur, str):
            curr_list.append(cur)
    if curr_list:
        lines.append(f"{Fore.YELLOW}Валюты:{Style.RESET_ALL} {', '.join(curr_list)}")

    population = country_data.get('population')
    if population is not None:
        lines.append(f"{Fore.YELLOW}Население:{Style.RESET_ALL} {format_number(population)} человек")

    area = country_data.get('area')
    area_km = None
    if isinstance(area, dict):
        area_km = area.get('kilometers')
    else:
        area_km = area
    if area_km is not None:
        lines.append(f"{Fore.YELLOW}Площадь:{Style.RESET_ALL} {format_number(area_km)} км²")

    borders = country_data.get('borders') or []
    if borders:
        lines.append(f"{Fore.YELLOW}Граничит с:{Style.RESET_ALL} {', '.join(borders)}")
    else:
        lines.append(f"{Fore.YELLOW}Граничит с:{Style.RESET_ALL} нет")

    tlds = country_data.get('tlds') or []
    if tlds:
        lines.append(f"{Fore.YELLOW}Домен верхнего уровня:{Style.RESET_ALL} {', '.join(tlds)}")

    codes = country_data.get('codes') or {}
    iso = codes.get('alpha_3') or codes.get('alpha_2')
    if iso:
        lines.append(f"{Fore.YELLOW}Код страны (ISO):{Style.RESET_ALL} {iso}")

    timezones = country_data.get('timezones') or []
    if timezones:
        lines.append(f"{Fore.YELLOW}Часовые пояса:{Style.RESET_ALL} {', '.join(timezones)}")

    flag = country_data.get('flag') or {}
    flag_desc = flag.get('description')
    if flag_desc:
        lines.append(f"{Fore.YELLOW}Флаг:{Style.RESET_ALL} {flag_desc}")

    flag_url = flag.get('url_png') or flag.get('url_svg') or (country_data.get('flags') or {}).get('png') or (country_data.get('flags') or {}).get('svg')
    if flag_url:
        lines.append(f"{Fore.YELLOW}Ссылка на изображение флага:{Style.RESET_ALL} {flag_url}")

    return '\n'.join(lines)


def extract_country_data(result):
    if not result:
        return None
    if isinstance(result, dict):
        data = result.get('data')
        if isinstance(data, dict):
            objs = data.get('objects')
            if isinstance(objs, list) and objs:
                return objs[0]
        if 'objects' in result:
            objs = result['objects']
            if isinstance(objs, list) and objs:
                return objs[0]
        return result
    if isinstance(result, list) and result:
        return result[0]
    return result


def show_menu():
    print_header("CLI Menu")
    print(f"{Fore.WHITE}1. {Style.BRIGHT}GET по URL{Style.RESET_ALL}")
    print(f"{Fore.WHITE}2. {Style.BRIGHT}Страна{Style.RESET_ALL}")
    print(f"{Fore.WHITE}3. {Style.BRIGHT}Случайная собака{Style.RESET_ALL}")
    print(f"{Fore.WHITE}0. {Style.BRIGHT}Выход{Style.RESET_ALL}")
    print()


def get_url_menu():
    print_header("GET запрос по URL")
    try:
        url = input(f"{Fore.CYAN}Введите URL: {Style.RESET_ALL}").strip()
    except EOFError:
        return
    if not url:
        print_error("URL не может быть пустым")
        return
    try:
        params_str = input(f"{Fore.CYAN}Параметры (key=value&...) или Enter: {Style.RESET_ALL}").strip()
    except EOFError:
        params_str = ""
    params = None
    if params_str:
        try:
            params = {}
            for pair in params_str.split('&'):
                if '=' in pair:
                    k, v = pair.split('=', 1)
                    params[k] = v
        except Exception:
            params = None
    try:
        print_info("Выполняем GET запрос...")
        response = get(url, params=params, timeout=10)
        print_success("\n✓ Запрос выполнен успешно")
        print_header("Результат ответа")
        if isinstance(response, dict):
            print(format_json_pretty(response))
        elif isinstance(response, str):
            try:
                import json
                parsed = json.loads(response)
                print(format_json_pretty(parsed))
            except Exception:
                print(response)
        else:
            print(str(response))
    except Exception as e:
        print_error(f"Ошибка: {e}")


def country_menu():
    print_header("Информация о стране")
    try:
        country_name = input(f"{Fore.CYAN}Введите название страны на английском: {Style.RESET_ALL}").strip()
    except EOFError:
        return
    if not country_name:
        print_error("Название страны не может быть пустым")
        return
    try:
        print_info("Получаем информацию о стране...")
        result = get_country_info(country_name)
        country = extract_country_data(result)
        print_success("\n✓ Информация получена успешно")
        print_header("Информация о стране")
        if country:
            print(format_country_russian(country))
            print(f"\n{Fore.CYAN}{Style.BRIGHT}Полные данные (JSON):{Style.RESET_ALL}")
            print(format_json_pretty(country))
        else:
            print(format_json_pretty(result))
    except Exception as e:
        print_error(f"Ошибка: {e}")


def dog_menu():
    print_header("Случайная собака")
    try:
        print_info("Получаем случайное изображение собаки...")
        url = "https://dog.ceo/api/breeds/image/random"
        response = get(url, timeout=10)
        if response:
            print_success("\n✓ Получено успешно")
            print_header("Результат")
            print(format_json_pretty(response))
            if isinstance(response, dict) and response.get('message'):
                print(f"\n{Fore.CYAN}Ссылка на изображение:{Style.RESET_ALL}")
                print(f"{Fore.GREEN}{response['message']}{Style.RESET_ALL}")
        else:
            print_error("Не удалось получить данные")
    except Exception as e:
        print_error(f"Ошибка: {e}")


def main():
    while True:
        try:
            show_menu()
            choice = input(f"{Fore.CYAN}Выберите пункт меню: {Style.RESET_ALL}").strip()
        except EOFError:
            sys.exit(0)
        except KeyboardInterrupt:
            print_success("\nДо свидания!")
            sys.exit(0)
        if choice == '1':
            get_url_menu()
        elif choice == '2':
            country_menu()
        elif choice == '3':
            dog_menu()
        elif choice == '0':
            print_success("До свидания!")
            sys.exit(0)
        else:
            print_error("Неверный выбор. Попробуйте снова.")
        try:
            input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        except EOFError:
            break
        except KeyboardInterrupt:
            print_success("\nДо свидания!")
            sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import json
import sys
import textwrap
from time import sleep
from typing import Any, Dict, List

import requests
from rich.console import Console

from letsdebughelper.helpers import ValidateArgRegex

console = Console(highlight=False)
LE_API_URL = 'https://letsdebug.net'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Checks the DNS of a domain')
    parser.add_argument('domain', type=ValidateArgRegex('domain'), nargs=1)
    args: argparse.Namespace = parser.parse_args()
    args.domain = args.domain[0]  # Remove from list.
    return args


def le_get_call(check_url: str) -> requests.Response:
    headers = {'accept': 'application/json'}
    return requests.get(check_url, headers=headers)


def le_post_call(post_data: Dict[str, str]) -> requests.Response:
    headers = {'content-type': 'application/json'}
    return requests.post(LE_API_URL, data=json.dumps(post_data), headers=headers)


def check_status(result: requests.Response, result_json: Dict[str, Any]) -> None:
    if result.status_code != 200:
        print("ERROR: not a 200 result. instead got: %s." % result.status_code)
        print(json.dumps(result_json, indent=2))
        sys.exit()


def decode_result(result: requests.Response) -> Dict[str, Any]:
    try:
        return result.json()  # type: ignore
    except Exception as e:
        console.log("Couldn't decode the response as JSON:", e)
        sys.exit()


def check_debug_test_status(test_id_url: str) -> Dict[str, Any]:
    console.print("\n[bold blue]Waiting for test to complete....[/]")
    check_result_json: Dict[str, Any] = {"status": "initial"}
    while check_result_json.get("status") != 'Complete':
        check_result: requests.Response = le_get_call(check_url=test_id_url)
        check_result_json = decode_result(result=check_result)
        check_status(result=check_result, result_json=check_result_json)
        sleep(1)
    return check_result_json


def pre_result_output(domain: str, test_id: str, test_id_url: str) -> None:
    console.print(f"\n[bold green]Checking Domain:[/] {domain}")
    console.print(f"[bold green]     Testing ID:[/] {test_id}")
    console.print(f"[bold green]            URL:[/] {test_id_url}")


def format_problem_output(problems: List[str], domain: str) -> None:
    if problems:
        for problem in problems:
            console.print(f"\n[bold yellow]Warning Type:[/] {problem.get('name')}")  # type: ignore
            explanation = textwrap.wrap(
                f"[bold yellow] Explanation:[/] {problem.get('explanation')}",  # type: ignore
                width=120,
                subsequent_indent="              ")
            for line in explanation:
                console.print(line)
            console.print(f"     [bold yellow]Details:[/] {problem.get('detail')}")  # type: ignore
            console.print(f"    [bold yellow]Severity:[/] {problem.get('severity')}")  # type: ignore
        print()
    else:
        console.print("\n[bold green]All OK![/]")
        print('\nNo issues were found with {}. If you are having problems with creating an\n\
SSL certificate, please visit the Let\'s Encrypt Community forums and post a question there.\n\
https://community.letsencrypt.org/\n'.format(domain))


def main() -> None:
    args: argparse.Namespace = parse_args()
    post_data: Dict[str, str] = {"method": "http-01", "domain": args.domain}
    result: requests.Response = le_post_call(post_data)
    result_json: Dict[str, Any] = decode_result(result)
    check_status(result=result, result_json=result_json)
    test_id_url = '{}/{}/{}'.format(LE_API_URL, result_json.get('Domain'), result_json.get('ID'))
    pre_result_output(domain=result_json.get('Domain', ""), test_id=result_json.get('ID', ""), test_id_url=test_id_url)
    check_result_dict: Dict[str, Any] = check_debug_test_status(test_id_url)
    problems: List[str] = check_result_dict.get('result', dict(problems=[])).get('problems')
    format_problem_output(problems=problems, domain=args.domain)


if __name__ == '__main__':
    main()

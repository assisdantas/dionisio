import requests
import csv
import json
import time
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread


print('''

                                                                                                                                                                 
    ,---,                                                                        
  .'  .' `\    ,--,                         ,--,                 ,--,            
,---.'     \ ,--.'|    ,---.        ,---, ,--.'|               ,--.'|    ,---.   
|   |  .`\  ||  |,    '   ,'\   ,-+-. /  ||  |,      .--.--.   |  |,    '   ,'\  
:   : |  '  |`--'_   /   /   | ,--.'|'   |`--'_     /  /    '  `--'_   /   /   | 
|   ' '  ;  :,' ,'| .   ; ,. :|   |  ,"' |,' ,'|   |  :  /`./  ,' ,'| .   ; ,. : 
'   | ;  .  |'  | | '   | |: :|   | /  | |'  | |   |  :  ;_    '  | | '   | |: : 
|   | :  |  '|  | : '   | .; :|   | |  | ||  | :    \  \    `. |  | : '   | .; : 
'   : | /  ; '  : |_|   :    ||   | |  |/ '  : |__   `----.   \'  : |_|   :    | 
|   | '` ,/  |  | '.'\   \  / |   | |--'  |  | '.'| /  /`--'  /|  | '.'\   \  /  
;   :  .'    ;  :    ;`----'  |   |/      ;  :    ;'--'.     / ;  :    ;`----'   
|   ,.'      |  ,   /         '---'       |  ,   /   `--'---'  |  ,   /          
'---'         ---`-'                       ---`-'               ---`-'           

      by: c0y073
      API Stress Testing                                                                             

''')



URL = input('Endpoint da API: ')
TOTAL_REQUESTS = int(input('Total de requisições: '))
CONCURRENT_REQUESTS = int(input('Requisições simultâneas: '))
JSON_FILE = input('Caminho do arquivo JSON para o corpo da requisição: ')
BEARER_TOKEN = input('Bearer token (pressione Enter para ignorar): ')
OUTPUT_FILE = input('Nome do arquivo de relatório (CSV): ')

response_times = []
requests_per_second = []
total_requests_made = 0

with open(JSON_FILE, 'r', encoding='utf-8') as f:
    BODY = json.load(f)

def make_request(session, url, body, headers):
    try:
        response = session.post(url, json=body, headers=headers)
        return response.status_code, response.text, response.elapsed.total_seconds()
    except Exception as e:
        return None, str(e), None

def stress_test(url, body, total_requests, concurrent_requests, headers):
    global total_requests_made
    results = []
    with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        with requests.Session() as session:
            futures = [executor.submit(make_request, session, url, body, headers) for _ in range(total_requests)]
            for future in futures:
                status, response_body, time_resp = future.result()
                if time_resp:
                    response_times.append(time_resp)
                total_requests_made += 1
                results.append((status, response_body, time_resp))
    return results

def save_results_to_csv(results, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Status Code", "Response Body", "Response Time (s)"])
        for status, response_body, time in results:
            writer.writerow([status, response_body, time])

def update_graph(frame):
    current_time = time.time()
    elapsed_time = current_time - start_time
    if len(response_times) > 0:
        requests_per_second.append(len(response_times) / elapsed_time)

    ax1.clear()
    ax1.plot(response_times, label="Tempo de Resposta (s)")
    ax1.set_xlabel("Requisições")
    ax1.set_ylabel("Tempo de Resposta (s)")
    ax1.legend()

    ax2.clear()
    ax2.plot(requests_per_second, label="Requisições por Segundo", color='orange')
    ax2.set_xlabel("Tempo (s)")
    ax2.set_ylabel("Requisições por Segundo")
    ax2.legend()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.tight_layout()

if __name__ == "__main__":

    headers = {"Content-Type": "application/json"}
    if BEARER_TOKEN:
        headers["Authorization"] = f"Bearer {BEARER_TOKEN}"

    print(f"Iniciando o teste de estresse em {URL}")

    start_time = time.time()

    stress_test_thread = Thread(target=stress_test, args=(URL, BODY, TOTAL_REQUESTS, CONCURRENT_REQUESTS, headers))
    stress_test_thread.start()

    ani = FuncAnimation(fig, update_graph, cache_frame_data=False, interval=1000)
    plt.show()

    stress_test_thread.join()

    resultados = stress_test(URL, BODY, TOTAL_REQUESTS, CONCURRENT_REQUESTS, headers)
    save_results_to_csv(resultados, OUTPUT_FILE)

    print(f"Os resultados foram salvos no arquivo: {OUTPUT_FILE}")

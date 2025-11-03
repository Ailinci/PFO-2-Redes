"""
Servidor que recibe tareas por socket y las distribuye a workers
"""
import socket
import threading
import json
import queue
import time
from itertools import cycle

# Configuración
HOST = '0.0.0.0'
PORT = 9000

# Gestión de workers y tareas
workers = {}  # {worker_id: socket}
task_queue = queue.Queue()
pending_responses = {}  # {task_id: client_socket}
worker_lock = threading.Lock()
worker_counter = 0  # Contador para IDs únicos
current_worker_index = 0  # Índice para round-robin


def handle_client(client_socket, address):
    """Maneja la conexión de un cliente o worker"""
    try:
        # Recibir primer mensaje
        data = client_socket.recv(4096).decode('utf-8')
        message = json.loads(data)

        if message['type'] == 'WORKER_REGISTER':
            # Registrar worker con ID único
            global worker_counter
            with worker_lock:
                worker_counter += 1
                worker_id = f"worker_{worker_counter}"
                workers[worker_id] = client_socket

            print(f"[INFO] Worker registrado: {worker_id}")

            # Confirmar registro
            response = json.dumps({'type': 'REGISTERED', 'worker_id': worker_id})
            client_socket.send(response.encode('utf-8'))

            # Manejar respuestas del worker
            handle_worker_responses(worker_id, client_socket)

        elif message['type'] == 'TASK':
            # Cliente enviando tarea
            task_id = message['task_id']
            print(f"[INFO] Tarea recibida: {task_id}")

            pending_responses[task_id] = client_socket
            task_queue.put(message)

    except Exception as e:
        print(f"[ERROR] {e}")
        client_socket.close()


def handle_worker_responses(worker_id, worker_socket):
    """Recibe respuestas de un worker"""
    while True:
        try:
            data = worker_socket.recv(4096).decode('utf-8')
            if not data:
                break

            response = json.loads(data)
            task_id = response['task_id']

            print(f"[INFO] Tarea {task_id} completada por {worker_id}")

            # Enviar respuesta al cliente
            client_socket = pending_responses.pop(task_id, None)
            if client_socket:
                client_socket.send(json.dumps(response).encode('utf-8'))
                client_socket.close()

        except Exception as e:
            print(f"[ERROR] Worker {worker_id}: {e}")
            break

    # Remover worker
    with worker_lock:
        workers.pop(worker_id, None)
    print(f"[INFO] Worker {worker_id} desconectado")


def distribute_tasks():
    """Distribuye tareas a workers disponibles usando round-robin"""
    worker_cycle = None

    while True:
        try:
            task = task_queue.get(timeout=1)

            # Buscar worker disponible usando round-robin
            with worker_lock:
                if workers:
                    # Recrear ciclo si cambió la lista de workers
                    current_worker_ids = list(workers.keys())
                    if worker_cycle is None:
                        worker_cycle = cycle(current_worker_ids)

                    # Obtener siguiente worker en round-robin
                    worker_id = next(worker_cycle)

                    # Verificar que el worker todavía existe
                    if worker_id in workers:
                        worker_socket = workers[worker_id]
                        try:
                            worker_socket.send(json.dumps(task).encode('utf-8'))
                            print(f"[INFO] Tarea {task['task_id']} asignada a {worker_id}")
                        except Exception as e:
                            print(f"[ERROR] Error enviando a {worker_id}: {e}")
                            task_queue.put(task)
                            worker_cycle = None  # Resetear ciclo en error
                    else:
                        # Worker desapareció, volver a encolar tarea
                        task_queue.put(task)
                        worker_cycle = None  # Resetear ciclo
                else:
                    task_queue.put(task)
                    worker_cycle = None
                    time.sleep(0.5)

        except queue.Empty:
            continue
        except Exception as e:
            print(f"[ERROR] Distribución: {e}")


def main():
    # Iniciar hilo de distribución
    threading.Thread(target=distribute_tasks, daemon=True).start()

    # Crear socket servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)

    print(f"[INFO] Servidor iniciado en {HOST}:{PORT}")
    print(f"[INFO] Esperando conexiones...")

    while True:
        try:
            client_socket, address = server.accept()
            print(f"[INFO] Nueva conexión desde {address}")
            threading.Thread(
                target=handle_client,
                args=(client_socket, address),
                daemon=True
            ).start()
        except KeyboardInterrupt:
            print("\n[INFO] Servidor detenido")
            break


if __name__ == '__main__':
    main()

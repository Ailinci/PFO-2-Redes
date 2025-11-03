"""
Worker con pool de hilos que procesa tareas
"""
import socket
import json
import hashlib
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# Configuración
SERVER_HOST = 'localhost'
SERVER_PORT = 9000
NUM_THREADS = 4  # Pool de hilos

# Lock para proteger el socket compartido
sock_lock = threading.Lock()


def procesar_tarea(task_type, task_data):
    """Procesa diferentes tipos de tareas"""
    if task_type == 'hash':
        # Calcular hash SHA-256
        text = task_data.get('text', '')
        hash_result = hashlib.sha256(text.encode()).hexdigest()
        return {'hash': hash_result}

    elif task_type == 'fibonacci':
        # Calcular Fibonacci
        n = task_data.get('n', 10)
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return {'sequence': fib[:n]}

    elif task_type == 'reverse':
        # Invertir string
        text = task_data.get('text', '')
        return {'reversed': text[::-1]}

    elif task_type == 'compute':
        # Cálculo computacional
        iterations = task_data.get('iterations', 1000)
        result = sum(i ** 2 for i in range(iterations))
        return {'result': result}

    else:
        return {'message': 'Tarea procesada', 'data': task_data}


def handle_task(sock, task, worker_id):
    """Maneja el procesamiento de una tarea en el pool de hilos"""
    task_id = task['task_id']
    task_type = task['task_type']
    task_data = task.get('task_data', {})

    print(f"[WORKER] Procesando tarea {task_id} (tipo: {task_type})")

    start_time = time.time()

    try:
        # Procesar la tarea
        result = procesar_tarea(task_type, task_data)
        processing_time = time.time() - start_time

        # Enviar respuesta al servidor
        response = {
            'task_id': task_id,
            'status': 'success',
            'result': result,
            'worker_id': worker_id,
            'processing_time': processing_time
        }

        # Proteger el envío con lock (múltiples threads comparten el socket)
        with sock_lock:
            sock.send(json.dumps(response).encode('utf-8'))

        print(f"[WORKER] Tarea {task_id} completada en {processing_time:.3f}s")

    except Exception as e:
        print(f"[WORKER] Error procesando {task_id}: {e}")


def main():
    # Conectar al servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))

    print(f"[WORKER] Conectado al servidor {SERVER_HOST}:{SERVER_PORT}")

    # Registrarse como worker
    register_msg = json.dumps({'type': 'WORKER_REGISTER'})
    sock.send(register_msg.encode('utf-8'))

    # Recibir confirmación
    data = sock.recv(4096).decode('utf-8')
    response = json.loads(data)
    worker_id = response.get('worker_id', 'unknown')

    print(f"[WORKER] Registrado con ID: {worker_id}")
    print(f"[WORKER] Pool de hilos: {NUM_THREADS} hilos")

    # Crear pool de hilos
    executor = ThreadPoolExecutor(max_workers=NUM_THREADS)

    # Procesar tareas
    while True:
        try:
            data = sock.recv(4096).decode('utf-8')
            if not data:
                break

            task = json.loads(data)

            # Procesar tarea en el pool de hilos
            executor.submit(handle_task, sock, task, worker_id)

        except KeyboardInterrupt:
            print("\n[WORKER] Deteniendo worker...")
            break
        except Exception as e:
            print(f"[WORKER] Error: {e}")
            break

    executor.shutdown(wait=True)
    sock.close()
    print("[WORKER] Worker detenido")


if __name__ == '__main__':
    main()

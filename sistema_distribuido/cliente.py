import socket
import json
import uuid
import time
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 9000


def enviar_tarea(task_type, task_data):
    """Envía una tarea al servidor y espera el resultado"""
    # Crear socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30)  # Timeout de 30 segundos

    try:
        sock.connect((SERVER_HOST, SERVER_PORT))

        # Generar ID único para la tarea
        task_id = str(uuid.uuid4())[:8]
        message = {
            'type': 'TASK',
            'task_id': task_id,
            'task_type': task_type,
            'task_data': task_data
        }

        print(f"\n[CLIENTE] Enviando tarea {task_id} (tipo: {task_type})")

        # Enviar tarea
        sock.send(json.dumps(message).encode('utf-8'))

        # Recibir resultado
        data = sock.recv(4096).decode('utf-8')
        result = json.loads(data)

        print(f"[CLIENTE] Tarea {task_id} completada")
        print(f"[CLIENTE] Resultado: {result}")

        return result

    except socket.timeout:
        print(f"[CLIENTE] Timeout: la tarea tardó demasiado")
    except Exception as e:
        print(f"[CLIENTE] Error: {e}")
    finally:
        sock.close()


def cliente_interactivo():
    """Cliente interactivo para probar el sistema"""
    print("="*60)
    print("CLIENTE DEL SISTEMA DISTRIBUIDO")
    print("="*60)

    while True:
        print("\n" + "-"*60)
        print("TIPOS DE TAREAS:")
        print("-"*60)
        print("1. Hash SHA-256")
        print("2. Fibonacci")
        print("3. Invertir texto")
        print("4. Cálculo computacional")
        print("5. Enviar múltiples tareas")
        print("0. Salir")
        print("-"*60)

        opcion = input("\nSelecciona una opción: ")

        if opcion == '0':
            print("¡Hasta luego!")
            break

        elif opcion == '1':
            text = input("Ingresa el texto: ")
            enviar_tarea('hash', {'text': text})

        elif opcion == '2':
            n = int(input("Cantidad de números (default 10): ") or 10)
            enviar_tarea('fibonacci', {'n': n})

        elif opcion == '3':
            text = input("Ingresa el texto: ")
            enviar_tarea('reverse', {'text': text})

        elif opcion == '4':
            iterations = int(input("Iteraciones (default 1000): ") or 1000)
            enviar_tarea('compute', {'iterations': iterations})

        elif opcion == '5':
            num = int(input("¿Cuántas tareas? "))
            print(f"\nEnviando {num} tareas en paralelo...")

            start = time.time()
            threads = []

            # Enviar todas las tareas en paralelo usando hilos
            for i in range(num):
                thread = threading.Thread(
                    target=enviar_tarea,
                    args=('hash', {'text': f'tarea_{i}'})
                )
                thread.start()
                threads.append(thread)

            # Esperar a que todas terminen
            for thread in threads:
                thread.join()

            elapsed = time.time() - start

            print(f"\n✓ {num} tareas completadas en {elapsed:.2f}s")
            print(f"✓ Promedio: {elapsed/num:.3f}s por tarea")

        else:
            print("Opción inválida")

        input("\nPresiona Enter para continuar...")


if __name__ == '__main__':
    try:
        cliente_interactivo()
    except KeyboardInterrupt:
        print("\n\n[CLIENTE] Finalizando...")

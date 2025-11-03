# Sistema Distribuido con Sockets y Workers

Sistema distribuido implementado en Python que utiliza sockets TCP para comunicación, con un servidor que distribuye tareas a workers con pool de hilos.

## Descripción

Este proyecto implementa una arquitectura distribuida donde:
- **Clientes** envían tareas al servidor por sockets TCP
- **Servidor** recibe tareas y las distribuye a workers disponibles (puerto 9000)
- **Workers** procesan tareas en paralelo usando pool de hilos (ThreadPoolExecutor con 4 hilos)
- **Resultados** se envían de vuelta al cliente

## Arquitectura

```
Clientes → Servidor (Puerto 9000) → Workers (Pool de 4 Hilos c/u)
                                       ↓
                              Procesamiento Paralelo
```

Ver [diagrama completo](sistema_distribuido.png) para arquitectura extendida con RabbitMQ y PostgreSQL

## Archivos del Proyecto

- `servidor.py` - Servidor que distribuye tareas a workers
- `worker.py` - Worker con pool de 4 hilos para procesar tareas
- `cliente.py` - Cliente interactivo para enviar tareas
- `sistema_distribuido.png` - Diagramas de arquitectura del sistema

## Requisitos

- Python 3.7 o superior
- No requiere librerías externas (usa solo biblioteca estándar de Python: `socket`, `threading`, `json`, `hashlib`)

## Uso

### 1. Iniciar el Servidor

En una terminal:
```bash
python servidor.py
```

Salida esperada:
```
[INFO] Servidor iniciado en 0.0.0.0:9000
[INFO] Esperando conexiones...
```

### 2. Iniciar Workers

En terminales separadas, iniciar uno o más workers:

**Terminal 2:**
```bash
python worker.py
```

**Terminal 3:**
```bash
python worker.py
```

**Terminal 4:**
```bash
python worker.py
```

Cada worker mostrará:
```
[WORKER] Conectado al servidor localhost:9000
[WORKER] Registrado con ID: worker_1
[WORKER] Pool de hilos: 4 hilos
```

### 3. Ejecutar el Cliente

En otra terminal:
```bash
python cliente.py
```

Esto abrirá un menú interactivo:
```
============================================================
CLIENTE DEL SISTEMA DISTRIBUIDO
============================================================

------------------------------------------------------------
TIPOS DE TAREAS:
------------------------------------------------------------
1. Hash SHA-256
2. Fibonacci
3. Invertir texto
4. Cálculo computacional
5. Enviar múltiples tareas
0. Salir
------------------------------------------------------------

Selecciona una opción:
```

## Ejemplos de Uso

### Ejemplo 1: Calcular Hash SHA-256
```
Selecciona una opción: 1
Ingresa el texto: Hola Mundo

[CLIENTE] Enviando tarea abc123 (tipo: hash)
[CLIENTE] Tarea abc123 completada
[CLIENTE] Resultado: {'task_id': 'abc123', 'status': 'success',
          'result': {'hash': '...'}, 'worker_id': 'worker_1'}
```

### Ejemplo 2: Fibonacci
```
Selecciona una opción: 2
Cantidad de números (default 10): 15

[CLIENTE] Enviando tarea def456 (tipo: fibonacci)
[CLIENTE] Tarea def456 completada
[CLIENTE] Resultado: {'sequence': [0, 1, 1, 2, 3, 5, 8, 13, ...]}
```

### Ejemplo 3: Múltiples Tareas
```
Selecciona una opción: 5
¿Cuántas tareas? 10

Enviando 10 tareas...
[CLIENTE] Enviando tarea 1...
[CLIENTE] Enviando tarea 2...
...
✓ 10 tareas completadas en 2.45s
✓ Promedio: 0.245s por tarea
```

## Tipos de Tareas Soportadas

1. **hash** - Calcula SHA-256 de un texto
   ```python
   {'task_type': 'hash', 'task_data': {'text': 'ejemplo'}}
   ```

2. **fibonacci** - Calcula secuencia de Fibonacci
   ```python
   {'task_type': 'fibonacci', 'task_data': {'n': 10}}
   ```

3. **reverse** - Invierte un string
   ```python
   {'task_type': 'reverse', 'task_data': {'text': 'hola'}}
   ```

4. **compute** - Cálculo computacional intensivo
   ```python
   {'task_type': 'compute', 'task_data': {'iterations': 5000}}
   ```

## Cómo Funciona

### 1. Cliente envía tarea
```python
# Cliente crea tarea
task = {
    'type': 'TASK',
    'task_id': 'unique_id',
    'task_type': 'hash',
    'task_data': {'text': 'ejemplo'}
}
# Envía por socket TCP
socket.send(json.dumps(task).encode())
```

### 2. Servidor recibe y distribuye
```python
# Servidor recibe tarea
task = socket.recv(4096)
# Encola tarea
task_queue.put(task)
# Distribuye a worker disponible
worker_socket.send(task)
```

### 3. Worker procesa con pool de hilos
```python
# Worker usa ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=4)
# Procesa tarea en un hilo
executor.submit(procesar_tarea, task)
```

### 4. Resultado vuelve al cliente
```python
# Worker envía resultado al servidor
result = {'task_id': id, 'status': 'success', 'result': data}
socket.send(json.dumps(result).encode())
# Servidor envía al cliente
client_socket.send(result)
```

## Protocolo de Comunicación

Todos los mensajes son JSON sobre TCP:

**Registro de Worker:**
```json
{"type": "WORKER_REGISTER"}
```

**Tarea:**
```json
{
  "type": "TASK",
  "task_id": "abc123",
  "task_type": "hash",
  "task_data": {"text": "ejemplo"}
}
```

**Respuesta:**
```json
{
  "task_id": "abc123",
  "status": "success",
  "result": {"hash": "..."},
  "worker_id": "worker_1",
  "processing_time": 0.123
}
```

## Arquitectura Extendida (Opcional)

El sistema puede extenderse con:

### Balanceador de Carga (Nginx)
Distribuir tráfico entre múltiples servidores

### Cola de Mensajes (RabbitMQ)
Gestionar comunicación asíncrona

### Base de Datos (PostgreSQL)
Persistir tareas y resultados

### Almacenamiento (S3)
Guardar archivos grandes

Ver [sistema_distribuido.png](sistema_distribuido.png) para arquitectura completa

## Características

- ✅ Comunicación por sockets TCP/IP
- ✅ Servidor que distribuye tareas
- ✅ Workers con pool de hilos (4 hilos cada uno)
- ✅ Cliente interactivo
- ✅ 4 tipos de tareas diferentes
- ✅ Procesamiento paralelo
- ✅ Round-robin para distribución
- ✅ Escalable (agregar más workers)



## Estructura del Código

```
sistema_distribuido/
├── servidor.py               # Servidor que distribuye tareas (puerto 9000)
├── worker.py                 # Worker con pool de hilos (ThreadPoolExecutor)
├── cliente.py                # Cliente interactivo para enviar tareas
├── sistema_distribuido.png   # Diagrama de arquitectura
└── README.md                 # Esta documentación
```

## Notas de Implementación

- El servidor usa **round-robin** para distribuir tareas entre workers
- Cada worker tiene un **pool de 4 hilos** para procesamiento paralelo
- La comunicación usa **JSON sobre sockets TCP**
- El sistema es **escalable horizontalmente** (agregar más workers)
- Los workers se **auto-registran** al conectarse al servidor

---

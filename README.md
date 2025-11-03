# PFO-2 - Programación en Redes

Este repositorio contiene dos proyectos relacionados con programación en redes:

## Proyectos

### 1. Sistema Distribuido con Sockets (Proyecto Principal)

Sistema distribuido implementado en Python con sockets TCP, servidor que distribuye tareas y workers con pool de hilos.

**Ubicación:** [sistema_distribuido/](sistema_distribuido/)

**Características:**
- ✅ Comunicación por sockets TCP/IP
- ✅ Servidor que distribuye tareas (puerto 9000)
- ✅ Workers con pool de 4 hilos cada uno
- ✅ Cliente interactivo para enviar tareas
- ✅ Procesamiento paralelo y escalable
- ✅ 4 tipos de tareas: hash SHA-256, Fibonacci, invertir texto, cálculo computacional
- ✅ Diagrama de arquitectura

**Inicio rápido:**
```bash
cd sistema_distribuido

# Terminal 1: Servidor
python servidor.py

# Terminal 2: Worker(s) - puedes iniciar múltiples workers
python worker.py

# Terminal 3: Cliente
python cliente.py
```

**Diagramas:** [sistema_distribuido/sistema_distribuido.png](sistema_distribuido/sistema_distribuido.png)

---

### 2. Sistema de Gestión de Tareas (Flask + SQLite)

API REST con Flask que permite registro de usuarios, inicio de sesión y gestión de tareas con persistencia en SQLite.

**Ubicación:** Raíz del proyecto - [servidor.py](servidor.py)

**Características:**
- API REST con Flask
- Autenticación de usuarios
- Hash de contraseñas con SHA-256
- Base de datos SQLite
- Endpoints: registro, login, tareas

**Inicio rápido:**
```bash
# Instalar Flask
pip install flask

# Ejecutar servidor
python servidor.py
```

El servidor se ejecutará en `http://localhost:5000`

**Documentación detallada:** Ver sección más abajo

---

## Requisitos

### Sistema Distribuido
- Python 3.7 o superior
- No requiere librerías externas (solo biblioteca estándar)

### Sistema Flask
- Python 3.7 o superior
- Flask (`pip install flask`)

## Instalación

```bash
git clone https://github.com/Ailinci/PFO-2-Redes.git
cd PFO-2-Redes
```

## Estructura del Proyecto

```
PFO-2-OjedaPytelAilin/
├── sistema_distribuido/          # Proyecto principal - Sistema Distribuido
│   ├── servidor.py              # Servidor que distribuye tareas
│   ├── worker.py                # Worker con pool de hilos
│   ├── cliente.py               # Cliente interactivo
│   ├── sistema_distribuido.png  # Diagrama de arquitectura
│   └── README.md                # Documentación del sistema distribuido
├── servidor.py                   # Servidor Flask (API REST)
├── usuarios.db                   # Base de datos SQLite (se crea automáticamente)
└── README.md                     # Este archivo
```

---

# Sistema de Gestión de Tareas con API y Base de Datos (Flask)

## Ejecución

```bash
python servidor.py
```

El servidor se ejecutará en `http://localhost:5000`


## Autor

Ailin Ojeda Pytel

## Repositorio

GitHub: [Ailinci/PFO-2-Redes](https://github.com/Ailinci/PFO-2-Redes)

# VerbalMaster 🌐
## Plataforma de aprendizaje del Presente Verbal en 5 idiomas

Aplicación web Flask completa para memorizar las 100 técnicas del presente verbal en:
🇪🇸 Español · 🇬🇧 Inglés · 🇨🇳 Chino · 🇮🇳 Hindi · 🇷🇺 Ruso

---

## Estructura del proyecto

```
verbal_app/
├── app.py                  # Aplicación Flask principal
├── requirements.txt        # Dependencias
├── README.md
├── data/
│   ├── flashcards.json     # 50 flashcards de estudio
│   ├── exercises.json      # 100 ejercicios de escritura
│   ├── users.json          # Usuarios (auto-generado)
│   └── scores.json         # Puntuaciones (auto-generado)
└── templates/
    ├── base.html           # Plantilla base con navegación
    ├── login.html          # Inicio de sesión
    ├── register.html       # Registro de usuarios
    ├── dashboard.html      # Panel principal
    ├── flashcards.html     # 50 flashcards interactivas
    ├── exercises.html      # 100 ejercicios escritos
    ├── exam.html           # Examen cronometrado
    ├── profile.html        # Perfil con medallas y niveles
    └── admin.html          # Panel de administración
```

---

## Instalación y ejecución

```bash
# 1. Instalar dependencias
pip install flask

# 2. Ejecutar
cd verbal_app
python app.py

# 3. Abrir en el navegador
# http://localhost:5000
```

---

## Funcionalidades

### 🔐 Autenticación
- Registro de usuarios con email y contraseña
- Login seguro (contraseñas hasheadas con SHA-256)
- El primer usuario registrado es automáticamente Admin

### 📊 Dashboard
- Resumen de puntuación, nivel y medalla actual
- Barra de progreso al siguiente nivel
- Puntos por idioma
- Tabla de líderes (top 5)
- Acceso rápido a todas las actividades

### ⚡ Flashcards (50 tarjetas)
- Tarjetas 3D con efecto flip animado
- Filtro por idioma (Todos / ES / EN / ZH / HI / RU)
- Modo aleatorio (mezclar)
- Mini-grid con todas las tarjetas para saltar directamente
- Barra de progreso

### ✍️ Ejercicios escritos (100 ejercicios)
- Un ejercicio por técnica (20 por idioma)
- Evaluación por palabras clave con 3 niveles:
  - ✅ Correcto: +10 puntos
  - ⚠️ Parcial: +5 puntos
  - ❌ Incorrecto: 0 puntos
- Estadísticas de sesión en tiempo real
- Botón "Ver respuesta" para consultar la solución
- Filtro por idioma, mezcla aleatoria

### 🎯 Examen
- Configuración: idioma y número de preguntas (10/20/50/100)
- Cronómetro en tiempo real
- Evaluación automática con feedback inmediato
- Resultados finales con:
  - Porcentaje de aciertos
  - Tiempo total
  - Medalla obtenida (Bronce/Plata/Oro/Diamante)
  - Puntos ganados

### 👤 Perfil
- Avatar generado automáticamente
- Estadísticas completas (puntos, correctas, precisión)
- Sistema de medallas: 🥉Bronce · 🥈Plata · 🥇Oro · 💎Platino · 💠Diamante
- Sistema de niveles: Principiante → Básico → Intermedio → Avanzado → Experto → Maestro
- Historial de las últimas 20 respuestas
- Edición de email y contraseña

### ⚙️ Panel Admin
- Estadísticas globales del sistema
- Gestión de usuarios: tabla con puntos, nivel, medalla
- Promover/degradar usuarios a admin
- Eliminar usuarios
- Tabla de líderes global completa

---

## Sistema de puntuación

| Acción | Puntos |
|--------|--------|
| Respuesta correcta (≥35% keywords) | +10 |
| Respuesta parcial (≥15% keywords) | +5 |
| Respuesta incorrecta | 0 |

## Niveles

| Nivel | Nombre | Puntos |
|-------|--------|--------|
| 1 | Principiante | 0 |
| 2 | Básico | 100 |
| 3 | Intermedio | 300 |
| 4 | Avanzado | 600 |
| 5 | Experto | 1000 |
| 6 | Maestro | 1800 |

## Medallas

| Medalla | Puntos |
|---------|--------|
| 🥉 Bronce | 0 |
| 🥈 Plata | 200 |
| 🥇 Oro | 500 |
| 💎 Platino | 1000 |
| 💠 Diamante | 2000 |

# SPEC-001 — Predicción de afluencia turística

## 1. Información General

**Módulo / Característica:** Predicción de afluencia turística.

**Actor Principal:** Usuario.

**Objetivo:** Permitir al usuario consultar una estimación de la cantidad de visitantes que podría recibir el atractivo turístico **El Velo de las Ninfas**, utilizando las condiciones meteorológicas previstas y las características de la fecha seleccionada.

**Ubicación de referencia:** El Velo de las Ninfas, Tambillo Chico, distrito de Mariano Dámaso Beraún, Huánuco, Perú.

**Coordenadas de referencia:**

* Latitud: `-9.430436`
* Longitud: `-75.965934`

Las coordenadas serán utilizadas internamente por el backend para solicitar información meteorológica. El usuario no deberá introducir ni modificar la ubicación.

---

# 2. Requerimientos Funcionales

## RF-01 — Selección de fecha

El sistema debe permitir al usuario seleccionar una fecha para realizar la predicción de afluencia turística.

## RF-02 — Ubicación meteorológica

El sistema debe utilizar como ubicación meteorológica de referencia las coordenadas configuradas para **El Velo de las Ninfas**:

* Latitud: `-9.430436`
* Longitud: `-75.965934`

El usuario no debe seleccionar ni introducir manualmente la ubicación.

## RF-03 — Consulta meteorológica

El sistema debe consultar las condiciones meteorológicas correspondientes a la ubicación del atractivo y a la fecha seleccionada mediante un proveedor externo de información meteorológica.

La consulta al proveedor debe realizarse utilizando las coordenadas geográficas de El Velo de las Ninfas.

WeatherAPI permite utilizar coordenadas de latitud y longitud como valor del parámetro `q` para realizar consultas meteorológicas.

## RF-04 — Variables meteorológicas

El sistema debe obtener como mínimo las siguientes variables meteorológicas necesarias para realizar la predicción:

* Temperatura.
* Probabilidad de precipitación.
* Precipitación esperada, cuando esté disponible.

## RF-05 — Datos históricos

El sistema debe considerar información histórica de afluencia turística almacenada en un conjunto de datos.

Cuando no existan datos reales disponibles, el sistema podrá utilizar un conjunto de datos sintético generado para fines de desarrollo y evaluación del prototipo.

## RF-06 — Características de la fecha

El sistema debe determinar si la fecha seleccionada corresponde a:

* Día laborable.
* Fin de semana.

El sistema podrá considerar adicionalmente si la fecha corresponde a un feriado registrado en el conjunto de datos utilizado.

## RF-07 — Predicción

El sistema debe procesar las variables meteorológicas, las características de la fecha y los datos históricos mediante el algoritmo de predicción definido para el sistema.

## RF-08 — Cantidad estimada

El sistema debe mostrar la cantidad estimada de visitantes para la fecha seleccionada.

## RF-09 — Nivel de afluencia

El sistema debe clasificar la cantidad estimada de visitantes en uno de los siguientes niveles:

* **Baja**
* **Media**
* **Alta**

Los rangos numéricos utilizados para esta clasificación deberán estar definidos en la implementación y documentados como parámetros del prototipo.

## RF-10 — Variables de predicción

El sistema debe mostrar al usuario las principales variables utilizadas para generar la predicción, incluyendo como mínimo:

* Fecha.
* Temperatura.
* Probabilidad de precipitación.
* Condición de fin de semana.

## RF-11 — Error del servicio meteorológico

Si no es posible obtener información meteorológica para la fecha seleccionada, el sistema debe informar al usuario que no fue posible obtener los datos necesarios y no debe presentar una predicción como si fuera válida.

## RF-12 — API REST

El backend debe proporcionar un endpoint REST para solicitar la predicción de afluencia turística.

## RF-13 — Consumo del backend

El frontend debe consumir el endpoint REST y mostrar los resultados de la predicción de forma clara.

---

# 3. Diseño de API

## Endpoint

```text
GET /api/v1/prediction
```

## Parámetro

```text
?date=2026-10-12
```

La fecha debe utilizar el formato:

```text
YYYY-MM-DD
```

## Ejemplo de solicitud

```text
GET /api/v1/prediction?date=2026-10-12
```

## Ubicación utilizada por el backend

El backend utilizará internamente:

```json
{
  "name": "El Velo de las Ninfas",
  "latitude": -9.430436,
  "longitude": -75.965934
}
```

Estas coordenadas no deben ser enviadas por el frontend, ya que la aplicación está diseñada específicamente para realizar predicciones sobre este atractivo turístico.

## Ejemplo de respuesta exitosa

```json
{
  "location": {
    "name": "El Velo de las Ninfas",
    "latitude": -9.430436,
    "longitude": -75.965934
  },
  "date": "2026-10-12",
  "weather": {
    "temperature": 28,
    "rain_probability": 20,
    "precipitation_mm": 0.4
  },
  "prediction": {
    "visitors": 67,
    "level": "Media"
  },
  "factors": {
    "weekend": false
  }
}
```

Los valores de `28`, `20`, `0.4` y `67` son únicamente valores ilustrativos; los valores reales serán obtenidos y calculados durante la ejecución.

---

# 4. Criterios de Aceptación

## Escenario 1 — Predicción exitosa

**Dado** que el usuario se encuentra en la pantalla de predicción

**Y** el sistema tiene configuradas las coordenadas de El Velo de las Ninfas

**Cuando** selecciona una fecha válida

**Y** presiona el botón "Predecir"

**Entonces** el sistema debe consultar las condiciones meteorológicas correspondientes a El Velo de las Ninfas

**Y** debe procesar los datos meteorológicos junto con los datos históricos

**Y** debe generar una cantidad estimada de visitantes

**Y** debe mostrar el nivel de afluencia correspondiente.

## Escenario 2 — Consulta meteorológica mediante coordenadas

**Dado** que el usuario selecciona una fecha válida

**Cuando** presiona el botón "Predecir"

**Entonces** el backend debe utilizar la latitud `-9.430436`

**Y** debe utilizar la longitud `-75.965934`

**Y** debe consultar el servicio meteorológico utilizando dicha ubicación

**Y** debe obtener las condiciones meteorológicas correspondientes a la fecha seleccionada.

## Escenario 3 — Día con condiciones meteorológicas disponibles

**Dado** que el usuario selecciona una fecha válida

**Y** existen datos meteorológicos disponibles para dicha fecha

**Cuando** presiona el botón "Predecir"

**Entonces** el sistema debe obtener la información meteorológica

**Y** debe generar la predicción de visitantes

**Y** debe mostrar la temperatura

**Y** debe mostrar la probabilidad de precipitación

**Y** debe indicar si la fecha corresponde a un fin de semana.

## Escenario 4 — Fecha inválida

**Dado** que el usuario se encuentra en la pantalla de predicción

**Cuando** intenta generar una predicción sin seleccionar una fecha válida

**Entonces** el sistema debe mostrar un mensaje indicando que debe seleccionar una fecha válida

**Y** no debe realizar una consulta al servicio meteorológico.

## Escenario 5 — Servicio meteorológico no disponible

**Dado** que el usuario seleccionó una fecha válida

**Cuando** el servicio meteorológico no está disponible

**Y** presiona el botón "Predecir"

**Entonces** el sistema debe informar que no fue posible obtener los datos meteorológicos

**Y** no debe mostrar una predicción como válida.

## Escenario 6 — Ubicación fija del atractivo

**Dado** que el usuario se encuentra en la pantalla de predicción

**Cuando** solicita una predicción para cualquier fecha válida

**Entonces** el sistema debe utilizar las coordenadas configuradas de El Velo de las Ninfas

**Y** no debe solicitar al usuario una ubicación diferente.

---

# 5. Frontend

El frontend tendrá una única pantalla principal.

```text
┌──────────────────────────────────────────┐
│              VELOPREDICT                 │
│                                          │
│       El Velo de las Ninfas              │
│   Predicción de afluencia turística      │
│                                          │
│  Ubicación                               │
│  El Velo de las Ninfas                   │
│  Tambillo Chico, Huánuco                 │
│                                          │
│  Seleccione una fecha                    │
│  ┌──────────────────────┐                │
│  │ 12/10/2026           │                │
│  └──────────────────────┘                │
│                                          │
│            [ PREDECIR ]                  │
│                                          │
├──────────────────────────────────────────┤
│                                          │
│  Predicción para 12/10/2026              │
│                                          │
│          67 visitantes                   │
│                                          │
│          Afluencia MEDIA                 │
│                                          │
│  Temperatura          28 °C              │
│  Prob. de lluvia      20 %               │
│  Fin de semana        No                  │
│                                          │
└──────────────────────────────────────────┘
```

La ubicación puede mostrarse en el frontend únicamente como **información descriptiva**. Las coordenadas deben permanecer configuradas en el backend.

---

# 6. Arquitectura

```text
                    USUARIO
                       │
                       ▼
              ┌─────────────────┐
              │    FRONTEND      │
              │    HTML/CSS/JS  │
              └────────┬────────┘
                       │
                 GET /api/v1/prediction
                       │
                       ▼
              ┌─────────────────┐
              │     BACKEND     │
              │      Python     │
              └────────┬────────┘
                       │
          ┌────────────┼─────────────┐
          │            │             │
          ▼            ▼             ▼
    Coordenadas    WeatherAPI    Dataset histórico
    del atractivo       │         de visitantes
          │             │             │
          └─────────────┴──────┬──────┘
                               ▼
                         PREDICTOR
                               │
                               ▼
                     Visitantes estimados
                               │
                               ▼
                           FRONTEND
```

La arquitectura de despliegue contempla adicionalmente un entorno de ejecución en AWS:

```text
                    GITHUB
                       │
                       │ Push / Pull Request
                       ▼
              ┌─────────────────┐
              │ GITHUB ACTIONS  │
              │                 │
              │ Instalar        │
              │ dependencias    │
              │ Ejecutar tests  │
              └────────┬────────┘
                       │
                 Tests exitosos
                       │
                       ▼
              ┌─────────────────┐
              │    AWS EC2      │
              │                 │
              │ Python Backend  │
              │ + Frontend      │
              └────────┬────────┘
                       │
                       ▼
                    USUARIO
```

---

# 7. Datos de ubicación

La aplicación utilizará una única ubicación meteorológica:

| Campo        | Valor                 |
| ------------ | --------------------- |
| Atractivo    | El Velo de las Ninfas |
| Localidad    | Tambillo Chico        |
| Distrito     | Mariano Dámaso Beraún |
| Departamento | Huánuco               |
| País         | Perú                  |
| Latitud      | -9.430436             |
| Longitud     | -75.965934            |

Las coordenadas deben mantenerse como configuración del backend y utilizarse para construir la consulta al proveedor meteorológico.

---

# 8. Requisitos de despliegue y CI/CD

## 8.1 Repositorio GitHub

El código fuente del sistema debe mantenerse en un repositorio de GitHub.

El repositorio deberá contener como mínimo:

* Código fuente del backend.
* Código fuente del frontend.
* Dataset utilizado por el predictor, cuando corresponda.
* Archivo de dependencias del proyecto.
* Pruebas automatizadas.
* Archivos necesarios para ejecutar la aplicación.
* Configuración del flujo de GitHub Actions.

Los archivos que contengan credenciales, claves de API u otros datos sensibles no deben almacenarse directamente en el repositorio.

## 8.2 Integración continua

El proyecto debe contar con un flujo de integración continua mediante **GitHub Actions**.

El flujo deberá ejecutarse cuando se realicen cambios en el repositorio y deberá:

1. Configurar el entorno de ejecución de Python.
2. Instalar las dependencias del proyecto.
3. Ejecutar las pruebas automatizadas.
4. Mostrar el resultado de la ejecución de las pruebas.
5. Marcar el workflow como fallido cuando alguna prueba no sea superada.

## 8.3 Pruebas automatizadas

El proyecto deberá contar con pruebas automatizadas para verificar el comportamiento del backend.

Las pruebas deberán contemplar, como mínimo:

* Solicitud de predicción con una fecha válida.
* Validación de una fecha inválida.
* Uso de las coordenadas configuradas del atractivo.
* Procesamiento de la información meteorológica.
* Manejo de errores del servicio meteorológico.
* Generación de la respuesta de predicción.

Las pruebas deberán poder ejecutarse mediante un comando definido en el proyecto y deberán ser ejecutadas automáticamente por GitHub Actions.

## 8.4 Despliegue en AWS EC2

La aplicación deberá desplegarse en una instancia **Amazon EC2**.

La instancia deberá contar con el entorno necesario para ejecutar la aplicación y deberá permitir que el backend:

* Ejecute el servidor Python.
* Atienda las solicitudes del frontend.
* Acceda al proveedor externo de información meteorológica.
* Utilice las variables de entorno requeridas por la aplicación.

## 8.5 Configuración del entorno

Las configuraciones sensibles deberán manejarse mediante variables de entorno.

Como mínimo, la aplicación deberá contemplar la configuración de:

```text
WEATHER_API_KEY
PORT
```

La clave de acceso al proveedor meteorológico no debe incluirse directamente en el código fuente ni almacenarse en el repositorio de GitHub.

Los valores reales de las variables de entorno deberán configurarse en el entorno de ejecución correspondiente.

## 8.6 Despliegue mediante GitHub Actions

El proyecto podrá utilizar GitHub Actions para automatizar el despliegue hacia la instancia EC2.

Cuando el flujo de despliegue automático sea implementado, deberá cumplir como mínimo con el siguiente proceso:

```text
Cambio en GitHub
       │
       ▼
GitHub Actions
       │
       ▼
Instalar dependencias
       │
       ▼
Ejecutar pruebas
       │
       ├── Fallan ──► Detener proceso
       │
       ▼
     Éxito
       │
       ▼
Desplegar en EC2
       │
       ▼
Aplicación actualizada
```

El despliegue automático no deberá ejecutarse si las pruebas automatizadas no finalizan correctamente.

---

# 9. Criterios de Aceptación de CI/CD y Despliegue

## Escenario 7 — Ejecución de pruebas mediante GitHub Actions

**Dado** que existe una modificación en el repositorio de GitHub

**Cuando** se ejecuta el workflow de GitHub Actions

**Entonces** el sistema debe configurar el entorno de Python

**Y** debe instalar las dependencias del proyecto

**Y** debe ejecutar las pruebas automatizadas

**Y** debe mostrar el resultado de las pruebas.

## Escenario 8 — Fallo de pruebas en CI

**Dado** que existe una modificación en el repositorio

**Cuando** una o más pruebas automatizadas fallan durante la ejecución de GitHub Actions

**Entonces** el workflow debe finalizar indicando un estado de fallo

**Y** el proceso de despliegue no debe continuar.

## Escenario 9 — Despliegue exitoso en AWS EC2

**Dado** que las pruebas automatizadas finalizan correctamente

**Cuando** se ejecuta el proceso de despliegue configurado

**Entonces** la aplicación debe ser desplegada en la instancia EC2 configurada

**Y** el backend debe quedar disponible para recibir solicitudes

**Y** la aplicación debe utilizar las variables de entorno configuradas para el entorno de ejecución.

## Escenario 10 — Protección de credenciales

**Dado** que la aplicación requiere una clave de acceso al proveedor meteorológico

**Cuando** el código fuente es almacenado en GitHub

**Entonces** la clave de acceso no debe encontrarse escrita directamente en el código fuente

**Y** debe ser proporcionada mediante una variable de entorno o mecanismo equivalente de configuración segura.

---

# 10. Restricciones y consideraciones

* La aplicación está diseñada específicamente para realizar predicciones sobre **El Velo de las Ninfas**.
* El usuario no podrá modificar las coordenadas utilizadas para la consulta meteorológica.
* Las coordenadas `-9.430436` y `-75.965934` corresponden a la ubicación configurada para el atractivo y deberán mantenerse consistentes entre las diferentes ejecuciones del sistema.
* La disponibilidad y precisión de la información meteorológica dependerá del proveedor externo utilizado.
* Los datos sintéticos de afluencia turística, cuando sean utilizados, deberán identificarse como datos generados para el desarrollo y evaluación del prototipo.
* Los rangos utilizados para clasificar la afluencia como Baja, Media o Alta deberán documentarse y mantenerse como parámetros configurables del sistema.
* Las credenciales y claves de acceso a servicios externos no deberán formar parte del código fuente almacenado en GitHub.
* La disponibilidad de la aplicación en AWS dependerá de la configuración y disponibilidad de la instancia EC2.

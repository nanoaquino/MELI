# Proyecto Challenge +: Best Seller

## Objetivo del programa
El objetivo de este desafío es que desarrolles un proceso que barra diferentes items de
nuestro search a través de APIs públicas para luego ir obteniendo sus diferentes atributos y
particularidades, como también poder mostrarnos su precio en dólares

## Issues
> La paginación (parámetro offset) no permite valores superiores a 950. Si bien en la API informa:
 "message": "The requested offset is higher than the allowed. Maximum allowed is 1000"

> La cantidad de items que se permite incluir en la url de la API es de 20, de ahi que utilizo la constante "chunk=20"



## Requisitos
El sw solo fue probado en un entorno windows

## Requerimientos
Ejecutar el siguiente comando para instalar dependencias:
```sh
pip install -r requirements.txt
```
## Consideraciones
> Se da por sentado que el programa se ejecuta una vez al día y no reprocesa si ya fue ejecutado. 
Cosideré insertar registros nuevos para permitir reporocesar un mismo día, pero me hubiese llevado más tiempo y suponer nuevos registros para testear y no poder asegurarme de que realmente ande al interactuar con la API
>Se entiende (y se asume) que los métodos de shipping son los que se encuentran en el atributo: "shipping":"logistic_type":
cross_docking
xd_drop_off
fulfillment
drop_off

>Falta filtrar por categoría: category_id=MLB1055 es "Celulares e Smartphones"

## TODO list
> Me quedó por realizar: 
Pasar los métodos a utils.py
query: Promedio de ventas por seller?
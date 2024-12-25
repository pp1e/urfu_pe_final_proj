# Финальный проект по дисциплине Программная инженерия


## Запуск в режиме разработки

1. Установить менеджер виртуального окружения `Poetry`:
   ```shell
   pip install poetry
   ```

2. Перейти в директорию с `Todo App`:
    ```shell
    cd todo_app 
    ```
3. Установить зависимости:
    ```shell
    poetry install 
    ```
4. Создать директорию для сохранения данных:
     ```shell
    mkdir data 
    ```   
5. Запустить `Todo App`:
    ```shell
    cd todo_app
    poetry run uvicorn main:app --reload --port 8000
    ```
6. Перейти в директорию с `Shorturl App`:
    ```shell
    cd ../../shorturl_app 
    ``` 
7. Установить зависимости:
    ```shell
    poetry install 
    ```
8. Создать директорию для сохранения данных:
     ```shell
    mkdir data 
    ``` 
9. Запустить `Todo App`:
    ```shell
    cd shorturl_app
    poetry run uvicorn main:app --reload --port 8001
    ```
   
## Запуск в продуктовой среде

1. Установить `docker` и `docker compose plugin`
2. Собрать контейнеры и запустить их:
   ```shell
   docker compose build && docker compose up -d
   ```
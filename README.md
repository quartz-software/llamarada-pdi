## crear un entorno virtual

```sh
python -m venv venv
```

## activar el entorno virtual

Terminal de Windows

```sh
venv/Scripts/activate.bat
```

Terminal de Sh

```sh
source venv/Scripts/activate
```

## instalar dependencias

```sh
pip install -r requirements.txt
```

## actualizar dependencias

```sh
pip freeze > requirements.txt
```

## levantar el servidor

```sh
uvicorn main:app --host=localhost --port=10000
```

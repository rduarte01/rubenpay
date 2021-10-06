# Comenzando 🚀
_Para correr el proyecto sigue estos pasos_

## Clona el repositorio

```
git clone https://github.com/rduarte01/rubenpay.git
```

## Si usa Django con Python 3, escriba lo siguiente:

```
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```

## Crear un entorno virtual de Python para su proyecto

```
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
cd ~/rubenpay
virtualenv myenv
source myenv/bin/activate
```

## En el archivo config.py

```
settings["SECRET_KEY"] = '' ###crear secret key aleatoria
```

## Correr

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

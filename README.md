# Objetivo

Permitir configurar los settings de una app django en runtime.
Son 2 applicaciones: main y setup. Hasta que no se termine la configuracion se accede a la app setup, una vez completada se utiliza la app main de forma transparente.

Mas o menos lo que pense fue lo siguiente.

1 - Database default es un diccionario vacio {}. arrancamos sin conexion a base de datos.
2 - Crear middleware. mientras la variable SETUP_COMPLETED sea False, redireccionar a setup.
3 - Setup configurar DB y agregar cambios en environment y settings. DONE
4 - Checkear que la nueva DB esta configurada correctamente, pingear de alguna forma la DB
5 - Correr collectstatic con subprocess.popen.
6 - Si hubo error, mostrar output de collectstatic y permanecer ahi.
5 - Correr migrate con subprocess.popen.
6 - Si hubo error, mostrar output de migrate y permanecer ahi.
7 - Si todo va bien SETUP_COMPLETED en true y redirect a /


El problema lo estoy teniendo al configurar la DB, hay que levantar el engine de la DB de forma manual sino por mas que cambies el environment no influye en nada, hay que cambiar el env y llamar a algo asi como config.load()


# Documentacion

https://docs.djangoproject.com/en/1.11/topics/db/multi-db/

If the concept of a default database doesn’t make sense in the context of your project, you need to be careful to always specify the database that you want to use. Django requires that a default database entry be defined, but the parameters dictionary can be left blank if it will not be used. To do this, you must set up DATABASE_ROUTERS for all of your apps’ models, including those in any contrib and third-party apps you’re using, so that no queries are routed to the default database. The following is an example settings.py snippet defining two non-default databases, with the default entry intentionally left empty:

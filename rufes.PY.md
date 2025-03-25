# Guia para hacer contribuciones al repositorio

## Resumen 

este es un resumen 

---
## tabla de contenidos

1. [Variables](#variable)
2. [Funciones](#funcion)
3. [Clases](#clases)
4. [Separación de bloques de código](#organizacion)
5. [Archivos y organización](#manejodearchivo)

---

## Variable 
 - las variables deben escribirse con Snake_case
 - el nombre de la variable debe ser otorgado por la información que almacena 
 - en la declaración de la misma debe tener un espacio entre el igual, el nombre y el dato

 **Código esperado:**
 nombre_de_usuario = "Pedro"
  ```python
  nombre_de_usuario = "Pedro"
  ```

**Evitar**:

```python
nombredeusuario ="Pedro"
```

## Funciones

- las funciones al igual a las variables mantienen el Snake_case.

- debajo de cada función (después de su declaración) debe hacer un comentario Pydoc que explique que operación realiza, argumentos que recibe y valores que devuelve.

- el nombre de la función debe ser autoexplicativo.

  **Código esperado**:

  ```python
  def suma(num:int,num2:int):
      """
      descripcion:
      esta funcion recibe 2 numeros y devuelve la suma de los mismos
      args:
      num: uno de los numeros de la operacion
      num2: otro numero entero 
      return:
      la suma de los 2 numeros
      """
      return num + num2
      
  ```

  evitar:

  ```python
  def arepa32(w,a):
      return w-a
  ```

  ---

  ##  Clases

  - los nombres de las clases deben escribirse PascalCase.

  - los nombres de los métodos deben escribirse en Snake_case, lo mismo aplica para los atributos.

  - cada método debe contener la misma descripción después de la declaración que una función.

    ```python
    class MrStickman:
        """
        descripcion:
        el MrStikman va a hablar con la personavy tiene cancer terminal
        """
        def __init__(self,name:str,enfermedades:Dict, extremidades:int):
            self.name= name
            self.enfermedades=enfermedades
            self.extremidades=extremidades
        def saludar(self,word:str):
            """
            descripcion:
            	MrStikman va a decir lo que el usuario quiere 
            args:
            	words:lo que quieres que diga MrStikman
         	"""
            print(f"MrStigman dice{words}")
            
    ```

    evitar

    ```python
    class mrstickman:
        def __init__(self,name:str,enfermedades:Dict, extremidades:int):
            self.name= name
            self.enfermedades=enfermedades
            self.extremidades=extremidades
        def saludar(self,word:str):
            print(f"MrStigman dice{words}")
    ```

    




from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from Carros import Carros
from Usuarios import Usuario
app = Flask(__name__)
app.secret_key = '$uper4utos#' 

#Se utilizao un diccionario para almacenar los nombres de usuario y las contraseñas
users = {"empleado": generate_password_hash("$uper4utos#")}
cars = []

@app.route('/', methods=['GET', 'POST'])
def login():
    #Con el metodo POST se envian los datos
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user_password_hash = users.get(username)
        #El check password sirve para comparar la contraseña ingresado con la contraseña 
        #almacenada en el diccionario, si es valida se crea la sesion con session.
        if user_password_hash and check_password_hash(user_password_hash, password):
            session['logged_in'] = True
            return redirect(url_for('registro_Auto'))
        else:
            flash('Usuario o contraseña incorrectos')
    
    return render_template('login.html')

@app.route('/registro_Auto', methods=['GET', 'POST'])
def registro_Auto():
    #Hace la verificacion del usuario
    if not session.get('logged_in'):
        return redirect(url_for('login')) 

    #Se validan los datos del formulario y se crea el objeto de tipo carro
    if request.method == 'POST':
        try:
            idTipoAuto = int(request.form['idTipoAuto'])
            marca = request.form['marca']
            modelo = request.form['modelo']
            descripcion = request.form['descripcion']
            precioUnitario = float(request.form['precioUnitario'])
            cantidad = int(request.form['cantidad'])
            imagen = request.form['imagen']

            #En esta parte se hace la validacion del Id existente
            for car in cars:
                if car.idTipoAuto == idTipoAuto:
                    flash(f'Error: El ID de auto {idTipoAuto} ya existe. Por favor, ingrese otro ID.')
                    return redirect(url_for('registro_Auto'))

            car = Carros(idTipoAuto, marca, modelo, descripcion, precioUnitario, cantidad, imagen)
            cars.append(car)
            flash('Auto registrado exitosamente')
            return redirect(url_for('lista_Autos'))

        except ValueError:
            flash('Datos incorrectos, por favor verifique los campos')

    return render_template('registro_Auto.html')

#En esta ruta se muestra la lista de los autos registrados
@app.route('/lista_Autos')
def lista_Autos():
    #Hace la verificacion de que el usuraio este autenticado para mostrar la lista
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template('lista_Autos.html', cars=cars)

#En esta ruta se elimina un carro de la lista por medio de su id
@app.route('/eliminar_Carro/<int:index>', methods=['POST'])
def eliminar_Carro(index):
    #Hace la verificacion de que el usuraio este autenticado para mostrar la lista
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    #Luego verifica la existencia del indice seleccionado, valida que este dentro de la lista
    if 0 <= index < len(cars):
        cars.pop(index)
        flash('Auto eliminado exitosamente')
    else:
        flash('Auto no encontrado')
    
    return redirect(url_for('lista_Autos'))

#Cierra la sesion del usuario 
@app.route('/cerrar_Sesion')
def cerrar_Sesion():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

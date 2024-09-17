from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esto por una clave secreta real en producción

# Datos simulados en lugar de una base de datos
users = {"empleado": generate_password_hash("$uper4utos#")}
cars = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user_password_hash = users.get(username)
        if user_password_hash and check_password_hash(user_password_hash, password):
            session['logged_in'] = True
            return redirect(url_for('register_car'))
        else:
            flash('Usuario o contraseña incorrectos')
    
    return render_template('login.html')

@app.route('/register_car', methods=['GET', 'POST'])
def register_car():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            idTipoAuto = int(request.form['idTipoAuto'])
            marca = request.form['marca']
            modelo = request.form['modelo']
            descripcion = request.form['descripcion']
            precio_unitario = float(request.form['precioUnitario'])
            cantidad = int(request.form['cantidad'])
            imagen = request.form['imagen']
            
            car = {
                'idTipoAuto': idTipoAuto,
                'marca': marca,
                'modelo': modelo,
                'descripcion': descripcion,
                'precioUnitario': precio_unitario,
                'cantidad': cantidad,
                'imagen': imagen
            }
            cars.append(car)
            flash('Auto registrado exitosamente')
            return redirect(url_for('cars_list'))
        except ValueError:
            flash('Datos incorrectos, por favor verifique los campos')
    
    return render_template('register_car.html')

@app.route('/cars_list')
def cars_list():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template('cars_list.html', cars=cars)

@app.route('/delete_car/<int:index>', methods=['POST'])
def delete_car(index):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if 0 <= index < len(cars):
        cars.pop(index)
        flash('Auto eliminado exitosamente')
    else:
        flash('Auto no encontrado')
    
    return redirect(url_for('cars_list'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

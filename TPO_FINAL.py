# try:
#     arch = open(r"C:/Users/agust/Desktop/programacion 1/TP FINAL/data_ventas_pasajes_micros.csv", "wt")
#     arch.write("id_micro, user_id,dni, telefono, nombre_pas, apellido_pas, destino, fecha_salida, num_asiento, total\n")

# finally: 
#     try:
#         arch.close()
#     except NameError:
#         pass
    

def validar_registrar_pasajero():
    while True:
        try:
            dni = input("DNI pasajero: ")
            assert dni.isdigit(), "DNI debe contener solo numeros"
            break 
        #no se si este break es correcto, corregir si es necesario
        
        except AssertionError as mensaje:
            print(mensaje)

    encontrado = False
    
    try: 
        arch = open("datos_pasajeros.csv","rt")
        for linea in arch:
            linea = linea.strip().split(",")
            dni_arch = [0]

            if dni_arch == dni:
                encontrado = True
                nombre_arch = linea[1]
                apellido_arch = linea[2]
                telefono_arch = linea[3]
            
            nombre = input("Nombre del Pasajero: ")
            apellido = input("Apellido del Pasajero: ")

            try:
                assert nombre.lower() == nombre.arch.lower(), "Nombre incorrecto"
                assert apellido.lower() == apellido_arch.lower(), "Apellido incorrecto"
            except AssertionError as mensaje:
                print(mensaje)
                return None
            

            print("Datos de Pasajero validados")

            return {
                "dni": dni_arch,
                "nombre": nombre_arch,
                "apellido": apellido_arch,
                "telefono": telefono_arch
            }

    except FileNotFoundError:
        print("archivo no encontrado, CREANDO...")
    
    finally:
        try:
            arch.close()
        except NameError:
            pass

    if not encontrado:
        print("pasajero no encontrado. REGISTRANDO...")

        while True:
            nombre = input("Nombre del Pasajero: ")
            try:
                
                assert nombre != "", "Nombre no valido"
                #probando una cosita, si da error, mover la variable nombre afuera del try
                # y poner un break al final del try
                break
            except AssertionError as mensaje:
                print(mensaje)

        while True:
            apellido = input("Apellido del Pasajero: ")
            try:
                assert apellido != "", "Apellido no valido"
                break
            except AssertionError as mensaje:
                print(mensaje)

        telefono = input("Numero de Telefono: ").strip()

        try:
            arch = open("pasajeros.csv","a", encoding = "utf-8")
            arch.write(f"{dni},{nombre},{apellido},{telefono}\n")
            print ("PASAJERO REGISTRADO EXITOSAMENTE")
        
        except Exception as mensaje:
            print("Error: ",mensaje)

        finally:
            try:
                arch.close()
            except NameError:
                pass

        return {
            "dni": dni,
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono
        }
    

#en teoria las paginas de pasajes no cargan los datos de los micros, si no que los reciben y de x lado y ahi ya tienen 
#la info sobre horarios, destinos, osea vienen de las empresas asi que no tenemos porque modificarlos, mejor que vengan
#precargados
def elegir_micro(lista_destinos):
    
    print("="*100)
    print("DESTINOS DISPONIBLES".center(100))
    print("="*100)
    mensaje = (
        "1. Mar de Ajó\n"
        "2. Pinamar\n"
        "3. Villa Gesell\n"
        "4. Mar del Plata\n"
        "5. Miramar\n"
        "6. Necochea\n"
        "7. Salir"
    )
    print(mensaje)
    
    while True:
        try:
            dest = int(input("\nElija su destino: ").strip())
            assert 1 <= dest <= 7, "Elija una de las opciones posibles (1 a 7)." 
            assert destino in lista_destinos, "Destino no válido"
            break
        except ValueError:
            print("La opción ingresada no es válida. Intente nuevamente.")
        except AssertionError as mensaje:
            print(mensaje)
    
    if dest == 7:
        print("Saliendo...")
        return None

#esta funcion me la paso chatgpt, esta dejenla que la corrijo yo, hay que validar algunas cosas un poco mejor
#preferiblemente el programa deberia mostrar las fechas disponibles para el destino que elija el usario
# asi que voy a estar revisando eso
    while True:
        fecha = input("Fecha de Viaje: (dd/mm/aaaa)")
        
        try:
            partes = fecha.split("/")
            assert len(partes) == 3,"Los datos no se ingresaron correctamente"
            d,m,a = partes
            assert d.isdigit() and m.isdigit() and a.isdigit(),"La fecha solo debe contener numeros"
            d,m,a = int(d),int(m),int(a)

            assert 1 <= d <= 31, "La fecha ingresada no es valida"
            assert 1 <= m <=12, "La fecha ingresada no es valida"
            assert 2025 <= a <= 2026, "La fecha ingresada no es valida"

            break

        except AssertionError as mensaje:
            print("ERROR: ",mensaje)

#no estoy seguro de esta variable que me dio chatgpt, hay que revisarla
    destino_csv = destino.title()

    micro_encontrado = None

    try:
        arch = open("micros.csv", "r")
        
        for linea in arch:
            linea = linea.strip().split(",")

            id_micro_arch = linea[0]
            destino_arch = linea[1]
            fecha_arch = linea[2]
            cant_asientos_arch = linea[3]

            if destino_arch.lower() == destino and fecha_arch == fecha:
                micro_encontrado = {
                    "id_micro": id_micro_arch,
                    "destino": destino_arch,
                    "fecha": fecha_arch,
                    "cant_asientos": int(cant_asientos_arch)
                }
                break

    except FileNotFoundError:
        print("ERROR: archivo micros.csv no encontrado")
        return None
    
    finally: 
        try:
            arch.close()
        except NameError:
            pass
    
    if micro_encontrado is None:
        print("No se encontraron coincidencias")
        return None
    
    print("Coincidencia encontrada")
    return micro_encontrado


def elegir_asiento(micro):
    id_micro = micro["id_micro"]
    cant_asientos = micro["cant_asientos"]

    asientos_ocupados = []

    try:
        arch = open("pasajes.csv","r")

        for linea in arch:
            linea = linea.strip().split(",")
            id_pasaje = linea[0]
            dni_arch = linea[1]
            id_micro_arch = linea[2]
            asiento_arch = linea[3]

        if id_micro_arch == id_micro:
            try:
                asiento_num = int(asiento_arch)
                asientos_ocupados.append(asiento_num)

            except ValueError:
                pass
    
    except FileNotFoundError:
        print("ERROR: Archivo pasajes.csv no encontrado")
        return None
    
    finally:
        try:
            arch.close()
        except NameError:
            pass

#esta funcion de libres podriamos cambiarla un poco
    todos = list(range(1, cant_asientos + 1))
    libres = [x for x in todos x not in asientos_ocupados]

    if len(libres) == 0:
        print("Sin asientos disponibles")
        return None
    
    print(f"Asientos ocupados: {asientos_ocupados}")
    print(f"Asientos disponibles: {libres}")

    while True:
        eleccion = input("Seleccion de Asiento: ")

        try:
            assert eleccion.isdigit(), "Solo se admiten numeros"
            eleccion = int(eleccion)

            assert 1 <= eleccion <= cant_asientos, "Numero de asiento fuera de rango"
            assert eleccion in libres, "Asiento ocupado"

            break
        except AssertionError as mensaje:
            print("ERROR: ", mensaje)

    print(f"Asiento {eleccion} reservado correctamente")
    return eleccion


def registrar_pasaje (dni, id_micro, asiento):
    nuevo_id = 1

    try: 
        arch = open("pasajes.csv","r")

        ultimo_id = 0

        for linea in arch:
            linea = linea.strip().split(",")
            try: 
                id_leido = int(linea[0])
                if id_leido > ultimo_id:
                    ultimo_id = id_leido
            except ValueError:
                pass
        
        nuevo_id = ultimo_id + 1
    
    except FileNotFoundError:
        nuevo_id = 1

    finally:
        try:
            arch.close()
        except NameError:
            pass

    try:
        arch = open("pasajes.csv","a")
        linea = f"{nuevo_id},{dni},{id_micro},{asiento}\n"
        arch.write(linea)

    except Exception as mensaje:
        print("ERROR: "mensaje)
        return None
    
    finally: 
        try:
            arch.close()
        except NameError:
            pass

    print("Pasaje registrado exitosamente")
    print(f"ID de pasaja: {nuevo_id}")

    return nuevo_id



def main():
    print("="*100)
    print("BIENVENIDO AL SISTEMA DE VENTAS DE PASAJES".center(100))
    print("="*100)
    print("1. Registrar Pasajero")
    print("2. Editar datos de Pasajero")
    print("3. Limpiar datos de Pasajero")
    print("4. Buscar Pasajero")
    print("5. Salir")
    print("="*100)

    destinos = ["Mar de Ajó", "Pinamar", "Villa Gesell", "Mar del Plata", "Miramar", "Necochea"]

    while True:
        try:
            opcion = int(input("Elija la operacion a realizar, por favor: \n"))
        
            assert opcion in [1, 2, 3, 4, 5, 6]

            if opcion == 1:
                # funcion para cargar pasaje
                print("Usted selecciono CARGAR PASAJERO... \n")

            elif opcion == 2:
                # modificar pasaje 
                print("Usted selecciono EDITAR DATOS DE PASAJERO... \n")

            elif opcion == 3:
                # cancelar pasaje
                print("Usted selecciono LIMPIAR DATOS DE PASAJERO... \n")

            elif opcion == 4:
                # busqueda de pasaje segun parametro
                print("Usted selecciono BUSCAR PASAJERO... \n")

            elif opcion == 5:
                print("SALIENDO DE VENTAS DE PASAJES, GRACIAS POR SU VISITA... \n")
                break

        except ValueError: 
            print("Opcion invalida, intente nuevamente \n\n")
        except AssertionError:
            print("La opción ingresada es inexistente, intente nuevamente \n\n")

main()


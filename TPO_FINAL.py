def validar_registrar_pasajero():
    while True:
        try:
            dni = input("DNI pasajero: ")
            assert dni.isdigit(), "DNI debe contener solo numeros"
            break 
        
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
        print("ERROR: archivo datos_pasajeros.csv no encontrado")
    
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
    

def elegir_micro():
    destinos = ["mar del plata","pinamar","mar de ajo"]
    
    while True:
        #hay que arreglar esto, en realidad deberia ser un menu con opciones, ya nos habia criticado esto thompson
        destino = input("DESTINO: (mar del plata/pinamar/mar de ajo): ")

        try:
            assert destino in destinos, "Destino no valido"
            break
        except AssertionError as mensaje:
            print(mensaje)

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
            assert 1 <= m <= 12, "La fecha ingresada no es valida"
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
        print("No se hallaron coincidencias")
        return None
    
    print("Coincidencia encontrada")
    return micro_encontrado


def eligir_asiento(micro):
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
    libres = [x for x in todos if x not in asientos_ocupados]

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
        print("ERROR: ",mensaje)
        return None
    
    finally: 
        try:
            arch.close()
        except NameError:
            pass

    print("Pasaje registrado exitosamente")
    print(f"ID de pasaja: {nuevo_id}")

    return nuevo_id


def cargar_pasaje():
    print("="*100)
    print("REGISTRO DE PASAJE".center(100))
    print("="*100)
    print("")

    while True:
        try:
            dni = input("DNI del pasajero: \n").strip()
            assert dni.isdigit(), "El DNI ingresado es invalido"
            break
        except AssertionError as mensaje:
            print(mensaje)

    encontrado = False
    nombre = ""
    apellido = ""

    try:
        arch = open("pasajeros.csv", "r")
        
        for linea in arch:
            fila = linea.strip().split(",")
            if fila[0] == dni:
                encontrado = True
                nombre = fila[1]
                apellido = fila[2]
                break
        
    except FileNotFoundError:
        pass

    finally:
        try:
            arch.close()
        except NameError:
            pass

    if not encontrado:
        #podriamos agregar una opcion por si el pasajero no quiere registrarse
        print("Pasajero no registrado.\n")
        nombre = input("Nombre del Pasajero: ").strip()
        apellido = input("Apellido del Pasajero: ").strip()

        try:
            arch = open("pasajeros.csv","a")
            arch.write(f"{dni},{nombre},{apellido}\n")

        except Exception as mensaje:
            print("ERROR: ",mensaje)

        finally:
            try:
                arch.close()
            except NameError:
                pass

    print(f"\nPasajero confirmado exitosamente: {nombre} {apellido}\n")

    destinos = ["Mar de Ajó", "Pinamar", "Villa Gesell", "Mar del Plata", "Miramar", "Necochea"]

    #aca iria el menu donde se muestran los destinos
    #
    #
    #

    while True:
        try:
            opcion = int(input("Destino: \n"))
            
            assert 1 <= op <= len(destinos),"La opcion ingresada es invalida"
            destino = destinos[opcion - 1]
            break
            
        except Exception as mensaje:
            print(mensaje)
        
    micros_disponibles = []

    try:
        arch = open("micros.csv", "r")

        for linea in arch:
            fila = linea.strip.split(",")
            if fila[2] == destino:
                micros_disponibles.append({
                    "id_micro": fila[0],
                    "fecha": fila[1],
                    "destino": fila[2],
                    "asientos": int(fila[3])
                })
            
    except FileNotFoundError:
        print("")
        return

    finally:
        try:
            arch.close()
        except NameError:
            pass

    if len(micros_disponibles) == 0:
        print("No se hallaron coincidencias para el destino seleccionado\n")
        return

    print("\nMicros disponibles: ")
    for i, m in enumerate(micros_disponibles, 1):
        print(f"{i}. micro {m['id_micro']} - fecha {m['fecha']} - asientos {m['asientos']}")

#mmmmm podriamos cambiar esto, es muy obvio que lo hizo chatgpt

    while True:
        try:
            op = int(input("Micro seleccionado: \n"))
            assert 1 <= op <= len(micros_disponibles), "La opcion ingresada es invalida"
            micro_sel = micros_disponibles [op - 1]
            break
            
        except Exception as mensaje:
            print(mensaje)
    
    print(f"\nMicro seleccionado: {micro_sel['id_micro']} ({micro_sel['fecha']})\n")

    ocupado = set()

    try:
        arch = open("pasajes.csv","r")

        for linea in arch:
            fila = linea.strip().split(",")
            if fila[2] == micro_sel["id_micro"]:
                ocupado.add(int(fila[3]))
    
    except FileNotFoundError:
        pass
    
    finally:
        try:
            arch.close()
        except NameError:
            pass
    
    total = micro_sel["asientos"]

    print("Asientos disponibles: ")
    libres = []
    for n in range(1, total + 1):
        if n not in ocupado:
            libres.append(n)

    print(libres)

    if not libres:
        print("No se encontraron asientos disponibles para el micro seleccionado")
        return
    
#hay que preguntarle a chatgpt por que pone estas funciones como return asi nomas

    while True:
        try:
            asiento = int(input("Numero de asiento: \n"))
            assert asiento in libres, "El valor ingresado no es valido"
            break
        
        except Exception as mensaje:
            print(mensaje)

    registrar_pasaje(dni, micro_sel["id_micro"], asiento)

    print("")
    print("PASAJE REGISTRADO EXITOSAMENTE".center(100))


def eliminar_pasaje():
    print("="*100)
    print("CANCELAR PASAJE".center(100))
    print("="*100)

    while True:
        try:
            id_buscar = input("ID del pasaje: \n").strip()
            assert id_buscar.isdigit(), "El ID ingresado no es valido"
            break

        except AssertionError as mensaje:
            print(mensaje)

    id_buscar = int(id_buscar)

    lineas_filtradas = []
    encontrado = False

    try: 
        arch = open("pasajes.csv","r")
        encabezado = arch.readline()
        lineas_filtradas.append(encabezado)

        for linea in arch:
            fila = linea.strip().split(",")
            try:
                id_actual = int(fila[0])
            except:
                continue

        if id_actual == id_buscar:
            encontrado = True
        else:
            lineas_filtradas.append(linea)
    
    except FileNotFoundError:
        print("ERROR: archivo pasajes.csv no encontrado")
        return
    
    finally:
        try:
            arch.close()
        except NameError:
            pass
    
    if not encontrado:
        print("No se hallaron coincidencias para el ID ingresado")
        return
    
    try:
        arch = open("pasaje.csv","w")
        for linea in lineas_filtradas:
            arch.write(linea)
    
    except Exception as mensaje:
        print("ERROR:", mensaje)
        return
    
    finally:
        try:
            arch.close()
        except NameError:
            pass
    
    print(f"Pasaje con ID {id_buscar} eliminado exitosamente \n")


def buscar_pasaje_por_id():
    try:
        id_buscar = input("Ingrese el ID del pasaje (o 'X' para salir): ").strip()

        if id_buscar.upper() == "X":
            print("B煤squeda cancelada por el usuario.\n")
            return

        assert id_buscar.isdigit(), "El ID debe contener solo n煤meros."

        encontrado = False
        dni_pasajero = None

        try:
            arch_pasajes = open("pasajes.csv", "r")
            for linea in arch_pasajes:
                fila = linea.strip().split(",")
                if len(fila) < 4:
                    continue

                id_pasaje_arch = fila[0].strip()
                dni_arch = fila[1].strip()

                if id_pasaje_arch == id_buscar:
                    encontrado = True
                    dni_pasajero = dni_arch
                    break

        except FileNotFoundError:
            print("ERROR: archivo pasajes.csv no encontrado.")
            return

        finally:
            try:
                arch_pasajes.close()
            except NameError:
                pass

        if not encontrado:
            print("No se encontr贸 ning煤n pasaje con ese ID. Intente nuevamente.\n")
            return buscar_pasaje_por_id()

        nombre = ""
        apellido = ""

        try:
            arch_pasajeros = open("pasajeros.csv", "r")
            for linea in arch_pasajeros:
                fila = linea.strip().split(",")
                if len(fila) < 3:
                    continue
                dni_arch = fila[0].strip()
                if dni_arch == dni_pasajero:
                    nombre = fila[1].strip()
                    apellido = fila[2].strip()
                    break

        except FileNotFoundError:
            print("ERROR: archivo pasajeros.csv no encontrado.")
            return

        finally:
            try:
                arch_pasajeros.close()
            except NameError:
                pass

        print("\n=== RESULTADO DE LA B脷SQUEDA ===")
        print(f"ID del pasaje: {id_buscar}")
        print(f"DNI del pasajero: {dni_pasajero}")
        print(f"Nombre del pasajero: {nombre} {apellido}")
        print("===============================\n")

    except AssertionError as mensaje:
        print("ERROR:", mensaje)
        return buscar_pasaje_por_id()


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
            print("Opcion invalida, intente nuevamente \n\n")
main()

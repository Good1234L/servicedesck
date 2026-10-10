import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Configuración inicial de la página
st.set_page_config(
    page_title="Service Desk ITSM - ITIL v4",
    page_icon="🛠️",
    layout="wide"
)

# Archivo local para persistencia de datos
DATA_FILE = "tickets.json"

def cargar_tickets():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_tickets(tickets):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tickets, f, ensure_ascii=False, indent=4)

# Función para generar la guía de procedimiento ITIL v4 según el tipo de incidencia
def obtener_guia_resolucion(asunto):
    guias = {
        "Fallo de encendido": "1. Verificar conexión del cable de corriente y tomacorriente.\n2. Desconectar periféricos externos y probar encendido.\n3. Revisar el estado de la fuente de poder, placa base o batería.",
        "Periféricos dañados": "1. Probar el teclado, ratón o monitor en otro puerto o equipo.\n2. Actualizar o reinstalar controladores (Drivers) de hardware.\n3. Reemplazar el dispositivo si presenta daño físico irreparable.",
        "Problemas de batería / cargador": "1. Comprobar si el LED indicador de carga se enciende.\n2. Limpiar el puerto de carga de polvo u obstrucciones.\n3. Reemplazar el adaptador de corriente o la batería degradada.",
        "Daño físico": "1. Evaluar la gravedad del daño (pantalla, carcasa o derrame).\n2. Resguardar y extraer el disco de almacenamiento para evitar pérdida de datos.\n3. Derivar el equipo al taller técnico especializado.",
        "Error de inicio de sesión": "1. Validar la correcta escritura de credenciales y dominio.\n2. Borrar caché y archivos temporales de la aplicación afectada.\n3. Reinstalar el software o reparar dependencias del sistema.",
        "Instalación o actualización": "1. Comprobar requisitos mínimos de hardware y espacio en disco.\n2. Otorgar permisos temporales de administrador al instalador.\n3. Ejecutar el paquete de instalación oficial y verificar registros (logs).",
        "Licencia vencida": "1. Consultar el estado de la suscripción con el administrador de licencias.\n2. Renovar la clave de producto en el portal corporativo.\n3. Ingresar el nuevo código de activación en la aplicación.",
        "Lentitud general": "1. Monitorear el uso de CPU, Memoria RAM y Disco en el Administrador de Tareas.\n2. Finalizar procesos en segundo plano innecesarios.\n3. Optimizar el arranque del sistema o proponer ampliación de hardware.",
        "Sin conexión a internet": "1. Comprobar el estado físico del cable de red UTP o la señal Wi-Fi.\n2. Reiniciar el equipo y el switch o router de área.\n3. Renovar la dirección IP mediante comandos de consola (ipconfig /renew).",
        "Problemas con la VPN": "1. Verificar que el acceso a internet general funcione correctamente.\n2. Validar credenciales de autenticación para red remota.\n3. Reinstalar el certificado de seguridad o el cliente VPN corporativo.",
        "Corte en la red local": "1. Comprobar la accesibilidad al servidor y gateway predeterminado.\n2. Verificar permisos de acceso a carpetas compartidas e impresoras de red.\n3. Revisar el estado de los switches de distribución locales.",
        "Intermitencia": "1. Revisar la integridad de los conectores RJ45 y el cableado estructurado.\n2. Realizar pruebas de ping sostenido para detectar pérdida de paquetes.\n3. Reportar saturación de línea al proveedor de servicios de internet (ISP).",
        "Bloqueo de cuenta": "1. Revisar las políticas de bloqueo por intentos fallidos en Active Directory.\n2. Desbloquear la cuenta del usuario afectado.\n3. Indicar al usuario las pautas de seguridad para contraseñas.",
        "Restablecimiento de clave": "1. Validar la identidad del usuario mediante canales autorizados.\n2. Generar una contraseña temporal de un solo uso.\n3. Forzar el cambio obligatorios de clave en el próximo inicio de sesión.",
        "Altas y bajas de usuario": "1. Recibir la solicitud formal aprobada por la Jefatura de Área.\n2. Crear o deshabilitar la cuenta de usuario en los sistemas corporativos.\n3. Asignar los perfiles de seguridad correspondientes al puesto.",
        "Error de permisos": "1. Revisar las listas de control de acceso (ACL) de la carpeta o recurso.\n2. Incorporar al usuario al grupo de seguridad adecuado.\n3. Actualizar los tokens de sesión del usuario en la red.",
        "Fallo en el teléfono IP / Anexo": "1. Comprobar la conexión del cable de red PoE en el aparato telefónico.\n2. Reiniciar el dispositivo desconectando la alimentación eléctrica.\n3. Validar el registro de la extensión en la central telefónica IP (PBX).",
        "Problemas de videoconferencia": "1. Verificar la configuración de permisos de cámara y micrófono en el navegador o app.\n2. Realizar una llamada de prueba en la plataforma (Teams/Zoom/Meet).\n3. Ajustar la resolución de video si existe congestión de red.",
        "Correo electrónico": "1. Comprobar la conectividad con los servidores de correo (SMTP/IMAP).\n2. Revisar la cuota de almacenamiento disponible en el buzón.\n3. Reconfigurar el perfil de correo en Outlook o cliente webmail.",
        "Atasco de papel": "1. Abrir con precaución las bandejas y cubiertas de acceso de la impresora.\n2. Extraer el papel atascado siguiendo la dirección del trayecto sin rasgarlo.\n3. Comprobar el buen estado de los rodillos de alimentación.",
        "Falta de consumibles": "1. Identificar el cartucho, tóner o rodillo con nivel crítico.\n2. Solicitar el insumo de reemplazo al almacén de logística.\n3. Instalar el consumible nuevo siguiendo las indicaciones del fabricante.",
        "Cola de impresión bloqueada": "1. Detener el servicio de cola de impresión (Spooler) desde el sistema operativo.\n2. Limpiar los archivos temporales acumulados en la ruta de impresión.\n3. Reiniciar el servicio y reanudar el envío de trabajos."
    }
    return guias.get(asunto, "1. Realizar diagnóstico preliminar de la incidencia.\n2. Aplicar pruebas de aislamiento y verificación.\n3. Documentar la solución aplicada y cerrar el ticket.")

# Inicialización con los 22 casos oficiales del documento técnico
if "tickets" not in st.session_state:
    tickets_cargados = cargar_tickets()
    if not tickets_cargados:
        st.session_state.tickets = [
            {
                "ID": "INC-1001", "Fecha": "2026-10-10 08:00", "Cliente": "Mario Gómez", "Area": "Sistemas",
                "Categoria": "1. Hardware y Equipos", "Asunto": "Fallo de encendido", "Prioridad": "Alta", "Estado": "Abierto",
                "Descripcion": "Equipo no enciende o se apaga de forma inesperada."
            },
            {
                "ID": "INC-1002", "Fecha": "2026-10-10 08:20", "Cliente": "Lucía Torres", "Area": "Administración",
                "Categoria": "1. Hardware y Equipos", "Asunto": "Periféricos dañados", "Prioridad": "Media", "Estado": "En Proceso",
                "Descripcion": "Problemas con teclado, ratón, monitor, cámara web o auriculares."
            },
            {
                "ID": "INC-1003", "Fecha": "2026-10-10 08:40", "Cliente": "Carlos Ruiz", "Area": "Ventas",
                "Categoria": "1. Hardware y Equipos", "Asunto": "Problemas de batería / cargador", "Prioridad": "Media", "Estado": "Abierto",
                "Descripcion": "Batería no carga, descarga muy rápida o puerto de corriente flojo."
            },
            {
                "ID": "INC-1004", "Fecha": "2026-10-10 09:00", "Cliente": "Ana Mendoza", "Area": "Gerencia",
                "Categoria": "1. Hardware y Equipos", "Asunto": "Daño físico", "Prioridad": "Crítica", "Estado": "Abierto",
                "Descripcion": "Pantalla rota, carcasa agrietada o derrame de líquidos."
            },
            {
                "ID": "INC-1005", "Fecha": "2026-10-10 09:20", "Cliente": "Jorge Quispe", "Area": "Contabilidad",
                "Categoria": "2. Software y Aplicaciones", "Asunto": "Error de inicio de sesión", "Prioridad": "Alta", "Estado": "En Proceso",
                "Descripcion": "Aplicación que se cierra sola, se congela o muestra código de error."
            },
            {
                "ID": "INC-1006", "Fecha": "2026-10-10 09:40", "Cliente": "Elena Ramos", "Area": "Logística",
                "Categoria": "2. Software y Aplicaciones", "Asunto": "Instalación o actualización", "Prioridad": "Media", "Estado": "Abierto",
                "Descripcion": "Solicitud o fallo al instalar/actualizar un programa requerido."
            },
            {
                "ID": "INC-1007", "Fecha": "2026-10-10 10:00", "Cliente": "Rosa Perez", "Area": "Finanzas",
                "Categoria": "2. Software y Aplicaciones", "Asunto": "Licencia vencida", "Prioridad": "Baja", "Estado": "Resuelto",
                "Descripcion": "Mensaje de producto no activado o pérdida de suscripción de software."
            },
            {
                "ID": "INC-1008", "Fecha": "2026-10-10 10:20", "Cliente": "Pedro Infantes", "Area": "Sistemas",
                "Categoria": "2. Software y Aplicaciones", "Asunto": "Lentitud general", "Prioridad": "Baja", "Estado": "Resuelto",
                "Descripcion": "Consumo excesivo de CPU o memoria RAM por parte de un programa."
            },
            {
                "ID": "INC-1009", "Fecha": "2026-10-10 10:40", "Cliente": "Rosaura Limachi", "Area": "Operaciones",
                "Categoria": "3. Conectividad y Red", "Asunto": "Sin conexión a internet", "Prioridad": "Crítica", "Estado": "Abierto",
                "Descripcion": "Pérdida total de acceso a la red (alámbrica o Wi-Fi)."
            },
            {
                "ID": "INC-1010", "Fecha": "2026-10-10 11:00", "Cliente": "David Mamani", "Area": "Recursos Humanos",
                "Categoria": "3. Conectividad y Red", "Asunto": "Problemas con la VPN", "Prioridad": "Alta", "Estado": "En Proceso",
                "Descripcion": "Error al autenticar o conectar la red privada virtual para trabajo remoto."
            },
            {
                "ID": "INC-1011", "Fecha": "2026-10-10 11:20", "Cliente": "Sofía Cárdenas", "Area": "Legal",
                "Categoria": "3. Conectividad y Red", "Asunto": "Corte en la red local", "Prioridad": "Alta", "Estado": "Abierto",
                "Descripcion": "Imposibilidad de acceder a carpetas compartidas o impresoras de la red."
            },
            {
                "ID": "INC-1012", "Fecha": "2026-10-10 11:40", "Cliente": "Raúl Benavides", "Area": "Sistemas",
                "Categoria": "3. Conectividad y Red", "Asunto": "Intermitencia", "Prioridad": "Media", "Estado": "En Proceso",
                "Descripcion": "Caídas constantes de señal o velocidad muy por debajo de lo normal."
            },
            {
                "ID": "INC-1013", "Fecha": "2026-10-10 12:00", "Cliente": "Carmen Salas", "Area": "Marketing",
                "Categoria": "4. Accesos y Cuentas (Identidad)", "Asunto": "Bloqueo de cuenta", "Prioridad": "Media", "Estado": "Resuelto",
                "Descripcion": "Usuario bloqueado por intentos fallidos de contraseña."
            },
            {
                "ID": "INC-1014", "Fecha": "2026-10-10 12:20", "Cliente": "Héctor Soto", "Area": "Administración",
                "Categoria": "4. Accesos y Cuentas (Identidad)", "Asunto": "Restablecimiento de clave", "Prioridad": "Baja", "Estado": "Cerrado",
                "Descripcion": "Solicitud de cambio o blanqueo de contraseña."
            },
            {
                "ID": "INC-1015", "Fecha": "2026-10-10 12:40", "Cliente": "Diana Flores", "Area": "Recursos Humanos",
                "Categoria": "4. Accesos y Cuentas (Identidad)", "Asunto": "Altas y bajas de usuario", "Prioridad": "Alta", "Estado": "Abierto",
                "Descripcion": "Creación de nueva cuenta, asignación de permisos o desactivación por salida de personal."
            },
            {
                "ID": "INC-1016", "Fecha": "2026-10-10 13:00", "Cliente": "Fernando Gomez", "Area": "Sistemas",
                "Categoria": "4. Accesos y Cuentas (Identidad)", "Asunto": "Error de permisos", "Prioridad": "Media", "Estado": "En Proceso",
                "Descripcion": "Denegación de acceso a una carpeta, sistema o recurso específico."
            },
            {
                "ID": "INC-1017", "Fecha": "2026-10-10 13:20", "Cliente": "Valeria Luna", "Area": "Ventas",
                "Categoria": "5. Telefonía y Comunicaciones", "Asunto": "Fallo en el teléfono IP / Anexo", "Prioridad": "Media", "Estado": "Abierto",
                "Descripcion": "Sin tono, llamadas que no entran o no salen."
            },
            {
                "ID": "INC-1018", "Fecha": "2026-10-10 13:40", "Cliente": "Gabriel Condori", "Area": "Sistemas",
                "Categoria": "5. Telefonía y Comunicaciones", "Asunto": "Problemas de videoconferencia", "Prioridad": "Baja", "Estado": "Resuelto",
                "Descripcion": "Fallos de audio o video en plataformas como Zoom, Teams o Meet."
            },
            {
                "ID": "INC-1019", "Fecha": "2026-10-10 14:00", "Cliente": "Patricia Vega", "Area": "Logística",
                "Categoria": "5. Telefonía y Comunicaciones", "Asunto": "Correo electrónico", "Prioridad": "Alta", "Estado": "En Proceso",
                "Descripcion": "No recibe o no envía correos, o problemas con la configuración del cliente (Outlook, webmail)."
            },
            {
                "ID": "INC-1020", "Fecha": "2026-10-10 14:20", "Cliente": "Manuel Paredes", "Area": "Contabilidad",
                "Categoria": "6. Impresión y Escaneo", "Asunto": "Atasco de papel", "Prioridad": "Baja", "Estado": "Resuelto",
                "Descripcion": "Papel trabado en la bandeja o fusor."
            },
            {
                "ID": "INC-1021", "Fecha": "2026-10-10 14:40", "Cliente": "Silvia Morales", "Area": "Administración",
                "Categoria": "6. Impresión y Escaneo", "Asunto": "Falta de consumibles", "Prioridad": "Media", "Estado": "Abierto",
                "Descripcion": "Nivel bajo o agotamiento de tóner, cartuchos o rodillos."
            },
            {
                "ID": "INC-1022", "Fecha": "2026-10-10 15:00", "Cliente": "Renzo Morales", "Area": "Finanzas",
                "Categoria": "6. Impresión y Escaneo", "Asunto": "Cola de impresión bloqueada", "Prioridad": "Media", "Estado": "En Proceso",
                "Descripcion": "Trabajos acumulados que no se envían a la impresora."
            }
        ]
        guardar_tickets(st.session_state.tickets)
    else:
        st.session_state.tickets = tickets_cargados

if "es_admin" not in st.session_state:
    st.session_state.es_admin = False

# Título de la Aplicación
st.title("🛠️ Sistema de Gestión de Tickets - Service Desk")
st.markdown("Plataforma de atención de incidentes ITIL v4 y seguimiento de SLAs.")

st.divider()

# Menú lateral para navegación
menu = st.sidebar.radio(
    "Navegación / Módulos",
    ["📊 Panel General", "➕ Registrar Ticket", "🎟️ Consulta y Ticket Digital", "🔐 Panel de Administrador"]
)

# ---------------------------------------------------------
# MÓDULO 1: PANEL GENERAL
# ---------------------------------------------------------
if menu == "📊 Panel General":
    st.subheader("📊 Indicadores de Soporte Técnico (SLA & KPIs)")

    df = pd.DataFrame(st.session_state.tickets)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tickets", len(df))
    
    if not df.empty:
        col2.metric("Abiertos", len(df[df["Estado"] == "Abierto"]))
        col3.metric("En Proceso", len(df[df["Estado"] == "En Proceso"]))
        col4.metric("Resueltos", len(df[df["Estado"] == "Resuelto"]))
    else:
        col2.metric("Abiertos", 0)
        col3.metric("En Proceso", 0)
        col4.metric("Resueltos", 0)

    st.divider()
    st.subheader("📋 Lista de Incidentes Registrados")

    if not df.empty:
        filtro_estado = st.selectbox("Filtrar por Estado", ["Todos"] + list(df["Estado"].unique()))
        if filtro_estado != "Todos":
            df_display = df[df["Estado"] == filtro_estado]
        else:
            df_display = df

        st.dataframe(df_display, use_container_width=True)
    else:
        st.info("No hay tickets registrados actualmente.")

# ---------------------------------------------------------
# MÓDULO 2: REGISTRAR TICKET
# ---------------------------------------------------------
elif menu == "➕ Registrar Ticket":
    st.subheader("➕ Registro de Nuevo Incidente / Solicitud")

    if not st.session_state.es_admin:
        st.warning("Solo un administrador puede registrar nuevos tickets. Accede desde el Panel de Administrador.")

    with st.form("form_ticket", clear_on_submit=True):
        col_a, col_b = st.columns(2)

        with col_a:
            cliente = st.text_input("Nombre del Cliente / Usuario", placeholder="Ej. Juan Pérez")
            area = st.selectbox("Área / Departamento", ["Sistemas", "Contabilidad", "Ventas", "Recursos Humanos", "Logística"])
            categoria = st.selectbox("Categoría del Problema", [
                "1. Hardware y Equipos", "2. Software y Aplicaciones", "3. Conectividad y Red", 
                "4. Accesos y Cuentas (Identidad)", "5. Telefonía y Comunicaciones", "6. Impresión y Escaneo"
            ])

        with col_b:
            prioridad = st.selectbox("Prioridad (Impacto/Urgencia)", ["Baja", "Media", "Alta", "Crítica"])
            asunto = st.text_input("Asunto Resumido", placeholder="Ej. Falla de red en laptop")

        descripcion = st.text_area("Descripción detallada del incidente", placeholder="Detalla los síntomas y código de error...")

        btn_guardar = st.form_submit_button(
            "💾 Generar y Guardar Ticket",
            disabled=not st.session_state.es_admin
        )

        if btn_guardar:
            if not st.session_state.es_admin:
                st.error("Solo un administrador puede registrar nuevos tickets.")
            elif cliente and asunto:
                next_id = 1001 + len(st.session_state.tickets)
                nuevo_id = f"INC-{next_id}"
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")

                nuevo_ticket = {
                    "ID": nuevo_id,
                    "Fecha": fecha_actual,
                    "Cliente": cliente,
                    "Area": area,
                    "Categoria": categoria,
                    "Asunto": asunto,
                    "Prioridad": prioridad,
                    "Estado": "Abierto",
                    "Descripcion": descripcion
                }

                st.session_state.tickets.append(nuevo_ticket)
                guardar_tickets(st.session_state.tickets)
                st.success(f"✅ Ticket **{nuevo_id}** registrado y guardado con éxito.")
            else:
                st.error("⚠️ Por favor completa los campos requeridos (Cliente y Asunto).")

# ---------------------------------------------------------
# MÓDULO 3: CONSULTA, TICKET DIGITAL Y GUÍA DE PROCEDIMIENTO
# ---------------------------------------------------------
elif menu == "🎟️ Consulta y Ticket Digital":
    st.subheader("🔍 Visualización, Comprobante y Guía de Procedimiento ITIL v4")

    if st.session_state.tickets:
        lista_ids = [t["ID"] for t in st.session_state.tickets]
        ticket_sel_id = st.selectbox("Seleccione el ID del Ticket", lista_ids)

        ticket = next(t for t in st.session_state.tickets if t["ID"] == ticket_sel_id)

        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown("### 📋 Cambiar Estado Rápido")
            estados_disponibles = ["Abierto", "En Proceso", "Resuelto", "Cerrado"]
            idx_actual = estados_disponibles.index(ticket["Estado"]) if ticket["Estado"] in estados_disponibles else 0
            
            nuevo_estado = st.selectbox("Actualizar Estado", estados_disponibles, index=idx_actual)
            if st.button("Actualizar Estado"):
                ticket["Estado"] = nuevo_estado
                guardar_tickets(st.session_state.tickets)
                st.success("Estado actualizado correctamente.")

            st.divider()
            st.markdown("### 🎫 Ticket Digital / Comprobante")
            ticket_box = f"""
----------------------------------------
           SERVICE DESK IT
         TICKET DE SOPORTE
----------------------------------------
N° Ticket  : {ticket['ID']}
Fecha      : {ticket['Fecha']}
Cliente    : {ticket['Cliente']}
Área       : {ticket['Area']}
----------------------------------------
Categoría  : {ticket['Categoria']}
Prioridad  : {ticket['Prioridad']}
Estado     : {ticket['Estado']}
----------------------------------------
Asunto:
{ticket['Asunto']}

Detalle:
{ticket['Descripcion']}
----------------------------------------
   Gracias por contactar al soporte.
----------------------------------------
            """
            st.code(ticket_box, language="text")
            st.download_button(
                label="📥 Descargar Ticket (TXT)",
                data=ticket_box,
                file_name=f"ticket_{ticket['ID']}.txt",
                mime="text/plain"
            )

        with col_right:
            st.markdown("### 📖 Guía de Procedimiento y Resolución (ITIL v4)")
            pasos_resolucion = obtener_guia_resolucion(ticket["Asunto"])

            documento_procedimiento = f"""
========================================
   GUÍA DE PROCEDIMIENTO TÉCNICO ITIL v4
========================================
ID de Incidente : {ticket['ID']}
Categoría       : {ticket['Categoria']}
Asunto / Falla  : {ticket['Asunto']}
----------------------------------------
PASOS RECOMENDADOS PARA LA RESOLUCIÓN:
----------------------------------------
{pasos_resolucion}
----------------------------------------
Validado por Mesa de Ayuda ITIL v4.
            """

            st.text_area("Protocolo Operativo de Soporte", value=documento_procedimiento, height=250)

            st.download_button(
                label="📥 Descargar Guía de Procedimiento (TXT)",
                data=documento_procedimiento,
                file_name=f"procedimiento_{ticket['ID']}.txt",
                mime="text/plain"
            )
    else:
        st.info("No hay tickets disponibles.")

# ---------------------------------------------------------
# MÓDULO 4: PANEL DE ADMINISTRADOR
# ---------------------------------------------------------
elif menu == "🔐 Panel de Administrador":
    st.subheader("🔐 Panel de Control Exclusivo - Administrador")
    st.markdown("Acceso restringido para la edición avanzada o eliminación de registros.")

    password = ""
    if not st.session_state.es_admin:
        password = st.text_input("Ingrese contraseña de Administrador", type="password")
        if password == "admin040906":
            st.session_state.es_admin = True

    if st.session_state.es_admin:
        st.success("Acceso concedido. Modo Administrador Activo.")
        if st.button("Cerrar sesión de administrador"):
            st.session_state.es_admin = False
            st.rerun()
        
        if st.session_state.tickets:
            st.divider()
            st.markdown("### 🛠️ Gestión y Edición de Tickets")

            lista_ids = [t["ID"] for t in st.session_state.tickets]
            id_a_editar = st.selectbox("Seleccione Ticket a Administrar", lista_ids)

            t_edit = next(t for t in st.session_state.tickets if t["ID"] == id_a_editar)

            with st.form("form_admin_edit"):
                nuevo_cliente = st.text_input("Cliente", value=t_edit["Cliente"])
                nuevo_asunto = st.text_input("Asunto", value=t_edit["Asunto"])
                nueva_desc = st.text_area("Descripción", value=t_edit["Descripcion"])
                nuevo_est = st.selectbox("Estado", ["Abierto", "En Proceso", "Resuelto", "Cerrado"], index=["Abierto", "En Proceso", "Resuelto", "Cerrado"].index(t_edit["Estado"]))
                nueva_prio = st.selectbox("Prioridad", ["Baja", "Media", "Alta", "Crítica"], index=["Baja", "Media", "Alta", "Crítica"].index(t_edit["Prioridad"]))

                guardar_cambios = st.form_submit_button("💾 Guardar Cambios")

                if guardar_cambios:
                    t_edit["Cliente"] = nuevo_cliente
                    t_edit["Asunto"] = nuevo_asunto
                    t_edit["Descripcion"] = nueva_desc
                    t_edit["Estado"] = nuevo_est
                    t_edit["Prioridad"] = nueva_prio
                    guardar_tickets(st.session_state.tickets)
                    st.success(f"Ticket {id_a_editar} modificado con éxito.")

            st.divider()
            st.markdown("### ⚠️ Zona de Peligro")
            if st.button("🗑️ Eliminar este Ticket"):
                st.session_state.tickets = [t for t in st.session_state.tickets if t["ID"] != id_a_editar]
                guardar_tickets(st.session_state.tickets)
                st.warning(f"El ticket {id_a_editar} ha sido eliminado permanentemente.")
                st.rerun()
        else:
            st.info("No hay tickets registrados en el sistema para administrar.")
            
    elif password != "":
        st.error("❌ Contraseña incorrecta.")
    else:
        st.info("💡 Ingresa tu contraseña de administrador para desbloquear las opciones de edición y control.")

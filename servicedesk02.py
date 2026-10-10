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

# Inicialización de la base de datos (Inicia completamente vacía, sin ejemplos)
if "tickets" not in st.session_state:
    st.session_state.tickets = cargar_tickets()

# Título de la Aplicación
st.title("🛠️ Sistema de Gestión de Tickets - Service Desk")
st.markdown("Plataforma de atención de incidentes ITIL v4 y seguimiento de SLAs.")

st.divider()

# Menú lateral para navegación (Incluye el panel de Administrador protegido)
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
        # Filtro dinámico
        filtro_estado = st.selectbox("Filtrar por Estado", ["Todos"] + list(df["Estado"].unique()))
        if filtro_estado != "Todos":
            df_display = df[df["Estado"] == filtro_estado]
        else:
            df_display = df

        st.dataframe(df_display, use_container_width=True)
    else:
        st.info("No hay tickets registrados actualmente. El sistema se encuentra vacío.")

# ---------------------------------------------------------
# MÓDULO 2: REGISTRAR TICKET
# ---------------------------------------------------------
elif menu == "➕ Registrar Ticket":
    st.subheader("➕ Registro de Nuevo Incidente / Solicitud")

    with st.form("form_ticket", clear_on_submit=True):
        col_a, col_b = st.columns(2)

        with col_a:
            cliente = st.text_input("Nombre del Cliente / Usuario", placeholder="Ej. Juan Pérez")
            area = st.selectbox("Área / Departamento", ["Sistemas", "Contabilidad", "Ventas", "Recursos Humanos", "Logística"])
            categoria = st.selectbox("Categoría del Problema", ["Hardware", "Software", "Redes / Conectividad", "Accesos / Permisos"])

        with col_b:
            prioridad = st.selectbox("Prioridad (Impacto/Urgencia)", ["Baja", "Media", "Alta", "Crítica"])
            asunto = st.text_input("Asunto Resumido", placeholder="Ej. Falla de red en laptop")

        descripcion = st.text_area("Descripción detallada del incidente", placeholder="Detalla los síntomas y código de error...")

        btn_guardar = st.form_submit_button("💾 Generar y Guardar Ticket")

        if btn_guardar:
            if cliente and asunto:
                next_id = 1001 + len(st.session_state.tickets)
                nuevo_id = f"INC-{next_id}"
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")

                nuevo_ticket = {
                    "ID": nuevo_id,
                    "Fecha": fecha_actual,
                    "Cliente": cliente,
                    "Area": area,
                    "Categoria": categoria,
                    "Prioridad": prioridad,
                    "Estado": "Abierto",
                    "Asunto": asunto,
                    "Descripcion": descripcion
                }

                st.session_state.tickets.append(nuevo_ticket)
                guardar_tickets(st.session_state.tickets)
                st.success(f"✅ Ticket **{nuevo_id}** registrado y guardado con éxito.")
            else:
                st.error("⚠️ Por favor completa los campos requeridos (Cliente y Asunto).")

# ---------------------------------------------------------
# MÓDULO 3: CONSULTA Y TICKET DIGITAL (IMPRIMIBLE)
# ---------------------------------------------------------
elif menu == "🎟️ Consulta y Ticket Digital":
    st.subheader("🔍 Visualización y Generación de Comprobante")

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

        with col_right:
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
    else:
        st.info("No hay tickets disponibles. El sistema está vacío.")

# ---------------------------------------------------------
# MÓDULO 4: PANEL DE ADMINISTRADOR (EXclusivo para ti)
# ---------------------------------------------------------
elif menu == "🔐 Panel de Administrador":
    st.subheader("🔐 Panel de Control Exclusivo - Administrador")
    st.markdown("Acceso restringido para la edición avanzada o eliminación de registros.")

    # Control de contraseña (puedes cambiar "admin123" por la clave que prefieras)
    password = st.text_input("Ingrese contraseña de Administrador", type="password")

    if password == "admin123":
        st.success("Accesso concedido. Modo Administrador Activo.")
        
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

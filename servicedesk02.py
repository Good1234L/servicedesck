import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración inicial de la página
st.set_page_config(
    page_title="Service Desk ITSM - ITIL v4",
    page_icon="🛠️",
    layout="wide"
)

# Inicialización de la base de datos en estado de sesión (Session State)
if "tickets" not in st.session_state:
    st.session_state.tickets = [
        {
            "ID": "INC-1001",
            "Fecha": "2026-10-10 10:15",
            "Cliente": "Carlos Mendoza",
            "Area": "Contabilidad",
            "Categoria": "Hardware",
            "Prioridad": "Alta",
            "Estado": "En Proceso",
            "Asunto": "Impresora de boletas no responde",
            "Descripcion": "La impresora no enciende ni responde al puerto USB."
        },
        {
            "ID": "INC-1002",
            "Fecha": "2026-10-10 11:30",
            "Cliente": "Ana Flores",
            "Area": "Ventas",
            "Categoria": "Software",
            "Prioridad": "Media",
            "Estado": "Abierto",
            "Asunto": "Error al ingresar al sistema de facturación",
            "Descripcion": "Muestra credenciales inválidas al intentar ingresar."
        }
    ]

# Título de la Aplicación
st.title("🛠️ Sistema de Gestión de Tickets - Service Desk")
st.markdown("Plataforma de atención de incidentes ITIL v4 y seguimiento de SLAs.")

st.divider()

# Menú lateral para navegación
menu = st.sidebar.radio(
    "Navegación / Módulos",
    ["📊 Panel General", "➕ Registrar Ticket", "🎟️ Consulta y Ticket Digital"]
)

# ---------------------------------------------------------
# MÓDULO 1: PANEL GENERAL
# ---------------------------------------------------------
if menu == "📊 Panel General":
    st.subheader("📊 Indicadores de Soporte Técnico (SLA & KPIs)")

    df = pd.DataFrame(st.session_state.tickets)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tickets", len(df))
    col2.metric("Abiertos", len(df[df["Estado"] == "Abierto"]))
    col3.metric("En Proceso", len(df[df["Estado"] == "En Proceso"]))
    col4.metric("Resueltos", len(df[df["Estado"] == "Resuelto"]))

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
        st.info("No hay tickets registrados actualmente.")

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
                nuevo_id = f"INC-{1001 + len(st.session_state.tickets)}"
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
                st.success(f"✅ Ticket **{nuevo_id}** registrado con éxito.")
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

        # Buscar el ticket seleccionado
        ticket = next(t for t in st.session_state.tickets if t["ID"] == ticket_sel_id)

        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown("### 📋 Cambiar Estado")
            nuevo_estado = st.selectbox("Actualizar Estado", ["Abierto", "En Proceso", "Resuelto", "Cerrado"], index=["Abierto", "En Proceso", "Resuelto", "Cerrado"].index(ticket["Estado"]))
            if st.button("Actualizar Estado"):
                ticket["Estado"] = nuevo_estado
                st.success("Estado actualizado correctamente.")

        with col_right:
            st.markdown("### 🎫 Ticket Digital / Comprobante")
            
            # Plantilla visual tipo Ticket
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

            # Botón para descargar ticket en archivo TXT
            st.download_button(
                label="📥 Descargar Ticket (TXT)",
                data=ticket_box,
                file_name=f"ticket_{ticket['ID']}.txt",
                mime="text/plain"
            )
    else:
        st.info("No hay tickets disponibles para visualizar.")

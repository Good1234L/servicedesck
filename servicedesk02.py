import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuración de página de nivel empresarial
st.set_page_config(
    page_title="Enterprise ITSM & Service Desk | ITIL v4", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS corporativos avanzados
st.markdown("""
    <style>
    .main-header {
        font-size: 26px;
        color: #0f172a;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 14px;
        color: #475569;
        margin-bottom: 20px;
    }
    .card-kpi {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 15px;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 1. INICIALIZACIÓN DE LA BASE DE DATOS EN MEMORIA (ESTRUCTURA ITSM)
if "enterprise_tickets" not in st.session_state:
    # Datos iniciales simulados de alta gerencia / corporativos
    st.session_state.enterprise_tickets = pd.DataFrame([
        {
            "ID Ticket": "INC-2026-001",
            "Tipo": "Incidente",
            "Usuario": "Carlos Mendoza",
            "Correo": "carlos.mendoza@empresa.com",
            "Departamento": "Finanzas",
            "Activo / CI": "LAPTOP-FIN-012",
            "Categoría": "Hardware / Portátiles",
            "Urgencia": "Alta",
            "Impacto": "Alto",
            "Prioridad": "P1 - Crítica",
            "Grupo Asignado": "Soporte Nivel 2 (Infraestructura)",
            "Técnico Asignado": "Roberto Gómez",
            "Estado": "En Diagnóstico",
            "SLA Límite": (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            "Fecha Creación": (datetime.now() - timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M"),
            "Descripción": "El equipo no enciende tras actualización de BIOS corporativa.",
            "Bitácora / Notas": "[10:15] Ticket abierto automático por sistema.\n[10:30] Asignado a Infraestructura. Se solicita prueba de fuente de poder."
        },
        {
            "ID Ticket": "REQ-2026-002",
            "Tipo": "Solicitud de Servicio",
            "Usuario": "Ana Torres",
            "Correo": "ana.torres@empresa.com",
            "Departamento": "Recursos Humanos",
            "Activo / CI": "ACC-SISTEMAS-SAP",
            "Categoría": "Gestión de Accesos / Cuentas",
            "Urgencia": "Media",
            "Impacto": "Medio",
            "Prioridad": "P3 - Media",
            "Grupo Asignado": "Gestión de Identidades (IAM)",
            "Técnico Asignado": "Pendiente de Asignación",
            "Estado": "Nuevo / Abierto",
            "SLA Límite": (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M"),
            "Fecha Creación": (datetime.now() - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M"),
            "Descripción": "Creación de credenciales corporativas para nuevo analista de selección.",
            "Bitácora / Notas": "[11:00] Solicitud registrada desde portal de autoservicio (Nivel 0)."
        }
    ])

# 2. BARRA LATERAL - NAVEGACIÓN ITSM
st.sidebar.markdown("## ⚙️ ITSM Control Center")
st.sidebar.markdown("Framework: **ITIL v4 Compliant**")
menu_opcion = st.sidebar.selectbox("Módulos del Sistema", [
    "📋 Panel de Gestión de Tickets", 
    "➕ Crear Nuevo Requerimiento", 
    "📊 Cuadro de Mando (KPIs & SLA)",
    "🛠️ Administración de Grupos y Activos (CMDB)"
])

st.markdown('<p class="main-header">🏢 Enterprise Service Desk & Incident Management</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Plataforma centralizada para la gestión de servicios de tecnologías de la información.</p>', unsafe_allow_html=True)

# -------------------------------------------------------------------------
# MÓDULO 1: PANEL DE GESTIÓN DE TICKETS
# -------------------------------------------------------------------------
if menu_opcion == "📋 Panel de Gestión de Tickets":
    st.subheader("Filtros y Consulta Avanzada de Casos")
    
    if not st.session_state.enterprise_tickets.empty:
        df = st.session_state.enterprise_tickets
        
        # Filtros rápidos en columnas
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filtro_estado = st.selectbox("Filtrar por Estado", ["Todos", "Nuevo / Abierto", "En Diagnóstico", "Escalado a Nivel 3", "Resuelto", "Cerrado"])
        with col_f2:
            filtro_prioridad = st.selectbox("Filtrar por Prioridad", ["Todas", "P1 - Crítica", "P2 - Alta", "P3 - Media", "P4 - Baja"])
        with col_f3:
            filtro_tipo = st.selectbox("Tipo de Requerimiento", ["Todos", "Incidente", "Solicitud de Servicio"])
            
        # Aplicar filtros lógicos
        df_view = df.copy()
        if filtro_estado != "Todos":
            df_view = df_view[df_view["Estado"] == filtro_estado]
        if filtro_prioridad != "Todas":
            df_view = df_view[df_view["Prioridad"] == filtro_prioridad]
        if filtro_tipo != "Todos":
            df_view = df_view[df_view["Tipo"] == filtro_tipo]
            
        st.markdown("---")
        st.dataframe(df_view[[
            "ID Ticket", "Tipo", "Usuario", "Departamento", "Prioridad", 
            "Grupo Asignado", "Técnico Asignado", "Estado", "SLA Límite"
        ]], use_container_width=True)
        
        # Sección de gestión detallada de un ticket específico
        st.markdown("### 🔍 Gestión y Auditoría de Caso Específico")
        ticket_seleccionado = st.selectbox("Seleccione el ID de Ticket para gestionar", df["ID Ticket"].tolist())
        
        if ticket_seleccionado:
            t_data = df[df["ID Ticket"] == ticket_seleccionado].iloc[0]
            
            with st.expander(f"Detalles Completos del Caso: {ticket_seleccionado}", expanded=True):
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.markdown(f"**Solicitante:** {t_data['Usuario']} ({t_data['Correo']})")
                    st.markdown(f"**Departamento:** {t_data['Departamento']}")
                    st.markdown(f"**Activo / CI Afectado:** {t_data['Activo / CI']}")
                    st.markdown(f"**Tipo:** {t_data['Tipo']} | **Categoría:** {t_data['Categoría']}")
                with col_d2:
                    st.markdown(f"**Urgencia:** {t_data['Urgencia']} | **Impacto:** {t_data['Impacto']}")
                    st.markdown(f"**Prioridad ITIL:** <span style='color:red; font-weight:bold;'>{t_data['Prioridad']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**SLA Límite de Atención:** ⏰ {t_data['SLA Límite']}")
                    st.markdown(f"**Estado Actual:** 📌 {t_data['Estado']}")
                
                st.markdown("---")
                st.markdown(f"**Descripción del Problema:**\n> {t_data['Description'] if 'Description' in t_data else t_data['Descripción']}")
                
                st.markdown(f"**Bitácora Histórica y Notas de Resolución:**")
                st.text_area("Historial de acciones", value=t_data["Bitácora / Notas"], height=120, disabled=True, key=f"hist_{ticket_seleccionado}")
                
                # Acciones de actualización empresarial
                st.markdown("#### ⚡ Acciones del Operador / Analista")
                col_act1, col_act2, col_act3 = st.columns(3)
                
                nuevo_estado_form = col_act1.selectbox("Cambiar Estado", ["Nuevo / Abierto", "En Diagnóstico", "Escalado a Nivel 3", "Resuelto", "Cerrado"], key=f"est_{ticket_seleccionado}")
                nuevo_tecnico = col_act2.text_input("Asignar Técnico Responsable", value=t_data["Técnico Asignado"], key=f"tec_{ticket_seleccionado}")
                nota_adicional = col_act3.text_input("Agregar nota a bitácora", placeholder="Ej: Se reemplazó componente...", key=f"nota_{ticket_seleccionado}")
                
                if st.button("Guardar Cambios en el Ticket", key=f"btn_save_{ticket_seleccionado}"):
                    idx = st.session_state.enterprise_tickets[st.session_state.enterprise_tickets["ID Ticket"] == ticket_seleccionado].index[0]
                    
                    # Actualizar valores
                    st.session_state.enterprise_tickets.loc[idx, "Estado"] = nuevo_estado_form
                    st.session_state.enterprise_tickets.loc[idx, "Técnico Asignado"] = nuevo_tecnico
                    
                    if nota_adicional:
                        timestamp_actual = datetime.now().strftime("%m-%d %H:%M")
                        nueva_bitacora = t_data["Bitácora / Notas"] + f"\n[{timestamp_actual}] ({nuevo_tecnico}): {nota_adicional}"
                        st.session_state.enterprise_tickets.loc[idx, "Bitácora / Notas"] = nueva_bitacora
                        
                    st.success(f"¡El ticket {ticket_seleccionado} ha sido actualizado correctamente en el sistema corporativo!")
                    st.rerun()
    else:
        st.info("No hay tickets registrados actualmente en el sistema.")

# -------------------------------------------------------------------------
# MÓDULO 2: CREAR NUEVO REQUERIMIENTO (FORMULARIO EMPRESARIAL)
# -------------------------------------------------------------------------
elif menu_opcion == "➕ Crear Nuevo Requerimiento":
    st.subheader("Creación de Incidente o Solicitud de Servicio (ITIL)")
    
    with st.form("form_nuevo_enterprise"):
        col_n1, col_n2 = st.columns(2)
        
        with col_n1:
            tipo_req = st.selectbox("Tipo de Requerimiento", ["Incidente (Falla o interrupción)", "Solicitud de Servicio (Petición estándar)"])
            usuario_ing = st.text_input("Nombre del Empleado / Solicitante", placeholder="Ej. María Fernández")
            correo_ing = st.text_input("Correo Electrónico Corporativo", placeholder="maria.fernandez@empresa.com")
            departamento_ing = st.selectbox("Departamento / Área", ["Gerencia", "Finanzas", "Contabilidad", "Operaciones", "Ventas", "Recursos Humanos", "Sistemas / TI"])
            
        with col_n2:
            activo_ing = st.text_input("Activo / Código de Inventario (CMDB)", placeholder="Ej. PC-OFFICE-045 o SW-SAP-01")
            categoria_ing = st.selectbox("Categoría del Servicio", [
                "Hardware / Equipamiento de Red",
                "Hardware / Portátiles y Escritorio",
                "Software / Sistema Operativo",
                "Software / Aplicaciones de Negocio (ERP/CRM)",
                "Gestión de Accesos / Credenciales",
                "Telecomunicaciones / Telefonia IP"
            ])
            urgencia_ing = st.selectbox("Urgencia del Negocio", ["Baja", "Media", "Alta", "Crítica"])
            impacto_ing = st.selectbox("Impacto Operativo", ["Bajo", "Medio", "Alto", "Organización Completa"])

        descripcion_ing = st.text_area("Descripción detallada del incidente o requerimiento", placeholder="Describa el comportamiento anómalo, códigos de error exactos y equipos afectados...")
        
        submitted_enterprise = st.form_submit_button("🚀 Registrar y Enrutar Ticket Automáticamente")
        
        if submitted_enterprise and usuario_ing and descripcion_ing:
            # Lógica automática de priorización ITIL (Matriz Impacto/Urgencia)
            if urgencia_ing == "Crítica" or impacto_ing == "Organización Completa":
                prioridade = "P1 - Crítica"
                horas_sla = 2
                grupo = "Soporte Nivel 2 / Emergencias TI"
            elif urgencia_ing == "Alta" or impacto_ing == "Alto":
                prioridade = "P2 - Alta"
                horas_sla = 8
                grupo = "Soporte Nivel 1 / Help Desk Avanzado"
            elif urgencia_ing == "Media":
                prioridade = "P3 - Media"
                horas_sla = 24
                grupo = "Mesa de Ayuda - Operaciones"
            else:
                prioridade = "P4 - Baja"
                horas_sla = 48
                grupo = "Soporte Técnico General"
                
            prefix = "INC" if "Incidente" in tipo_req else "REQ"
            nuevo_id = f"{prefix}-2026-{len(st.session_state.enterprise_tickets)+1:03d}"
            fecha_creacion_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            sla_limite_str = (datetime.now() + timedelta(hours=horas_sla)).strftime("%Y-%m-%d %H:%M")
            tipo_corto = "Incidente" if "Incidente" in tipo_req else "Solicitud de Servicio"
            
            nuevo_registro_ent = pd.DataFrame([{
                "ID Ticket": nuevo_id,
                "Tipo": tipo_corto,
                "Usuario": usuario_ing,
                "Correo": correo_ing,
                "Departamento": departamento_ing,
                "Activo / CI": activo_ing if activo_ing else "N/A",
                "Categoría": categoria_ing,
                "Urgencia": urgencia_ing,
                "Impacto": impacto_ing,
                "Prioridad": prioridade,
                "Grupo Asignado": grupo,
                "Técnico Asignado": "Pendiente de Asignación",
                "Estado": "Nuevo / Abierto",
                "SLA Límite": sla_limite_str,
                "Fecha Creación": fecha_creacion_str,
                "Descripción": descripcion_ing,
                "Bitácora / Notas": f"[{fecha_creacion_str}] Sistema: Ticket enrutado automáticamente a '{grupo}' con SLA de {horas_sla} horas."
            }])
            
            st.session_state.enterprise_tickets = pd.concat([st.session_state.enterprise_tickets, nuevo_registro_ent], ignore_index=True)
            st.success(f"¡Ticket corporativo {nuevo_id} generado y enrutado con éxito bajo directrices ITIL!")

# -------------------------------------------------------------------------
# MÓDULO 3: CUADRO DE MANDO Y KPIS (SERVICE DESK DASHBOARD)
# -------------------------------------------------------------------------
elif menu_opcion == "📊 Cuadro de Mando (KPIs & SLA)":
    st.subheader("📈 Analítica y Métricas del Centro de Servicio (ITSM)")
    
    if not st.session_state.enterprise_tickets.empty:
        df = st.session_state.enterprise_tickets
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total de Casos Activos", len(df))
        c2.metric("Incidentes Reportados", len(df[df["Tipo"] == "Incidente"]))
        c3.metric("Solicitudes de Servicio", len(df[df["Tipo"] == "Solicitud de Servicio"]))
        c4.metric("Cumplimiento SLA", "98.4%", "+1.2%")
        
        st.markdown("---")
        st.markdown("### Distribución de Casos por Prioridad (Matriz ITIL)")
        st.bar_chart(df["Prioridad"].value_counts())
        
        st.markdown("### Carga de Trabajo por Grupo Resolutor")
        st.bar_chart(df["Grupo Asignado"].value_counts())
    else:
        st.warning("No hay suficientes datos analíticos todavía. Registre requerimientos en el sistema.")

# -------------------------------------------------------------------------
# MÓDULO 4: ADMINISTRACIÓN DE ACTIVOS Y CONFIGURACIÓN (CMDB)
# -------------------------------------------------------------------------
elif menu_opcion == "🛠️ Administración de Grupos y Activos (CMDB)":
    st.subheader("🛠️ Gestión de Elementos de Configuración (CMDB) y Grupos de Soporte")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("#### 👥 Grupos Resolutores Activos")
        st.info("""
        * **Nivel 0:** Autoservicio / Portal de Conocimiento (FAQs)
        * **Nivel 1:** Mesa de Ayuda (Help Desk - Filtro y resolución básica)
        * **Nivel 2:** Especialistas de Infraestructura, Redes y Sistemas
        * **Nivel 3:** Arquitectos de TI y Expertos de Ciberseguridad
        * **Nivel 4:** Proveedores Externos / Fabricantes de Hardware o Software
        """)
    with col_c2:
        st.markdown("#### 🖥️ Catálogo de Servicios de TI")
        st.success("""
        * Gestión de Puestos de Trabajo (Hardware y Periféricos)
        * Conectividad y Redes Corporativas (LAN / VPN / Wi-Fi)
        * Sistemas ERP y Contables (SAP / Bases de datos)
        * Gestión de Identidades y Accesos (Active Directory)
        """)
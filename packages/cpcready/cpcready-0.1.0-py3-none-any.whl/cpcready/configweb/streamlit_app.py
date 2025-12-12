
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Título
st.title("CPCReady Configuration")
st.markdown("---")

# Inicializar ConfigManager
config_manager = ConfigManager()

# Obtener configuración actual
config = config_manager.get_current_config()

# Sección: DRIVES
st.header("Drives")

# Drive A
drive_a = st.text_input(
    "Drive A:",
    value=config['drive_a'] if config['drive_a'] else "",
    help="Path to DSK file for Drive A"
)

# Drive B
drive_b = st.text_input(
    "Drive B:",
    value=config['drive_b'] if config['drive_b'] else "",
    help="Path to DSK file for Drive B"
)

# Default Drive
default_drive_options = ["A", "B"]
default_index = 0 if config['default_drive'].lower() == "a" else 1
default_drive = st.radio(
    "Default Drive:",
    options=default_drive_options,
    index=default_index,
    horizontal=True
)

st.markdown("---")

# Sección: EMULATOR
st.header("Emulator")

emulator_options = ["RetroVirtualMachine", "CPCEmu", "M4Board"]
emulator_index = emulator_options.index(config['emulator']) if config['emulator'] in emulator_options else 0
emulator = st.selectbox(
    "Emulator:",
    options=emulator_options,
    index=emulator_index
)

st.markdown("---")

# Sección: M4BOARD
st.header("M4Board")

m4board_ip = st.text_input(
    "IP Address:",
    value=config['m4board_ip'] if config['m4board_ip'] else "",
    help="IP address for M4Board (required if M4Board is selected)"
)

st.markdown("---")

# Botones de acción
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    save_button = st.button("💾 Save", type="primary", use_container_width=True)

with col2:
    cancel_button = st.button("❌ Cancel", use_container_width=True)

# Procesar acciones
if save_button:
    errors = []
    
    # Validar que Drive A y Drive B no sean iguales
    if (drive_a and drive_a.strip()) and (drive_b and drive_b.strip()):
        if Path(drive_a).expanduser().resolve() == Path(drive_b).expanduser().resolve():
            errors.append("❌ Drive A and Drive B cannot point to the same file")
    
    # Validar que los archivos existen si se especificaron
    if drive_a and drive_a.strip():
        drive_a_path = Path(drive_a).expanduser()
        if not drive_a_path.exists():
            errors.append(f"❌ Drive A: File not found '{drive_a}'")
    
    if drive_b and drive_b.strip():
        drive_b_path = Path(drive_b).expanduser()
        if not drive_b_path.exists():
            errors.append(f"❌ Drive B: File not found '{drive_b}'")
    
    # Validar IP del M4Board
    # Si es M4Board, el campo IP es obligatorio
    if emulator == "M4Board" and (not m4board_ip or not m4board_ip.strip()):
        errors.append("❌ M4Board IP Address is required when M4Board is selected")
    
    # Si el campo IP tiene datos, validar el formato (independientemente del emulador)
    if m4board_ip and m4board_ip.strip():
        # Validar formato de IP
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if not ip_pattern.match(m4board_ip.strip()):
            errors.append("❌ Invalid IP Address format. Use format: xxx.xxx.xxx.xxx")
        else:
            # Validar rangos (0-255)
            try:
                octets = m4board_ip.strip().split('.')
                if not all(0 <= int(octet) <= 255 for octet in octets):
                    errors.append("❌ Invalid IP Address. Each octet must be between 0 and 255")
            except ValueError:
                errors.append("❌ Invalid IP Address format")
    
    if errors:
        # Mostrar errores
        for err in errors:
            st.error(err)
    else:
        # Guardar configuración
        try:
            config_manager.save_config(
                drive_a=drive_a.strip() if drive_a and drive_a.strip() else None,
                drive_b=drive_b.strip() if drive_b and drive_b.strip() else None,
                default_drive=default_drive.lower(),
                emulator=emulator,
                m4board_ip=m4board_ip.strip() if m4board_ip else ""
            )
            # st.success("✅ Configuration saved successfully!")
            st.toast('Configuration saved!', icon='✅')
        except Exception as e:
            st.error(f"❌ Error saving configuration: {e}")

if cancel_button:
    st.info("❌ Configuration cancelled. Close this tab to exit.")

# Mostrar configuración actual en el sidebar
with st.sidebar:
    # Logo/imagen
    logo_path = Path(__file__).parent.parent.parent / "docs" / "images" / "cpcready.jpg"
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    
    st.header("📋 Current Configuration")
    st.markdown("---")
    
    st.subheader("Drives")
    if config['drive_a']:
        st.text(f"A: {Path(config['drive_a']).name}")
    else:
        st.text("A: (empty)")
    
    if config['drive_b']:
        st.text(f"B: {Path(config['drive_b']).name}")
    else:
        st.text("B: (empty)")
    
    st.text(f"Default: {config['default_drive'].upper()}")
    
    st.markdown("---")
    st.subheader("Emulator")
    st.text(config['emulator'])
    
    if config['m4board_ip']:
        st.markdown("---")
        st.subheader("M4Board")
        st.text(f"IP: {config['m4board_ip']}")
    
    # Footer con versión
    st.markdown("---")
    from cpcready import __version__
    st.caption(f"v{__version__}")

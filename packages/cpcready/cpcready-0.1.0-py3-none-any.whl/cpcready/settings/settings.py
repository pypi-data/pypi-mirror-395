


def show_settings_form():
    """Muestra el formulario de configuración usando prompt_toolkit."""
    config_manager = ConfigManager()
    config = config_manager.get_all()
    
    # Campo de IP con validación
    ip_field = TextArea(
        height=1,
        prompt='',
        validator=IPValidator(),
        multiline=False,
        text=config.get('m4board_ip', '')
    )
    
    error_label = Label(text="", style="class:error")
    
    # RadioList para emuladores - determinar valor actual primero
    current_emulator = config.get('emulator', 'RetroVirtualMachine')
    
    emulator_options = [
        ("RetroVirtualMachine", "RetroVirtualMachine"),
        ("CPCEmu", "CPCEmu"),
        ("M4Board", "M4Board")
    ]
    
    # Crear RadioList con el valor predeterminado usando el valor, no el índice
    emuladores = RadioList(
        values=emulator_options,
        default=current_emulator  # Usar el valor directamente
    )
    
    resultado = {}
    
    def on_ok():
        """Validar y guardar la configuración."""
        texto_ip = ip_field.text.strip()
        
        # Obtener el emulador seleccionado
        idx = emuladores._selected_index
        selected_emulator = emulator_options[idx][0]
        
        # Si el emulador es M4Board, validar que haya IP
        if selected_emulator == "M4Board":
            if not texto_ip:
                error_label.text = "❌ Se requiere dirección IP para M4Board"
                return
            try:
                ipaddress.ip_address(texto_ip)
            except ValueError:
                error_label.text = "❌ Dirección IP no válida. Ejemplo: 192.168.1.10"
                return
        
        error_label.text = ""
        resultado['ip'] = texto_ip if texto_ip else None
        resultado['emulator'] = selected_emulator
        app.exit()
    
    def on_cancel():
        """Cancelar sin guardar."""
        resultado['cancelled'] = True
        app.exit()
    
    # Key bindings para Ctrl+C y Ctrl+Z
    kb = KeyBindings()
    
    @kb.add('c-c')
    @kb.add('c-z')
    def _(event):
        """Salir con Ctrl+C o Ctrl+Z."""
        on_cancel()
    
    dialog = Dialog(
        title="CPCReady Settings",
        body=HSplit([
            Label(text="IP or hostname:", style="bold"),
            ip_field,
            error_label,
            Label(text=""),
            Label(text="Emulators", style="bold"),
            emuladores
        ]),
        buttons=[
            Button(text="OK", handler=on_ok),
            Button(text="Cancel", handler=on_cancel)
        ],
        width=100,
        with_background=True
    )
    
    app = Application(
        layout=Layout(dialog),
        key_bindings=kb,
        full_screen=True
    )
    app.run()
    return resultado


@click.command(cls=CustomCommand)
def settings():
    """Configure CPCReady options in terminal UI"""
    try:
        result = show_settings_form()
        
        if result.get('cancelled'):
            blank_line(1)
            error("Configuration cancelled")
            blank_line(1)
            return
        
        if 'emulator' in result:
            # Guardar la configuración
            config_manager = ConfigManager()
            config_manager.save_config(
                m4board_ip=result.get('ip'),
                emulator=result.get('emulator')
            )
            
            blank_line(1)
            ok("Configuration saved successfully!")
            blank_line(1)
    except Exception as e:
        blank_line(1)
        error(f"Error running configuration: {e}")
        blank_line(1)

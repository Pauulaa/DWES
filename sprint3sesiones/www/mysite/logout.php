<?php
session_start(); // Iniciar sesión para poder destruirla
session_destroy(); // Destruir la sesión
header('Location: login.html'); // Redirigir al formulario de login
?>

<?php
session_start(); // Inicia la sesión

// Conexión a la base de datos
$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');

// Recibir las credenciales del formulario
$email = $_POST['email'];
$password = $_POST['password'];

// Consultar la base de datos para verificar si el usuario existe
$query = $db->prepare("SELECT id, contraseña FROM tUsuarios WHERE email = ?");
$query->bind_param("s", $email);
$query->execute();
$result = $query->get_result();

// Si el usuario existe
if ($result->num_rows > 0) {
    $user = $result->fetch_assoc(); // Obtener los datos del usuario
    
    // Verificar que la contraseña proporcionada es correcta
    if (password_verify($password, $user['contraseña'])) {
        $_SESSION['user_id'] = $user['id']; // Guardar el ID de usuario en la sesión
        header('Location: main.php'); // Redirigir a la página principal
        exit(); // Importante: Detener el script después de la redirección
    } else {
        echo 'Error: Contraseña incorrecta.';
    }
} else {
    echo 'Error: Usuario no encontrado.';
}

mysqli_close($db);

?>

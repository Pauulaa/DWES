<?php
session_start(); // Inicia o retoma la sesión del usuario
$db = mysqli_connect('localhost', 'root', '1234', 'web_canciones') or die('No se pudo conectar a la base de datos');

// Verificar si el usuario está logueado
if (!isset($_SESSION['user_id'])) {
    header('Location: login.php'); // Si no está logueado, redirige al login
    exit();
}

$user_id = $_SESSION['user_id']; // ID del usuario logueado
$old_password = $_POST['old_password']; // Contraseña actual
$new_password = $_POST['new_password']; // Nueva contraseña
$confirm_password = $_POST['confirm_password']; // Confirmación de la nueva contraseña

// Verificar que la nueva contraseña y la confirmación coincidan
if ($new_password !== $confirm_password) {
    echo "Las contraseñas no coinciden. Intenta nuevamente.";
    exit();
}

// Verificar si la contraseña actual es correcta
$query = $db->prepare("SELECT contraseña FROM tUsuarios WHERE id = ?");
$query->bind_param("i", $user_id);
$query->execute();
$result = $query->get_result();

if ($result->num_rows === 0) {
    echo "Usuario no encontrado.";
    exit();
}

$user = $result->fetch_assoc();
$current_password = $user['contraseña']; // Recupera la contraseña almacenada en la base de datos

// Verificar la contraseña actual con la ingresada por el usuario
if (!password_verify($old_password, $current_password)) {
    echo "La contraseña actual es incorrecta.";
    exit();
}

// Cifrar la nueva contraseña
$hashed_password = password_hash($new_password, PASSWORD_DEFAULT);

// Actualizar la contraseña en la base de datos
$update_query = $db->prepare("UPDATE tUsuarios SET contraseña = ? WHERE id = ?");
$update_query->bind_param("si", $hashed_password, $user_id);
$update_query->execute();

// Comprobar si la actualización fue exitosa
if ($update_query->affected_rows > 0) {
    echo "Contraseña cambiada correctamente.";
    header('Location: main.php'); // Redirige a la página principal
} else {
    echo "Hubo un error al cambiar la contraseña. Intenta nuevamente.";
}
?>


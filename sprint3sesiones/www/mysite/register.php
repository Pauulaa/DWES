<?php
// Conexión a la base de datos
$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');

// Recibir datos del formulario
$email = $_POST['email'];
$password = $_POST['password'];
$confirm_password = $_POST['confirm_password'];

// Validación de campos vacíos y coincidencia de contraseñas
if (empty($email) || empty($password) || empty($confirm_password)) {
    echo 'Error: Todos los campos son obligatorios.';
} elseif ($password !== $confirm_password) {
    echo 'Error: Las contraseñas no coinciden.';
} else {
    // Verificar si el email ya existe
    $query = $db->prepare("SELECT id FROM tUsuarios WHERE email = ?");
    $query->bind_param("s", $email);
    $query->execute();
    $result = $query->get_result();
    
    if ($result->num_rows > 0) {
        echo 'Error: El correo ya está registrado.';
    } else {
        // Encriptar la contraseña y almacenar el nuevo usuario
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);
        $insert_query = $db->prepare("INSERT INTO tUsuarios (email, contraseña) VALUES (?, ?)");
        $insert_query->bind_param("ss", $email, $hashed_password);
        $insert_query->execute();
        header('Location: main.php'); // Redirigir a la página principal
    }
}
?>

<?php
// Iniciar la sesión para verificar si el usuario ha iniciado sesión
session_start();

// Verificar si el usuario ha iniciado sesión
if (!isset($_SESSION['user_id'])) {
    // Si no está en sesión, redirigir al usuario a la página de login
    header('Location: login.html');
    exit();
}

// Conexión a la base de datos
$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Error al conectar a la base de datos');
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Libros</title>
</head>
<body>
    <h1>Lista de Libros</h1>

    <!-- Enlace para cerrar sesión -->
    <p><a href="logout.php">Cerrar sesión</a></p>

    <ul>
    <?php
        // Consultar la lista de libros desde la base de datos
        $query = 'SELECT * FROM tLibros';
        $result = mysqli_query($db, $query) or die('Error en la consulta: ' . mysqli_error($db));
       
        // Mostrar los libros en una lista
        while ($row = mysqli_fetch_array($result)) {
            echo "<li>";
            echo "<h2>".$row['nombre']."</h2>";
            echo "<br>";
            echo "<img src='".$row['url_imagen']."' alt='Imagen del libro'>";
            echo "<a href='detail.php?id=".$row['id']."'>Ver Detalles</a>";
            echo "<p>Autor: ".$row['autor']."</p>";
            echo "<p>Año de publicación: ".$row['año_publicacion']."</p>";
            echo "</li>";
        }
    ?>
    </ul>
</body>
</html>
<?php
// Cerrar la conexión a la base de datos
mysqli_close($db);
?>
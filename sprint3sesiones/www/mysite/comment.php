<?php
session_start();
// Conectar a la base de datos mysitedb
$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Error al conectar a la base de datos');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Obtener el ID del libro, comentario y usuario desde el formulario
    $libro_id = $_POST['libro_id'];
    echo $libro_id;
    $comentario = mysqli_real_escape_string($db, $_POST['new_comment']); // Limpia el comentario para evitar inyecciones SQL
    $usuario_id = $_POST['usuario_id']; // Obtener el usuario_id desde el formulario

    // Verificar que se han recibido los datos necesarios
    if (empty($comentario) || empty($libro_id) || empty($usuario_id)) {
        die('Comentario, ID del libro o ID del usuario no especificados.');
    }

    // Insertar el comentario en la base de datos con la fecha actual
    $query = "INSERT INTO tComentarios(comentario, libro_id, usuario_id, fecha)
              VALUES ('$comentario', $libro_id, $usuario_id, NOW())";
    mysqli_query($db, $query) or die('Error al insertar el comentario');

    echo "<p>Nuevo comentario añadido con éxito</p>";
    echo "<a href='/detail.php?id=".$libro_id."'>Volver a la página del libro</a>";
} else {
    echo "<p>Error: No se recibió ningún comentario.</p>";
}

if (isset($libro_id)) {
    $query = "SELECT c.comentario, c.fecha, u.nombre AS usuario_nombre
              FROM tComentarios c
              JOIN tUsuarios u ON c.usuario_id = u.id
              WHERE c.libro_id = $libro_id
              ORDER BY c.fecha DESC";

    $result = mysqli_query($db, $query);

    if (mysqli_num_rows($result) > 0) {
        echo "<h3>Comentarios:</h3>";
        while ($row = mysqli_fetch_assoc($result)) {
            echo "<div class='comentario'>";
            echo "<p><strong>" . htmlspecialchars($row['usuario_nombre']) . "</strong> (" . $row['fecha'] . ")</p>";
            echo "<p>" . nl2br(htmlspecialchars($row['comentario'])) . "</p>";
            echo "</div>";
        }
    } else {
        echo "<p>No hay comentarios aún para este libro.</p>";
    }
}

// Cerrar la conexión
mysqli_close($db);
?>
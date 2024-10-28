<?php
    $db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Error al conectar a la base de datos');

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $libro_id = $_POST['libro_id'];
        $comentario = mysqli_real_escape_string($db, $_POST['new_comment']); // Limpia el comentario para evitar inyecciones SQL

        // Insertar el comentario en la base de datos con la fecha actual
        $query = "INSERT INTO tComentarios(comentario, libro_id, usuario_id, fecha) VALUES ('$comentario', $libro_id, NULL, NOW())";
        mysqli_query($db, $query) or die('Error al insertar el comentario');

        echo "<p>Nuevo comentario añadido con éxito</p>";
        echo "<a href='/detail.php?id=".$libro_id."'>Volver a la página del libro</a>";
    } else {
        echo "<p>Error: No se recibió ningún comentario.</p>";
    }

    mysqli_close($db);
?>

<?php
    session_start();
    $db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Error al conectar a la base de datos');
    
    if (!isset($_GET['id'])) {
        die('No se ha especificado un libro');
    }

    $libro_id = $_GET['id'];

    // Obtener la información del libro
    $query = 'SELECT * FROM tLibros WHERE id=' . $libro_id;
    $result = mysqli_query($db, $query) or die('Error en la consulta');
    $only_row = mysqli_fetch_array($result);

    echo "<h1>" . $only_row['nombre'] . "</h1>";
    echo "<img src='" . $only_row['url_imagen'] . "' alt='Imagen del libro'>";
    echo "<p>Autor: " . $only_row['autor'] . "</p>";
    echo "<p>Año de publicación: " . $only_row['año_publicacion'] . "</p>";
?>
<!-- Formulario para añadir un comentario -->
<p>Deja un nuevo comentario:</p>                            
<form action="/comment.php" method="post">
    <textarea rows="4" cols="50" name="new_comment"></textarea><br>
    <input type="hidden" name="libro_id" value="<?php echo $libro_id; ?>">
    <input type="submit" value="Comentar">
</form>

<h3>Comentarios:</h3>
<ul>
<?php
    // Mostrar comentarios asociados al libro
    $query = "SELECT c.comentario, c.fecha, u.nombre AS usuario_nombre
          FROM tComentarios c
          JOIN tUsuarios u ON c.usuario_id = u.id
          WHERE c.libro_id = '" . $libro_id . "'
          ORDER BY c.fecha DESC";

    /*$query2 = 'SELECT c.comentario, c.fecha, u.nombre AS usuario_nombre 
               FROM tComentarios c 
               JOIN tUsuarios u ON c.usuario_id = u.id 
               WHERE c.libro_id = ' . $libro_id . ' 
               ORDER BY c.fecha DESC';*/

    $result2 = mysqli_query($db, $query2) or die('Error en la consulta de comentarios: ' . mysqli_error($db));

    // Verificar si hay comentarios y mostrarlos
    if (mysqli_num_rows($result2) > 0) {
        while ($row = mysqli_fetch_array($result2)) {
            echo '<li>';
            echo '<strong>' . $row['usuario_nombre'] . '</strong> (' . $row['fecha'] . ')<br>';
            echo nl2br($row['comentario']); // Convertir saltos de línea en el comentario
            echo '</li>';
        }
    } else {
        echo '<p>No hay comentarios aún para este libro.</p>';
    }
?>
</ul>



<?php
    mysqli_close($db);
?>



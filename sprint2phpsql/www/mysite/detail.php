<?php
    $db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Error al conectar a la base de datos');
    
    if (!isset($_GET['id'])) {
        die('No se ha especificado un libro');
    }

    $libro_id = $_GET['id'];

    // Obtener la información del libro
    $query = 'SELECT * FROM tLibros WHERE id='.$libro_id;
    $result = mysqli_query($db, $query) or die('Error en la consulta');
    $only_row = mysqli_fetch_array($result);

    echo "<h1>".$only_row['nombre']."</h1>";
    echo "<img src='".$only_row['url_imagen']."' alt='Imagen del libro'>";
    echo "<p>Autor: ".$only_row['autor']."</p>";
    echo "<p>Año de publicación: ".$only_row['año_publicacion']."</p>";
?>

<h3>Comentarios:</h3>
<ul>
<?php
    // Mostrar comentarios asociados al libro
    $query2 = 'SELECT * FROM tComentarios WHERE libro_id='.$libro_id;
    $result2 = mysqli_query($db, $query2) or die('Error en la consulta de comentarios: ' . mysqli_error($db));
    echo $result2;
    while ($row = mysqli_fetch_array($result2)) {
        echo '<li>'.$row['comentario'].'</li>';
    }
?>
</ul>

<!-- Formulario para añadir un comentario -->
<p>Deja un nuevo comentario:</p>                            
<form action="/comment.php" method="post">
    <textarea rows="4" cols="50" name="new_comment"></textarea><br>
    <input type="hidden" name="libro_id" value="<?php echo $libro_id; ?>">
    <input type="submit" value="Comentar">
</form>

<?php
    mysqli_close($db);
?>



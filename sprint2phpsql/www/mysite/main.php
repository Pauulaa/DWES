<?php
    $db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Error al conectar a la base de datos');
?>
<html>
<head>
    <title>Libros</title>
</head>
<body>
    <h1>Lista de Libros</h1>
    <ul>
    <?php
        $query = 'SELECT * FROM tLibros';
        $result = mysqli_query($db, $query) or die('Error en la consulta: ' . mysqli_error($db));
        
        while ($row = mysqli_fetch_array($result)) {
            echo "<li>";
            echo "<h2>".$row['nombre']."</h2>";
            echo "<br>";
            echo "<img src='".$row['url_imagen']."' alt='Imagen del libro'>";
            echo "<a href=detail.php?id=".$row['id'].">Ver Detalles</a>";
            echo "<p>Autor: ".$row['autor']."</p>";
            echo "<p>Año de publicación: ".$row['año_publicacion']."</p>";
            echo "</li>";
        }
    ?>
    </ul>
</body>
</html>
<?php
    mysqli_close($db);
?>

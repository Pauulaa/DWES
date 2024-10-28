<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ejercicios</title>
        <style>
            img{
                width:100px;
                height:100px;
            }
        </style>
    </head>

    <body>
        <?php
        $db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die ('Fail');
        ?>
        </body>
        
        <h1>Conexión establecida</h1>
        <?php

            $query = 'SELECT * FROM tPeliculas';
            $result = mysqli_query($db, $query) or die('Query error');
            if ($result){
                echo "<ul>";
                while ($row = mysqli_fetch_array($result)){
            
                    echo "<li> Id película: " . $row['id_pelicula'] . "</li>";
                    echo "<li> Nombre: " . $row['nombre'] . "</li>";
                    echo "<li><img src= " . $row['url_imagen'] . "'/></li>";
                    echo "<li>Director: " . $row['director'] . "</li>";
                    echo "<li>Año de estreno: " . $row['anio:estreno'] . "</li>";
                    echo "<br>";
                }
                echo "</ul>";
            } else {
                echo "<p>Error en la consulta: " . mysqli_error($db) . "</p>";
            }
            mysqli_close($db);
?>
</body>
</html>





















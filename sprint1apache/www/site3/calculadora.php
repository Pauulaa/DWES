<html>
<body>
<h1>Calculadora Simple</h1>
<p>Realiza operaciones aritméticas:</p>
<p>
<?php
if (isset($_POST["operacion"])) {
    $numero1 = $_POST["numero1"];
    $numero2 = $_POST["numero2"];
    $resultado = "";

    switch ($_POST["operacion"]) {
        case "suma":
            $resultado = $numero1 + $numero2;
            echo "Resultado: " . $numero1 . " + " . $numero2 . " = " . $resultado;
            break;
        case "resta":
            $resultado = $numero1 - $numero2;
            echo "Resultado: " . $numero1 . " - " . $numero2 . " = " . $resultado;
            break;
        case "multiplicacion":
            $resultado = $numero1 * $numero2;
            echo "Resultado: " . $numero1 . " * " . $numero2 . " = " . $resultado;
            break;
        case "division":
            if ($numero2 != 0) {
                $resultado = $numero1 / $numero2;
                echo "Resultado: " . $numero1 . " / " . $numero2 . " = " . $resultado;
            } else {
                echo "Error: División por cero no permitida.";
            }
            break;
        default:
            echo "Operación no soportada.";
            break;
    }
}
?>
</p>
<p>Realiza una nueva operación:</p>
<form action="/calculadora.php" method="post">
    <label for="numero1">Número 1:</label><br>
    <input type="number" id="numero1" name="numero1" required><br>
    
    <label for="numero2">Número 2:</label><br>
    <input type="number" id="numero2" name="numero2" required><br>
    
    <label for="operacion">Seleccione una operación:</label><br>
    <select id="operacion" name="operacion">
        <option value="suma">Suma</option>
        <option value="resta">Resta</option>
        <option value="multiplicacion">Multiplicación</option>
        <option value="division">División</option>
    </select><br><br>
    
    <input type="submit" value="Calcular">
</form>
</body>
</html>

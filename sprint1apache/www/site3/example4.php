<html>
	<body>
		<h1>Jubilación</h1>
			<?php
				$X =7;
				function edad_en_X_años($edad, $X) {
				return $edad + $X;
				}
	
				function mensaje($edad, $X) {
				  if (edad_en_X_años($edad, $X) > 65) {
					return "En 10 años tendrás edad de jubilación";
				} else {
					return "Disfruta de tu tiempo!";
					}
				}
			?>

			<table>
			  <tr>
				<th>Edad</th>
				<th>Info</th>
			  </tr>

			  <?php
			     $lista = array(50, 52, 58, 60, 63);
			     foreach ($lista as $valor) {
			     	echo "<tr>";
				echo "<td>".$valor."</td>";
				echo "<td>".mensaje($valor, $X)."</td>";
				echo "</tr>";
		        	}
			?>

			</table>
		</body>
</html>
	
		

<H1> Pacsun Sale Items</H1>

<?php

    echo "<H3> Choose how you want your sale items sorted! </H3> ";
    echo "<form action='sales.php' method='POST'>";
    echo "<input type=submit name=percentages value=Percentage>";
    echo "<input type=submit name=differences value=Difference>";
    echo "</form>";

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        // Something posted
    
        if (isset($_POST['differences'])) {
            echo "<p> Now showing sale items sorted by largest difference between original and sales price... </p>";
            echo shell_exec("python sales.py differences");
        } 
        else {
            echo "<p> Now showing sale items sorted by largest percentage sale... </p>";
            echo shell_exec("python sales.py percentages");
        }
    }
?>
<?php 
    include "connection.php"
?> 
<html>
<head>

<link rel="stylesheet" href="style.css">
<link rel="preconnect" href="https://fonts.googleapis.com"> 
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin> 
<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">

</head>

<body>

<div class = "title"><h1> <a href="index.php">  Kilburnazon Employee Management</a> </h1></div>

    <div class = "main"> 
        <?php
        $sql = "SELECT * FROM Audit";
        $result = $conn->query($sql);
        ?>
        <table class = "emp">
        <tr>
            <th style="border-top-left-radius: 10px;">ID</th>
            <th>Employee Number</th>
            <th>Date Deleted</th>
            <th>Deleted by BOSS</th>
            <th style="border-top-right-radius: 10px;">BOSS Num</th>
        </tr>


        <?php

        if ($result->num_rows > 0) {
                // output data of each row
                while($row = $result->fetch_assoc()) {  
                    
                $boss = $row["boss_id"];
                $qry = mysqli_query($conn, "SELECT emp_name, emp_num FROM Employee WHERE `emp_id` = '$boss' ");
                $qry = mysqli_fetch_assoc($qry);
                
                ?>

                    <tr>

                            <td><?php echo $row["aud_id"]; ?></td>
                            <td><?php echo $row["emp_num"]; ?></td>
                            <td><?php echo $row["aud_date"]; ?></td>
                            <td><?php echo $qry["emp_name"]; ?></td>
                            <td><?php echo $qry["emp_num"]; ?></td>
                    </tr>


                <?php
                }   
        } 

        else {
            ?>
            <td colspan="6"><?php echo "0 results"; ?></td>
        <?php
        }
        $conn->close();

        ?>
        
    </table>
    </div>
</body>
</html>
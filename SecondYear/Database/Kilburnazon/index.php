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

<div class = "ops"> 
    <button class="button-33"> <a href="add_emp.php"> Add Employee </a></button> 
    <div class = "search">
        <form action = "" method="POST">
            <input class = "search_bar" type="text" name="search_input" placeholder = "Search by number or name">
            <input class = "search_button" type = "submit" name = "search" value = "Search">
        </form> 
    </div>
    <div class = "dep_rel">
        <form action="" method="POST">
            <select class = "deps" name="dep">
                <option value="HR">HR</option>
                <option value="Managers">Managers</option>
                <option value="Driver">Driver</option>
                <option value="Packager">Packager</option>
            </select>
            <input class = "search_bar" type="text" name="relation" placeholder = "Input relation">
            <input class = "search_button" type = "submit" name = "search_dep_relation" value = "Search">
        </form>
    </div>  
    <form class = "birthdays" action="" method = "POST"> <input class = "search_button" type="submit" name = "birthday" value = "Birthdays"></form>
    <button class="button-33"> <a href="audit_emp.php"> Audit </a></button> 
</div>

<div class = "main"> 
    <?php
    if (isset($_POST['search'])) {
        $sql = "SELECT emp_id, emp_birthdate, emp_num, emp_name, emp_salary, dep_id, boss_id, emp_emergrelation, emp_NIN FROM Employee WHERE `emp_num` LIKE '%{$_POST['search_input']}%' OR `emp_name` LIKE '%{$_POST['search_input']}%'" ;
    }
    else if(isset($_POST['search_dep_relation'])){
        switch($_POST['dep']){
            case "HR":
                $dep_val = 1;
                break;
            case "Manager":
                $dep_val = 2;
                break;
            case "Driver":
                $dep_val = 3;
                break;
            case "Packager":
                $dep_val = 4;
                break;
            default:
                $dep_val = 1;
                break;
        }
        $sql = "SELECT emp_id, emp_birthdate, emp_num, emp_name, emp_salary, dep_id, boss_id, emp_emergrelation, emp_NIN FROM Employee WHERE `dep_id` = '$dep_val' AND `emp_emergrelation`LIKE '%{$_POST['relation']}%'" ;
    }
    else if(isset($_POST['birthday'])){
        $sql = "CALL getBday";
    }
    else{
        $sql = "SELECT emp_id, emp_birthdate, emp_num, emp_name, emp_salary, dep_id, boss_id, emp_emergrelation, emp_NIN FROM Employee";
    }
    $result = $conn->query($sql);
    ?>

    <table class = "emp">
        <tr>
            <th style="border-top-left-radius: 10px;">ID</th>
            <th>Number</th>
            <th>Full Name</th>
            <th>Salary</th>
            <th>NIN</th>
            <th>DOB</th>
            <th>Department</th>
            <?php if(!isset($_POST['birthday'])){?><th>Boss</th><?php }?>
            <th>Emerg. Relation</th>
            <th style="border-top-right-radius: 10px;">Edit/Delete</th>
        </tr>


        <?php

        if ($result->num_rows > 0) {
                // output data of each row
                while($row = $result->fetch_assoc()) {  
                    
                    switch ($row["dep_id"]) {
                        case 1:
                            $department = "HR";
                            break;
                        case 2:
                            $department = "Manager";
                            break;
                        case 3:
                            $department = "Driver";
                            break;
                        case 4:
                            $department = "Packager";
                            break;
                        default:
                            $department = "None";
                            break;
                    }
                $boss = $row["boss_id"];
                $qry = mysqli_query($conn, "SELECT emp_name FROM Employee WHERE `emp_id` = '$boss' ");
                $qry = mysqli_fetch_assoc($qry);
                
                ?>

                    <tr>

                            <td><?php echo $row["emp_id"]; ?></td>
                            <td><?php echo $row["emp_num"]; ?></td>
                            <td><?php echo $row["emp_name"]; ?></td>
                            <td><?php echo $row["emp_salary"]; ?></td>
                            <td><?php echo $row["emp_NIN"]; ?></td>
                            <td><?php echo $row["emp_birthdate"]; ?></td>
                            <td><?php echo $department; ?></td>
                            <?php if(!isset($_POST['birthday'])){?><td><?php echo $qry["emp_name"]; ?></td><?php }?>
                            <td><?php echo $row["emp_emergrelation"]; ?></td>
                            <td>
                                <button class = "edit_button" type = "submit" name = "edit_button"> <a href="edit_emp.php?action=edit&id=<?php echo $row['emp_id'] ?>"> Edit </a> </button> 
                                <button class = "edit_button" type = "submit" name = "edit_button"> <a href="edit_emp.php?action=delete&id=<?php echo $row['emp_id'] ?>"> Delete </a> </button> 
                            </td>
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
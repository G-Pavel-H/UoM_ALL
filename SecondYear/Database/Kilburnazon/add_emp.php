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

<div class = "add_main">
    <div class = "add">

        <form action="" method="POST">

            <label for="emp_num">Emp_id:</label> <br>  
            <input type="text" name = "emp_num"><br>

            <label for="emp_name">Name:</label>  <br> 
            <input type="text" name="emp_name"><br>

            <label for="emp_address">Address:</label>   <br>
            <input type="text" name="emp_address"><br>

            <label for="emp_salary">Salary:</label>   <br>
            <input type="text" name="emp_salary"><br>

            <label for="emp_birthdate">Dob: (DD/MM/YYYY)</label>   <br>
            <input type="text" name="emp_birthdate"><br>

            <label for="emp_NIN">Nin:</label>   <br>
            <input type="text" name="emp_NIN"><br>

            <label for="dep">Department:</label>   <br>
            <input type="text" name="dep"><br>

            <label for="emp_emergname">Emergency name:</label>  <br> 
            <input type="text" name="emp_emergname"><br>

            <label for="emp_emergrelation">Emergency relationship:</label>   <br>
            <input type="text" name="emp_emergrelation"><br>

            <label for="emp_emergphone">Emergency phone:</label>   <br>
            <input type="text" name="emp_emergphone"><br>

            <button type = "submit" name = "submit"> Submit</button>
        </form>

        <?php

        if(isset($_POST['submit'])){     
            $arr = array();
            $emp_num = $_POST['emp_num'];
            $emp_name = $_POST['emp_name'];
            $emp_address = $_POST['emp_address'];
            
            $emp_salary = $_POST['emp_salary'];
            $emp_birthdate = $_POST['emp_birthdate'];
            $emp_NIN = $_POST['emp_NIN'];
            
            $dep_name = $_POST['dep'];

            //Deciding the dep_id value to be inserted based on department entered 
            switch ($dep_name) {
                case "HR":
                    $dep_id = 1;
                    break;
                case "Manager":
                    $dep_id = 2;
                    break;
                case "Driver":
                    $dep_id = 3;
                    break;
                case "Packager":
                    $dep_id = 4;
                    break;
                default:
                    echo "<script> alert('Please input valid department name'); window.location.href='add_emp.php'; </script>";
                    break;
            }

            //Deciding on workspace based on department
            if($dep_id == 1 || $dep_id == 2){
                $workspace_id = 1;
            }
            else{
                $workspace_id = 3;
            }


            $emp_emergname = $_POST['emp_emergname'];
            $emp_emergrelation = $_POST['emp_emergrelation'];
            $emp_emergphone = $_POST['emp_emergphone'];

            //Setting the boss if input is not manager
            if($dep_id == 2){
                $boss_id = "";
            }
            else{
                $boss_id = 12;
            }

            array_push($arr, $emp_num, $emp_name, $emp_address, $emp_salary, $emp_birthdate, $emp_NIN, $dep_name, $emp_emergname,
            $emp_emergrelation, $emp_emergphone);


            for($i = 0; $i < count($arr); $i++){
                if ($arr[$i] == null){
                    echo "<script> alert('No input can be left blank'); window.location.href='add_emp.php'; </script>";
                }
            }

            if(mb_substr($emp_salary, 0, 1) != "£"){
                 echo "<script> alert('Please put £ in front of salary'); window.location.href='add_emp.php';</script>";
            }


            if(!(is_numeric(mb_substr($emp_salary, 1, count($emp_salary))))){
                echo "<script> alert('Please input valid salary'); window.location.href='add_emp.php';</script>";
            }


            $sql = "INSERT INTO `Employee` (`emp_num`, `emp_name`, `emp_address`,
            `emp_birthdate`, `emp_NIN`, `emp_salary`, `emp_emergname`, `emp_emergrelation`, 
            `emp_emergphone`, `dep_id`, `boss_id`, `workspace_id`) 
            VALUES ('$emp_num', '$emp_name ', '$emp_address', '$emp_birthdate', '$emp_NIN', '$emp_salary',
            '$emp_emergname', '$emp_emergrelation', '$emp_emergphone', '$dep_id', '$boss_id','$workspace_id')";

            $rs = mysqli_query($conn, $sql);

            if($rs)
            {
                echo "<script> alert('Contact Records Inserted Successfully!'); window.location.href='index.php'; </script>";
            } else {
                echo "<script> alert('$conn->error'); window.location.href='add_emp.php';</script>";

            }

            $conn->close();


    }
?>

    </div>


</div>




</body>
</html>
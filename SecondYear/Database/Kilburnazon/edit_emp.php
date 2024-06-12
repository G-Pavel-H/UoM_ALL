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
        <?php
        if ($_GET["action"] == "edit") {
            $result = mysqli_query($conn, "SELECT * FROM `Employee` WHERE `emp_id`='{$_GET['id']}';");
        }
        else{
            $result = mysqli_query($conn, "DELETE FROM `Employee` WHERE `emp_id`='{$_GET['id']}';");
            if($result){
                echo "<script> alert('Contact Records Deleted Successfully!'); window.location.href='index.php'; </script>";
            }
            else{
                echo "<script> alert('$conn->error'); window.location.href='index.php';</script>";
            }
        }
            $result = mysqli_fetch_assoc($result);
        ?>

        <form action="" method="POST">

            <label for="emp_num">Emp_id:</label> <br>  
            <input type="text" name = "emp_num" value = '<?php echo $result["emp_num"] ?>'><br>

            <label for="emp_name">Name:</label>  <br> 
            <input type="text" name="emp_name" value = "<?php echo $result['emp_name'] ?>"><br>

            <label for="emp_address">Address:</label>   <br>
            <input type="text" name="emp_address" value = "<?php echo $result['emp_address'] ?>"><br>

            <label for="emp_salary">Salary:</label>   <br>
            <input type="text" name="emp_salary" value = "<?php echo $result['emp_salary']?>"><br>

            <label for="emp_birthdate">Dob: (DD/MM/YYYY)</label>   <br>
            <input type="text" name="emp_birthdate" value = "<?php echo $result['emp_birthdate'] ?>"><br>

            <label for="emp_NIN">Nin:</label>   <br>
            <input type="text" name="emp_NIN" value = "<?php echo $result['emp_NIN'] ?>"><br>

            <?php
                switch($result['dep_id']){
                    case 1:
                        $dep_name = "HR";
                        break;
                    case 2:
                        $dep_name = "Manager";
                        break;
                    case 3:
                        $dep_name = "Driver";
                        break;
                    case 4:
                        $dep_name = "Packager";
                        break;
                }
            
            ?>

            <label for="dep">Department:</label>   <br>
            <input type="text" name="dep" value = "<?php echo $dep_name ?>"><br>

            <label for="emp_emergname">Emergency name:</label>  <br> 
            <input type="text" name="emp_emergname" value = "<?php echo $result['emp_emergname'] ?>"><br>

            <label for="emp_emergrelation">Emergency relationship:</label>   <br>
            <input type="text" name="emp_emergrelation" value = "<?php echo $result['emp_emergrelation'] ?>"><br>

            <label for="emp_emergphone">Emergency phone:</label>   <br>
            <input type="text" name="emp_emergphone" value = "<?php echo $result['emp_emergphone'] ?>"><br>

            <button type = "submit" name = "save"> Save</button>
        </form>

        <?php 

            if(isset($_POST['save'])){
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
                    echo "<script> alert('No input can be left blank'); window.location.href='edit_emp.php?id=" . $result['emp_id'] ."';</script>";
                }
            }

            if(mb_substr($emp_salary, 0, 1) != "£"){
                 echo "<script> alert('Please put £ in front of salary'); window.location.href='edit_emp.php?id=" . $result['emp_id'] ."';</script>";
            }


            if(!(is_numeric(mb_substr($emp_salary, 1, count($emp_salary))))){
                echo "<script> alert('Please input valid salary'); window.location.href='edit_emp.php?id=" . $result['emp_id'] ."';</script>";
            }


            $sql = "
            UPDATE
                `Employee`
            SET
                `emp_num` = '{$emp_num}',
                `emp_name` = '{$emp_name}',
                `emp_address` = '{$emp_address}',
                `emp_birthdate` = '{$emp_birthdate}',
                `emp_NIN` = '{$emp_NIN}',
                `emp_salary` = '{$emp_salary}',
                `emp_emergname` = '{$emp_emergname}',
                `emp_emergrelation` = '{$emp_emergrelation}',
                `emp_emergphone` = '{$emp_emergphone}',
                `dep_id` = '{$dep_id}',
                `workspace_id` = '{$workspace_id}'

            WHERE
                `emp_id` = '{$result['emp_id']}'";

            $rs = mysqli_query($conn, $sql);

            if($rs)
            {
                echo "<script> alert('Contact Records Updated Successfully!'); window.location.href='index.php'; </script>";
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
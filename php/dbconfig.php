<?php
$servername = "localhost";
$username = "id";
$password = "pw";
$dbname = "dbname";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die(json_encode(["error" => "연결 실패: " . $conn->connect_error]));
}
?>
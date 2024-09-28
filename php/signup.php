<?php
include 'dbconfig.php';

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("연결 실패: " . $conn->connect_error);
}

$member_id = $_POST['member_id'];
$member_password = $_POST['member_password'];
$name = $_POST['name'];
$phone_number = $_POST['phone_number'];

$id_check_sql = "SELECT * FROM library_user WHERE member_id = '$member_id'";
$result = $conn->query($id_check_sql);

if ($result->num_rows > 0) {
    echo json_encode(["status" => "error", "message" => "아이디가 이미 존재합니다."]);
    exit();
}

$hashed_password = password_hash($member_password, PASSWORD_DEFAULT);

$sql = "INSERT INTO library_user (member_id, member_password, name, phone_number) VALUES ('$member_id', '$hashed_password', '$name', '$phone_number')";

if ($conn->query($sql) === TRUE) {
    echo json_encode(["status" => "success", "message" => "회원가입 성공!"]);
} else {
    echo json_encode(["status" => "error", "message" => "오류: " . $conn->error]);
}

$conn->close();
?>

<?php
include 'dbconfig.php';

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("연결 실패: " . $conn->connect_error);
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $data = json_decode(file_get_contents("php://input"), true);

    $title = $data['title'];
    $author = $data['author'];
    $isbn = $data['isbn'];
    $total_copies = 1; 
    $available_copies = 1; 

    $sql = "INSERT INTO library_book (title, author, ISBN, total_copies, available_copies) VALUES (?, ?, ?, ?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ssssi", $title, $author, $isbn, $total_copies, $available_copies);

    if ($stmt->execute()) {
        echo json_encode(['status' => 'success', 'message' => '책이 성공적으로 추가되었습니다.']);
    } else {
        echo json_encode(['status' => 'error', 'message' => '책 추가 실패: ' . $stmt->error]);
    }

    $stmt->close();
}

$conn->close();
?>

<?php
include 'dbconfig.php';

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("연결 실패: " . $conn->connect_error);
}

$isbn = $_GET['isbn'];

$stmt = $conn->prepare("SELECT title, author, ISBN, available_copies FROM library_book WHERE ISBN = ?");
$stmt->bind_param("s", $isbn); 
$stmt->execute();

$result = $stmt->get_result();
$book = $result->fetch_assoc();

if ($book) {
    echo json_encode([
        'status' => 'success',
        'data' => $book
    ]);
} else {
    echo json_encode([
        'status' => 'error',
        'message' => '등록되지 않은 책입니다.'
    ]);
}

$stmt->close();
$conn->close();
?>

<?php
include 'dbconfig.php';

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("연결 실패: " . $conn->connect_error);
}

$member_id = $_POST['member_id'];
$book_title = $_POST['book_title']; 

$book_query = "SELECT book_id, available_copies FROM library_book WHERE title = '$book_title'";
$result = $conn->query($book_query);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $book_id = $row['book_id'];
    $available_copies = $row['available_copies'];

    if ($available_copies > 0) {
        $sql = "INSERT INTO library_history (member_id, book_id, loan_date, return_date) VALUES ('$member_id', '$book_id', NOW(), NULL)";

        if ($conn->query($sql) === TRUE) {
 
            echo "대여 정보가 추가되었습니다. (재고 감소 없음)";
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
    } else {
        echo "Error: 이 책의 남은 재고가 없습니다.";
    }
} else {
    echo "Error: 해당 제목의 책을 찾을 수 없습니다.";
}

$conn->close();
?>

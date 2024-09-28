<?php
include 'dbconfig.php';

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("연결 실패: " . $conn->connect_error);
}

$member_id = $_POST['member_id'];
$book_title = $_POST['book_title'];

$book_query = "SELECT book_id FROM library_book WHERE title = '$book_title'";
$result = $conn->query($book_query);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $book_id = $row['book_id'];

    $history_query = "SELECT * FROM library_history WHERE member_id = '$member_id' AND book_id = '$book_id' AND return_date IS NULL";
    $history_result = $conn->query($history_query);

    if ($history_result->num_rows > 0) {
        $return_query = "UPDATE library_history SET return_date = NOW() WHERE member_id = '$member_id' AND book_id = '$book_id' AND return_date IS NULL";
        if ($conn->query($return_query) === TRUE) {
            $update_copies_query = "UPDATE library_book SET available_copies = available_copies + 1 WHERE book_id = '$book_id'";
            $conn->query($update_copies_query);

            echo "책이 성공적으로 반납되었습니다.";
        } else {
            echo "Error: 반납 처리 중 오류가 발생했습니다.";
        }
    } else {
        echo "Error: 반납할 대여 기록을 찾을 수 없습니다.";
    }
} else {
    echo "Error: 해당 제목의 책을 찾을 수 없습니다.";
}

$conn->close();
?>

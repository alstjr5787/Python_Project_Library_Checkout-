<?php
include 'dbconfig.php';

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("연결 실패: " . $conn->connect_error);
}

$sql = "SELECT 
            lh.loan_date, 
            lh.return_date, 
            lb.title, 
            lb.author,
            lu.name 
        FROM 
            library_history lh 
        JOIN 
            library_book lb ON lh.book_id = lb.book_id 
        JOIN 
            library_user lu ON lh.member_id = lu.member_id";

$stmt = $conn->prepare($sql);
$stmt->execute();
$result = $stmt->get_result();

$books = [];

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $books[] = [
            'title' => $row['title'],
            'author' => $row['author'],
            'member_name' => $row['name'],
            'loan_date' => $row['loan_date'],
            'return_date' => $row['return_date'],
            'status' => $row['return_date'] ? '반납 완료' : '대출 중'
        ];
    }
} else {
    $books = []; 
}

header('Content-Type: application/json');
echo json_encode($books);

$stmt->close();
$conn->close();
?>

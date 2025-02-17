function getAuthHeader() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  return {
    Authorization: "Basic " + btoa(username + ":" + password),
  };
}

async function fetchBooks() {
  const response = await fetch("/books", {
    method: "GET",
    headers: {
      ...getAuthHeader(),
    },
  });
  const books = await response.json();
  const bookList = document.getElementById("book-list");
  bookList.innerHTML = ""; // Clear existing list

  if (books.length === 0) {
    bookList.innerHTML = "<li>No books found</li>";
    return;
  }

  books.forEach((book) => {
    const li = document.createElement("li");
    li.textContent = `${book.title} by ${book.author} (${book.year})`;
    bookList.appendChild(li);
  });
}

async function addBook() {
  const title = document.getElementById("title").value;
  const author = document.getElementById("author").value;
  const year = document.getElementById("year").value;

  const response = await fetch("/books", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeader(),
    },
    body: JSON.stringify({ title, author, year }),
  });

  if (response.ok) {
    alert("Book added successfully!");
    fetchBooks(); // Refresh the book list
  } else {
    alert("Failed to add book: " + (await response.text()));
  }
}

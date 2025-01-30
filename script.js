async function fetchArticle() {
    let url = document.getElementById("urlInput").value;
    if (!url) {
        alert("Please enter a URL");
        return;
    }

    try {
        let response = await fetch("http://localhost:5000/fetch-article", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        let data = await response.json();
        document.getElementById("result").innerHTML = `
            <div class="card p-3">
                <h3>${data.title}</h3>
                <p><strong>By:</strong> ${data.authors || "Unknown"} | <strong>Published on:</strong> ${data.publish_date || "N/A"}</p>
                <p>${data.summary}</p>
                <span class="badge bg-${getSentimentColor(data.sentiment)}">${data.sentiment}</span>
            </div>
        `;
    } catch (error) {
        console.error("Error fetching article:", error);
    }
}

function getSentimentColor(sentiment) {
    return sentiment === "Positive" ? "success" : sentiment === "Negative" ? "danger" : "secondary";
}

document.addEventListener("DOMContentLoaded", () => {
    lucide.createIcons()
})

const API_BASE_URL = "http://localhost:8000/api"
const accessToken = ""

// Google Login
document.getElementById("login-btn").addEventListener("click", async () => {
    const response = await fetch(`${API_BASE_URL}/auth/login/`)
    const data = await response.json()
    window.location.href = data.auth_url
})

// Fetch videos
async function fetchVideos() {
    const response = await fetch(`${API_BASE_URL}/videos/?access_token=${accessToken}`)
    const data = await response.json()
    const videoList = document.getElementById("videos")
    videoList.innerHTML = ""

    data.items.forEach((video) => {
        const li = document.createElement("li")
        li.className = "video-item"
        li.innerHTML = `
            <img src="${video.snippet.thumbnails.medium.url}" alt="${video.snippet.title}">
            <button onclick="fetchComments('${video.id}')">${video.snippet.title}</button>
        `
        videoList.appendChild(li)
    })

    document.getElementById("video-list").classList.remove("hidden")
}

// Fetch comments
async function fetchComments(videoId) {
    const response = await fetch(`${API_BASE_URL}/comments/${videoId}/?access_token=${accessToken}`)
    const data = await response.json()
    const commentList = document.getElementById("comments")
    commentList.innerHTML = ""

    data.items.forEach((comment) => {
        const li = document.createElement("li")
        li.textContent = comment.snippet.topLevelComment.snippet.textDisplay
        commentList.appendChild(li)
    })

    document.getElementById("comments-section").classList.remove("hidden")

    // Set event listeners
    document.getElementById("like-comments").onclick = () => likeComments(videoId)
    document.getElementById("delete-comments").onclick = () => deleteComments(videoId)
}

// Like all comments
async function likeComments(videoId) {
    try {
        await fetch(`${API_BASE_URL}/comments/${videoId}/like/`, {
            method: "POST",
            body: JSON.stringify({ access_token: accessToken }),
            headers: { "Content-Type": "application/json" },
        })
        alert("Liked all comments successfully!")
    } catch (error) {
        console.error("Error liking comments:", error)
        alert("Failed to like comments. Please try again.")
    }
}

// Delete filtered comments
async function deleteComments(videoId) {
    try {
        await fetch(`${API_BASE_URL}/comments/${videoId}/delete/`, {
            method: "POST",
            body: JSON.stringify({ access_token: accessToken }),
            headers: { "Content-Type": "application/json" },
        })
        alert("Deleted filtered comments successfully!")
        fetchComments(videoId) // Refresh the comments list
    } catch (error) {
        console.error("Error deleting comments:", error)
        alert("Failed to delete comments. Please try again.")
    }
}


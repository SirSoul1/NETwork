

document.addEventListener('DOMContentLoaded', function() {
    const menuButton = document.getElementById('menu-button');
    const navbarToggle = document.getElementById('navbarToggle');

    menuButton.addEventListener('click', function() {
        // Toggle the menu visibility
        navbarToggle.classList.toggle('hidden');

        // Rotate the menu icon
        this.classList.toggle('rotate-90');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const messagesLink = document.getElementById('messages-link');
    
    messagesLink.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default link click behavior
        console.log("Messages link clicked."); // Debugging log
        const badge = messagesLink.querySelector('.absolute');
        if (badge) {
            console.log("Badge found, hiding it now."); // Debugging log
            badge.style.display = 'none';
        } else {
            console.log("No badge found."); // Debugging log
        }
        
        const markUrl = messagesLink.getAttribute('data-mark-url');

        // Make an AJAX request to mark messages as read
        console.log("Sending fetch request to mark messages as read.");
        fetch(markUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ "user_id": "{{ user.id }}" })
        }).then(response => {
            if (response.ok) {
                console.log("Messages marked as read successfully.");
                // After marking messages as read, navigate to the messages page
                window.location.href = messagesLink.href;
            } else {
                console.error("Failed to mark messages as read.");
            }
        }).catch(error => {
            console.error("Error:", error);
        });
    });
});

$(document).ready(function() {
    $(".heart").on("click", function(event) {
        event.preventDefault();
        var $this = $(this);
        var post_id = $this.closest("form").data("post-id");
        var url = $this.closest("form").data("url");

        $.ajax({
            url: url,
            type: "POST",
            data: {
                'csrfmiddlewaretoken': csrfToken,
                'post_id': post_id,
            },
            success: function(response) {
                $this.toggleClass("is-active");
                $("#like-count").text(response.total_likes + " Likes");
            },
            error: function(response) {
                console.log("Error toggling like! Status:", response.status, response.statusText);
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var conversationContainer = document.querySelector(".conversation");
    if (conversationContainer) {
        conversationContainer.scrollTop = conversationContainer.scrollHeight;
    }
});



  







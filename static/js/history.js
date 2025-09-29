async function sendMessage() {
      const input = document.getElementById("user-input");
      const message = input.value.trim();
      if (!message) return;

      const chatBox = document.getElementById("chat-box");
      chatBox.innerHTML += `<div class="user-msg">🧑: ${message}</div>`;
      input.value = "";

      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const data = await response.json();
      chatBox.innerHTML += `<div class="bot-msg">🤖: ${data.reply}</div>`;
      chatBox.scrollTop = chatBox.scrollHeight;
    }

    const chatbotToggle = document.getElementById("chatbot-toggle");
    const chatbotContainer = document.getElementById("chatbot-container");

    chatbotToggle.addEventListener("click", () => {
      if (chatbotContainer.style.display === "flex") {
        chatbotContainer.style.display = "none";
      } else {
        chatbotContainer.style.display = "flex";
      }
    });
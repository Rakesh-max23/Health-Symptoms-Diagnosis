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
      chatbotContainer.style.display = chatbotContainer.style.display === "flex" ? "none" : "flex";
    });

    document.getElementById("search").addEventListener("keyup", function () {
      let filter = this.value.toLowerCase();
      let items = document.querySelectorAll(".symptom-item");
      items.forEach(item => {
        let text = item.textContent.toLowerCase();
        item.style.display = text.includes(filter) ? "" : "none";
      });
    });
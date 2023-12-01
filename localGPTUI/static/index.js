const inputMessages = [];

const messagesContainer = document.getElementById("messages");
const inputElement = document.getElementById("searchInput");
const promptForm = document.getElementById("promptForm");

inputElement.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    submitPromptForm();
  }
});

promptForm.addEventListener("submit", function (event) {
  event.preventDefault();
  submitPromptForm();
});

function submitPromptForm() {
  // const message = inputElement.value;
  // inputMessages.push(message);

  const formData = new FormData(promptForm);
  inputElement.value = "";

  fetch(promptForm.action, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      inputMessages.push(data);
      renderMessages();
    });
}

function renderMessages() {
  messagesContainer.innerHTML = "";

  if (inputMessages.length > 0) {
    inputMessages.forEach((each) => {
      const userPromptElement = document.createElement("p");
      userPromptElement.classList.add("chat-prompt");
      userPromptElement.textContent = each.Prompt;
      messagesContainer.appendChild(userPromptElement);

      const responseElement = document.createElement("p");
      responseElement.classList.add("chat-response");
      responseElement.textContent = each.Answer;
      messagesContainer.appendChild(responseElement);
    });
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
}

function openFileSelection() {
  const fileInput = document.getElementById("fileInput");
  fileInput.accept = ".csv, .pdf, .txt, .doc";
  fileInput.click();
  fileInput.addEventListener("change", handleFileSelection);
}

function handleFileSelection(event) {
  // You can perform some checks on the files here if you want
  // Open the modal after file selection
  const uploadModal = new bootstrap.Modal(
    document.getElementById("uploadModal")
  );
  uploadModal.show();
}

function submitForm(action) {
  var form = document.getElementById("uploadForm");

  var input = document.createElement("input");
  input.type = "hidden";
  input.name = "action";
  input.value = action;

  form.appendChild(input);

  // After the form is submitted, close the current modal and open the new one.
  $("#uploadModal").on("hidden.bs.modal", function () {
    $("#ingesting-modal").modal("show");
  });

  if (action == "add" || action == "reset") {
    $("#uploadModal").modal("hide");
  }

  form.submit();
}

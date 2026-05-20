function analyzeSentiment() {
  const text = document.getElementById("inputText").value;
  const model = document.getElementById("modelSelect").value;

  fetch("http://127.0.0.1:8000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      text: text,
      model: model
    })
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    alert("Sonuç: " + data.sentiment);
  });
}